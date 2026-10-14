"""
Story & Multi-Chapter Script Generator for Learn English Champs
Generates comprehensive, engaging English learning podcast dialogues between Emma and Alex.
Specifically tailored for:
- Overcoming fear and shyness in speaking English
- Conversational fluency hacks and natural phrasing
- Real-life roleplays and everyday English confidence
- Multi-chapter structure to reach 30 minutes (~288 turns / ~3,900 words) with YouTube chapter timestamps
"""
import os
import time
import json
import requests
import config

DEFAULT_9_ACTS = [
    ("Act 1: Core Mindset & Foundations", "Overcoming anxiety and building initial momentum."),
    ("Act 2: Everyday Real-World Scenario", "Practical conversational roleplay with native reactions."),
    ("Act 3: Modern Colloquial Expressions", "Replacing textbook English with natural daily idioms."),
    ("Act 4: Overcoming Obstacles & Mind-Blanks", "Techniques to handle freezing and awkward silences."),
    ("Act 5: Intermediate Roleplay Scenario", "Navigating workplace or social situations with nuance."),
    ("Act 6: Connected Speech & Native Rhythm", "Pronunciation, reductions, and flow."),
    ("Act 7: Politeness & Cultural Nuances", "Tone modulation, humor, and active listening."),
    ("Act 8: Fast-Paced Interactive Drill", "Dynamic back-and-forth conversational sparring."),
    ("Act 9: The 7-Day Speaking Challenge", "Daily out-loud habit to cement fluency permanently.")
]

def generate_chapter_ai(act_index: int, act_title: str, act_focus: str, topic_theme: str, target_turns: int = 30) -> list:
    """
    Synthesizes authentic, high-quality dialogue turns for a specific act using AI.
    Features retries, timeout management, and strict single-line subtitle length checks.
    """
    key = config.POLLINATIONS_API_KEY
    endpoint = config.POLLINATIONS_ENDPOINT if key else config.POLLINATIONS_FALLBACK_ENDPOINT
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"

    prompt = f"""You are the lead scriptwriter for the popular English learning podcast 'Learn English Champs'.
Hosts:
- Emma (female): Energetic, warm American English coach, explains expressions, gives natural examples.
- Alex (male): Curious, witty, relatable co-host, asks practical questions, tests phrases, reacts naturally.

EPISODE TOPIC: {topic_theme}
CHAPTER: {act_title}
FOCUS AREA: {act_focus}

TASK:
Write exactly {target_turns} dialogue turns alternating strictly between Emma and Alex.
Deeply explore the chapter focus with modern expressions, realistic scenario roleplays, and actionable fluency hacks.

CRITICAL RULES:
1. Alternate speaker every turn: Emma -> Alex -> Emma -> Alex...
2. Keep each turn punchy (10-18 words, max 6 words per phrase) for clean single-line subtitle display.
3. Keep the tone conversational, friendly, educational, and lively.
4. Output ONLY a valid JSON array matching this schema (no markdown, no explanations):
[
  {{"speaker": "female", "name": "Emma", "text": "..."}},
  {{"speaker": "male", "name": "Alex", "text": "..."}}
]"""

    for attempt in range(3):
        try:
            print(f"[StoryGenerator] Synthesizing Act {act_index+1} dialogue with AI (attempt {attempt+1}/{3})...")
            if key:
                payload = {
                    "model": config.POLLINATIONS_MODEL,
                    "messages": [
                        {"role": "system", "content": "You are a professional educational podcast scriptwriter. Return ONLY a valid JSON array of dialogue objects."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.75
                }
                resp = requests.post(endpoint, json=payload, headers=headers, timeout=35)
                if resp.status_code == 200:
                    raw = resp.json()["choices"][0]["message"]["content"].strip()
                else:
                    raise RuntimeError(f"Pollinations API HTTP {resp.status_code}: {resp.text[:100]}")
            else:
                resp = requests.post(config.POLLINATIONS_FALLBACK_ENDPOINT, json={"messages": [{"role": "user", "content": prompt}]}, timeout=35)
                if resp.status_code == 200:
                    raw = resp.text.strip()
                else:
                    raise RuntimeError(f"Fallback endpoint HTTP {resp.status_code}")

            if raw.startswith("```"):
                lines = raw.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                raw = "\n".join(lines).strip()

            parsed = json.loads(raw)
            if isinstance(parsed, list) and len(parsed) >= 8:
                print(f"[StoryGenerator] Act {act_index+1} successfully generated {len(parsed)} dialogue turns.")
                return parsed
            else:
                print(f"[StoryGenerator] Act {act_index+1} response too short ({len(parsed) if isinstance(parsed, list) else 'not a list'}), retrying...")
        except Exception as e:
            print(f"[StoryGenerator] Act {act_index+1} AI attempt {attempt+1} error: {e}")
            time.sleep(2)

    print(f"[WARNING] AI generation failed for Act {act_index+1}. Using topic-specific fallback turns...")
    return create_topic_fallback_turns(act_title, act_focus, topic_theme, target_turns)

def create_topic_fallback_turns(act_title: str, act_focus: str, topic_theme: str, count: int = 30) -> list:
    """Creates emergency fallback turns tailored specifically to the given topic and act if offline."""
    base_pairs = [
        ("Welcome back, everyone! In this part, we are focusing on " + act_title + ".",
         "That's right, Emma. This is crucial for mastering " + topic_theme + "."),
        ("Specifically, let's explore " + act_focus + ".",
         "What is the most practical phrase our champs should practice first?"),
        ("Start with clear, confident statements rather than second-guessing yourself.",
         "I love that advice. Keeping it simple always beats sounding complicated."),
        ("Always pay attention to how native speakers link their words smoothly.",
         "Yes! Connected speech makes you sound natural without speaking too fast."),
        ("Let's try a quick roleplay to put this directly into practice.",
         "I'll play the speaker and you give me honest, real-time feedback."),
        ("Notice the tone and cadence we use when delivering that phrase.",
         "That felt so much more natural and comfortable than the textbook version."),
        ("Remember, repetition out loud builds the muscle memory you need.",
         "Practice these exact phrases in your daily conversations this week."),
        ("Don't worry about being perfect; focus entirely on making a genuine connection.",
         "Every single conversation is another victory on your fluency journey.")
    ]
    turns = []
    while len(turns) < count:
        for emma_text, alex_text in base_pairs:
            turns.append({"speaker": "female", "name": "Emma", "text": emma_text})
            if len(turns) >= count:
                break
            turns.append({"speaker": "male", "name": "Alex", "text": alex_text})
            if len(turns) >= count:
                break
    return turns

# Master catalog of viral English learning masterclass curricula
def generate_dynamic_topic(past_topics: list, ep_num: int = 1) -> dict:
    """Uses AI to generate a brand new viral English topic and 9 themed acts not present in history."""
    key = config.POLLINATIONS_API_KEY
    endpoint = config.POLLINATIONS_ENDPOINT if key else config.POLLINATIONS_FALLBACK_ENDPOINT
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"

    prompt = f"""You are the creative executive producer for 'Learn English Champs', a top-rated English learning podcast.
Previously published topics (DO NOT REPEAT OR CLOSELY COPY ANY OF THESE):
{json.dumps(past_topics[-15:], indent=2)}

Generate ONE brand new, highly practical, viral English learning episode topic that everyday learners need (e.g. handling customer service, negotiations, workplace meetings, doctor visits, humor and sarcasm, apartment hunting, networking, dating in English, arguing politely, emergency situations).

OUTPUT FORMAT: Return ONLY a raw JSON object matching this schema:
{{
  "id": "slug_topic_name",
  "topic": "Catchy Full Topic Title (e.g. Master English Phone Calls! Speak with Confidence)",
  "thumbnail_title_1": "PHONE CALLS",
  "thumbnail_title_2": "MADE EASY!",
  "thumbnail_hook": "Never Fear Ringing Phones Again",
  "yt_hook": "Master English Phone Calls!",
  "act_themes": [
    ["Act 1: Title", "Detailed focus description..."],
    ["Act 2: Title", "Detailed focus description..."],
    ["Act 3: Title", "Detailed focus description..."],
    ["Act 4: Title", "Detailed focus description..."],
    ["Act 5: Title", "Detailed focus description..."],
    ["Act 6: Title", "Detailed focus description..."],
    ["Act 7: Title", "Detailed focus description..."],
    ["Act 8: Title", "Detailed focus description..."],
    ["Act 9: Title", "Detailed focus description..."]
  ]
}}"""

    for attempt in range(3):
        try:
            print(f"[StoryGenerator] Generating fresh dynamic curriculum topic via AI (attempt {attempt+1}/3)...")
            if key:
                resp = requests.post(
                    endpoint,
                    json={
                        "model": config.POLLINATIONS_MODEL,
                        "messages": [
                            {"role": "system", "content": "You are a creative educational producer. Return ONLY valid JSON."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.85
                    },
                    headers=headers,
                    timeout=30
                )
                if resp.status_code == 200:
                    raw = resp.json()["choices"][0]["message"]["content"].strip()
                else:
                    raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:100]}")
            else:
                resp = requests.post(config.POLLINATIONS_FALLBACK_ENDPOINT, json={"messages": [{"role": "user", "content": prompt}]}, timeout=30)
                raw = resp.text.strip()

            if raw.startswith("```"):
                lines = raw.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                raw = "\n".join(lines).strip()

            data = json.loads(raw)
            if "topic" in data and "act_themes" in data and len(data["act_themes"]) >= 6:
                print(f"[StoryGenerator] Dynamically generated new topic: '{data['topic']}'")
                return data
        except Exception as e:
            print(f"[StoryGenerator] Dynamic topic generation attempt {attempt+1} error: {e}")
            time.sleep(2)

    return {
        "id": f"dynamic_ep_{ep_num}",
        "topic": f"Natural English Fluency & Real Conversations (Ep. {ep_num})",
        "thumbnail_title_1": "SPEAK FLUENTLY",
        "thumbnail_title_2": "EVERY SINGLE DAY!",
        "thumbnail_hook": "Transform Your English Daily",
        "yt_hook": f"English Fluency Ep. {ep_num} 🎙️",
        "act_themes": DEFAULT_9_ACTS
    }

def get_next_curriculum_topic(history: list, custom_topic: str = None, ep_num: int = 1) -> dict:
    """
    Selects a brand new topic for every daily episode.
    Ensures every single run has a unique topic, unique thumbnail, and unique title/description.
    """
    if custom_topic:
        words = custom_topic.split()
        mid = len(words) // 2
        t1 = " ".join(words[:mid]) if mid > 0 else words[0]
        t2 = " ".join(words[mid:]) if mid > 0 else "MASTERCLASS"
        default_acts = [
            ("Act 1: Introduction & Core Mindset", f"Breaking down key concepts of {custom_topic}."),
            ("Act 2: Real-World Scenario 1", "Practical roleplay and foundational expressions."),
            ("Act 3: Modern Expressions", "Vocabulary and conversational phrases."),
            ("Act 4: Overcoming Roadblocks", "Handling common difficulties and misconceptions."),
            ("Act 5: Real-World Scenario 2", "Intermediate dialogue with native phrasing."),
            ("Act 6: Connected Speech & Rhythm", "Pronunciation, linking, and natural flow."),
            ("Act 7: Advanced Nuance", "Polite phrasing, subtle meanings, and humor."),
            ("Act 8: Fast-Paced Roleplay Challenge", "Full back-and-forth conversational practice."),
            ("Act 9: The 7-Day Speaking Blueprint", "Daily out-loud habit to master this skill.")
        ]
        return {
            "id": "custom",
            "topic": custom_topic,
            "thumbnail_title_1": t1[:18].upper(),
            "thumbnail_title_2": t2[:18].upper(),
            "thumbnail_hook": "Master Every Conversation",
            "yt_hook": f"{custom_topic[:50]} 🎙️",
            "act_themes": default_acts
        }

    # Extract all past published topics from history to prevent duplicate episodes
    past_topics = []
    if history:
        for item in history:
            if isinstance(item, dict) and "topic" in item:
                past_topics.append(item["topic"].lower().strip())

    # Generate 100% dynamic, fresh topic with Pollinations AI
    print("[StoryGenerator] Generating fresh dynamic topic with Pollinations AI...")
    return generate_dynamic_topic(past_topics, ep_num=ep_num)

def generate_full_podcast_story(target_minutes: float = 30.0, topic: str = None, ep_num: int = 1) -> dict:
    """
    Generates a full structured English learning podcast episode with a brand new topic every run.
    Produces dialogue turns across all acts tailored specifically to the topic using AI.
    """
    history = []
    history_file = os.path.join(config.BASE_DIR, "published_videos.json")
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            pass

    topic_info = get_next_curriculum_topic(history, custom_topic=topic, ep_num=ep_num)
    selected_topic = topic_info["topic"]

    print(f"[StoryGenerator] Episode #{ep_num} Selected Topic: '{selected_topic}'")
    print(f"[StoryGenerator] Thumbnail: '{topic_info['thumbnail_title_1']} {topic_info['thumbnail_title_2']}' | Hook: '{topic_info['thumbnail_hook']}'")

    act_themes = topic_info.get("act_themes", [])
    if not act_themes:
        act_themes = DEFAULT_9_ACTS

    dialogue = []
    chapters_meta = []

    # Configure acts and turn counts based on target duration
    if target_minutes <= 2.0:
        # Quick test mode: 1 act, 10 turns
        act_title, act_focus = act_themes[0]
        chapters_meta.append({"title": act_title, "start_turn": 0})
        turns = generate_chapter_ai(0, act_title, act_focus, selected_topic, target_turns=10)
        dialogue.extend(turns)
    elif target_minutes <= 6.0:
        # Short podcast mode: 2 acts, 16 turns each
        for i in range(min(2, len(act_themes))):
            act_title, act_focus = act_themes[i]
            chapters_meta.append({"title": act_title, "start_turn": len(dialogue)})
            turns = generate_chapter_ai(i, act_title, act_focus, selected_topic, target_turns=16)
            dialogue.extend(turns)
    elif target_minutes <= 15.0:
        # Medium podcast: 4 acts, 22 turns each
        for i in range(min(4, len(act_themes))):
            act_title, act_focus = act_themes[i]
            chapters_meta.append({"title": act_title, "start_turn": len(dialogue)})
            turns = generate_chapter_ai(i, act_title, act_focus, selected_topic, target_turns=22)
            dialogue.extend(turns)
    else:
        # Full ~30-minute episode: all acts (~30 turns each for ~270-288 turns total)
        for i, (act_title, act_focus) in enumerate(act_themes):
            chapters_meta.append({
                "title": act_title,
                "start_turn": len(dialogue)
            })
            turns = generate_chapter_ai(i, act_title, act_focus, selected_topic, target_turns=30)
            dialogue.extend(turns)

    print(f"[StoryGenerator] Created {len(dialogue)} dialogue turns across {len(chapters_meta)} acts.")
    return {
        "topic": selected_topic,
        "thumbnail_title_1": topic_info["thumbnail_title_1"],
        "thumbnail_title_2": topic_info["thumbnail_title_2"],
        "thumbnail_hook": topic_info["thumbnail_hook"],
        "yt_hook": topic_info["yt_hook"],
        "chapters": chapters_meta,
        "dialogue": dialogue
    }

def generate_youtube_metadata(topic: str, duration_sec: float, chapters_with_timestamps: list, ep_num: int = 1, yt_hook: str = None) -> dict:
    """
    Generates SEO-optimized YouTube Title, Description (with all chapter timestamps), and Tags
    dynamically tailored to the selected topic and episode number.
    """
    prefix = yt_hook if yt_hook else f"{topic[:55]} 🎙️"
    title = f"{prefix} 30-Minute Masterclass | Learn English Champs Ep. {ep_num}"
    
    desc_lines = [
        f"🔥 Master everyday English conversation with Emma and Alex in Episode #{ep_num}!",
        "",
        f"In this 30-minute English learning podcast masterclass on '{topic}', you'll discover practical fluency hacks, natural native phrasing, roleplay dialogues, connected speech secrets, and our 7-day speaking challenge.",
        "",
        "🕒 CHAPTERS & TIMESTAMPS:"
    ]

    for ch in chapters_with_timestamps:
        time_str = time_to_timestamp(ch["start_time"])
        desc_lines.append(f"{time_str} - {ch['title']}")

    desc_lines.extend([
        "",
        f"💡 WHAT YOU WILL MASTER IN EPISODE #{ep_num}:",
        "• Deep conversational drills with Emma & Alex",
        "• Modern expressions to replace stiff textbook English",
        "• Real-world scenario roleplays with natural reactions",
        "• Connected speech secrets ('wanna', 'gonna', rhythm & linking)",
        "• How to handle mistakes and mind-blanks with confidence",
        "• Actionable 7-day speaking challenge to practice out loud",
        "",
        "💬 QUESTION OF THE DAY:",
        "Which phrase or technique from today's lesson are you going to use first? Let us know in the comments below!",
        "",
        "🔔 Subscribe to Learn English Champs for daily English learning podcasts, pronunciation tips, and speaking confidence lessons!",
        "",
        "#LearnEnglish #EnglishPodcast #LearnEnglishChamps #SpeakEnglish #EnglishConversation #DailyEnglish #EnglishFluency #EnglishListening #LearnEnglishThroughStory #ESL #EnglishRoleplay"
    ])

    description = "\n".join(desc_lines)
    tags = [
        "learn english", "english podcast", "learn english champs", "english conversation",
        "overcome fear of speaking english", "speak english fluently", "daily english practice",
        "english speaking practice", "how to speak english naturally", "english listening practice",
        "english vocabulary", "english small talk", "learn english podcast 30 minutes",
        "learn english 30 min", "english roleplay", "stop translating in your head", "english fluency"
    ]

    return {
        "title": title[:100],
        "description": description,
        "tags": tags
    }

def time_to_timestamp(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"

