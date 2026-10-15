import os
import json
import asyncio
import random
import edge_tts
from pydub import AudioSegment
import config

EDGE_ENDPOINTS = [
    "wss://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1?TrustedClientToken=6A5AA1D4EAFF4E9FB37E23D68491D6F4",
    "wss://api.msedgeservices.com/tts/cognitiveservices/websocket/v1?Ocp-Apim-Subscription-Key=6A5AA1D4EAFF4E9FB37E23D68491D6F4"
]

def set_edge_tts_endpoint(url: str):
    """Dynamically set the active Microsoft Edge TTS endpoint."""
    try:
        import edge_tts.constants
        import edge_tts.communicate
        edge_tts.constants.WSS_URL = url
        edge_tts.communicate.WSS_URL = url
    except Exception:
        pass


async def synthesize_turn(text: str, voice: str, turn_index: int) -> dict:
    """
    Synthesizes a single dialogue turn using Microsoft Edge TTS with WordBoundary tracking.
    Uses the channel's 2 authentic host voices (Ava for Emma, Andrew for Andrew) with
    multi-endpoint failover across Microsoft clusters and exponential backoff on 429.
    """
    last_err = None
    temp_turn_path = os.path.join(config.TEMP_DIR, f"turn_{turn_index}.mp3")

    # Cycle between the 2 Microsoft cloud endpoints on retries
    for attempt in range(5):
        target_endpoint = EDGE_ENDPOINTS[attempt % len(EDGE_ENDPOINTS)]
        set_edge_tts_endpoint(target_endpoint)

        try:
            comm = edge_tts.Communicate(text, voice, boundary="WordBoundary")
            audio_data = bytearray()
            words = []
            
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    audio_data.extend(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    w_text = chunk["text"].strip()
                    start_s = chunk["offset"] / 10_000_000.0
                    dur_s = chunk["duration"] / 10_000_000.0
                    words.append({
                        "word": w_text,
                        "rel_start": start_s,
                        "rel_end": start_s + dur_s,
                        "duration": dur_s
                    })

            if len(audio_data) > 0:
                with open(temp_turn_path, "wb") as f:
                    f.write(audio_data)

                seg = AudioSegment.from_file(temp_turn_path)
                dur_sec = len(seg) / 1000.0

                return {
                    "audio_segment": seg,
                    "duration": dur_sec,
                    "words": words,
                    "turn_index": turn_index
                }
        except Exception as e:
            last_err = e
            err_str = str(e).lower()
            endpoint_name = "Bing" if "bing" in target_endpoint else "MSEdge"
            if "429" in err_str or "rate" in err_str or "invalid response status" in err_str:
                backoff = (2 ** (attempt % 3)) * 1.5 + random.uniform(1.0, 2.5)
                print(f"  [Edge TTS Throttled] Turn {turn_index} on {endpoint_name} (Voice: {voice}). Backing off {backoff:.1f}s and switching endpoint...")
                await asyncio.sleep(backoff)
            else:
                print(f"  [Edge TTS Retry] Turn {turn_index} attempt {attempt+1}/5 error ({e}). Switching endpoint...")
                await asyncio.sleep(1.0)

    # Emergency fallback only if all 5 Microsoft attempts on both endpoints failed
    print(f"  [TTS Emergency] Edge TTS failed for turn {turn_index} across all Microsoft endpoints ({last_err}). Generating silent segment...")
    words_count = len(text.split())
    est_dur = max(2.0, words_count * 0.35)
    seg = AudioSegment.silent(duration=int(est_dur * 1000))
    seg.export(temp_turn_path, format="mp3")

    dur_sec = len(seg) / 1000.0
    words_list = text.split()
    w_dur = dur_sec / max(1, len(words_list))
    words = []
    for i, w in enumerate(words_list):
        words.append({
            "word": w,
            "rel_start": round(i * w_dur, 3),
            "rel_end": round((i + 1) * w_dur, 3),
            "duration": round(w_dur, 3)
        })

    return {
        "audio_segment": seg,
        "duration": dur_sec,
        "words": words,
        "turn_index": turn_index
    }

def chunk_turn_words(words: list, speaker: str, global_turn_offset: float, turn_duration: float, max_words_per_line: int = 6) -> list:
    """
    Chunks a turn's words into strictly single-line subtitle chunks (optimum 5 to 6 words each, strictly never more than 6 words).
    Ensures text remains strictly centered between the two speakers without overflowing horizontally.
    """
    if not words:
        return []

    total_words = len(words)
    chunks = []

    # If the sentence is already 6 words or fewer, keep it on a single line
    if total_words <= max_words_per_line:
        chunks = [words]
    else:
        current_chunk = []
        for i, w in enumerate(words):
            current_chunk.append(w)
            remaining = len(words) - (i + 1)
            has_punct = any(w["word"].endswith(p) for p in [".", ",", "!", "?", ";", ":"])

            # Break chunk when:
            # 1. Hard cap reached (max 6 words)
            # 2. Punctuation hit and chunk has >= 3 words and remaining >= 3 words
            # 3. If remaining == 1 and current chunk already has 4 words, break to avoid 1-word dangling line
            if len(current_chunk) >= max_words_per_line:
                chunks.append(current_chunk)
                current_chunk = []
            elif len(current_chunk) >= 3 and has_punct and remaining >= 3:
                chunks.append(current_chunk)
                current_chunk = []
            elif len(current_chunk) >= 4 and remaining == 1:
                chunks.append(current_chunk)
                current_chunk = []

        if current_chunk:
            # Rebalance if last chunk is a single lonely word
            if len(current_chunk) == 1 and len(chunks) > 0 and len(chunks[-1]) >= 4:
                borrowed = chunks[-1].pop()
                current_chunk.insert(0, borrowed)
            chunks.append(current_chunk)

    formatted_chunks = []
    for i, c_words in enumerate(chunks):
        c_start = global_turn_offset + c_words[0]["rel_start"]
        c_end = global_turn_offset + c_words[-1]["rel_end"]
        
        # Add slight trailing display margin so the line stays visible until the next begins
        if i + 1 < len(chunks):
            next_start = global_turn_offset + chunks[i+1][0]["rel_start"]
            c_end = min(next_start, c_end + 0.15)
        else:
            c_end = min(global_turn_offset + turn_duration, c_end + 0.3)

        chunk_words_data = []
        for w in c_words:
            chunk_words_data.append({
                "word": w["word"],
                "start": global_turn_offset + w["rel_start"],
                "end": global_turn_offset + w["rel_end"]
            })

        formatted_chunks.append({
            "line_text": " ".join(w["word"] for w in c_words),
            "start": round(c_start, 3),
            "end": round(c_end, 3),
            "speaker": speaker,
            "words": chunk_words_data
        })

    return formatted_chunks

async def generate_podcast_audio(dialogue: list) -> tuple:
    """
    Generates realistic speech for all dialogue turns concurrently using asyncio,
    concatenates with natural pauses, and returns (master_audio_path, subtitle_chunks, total_duration).
    """
    print(f"[TTS] Synthesizing speech for {len(dialogue)} dialogue turns with controlled concurrency (2 workers)...")
    semaphore = asyncio.Semaphore(2)

    async def worker(idx: int, turn: dict):
        async with semaphore:
            speaker = turn.get("speaker", "female").lower()
            voice = config.VOICE_FEMALE if "female" in speaker else config.VOICE_MALE
            text = turn.get("text", "").strip()
            res = await synthesize_turn(text, voice, idx)
            res["speaker"] = speaker
            res["name"] = turn.get("name", "Host")
            res["turn_text"] = text
            if (idx + 1) % 25 == 0 or idx == len(dialogue) - 1:
                print(f"  [TTS Progress] Synthesized {idx + 1}/{len(dialogue)} dialogue turns")
            await asyncio.sleep(0.08)
            return idx, res

    tasks = [worker(i, t) for i, t in enumerate(dialogue)]
    results = await asyncio.gather(*tasks)
    
    # Sort back by original sequential dialogue index
    results.sort(key=lambda x: x[0])
    ordered_turns = [r[1] for r in results]

    print(f"[TTS] All {len(ordered_turns)} turns synthesized! Assembling master audio track...")
    master_audio = AudioSegment.silent(duration=200) # Small 0.2s pre-roll silence
    current_offset = 0.2
    all_chunks = []

    for idx, turn_res in enumerate(ordered_turns):
        speaker = turn_res["speaker"]
        turn_chunks = chunk_turn_words(
            turn_res["words"],
            speaker=speaker,
            global_turn_offset=current_offset,
            turn_duration=turn_res["duration"],
            max_words_per_line=config.MAX_WORDS_PER_LINE
        )
        for c in turn_chunks:
            c["turn_idx"] = idx
        all_chunks.extend(turn_chunks)

        master_audio += turn_res["audio_segment"]
        current_offset += turn_res["duration"]

        if idx + 1 < len(ordered_turns):
            pause_ms = int(config.PAUSE_BETWEEN_TURNS * 1000)
            master_audio += AudioSegment.silent(duration=pause_ms)
            current_offset += config.PAUSE_BETWEEN_TURNS

    # Add 0.5s outro silence
    master_audio += AudioSegment.silent(duration=500)
    total_duration = len(master_audio) / 1000.0

    master_audio_path = os.path.join(config.TEMP_DIR, "master_audio.wav")
    master_audio.export(master_audio_path, format="wav")
    print(f"[TTS] Master audio saved: {master_audio_path} ({total_duration:.2f}s / {total_duration/60.0:.1f} mins)")

    # Save chunks metadata
    timing_file = os.path.join(config.TEMP_DIR, "subtitles_chunks.json")
    with open(timing_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    return master_audio_path, all_chunks, total_duration

if __name__ == "__main__":
    test_dialogue = [
        {"speaker": "female", "name": "Emma", "text": "Water from a bottle or tap?"},
        {"speaker": "male", "name": "Alex", "text": "I always drink filtered tap water!"}
    ]
    audio_path, chunks, dur = asyncio.run(generate_podcast_audio(test_dialogue))
    print(f"Done! Duration: {dur}s, Chunks: {len(chunks)}")
    for c in chunks:
        print(f"  [{c['start']:.2f}s - {c['end']:.2f}s] {c['line_text']}")
