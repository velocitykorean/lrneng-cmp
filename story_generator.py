import os
import json
import random
import requests
import config

# Curated English learning podcast topics for variety and high YouTube CTR
CURATED_TOPICS = [
    {
        "topic": "Stop Saying 'Very' in English",
        "thumbnail_title_1": "STOP SAYING",
        "thumbnail_title_2": "VERY TIRED!",
        "thumbnail_hook": "10 Natural Alternatives",
        "dialogue": [
            {"speaker": "female", "name": "Emma", "text": "Alex, have you noticed how often English learners overuse the word 'very'?"},
            {"speaker": "male", "name": "Alex", "text": "All the time! Instead of saying 'very tired', natives usually say 'exhausted'."},
            {"speaker": "female", "name": "Emma", "text": "Exactly! And for 'very cold', you can say 'freezing'."},
            {"speaker": "male", "name": "Alex", "text": "What about 'very hungry'? You can simply say 'starving'!"},
            {"speaker": "female", "name": "Emma", "text": "Using advanced adjectives makes your English sound instantly more natural."},
            {"speaker": "male", "name": "Alex", "text": "Which one will you try today? Let us know in the comments!"}
        ]
    },
    {
        "topic": "How to Order Coffee Like a Native Speaker",
        "thumbnail_title_1": "ORDER COFFEE",
        "thumbnail_title_2": "LIKE A NATIVE!",
        "thumbnail_hook": "5 Natural Phrases",
        "dialogue": [
            {"speaker": "female", "name": "Emma", "text": "Today we're talking about ordering coffee without sounding like a textbook."},
            {"speaker": "male", "name": "Alex", "text": "Never say 'I want coffee please'. It sounds a bit robotic!"},
            {"speaker": "female", "name": "Emma", "text": "Instead, just say: 'Can I get an iced latte to go?'"},
            {"speaker": "male", "name": "Alex", "text": "Or even simpler: 'Could I have a medium cappuccino?'"},
            {"speaker": "female", "name": "Emma", "text": "Notice how polite and natural 'Can I get' sounds in everyday life."},
            {"speaker": "male", "name": "Alex", "text": "Try it next time you visit a cafe and see how easy it feels!"}
        ]
    },
    {
        "topic": "Common Slang You Hear in Everyday English",
        "thumbnail_title_1": "ENGLISH SLANG",
        "thumbnail_title_2": "YOU MUST KNOW!",
        "thumbnail_hook": "Speak Confidently Daily",
        "dialogue": [
            {"speaker": "female", "name": "Emma", "text": "Alex, what's a modern slang word that confuses English learners?"},
            {"speaker": "male", "name": "Alex", "text": "Definitely the phrase 'no worries' or when someone says 'I'm down'."},
            {"speaker": "female", "name": "Emma", "text": "Right! 'I'm down' actually means 'I'm interested' or 'I agree'!"},
            {"speaker": "male", "name": "Alex", "text": "So if your friend asks to hang out, just say 'I'm down!'"},
            {"speaker": "female", "name": "Emma", "text": "It sounds relaxed, friendly, and very natural in casual conversations."},
            {"speaker": "male", "name": "Alex", "text": "Keep listening to podcasts to catch more real-life English expressions."}
        ]
    }
]

def generate_story(topic: str = None, num_turns: int = 6) -> dict:
    """
    Generates an educational English learning dialogue using Pollinations AI,
    or falls back to curated scripts if offline or error occurs.
    """
    if topic:
        user_prompt = f"""You are an expert English teacher creating an engaging English learning podcast.
Generate a lively, natural conversation between two hosts: Emma (female) and Alex (male).
Topic: {topic}
Requirements:
- Exactly {num_turns} dialogue turns alternating between Emma and Alex.
- Keep each line relatively concise (under 16 words) so it fits nicely on a single subtitle line.
- Make it sound like two real podcast friends speaking clearly and warmly.
- Explain 1 or 2 practical English tips, phrases, or vocabulary.

Return ONLY a JSON object with this exact structure:
{{
  "topic": "{topic}",
  "thumbnail_title_1": "SHORT TITLE 1",
  "thumbnail_title_2": "SHORT TITLE 2",
  "thumbnail_hook": "Catchy Hook Pill (4-6 words)",
  "dialogue": [
    {{"speaker": "female", "name": "Emma", "text": "..."}},
    {{"speaker": "male", "name": "Alex", "text": "..."}}
  ]
}}"""
    else:
        user_prompt = f"""You are an expert English teacher creating an engaging English learning podcast.
Pick a high-interest topic (e.g. daily idioms, sounding polite, stopping common mistakes, ordering food, natural reactions).
Generate a lively, natural conversation between two hosts: Emma (female) and Alex (male).
Requirements:
- Exactly {num_turns} dialogue turns alternating between Emma and Alex.
- Keep each line relatively concise (under 16 words) so it fits nicely on a single subtitle line.
- Make it sound like two real podcast friends speaking clearly and warmly.
- Explain 1 or 2 practical English tips, phrases, or vocabulary.

Return ONLY a JSON object with this exact structure:
{{
  "topic": "Topic Name",
  "thumbnail_title_1": "SHORT TITLE 1",
  "thumbnail_title_2": "SHORT TITLE 2",
  "thumbnail_hook": "Catchy Hook Pill (4-6 words)",
  "dialogue": [
    {{"speaker": "female", "name": "Emma", "text": "..."}},
    {{"speaker": "male", "name": "Alex", "text": "..."}}
  ]
}}"""

    headers = {"Content-Type": "application/json"}
    if config.POLLINATIONS_API_KEY:
        headers["Authorization"] = f"Bearer {config.POLLINATIONS_API_KEY}"

    payload = {
        "messages": [
            {"role": "system", "content": "You are a JSON-only API that produces educational English learning scripts. Output ONLY raw valid JSON."},
            {"role": "user", "content": user_prompt}
        ],
        "model": config.POLLINATIONS_MODEL,
        "temperature": 0.7
    }

    try:
        print("[StoryGenerator] Requesting podcast script from Pollinations AI...")
        resp = requests.post(config.POLLINATIONS_ENDPOINT, json=payload, headers=headers, timeout=25)
        if resp.status_code == 200:
            content = resp.json()["choices"][0]["message"]["content"].strip()
            # Strip markdown fences if present
            if content.startswith("```"):
                lines = content.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                content = "\n".join(lines).strip()
            
            data = json.loads(content)
            if "dialogue" in data and len(data["dialogue"]) >= 4:
                print(f"[StoryGenerator] Successfully generated script for topic: '{data.get('topic')}'")
                return data
    except Exception as e:
        print(f"[StoryGenerator] Warning: API generation encountered error: {e}")

    # Fallback to curated topics
    print("[StoryGenerator] Using high-quality curated English learning script.")
    choice = random.choice(CURATED_TOPICS)
    return choice

if __name__ == "__main__":
    story = generate_story()
    print("Generated Topic:", story["topic"])
    for d in story["dialogue"]:
        print(f"[{d['name']}]: {d['text']}")
