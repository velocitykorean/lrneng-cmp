import os
import json
import asyncio
import edge_tts
from pydub import AudioSegment
import config

async def synthesize_turn(text: str, voice: str, turn_index: int) -> dict:
    """
    Synthesizes a single dialogue turn using edge_tts with WordBoundary tracking.
    """
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

    # Save temp turn audio
    temp_turn_path = os.path.join(config.TEMP_DIR, f"turn_{turn_index}.mp3")
    with open(temp_turn_path, "wb") as f:
        f.write(audio_data)

    seg = AudioSegment.from_file(temp_turn_path)
    dur_sec = len(seg) / 1000.0

    return {
        "audio_segment": seg,
        "duration": dur_sec,
        "words": words
    }

def chunk_turn_words(words: list, speaker: str, global_turn_offset: float, turn_duration: float, max_words_per_line: int = 5) -> list:
    """
    Chunks a turn's words into strictly single-line subtitle chunks (3 to 6 words each),
    computing absolute start/end times and word boundaries.
    """
    if not words:
        return []

    chunks = []
    current_chunk_words = []

    for w in words:
        current_chunk_words.append(w)
        # Check if we should split at punctuation or max words
        has_punctuation = any(w["word"].endswith(p) for p in [".", ",", "!", "?", ";", ":"])
        if len(current_chunk_words) >= max_words_per_line or (has_punctuation and len(current_chunk_words) >= 3):
            chunks.append(current_chunk_words)
            current_chunk_words = []

    if current_chunk_words:
        chunks.append(current_chunk_words)

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
    Generates realistic speech for all dialogue turns, concatenates with natural pauses,
    and returns (master_audio_path, subtitle_chunks, total_duration).
    """
    print(f"[TTS] Synthesizing speech for {len(dialogue)} dialogue turns...")
    master_audio = AudioSegment.silent(duration=200) # Small 0.2s pre-roll silence
    current_offset = 0.2
    
    all_chunks = []

    for idx, turn in enumerate(dialogue):
        speaker = turn.get("speaker", "female").lower()
        voice = config.VOICE_FEMALE if "female" in speaker else config.VOICE_MALE
        speaker_name = turn.get("name", "Host")
        text = turn.get("text", "").strip()

        print(f"  Turn {idx+1}/{len(dialogue)}: [{speaker_name}]: {text}")
        turn_result = await synthesize_turn(text, voice, idx)
        
        # Append audio to master track
        master_audio += turn_result["audio_segment"]
        
        # Calculate chunks for subtitle display
        turn_chunks = chunk_turn_words(
            turn_result["words"],
            speaker=speaker,
            global_turn_offset=current_offset,
            turn_duration=turn_result["duration"],
            max_words_per_line=config.MAX_WORDS_PER_LINE
        )
        all_chunks.extend(turn_chunks)
        
        current_offset += turn_result["duration"]

        # Add pause between turns if not the final turn
        if idx + 1 < len(dialogue):
            pause_ms = int(config.PAUSE_BETWEEN_TURNS * 1000)
            master_audio += AudioSegment.silent(duration=pause_ms)
            current_offset += config.PAUSE_BETWEEN_TURNS

    # Add 0.5s outro silence
    master_audio += AudioSegment.silent(duration=500)
    total_duration = len(master_audio) / 1000.0

    master_audio_path = os.path.join(config.TEMP_DIR, "master_audio.wav")
    master_audio.export(master_audio_path, format="wav")
    print(f"[TTS] Master audio saved: {master_audio_path} ({total_duration:.2f}s)")

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
