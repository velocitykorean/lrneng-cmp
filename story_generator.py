"""
Story & Multi-Chapter Script Generator for Learn English Champs
Generates comprehensive, engaging English learning podcast dialogues between Emma and Alex.
Specifically tailored for:
- Overcoming fear and shyness in speaking English
- Conversational fluency hacks and natural phrasing
- Real-life roleplays and everyday English confidence
- Multi-chapter structure to reach 30 minutes with YouTube chapter timestamps
"""
import os
import json
import random
import requests
import config

CHAPTER_TEMPLATES = [
    {
        "title": "Act 1: The Fear of Speaking - Why We Freeze",
        "focus": "Why English learners freeze when speaking to native speakers, how to overcome the psychological fear of making mistakes, and accepting imperfection."
    },
    {
        "title": "Act 2: The Translation Trap - Stop Thinking in Your Native Language",
        "focus": "How translating word-for-word slows down speaking, practical drills to start thinking directly in simple English, and using sensory descriptions."
    },
    {
        "title": "Act 3: 10 Natural Phrases for Everyday Small Talk",
        "focus": "Alternatives to robotic textbook phrases (e.g., 'How are you? I am fine and you?'), using natural reactions like 'No way!', 'I hear you', 'That makes sense'."
    },
    {
        "title": "Act 4: Real-World Roleplay - Ordering & Making Requests",
        "focus": "Real-world roleplay ordering at a coffee shop and restaurant, how to use 'Could I get' and 'I was wondering if', sounding polite without sounding stiff."
    },
    {
        "title": "Act 5: Never Run Out of Things to Say - The Flow Technique",
        "focus": "The question-and-comment technique, asking open-ended questions, bridging awkward silences with phrases like 'Speaking of which...' and 'That reminds me'."
    },
    {
        "title": "Act 6: Pronunciation Secrets & Natural Rhythm",
        "focus": "Connected speech in English, linking words ('want to' -> 'wanna', 'going to' -> 'gonna'), rhythm, intonation, and sounding smooth rather than robotic."
    },
    {
        "title": "Act 7: The 7-Day Speaking Challenge & Daily Habit",
        "focus": "Actionable daily habit to speak 5 minutes out loud every day, shadow podcasts, self-talk drills, encouragement, and inspiring closing words."
    }
]

# Comprehensive rich masterclass dialogues for complete 30-minute fallback or fast generation
FALLBACK_CHAPTER_SCRIPTS = [
    {
        "chapter_name": "The Fear of Speaking: Why We Freeze",
        "turns": [
            {"speaker": "female", "name": "Emma", "text": "Welcome to Learn English Champs! I'm Emma, and here with me is Alex."},
            {"speaker": "male", "name": "Alex", "text": "Hey everyone! Today we're tackling the single biggest obstacle for English learners."},
            {"speaker": "female", "name": "Emma", "text": "That's right. It's not grammar rules, and it's definitely not vocabulary tests."},
            {"speaker": "male", "name": "Alex", "text": "It is the sheer fear of speaking and freezing up when someone asks a question."},
            {"speaker": "female", "name": "Emma", "text": "Have you ever felt your heart race right before you say something in English?"},
            {"speaker": "male", "name": "Alex", "text": "Completely! Your brain goes blank, and suddenly every word disappears into thin air."},
            {"speaker": "female", "name": "Emma", "text": "Psychologists call this the affective filter. It's high stress blocking your memory."},
            {"speaker": "male", "name": "Alex", "text": "The key realization is that native speakers never expect perfection from you."},
            {"speaker": "female", "name": "Emma", "text": "Exactly. Communication is simply about connecting human beings, not grammar exams."},
            {"speaker": "male", "name": "Alex", "text": "When you focus on the message rather than mistakes, speaking becomes ten times easier."}
        ]
    },
    {
        "chapter_name": "The Translation Trap: Stop Thinking in Your First Language",
        "turns": [
            {"speaker": "female", "name": "Emma", "text": "Let's dive into the second big issue: translating in your head before speaking."},
            {"speaker": "male", "name": "Alex", "text": "Oh, the mental translation trap! It adds a three-second delay to every sentence."},
            {"speaker": "female", "name": "Emma", "text": "When someone says 'How was your weekend?', you translate to your native tongue."},
            {"speaker": "male", "name": "Alex", "text": "Then you formulate the reply, translate back to English, and check grammar!"},
            {"speaker": "female", "name": "Emma", "text": "By that time, the conversation has already moved on to something else entirely."},
            {"speaker": "male", "name": "Alex", "text": "So how do we break this habit and think directly in English?"},
            {"speaker": "female", "name": "Emma", "text": "Start by narrating simple daily actions in your mind using short phrases."},
            {"speaker": "male", "name": "Alex", "text": "Like: 'Making coffee. It's hot. The morning is chilly. Where are my keys?'"},
            {"speaker": "female", "name": "Emma", "text": "Yes! Associating English words directly with objects and actions rewires your brain."},
            {"speaker": "male", "name": "Alex", "text": "No intermediate translation required. Just direct English concept to speech."}
        ]
    },
    {
        "chapter_name": "10 Natural Phrases for Everyday Small Talk",
        "turns": [
            {"speaker": "female", "name": "Emma", "text": "Now let's replace textbook phrases with what natives actually say every day."},
            {"speaker": "male", "name": "Alex", "text": "Number one: Stop answering 'How are you?' with 'I am fine, thank you, and you?'"},
            {"speaker": "female", "name": "Emma", "text": "It sounds like a robot from an old nineties cassette tape, doesn't it?"},
            {"speaker": "male", "name": "Alex", "text": "Instead, try: 'Doing well, how about yourself?' or simply 'Can't complain!'"},
            {"speaker": "female", "name": "Emma", "text": "Another favorite natural reaction is 'I hear you' or 'That makes total sense'."},
            {"speaker": "male", "name": "Alex", "text": "It immediately signals empathy and keeps the speaker feeling understood and appreciated."},
            {"speaker": "female", "name": "Emma", "text": "And when something surprising happens, instead of 'It is unbelievable', say 'No way!'"},
            {"speaker": "male", "name": "Alex", "text": "Or 'You've got to be kidding me!' It adds genuine emotion to your voice."},
            {"speaker": "female", "name": "Emma", "text": "Notice how simple these words are. Fluency isn't complicated words; it's natural reactions."},
            {"speaker": "male", "name": "Alex", "text": "Practice these two or three times today and notice how natural you sound."}
        ]
    },
    {
        "chapter_name": "Real-World Roleplay: Ordering Coffee & Dining Out",
        "turns": [
            {"speaker": "female", "name": "Emma", "text": "Let's do a quick roleplay! Alex, you're the barista, and I'm ordering coffee."},
            {"speaker": "male", "name": "Alex", "text": "Hi there! Welcome to Sun Cafe. What can I get started for you today?"},
            {"speaker": "female", "name": "Emma", "text": "Hey! Could I get an iced oat latte with an extra espresso shot?"},
            {"speaker": "male", "name": "Alex", "text": "Sure thing! For here or to go?"},
            {"speaker": "female", "name": "Emma", "text": "To go, please. And could you make that with light ice?"},
            {"speaker": "male", "name": "Alex", "text": "You got it! That will be four dollars and fifty cents at the register."},
            {"speaker": "female", "name": "Emma", "text": "Freeze! Notice the phrases we used: 'Could I get' instead of 'I want'."},
            {"speaker": "male", "name": "Alex", "text": "'Could I get' is polite, effortless, and used millions of times daily."},
            {"speaker": "female", "name": "Emma", "text": "And my reply: 'To go, please'. Short, confident, and perfectly understood."},
            {"speaker": "male", "name": "Alex", "text": "Memorize that exact sentence pattern for every cafe in the English-speaking world."}
        ]
    },
    {
        "chapter_name": "Never Run Out of Things to Say: The Flow Technique",
        "turns": [
            {"speaker": "female", "name": "Emma", "text": "Alex, what should listeners do when an awkward silence suddenly appears?"},
            {"speaker": "male", "name": "Alex", "text": "Use what we call the 'Bridge Technique' to transition between topics seamlessly."},
            {"speaker": "female", "name": "Emma", "text": "Phrases like: 'Speaking of which...', 'That reminds me...', or 'By the way...'"},
            {"speaker": "male", "name": "Alex", "text": "These bridge phrases give your mind two full seconds to recall a related story."},
            {"speaker": "female", "name": "Emma", "text": "Also, always answer questions with the 'Answer Plus Detail' rule."},
            {"speaker": "male", "name": "Alex", "text": "Don't just answer 'Yes'. Say: 'Yes, because I've always loved outdoor hiking!'"},
            {"speaker": "female", "name": "Emma", "text": "The added detail gives the other person a conversational hook to respond to."},
            {"speaker": "male", "name": "Alex", "text": "Then bounce it back with an open-ended question: 'Have you ever tried it?'"},
            {"speaker": "female", "name": "Emma", "text": "Suddenly, the conversation flows back and forth like a relaxed tennis match."},
            {"speaker": "male", "name": "Alex", "text": "No pressure, no awkward pauses, just smooth mutual sharing between two people."}
        ]
    },
    {
        "chapter_name": "Connected Speech & Natural English Rhythm",
        "turns": [
            {"speaker": "female", "name": "Emma", "text": "Now let's explore why native speakers sound fast, even when speaking casually."},
            {"speaker": "male", "name": "Alex", "text": "It's because English is a stress-timed language with connected speech!"},
            {"speaker": "female", "name": "Emma", "text": "We don't pronounce every syllable separately like: 'What... are... you... going... to... do?'"},
            {"speaker": "male", "name": "Alex", "text": "We connect them together: 'Whaddya gonna do?' The words glide into one another."},
            {"speaker": "female", "name": "Emma", "text": "'Going to' naturally becomes 'gonna', and 'want to' becomes 'wanna'."},
            {"speaker": "male", "name": "Alex", "text": "This isn't sloppy slang; it is the natural phonetic rhythm of spoken English."},
            {"speaker": "female", "name": "Emma", "text": "Try saying: 'I have got to go' versus 'I gotta go'. Feel the difference?"},
            {"speaker": "male", "name": "Alex", "text": "'I gotta go' flows right off your tongue without straining your jaw muscles."},
            {"speaker": "female", "name": "Emma", "text": "When you practice connected speech, your listening comprehension explodes too."},
            {"speaker": "male", "name": "Alex", "text": "Because you finally hear English the way native ears process it every second."}
        ]
    },
    {
        "chapter_name": "The 7-Day Speaking Challenge & Daily Habit",
        "turns": [
            {"speaker": "female", "name": "Emma", "text": "We have covered so much gold today! Now here is your seven-day action challenge."},
            {"speaker": "male", "name": "Alex", "text": "For the next seven days, speak English out loud for five minutes every morning."},
            {"speaker": "female", "name": "Emma", "text": "Shadow our voices from this podcast. Repeat the phrases with our exact intonation."},
            {"speaker": "male", "name": "Alex", "text": "Record your voice on your phone so you can hear your incredible progress."},
            {"speaker": "female", "name": "Emma", "text": "Remember: Fluency is not an innate talent. It is a muscle that strengthens daily."},
            {"speaker": "male", "name": "Alex", "text": "Every single time you open your mouth and speak, you become a stronger English champ."},
            {"speaker": "female", "name": "Emma", "text": "Be kind to yourself, embrace your accent, and enjoy the beautiful learning journey."},
            {"speaker": "male", "name": "Alex", "text": "Subscribe to Learn English Champs, hit the notification bell, and leave a comment below!"},
            {"speaker": "female", "name": "Emma", "text": "Which phrase was your favorite from today's lesson? We read every single comment."},
            {"speaker": "male", "name": "Alex", "text": "Keep practicing, stay curious, and we will catch you in the next episode!"}
        ]
    }
]

def generate_chapter_ai(act_index: int, chapter_info: dict, topic_theme: str) -> list:
    """Uses Pollinations AI to generate an educational dialogue chapter."""
    key = config.POLLINATIONS_API_KEY
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"

    prompt = f"""You are writing a script for an English learning podcast channel named 'Learn English Champs'.
Hosts: Emma (female, encouraging, explains phrases) and Alex (male, witty, provides practical roleplays).
Topic Theme: {topic_theme}
Chapter: {chapter_info['title']}
Focus: {chapter_info['focus']}

Requirements:
- 10 to 14 dialogue turns alternating between Emma and Alex.
- Keep each line concise (10-18 words) so it fits on a single line subtitle.
- Educational, lively, encouraging, and natural conversational tone.
Return ONLY valid JSON matching this schema:
[
  {{"speaker": "female", "name": "Emma", "text": "..."}},
  {{"speaker": "male", "name": "Alex", "text": "..."}}
]"""

    try:
        resp = requests.post(
            config.POLLINATIONS_ENDPOINT,
            json={
                "messages": [
                    {"role": "system", "content": "You are a JSON-only API. Return only raw JSON arrays."},
                    {"role": "user", "content": prompt}
                ],
                "model": config.POLLINATIONS_MODEL,
                "temperature": 0.7
            },
            headers=headers,
            timeout=25
        )
        if resp.status_code == 200:
            content = resp.json()["choices"][0]["message"]["content"].strip()
            if content.startswith("```"):
                lines = content.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                content = "\n".join(lines).strip()
            parsed = json.loads(content)
            if isinstance(parsed, list) and len(parsed) >= 6:
                return parsed
    except Exception as e:
        print(f"[StoryGenerator] Warning: AI generation for chapter {act_index} failed ({e}), using fallback script.")

    # Return fallback turns for this chapter
    fallback_idx = min(act_index, len(FALLBACK_CHAPTER_SCRIPTS) - 1)
    return FALLBACK_CHAPTER_SCRIPTS[fallback_idx]["turns"]

def generate_full_podcast_story(target_minutes: float = 30.0, topic: str = None) -> dict:
    """
    Generates a full structured English learning podcast episode.
    If target_minutes >= 20, assembles 6-7 complete chapters to create an immersive 30-minute episode.
    """
    if not topic:
        topic = "Overcome Fear of Speaking English & Speak Like a Native"

    print(f"[StoryGenerator] Creating podcast story: '{topic}' (Target: {target_minutes:.1f} mins)...")

    # If short test duration (e.g. <= 2 mins)
    if target_minutes <= 2.0:
        chapters_to_generate = [CHAPTER_TEMPLATES[0]]
        dialogue = FALLBACK_CHAPTER_SCRIPTS[0]["turns"][:6]
        chapters_meta = [{"title": "Quick Lesson", "start_turn": 0}]
    elif target_minutes <= 5.0:
        chapters_to_generate = CHAPTER_TEMPLATES[:2]
        dialogue = FALLBACK_CHAPTER_SCRIPTS[0]["turns"] + FALLBACK_CHAPTER_SCRIPTS[1]["turns"]
        chapters_meta = [
            {"title": FALLBACK_CHAPTER_SCRIPTS[0]["chapter_name"], "start_turn": 0},
            {"title": FALLBACK_CHAPTER_SCRIPTS[1]["chapter_name"], "start_turn": len(FALLBACK_CHAPTER_SCRIPTS[0]["turns"])}
        ]
    else:
        # Full ~30 minute episode (all 7 chapters)
        dialogue = []
        chapters_meta = []
        for i, ch in enumerate(CHAPTER_TEMPLATES):
            ch_turns = generate_chapter_ai(i, ch, topic)
            chapters_meta.append({
                "title": ch["title"],
                "start_turn": len(dialogue)
            })
            dialogue.extend(ch_turns)

    title_1 = "SPEAK ENGLISH"
    title_2 = "WITHOUT FEAR!"
    hook = "Overcome Shyness & Speak Fluently"

    return {
        "topic": topic,
        "thumbnail_title_1": title_1,
        "thumbnail_title_2": title_2,
        "thumbnail_hook": hook,
        "chapters": chapters_meta,
        "dialogue": dialogue
    }

def generate_youtube_metadata(topic: str, duration_sec: float, chapters_with_timestamps: list) -> dict:
    """
    Generates SEO-optimized YouTube Title, Description (with chapter timestamps), and Tags.
    """
    title = f"Speak English Without Fear! | Daily Fluency Masterclass | Learn English Champs"
    
    desc_lines = [
        "🔥 Master everyday English conversation and overcome the fear of speaking with Emma and Alex!",
        "",
        "In this 30-minute English learning podcast lesson, you'll discover why English learners freeze when speaking, how to stop translating in your head, natural conversational phrases, real-world cafe roleplays, connected speech secrets, and a practical 7-day speaking challenge.",
        "",
        "🕒 CHAPTERS & TIMESTAMPS:"
    ]

    for ch in chapters_with_timestamps:
        time_str = time_to_timestamp(ch["start_time"])
        desc_lines.append(f"{time_str} - {ch['title']}")

    desc_lines.extend([
        "",
        "💡 WHAT YOU WILL LEARN IN THIS EPISODE:",
        "• Why your brain freezes when speaking English & how to relax",
        "• The mental translation trap and how to think directly in English",
        "• 10 natural alternatives to robotic textbook phrases",
        "• Real-life coffee shop and restaurant ordering dialogue roleplays",
        "• The Bridge Technique to never run out of things to say",
        "• Connected speech secrets ('wanna', 'gonna', rhythm & linking)",
        "• Actionable 7-day speaking challenge to practice out loud",
        "",
        "🔔 Subscribe to Learn English Champs for daily English learning podcasts, vocabulary tips, and speaking confidence lessons!",
        "",
        "#LearnEnglish #EnglishPodcast #LearnEnglishChamps #SpeakEnglish #EnglishConversation #OvercomeFearOfSpeaking #EnglishFluency #DailyEnglish"
    ])

    description = "\n".join(desc_lines)
    tags = [
        "learn english", "english podcast", "learn english champs", "english conversation",
        "overcome fear of speaking english", "speak english fluently", "daily english practice",
        "english speaking practice", "how to speak english naturally", "english listening practice",
        "english vocabulary", "english small talk", "learn english podcast 30 minutes"
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
