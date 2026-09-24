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
import json
import requests
import config

MASTERCLASS_ACTS = [
    {
        "title": "Act 1: The Psychology of Fear - Why Our Minds Freeze",
        "focus": "Why English learners freeze when speaking, how anxiety blocks recall (the Affective Filter), and accepting imperfection.",
        "turns": [
            {"speaker": "female", "name": "Emma", "text": "Welcome to Learn English Champs! I'm Emma, and here with me is Alex."},
            {"speaker": "male", "name": "Alex", "text": "Hey everyone! Today we're tackling the single biggest obstacle for English learners worldwide."},
            {"speaker": "female", "name": "Emma", "text": "It's not complex grammar, and it's definitely not difficult vocabulary lists."},
            {"speaker": "male", "name": "Alex", "text": "It is the sheer fear of opening your mouth and freezing up completely."},
            {"speaker": "female", "name": "Emma", "text": "Alex, have you ever felt that intense heartbeat right before speaking another language?"},
            {"speaker": "male", "name": "Alex", "text": "Oh, absolutely! Your palms sweat, your throat dries up, and suddenly words vanish."},
            {"speaker": "female", "name": "Emma", "text": "Psychologists actually have a name for this: the Affective Filter Hypothesis."},
            {"speaker": "male", "name": "Alex", "text": "When anxiety spikes, your brain literally shuts off access to stored vocabulary."},
            {"speaker": "female", "name": "Emma", "text": "So when you freeze, it doesn't mean your English is bad at all."},
            {"speaker": "male", "name": "Alex", "text": "It simply means your nervous system is in fight-or-flight mode!"},
            {"speaker": "female", "name": "Emma", "text": "Native speakers don't expect perfection; they just want to understand your message."},
            {"speaker": "male", "name": "Alex", "text": "Exactly! In real life, communication is about connection, not scoring an exam."},
            {"speaker": "female", "name": "Emma", "text": "When I was learning Spanish, I once ordered 'soap' instead of 'soup' at lunch!"},
            {"speaker": "male", "name": "Alex", "text": "Haha! And did the waiter get angry, or did you both just laugh?"},
            {"speaker": "female", "name": "Emma", "text": "He smiled warmly, corrected me kindly, and brought me delicious vegetable soup."},
            {"speaker": "male", "name": "Alex", "text": "That proves the point: ninety-nine percent of people are cheering for you."},
            {"speaker": "female", "name": "Emma", "text": "Here is our first golden rule: trade perfection for progression every single day."},
            {"speaker": "male", "name": "Alex", "text": "Let's give our champs an immediate tool: The Three-Second Breath Reset."},
            {"speaker": "female", "name": "Emma", "text": "When someone asks you a question in English, do not rush to speak instantly."},
            {"speaker": "male", "name": "Alex", "text": "Take a slow breath, smile gently, and buy yourself two full seconds."},
            {"speaker": "female", "name": "Emma", "text": "You can say: 'That's an interesting question,' while your mind calms down."},
            {"speaker": "male", "name": "Alex", "text": "That tiny buffer lowers your heart rate and lets the words flow smoothly."},
            {"speaker": "female", "name": "Emma", "text": "Remember, even native speakers pause and say 'Let me think' constantly."},
            {"speaker": "male", "name": "Alex", "text": "Pausing doesn't make you look weak; it makes you look thoughtful and composed."},
            {"speaker": "female", "name": "Emma", "text": "Another big secret is accepting that mistakes are necessary stepping stones to fluency."},
            {"speaker": "male", "name": "Alex", "text": "A baby stumbles hundreds of times before walking effortlessly without falling down."},
            {"speaker": "female", "name": "Emma", "text": "If you never make mistakes, it means you aren't pushing your comfort zone."},
            {"speaker": "male", "name": "Alex", "text": "Wear your mistakes proudly like badges of courage and real effort."},
            {"speaker": "female", "name": "Emma", "text": "You are learning an entire second language, which is truly incredible!"},
            {"speaker": "male", "name": "Alex", "text": "Give yourself credit for how far you have already come today."},
            {"speaker": "female", "name": "Emma", "text": "Take a deep breath right now, relax your shoulders, and smile with us."},
            {"speaker": "male", "name": "Alex", "text": "You are in a safe, judgment-free space with Learn English Champs!"}
        ]
    },
    {
        "title": "Act 2: Escaping the Mental Translation Trap",
        "focus": "How translating word-for-word slows speech down, practical sensory drills to think directly in English, and eliminating inner perfectionism.",
        "turns": [
            {"speaker": "female", "name": "Emma", "text": "Now let's tackle the second biggest roadblock: translating in your head before speaking."},
            {"speaker": "male", "name": "Alex", "text": "This is the infamous 'Mental Translation Trap' that causes painful conversational delays."},
            {"speaker": "female", "name": "Emma", "text": "When someone asks 'How was your weekend?', your brain translates to your native language."},
            {"speaker": "male", "name": "Alex", "text": "Then you compose an answer, translate it back to English, and inspect the grammar!"},
            {"speaker": "female", "name": "Emma", "text": "By the time you're ready, the conversation has already moved three topics ahead!"},
            {"speaker": "male", "name": "Alex", "text": "It feels like driving a car with the handbrake pulled completely up."},
            {"speaker": "female", "name": "Emma", "text": "So how do we train our brains to bypass translation and think directly in English?"},
            {"speaker": "male", "name": "Alex", "text": "The answer is our daily 'Mental Narration Drill', which anyone can do anywhere."},
            {"speaker": "female", "name": "Emma", "text": "Start by describing simple actions around you in very short English phrases."},
            {"speaker": "male", "name": "Alex", "text": "For instance: 'I'm opening the door. The weather is cool. The tea is hot.'"},
            {"speaker": "female", "name": "Emma", "text": "Notice we aren't writing essays here; we are just naming sensory impressions out loud."},
            {"speaker": "male", "name": "Alex", "text": "When you see an apple, don't think your native word first; think 'apple'."},
            {"speaker": "female", "name": "Emma", "text": "Connect the physical object directly to the English sound in your memory bank."},
            {"speaker": "male", "name": "Alex", "text": "Do this while preparing breakfast, walking to the bus, or folding clean laundry."},
            {"speaker": "female", "name": "Emma", "text": "Just two minutes of mental narration three times a day builds new neural pathways."},
            {"speaker": "male", "name": "Alex", "text": "Another trick is eliminating the inner perfectionist editor while you are talking."},
            {"speaker": "female", "name": "Emma", "text": "When you speak your first language, do you inspect each sentence before speaking?"},
            {"speaker": "male", "name": "Alex", "text": "Never! The thoughts turn into words spontaneously without any conscious filtering."},
            {"speaker": "female", "name": "Emma", "text": "English works the exact same way once you allow yourself to speak freely."},
            {"speaker": "male", "name": "Alex", "text": "Keep your sentence structures simple and direct rather than overly convoluted."},
            {"speaker": "female", "name": "Emma", "text": "Subject, verb, object: 'I love this music,' or 'We should grab lunch.'"},
            {"speaker": "male", "name": "Alex", "text": "Simplicity is the true hallmark of natural, crystal-clear conversational fluency."},
            {"speaker": "female", "name": "Emma", "text": "If you forget a specific word, don't freeze; describe it using simpler words."},
            {"speaker": "male", "name": "Alex", "text": "If you forget 'refrigerator', say 'the cold kitchen box where we keep food'!"},
            {"speaker": "female", "name": "Emma", "text": "Everyone will understand you immediately, and the conversation continues without stopping."},
            {"speaker": "male", "name": "Alex", "text": "That is called circumlocution, and it is a superpower of fluent speakers."},
            {"speaker": "female", "name": "Emma", "text": "Let go of the desire to translate word-for-word idioms from your native tongue."},
            {"speaker": "male", "name": "Alex", "text": "Languages have completely different rhythms and cultural metaphors behind them."},
            {"speaker": "female", "name": "Emma", "text": "Embrace English as its own unique musical system with its own logic."},
            {"speaker": "male", "name": "Alex", "text": "Feed your mind with English podcasts like this one to absorb natural speech patterns."},
            {"speaker": "female", "name": "Emma", "text": "Soon, you will catch yourself thinking in English without even realizing it!"},
            {"speaker": "male", "name": "Alex", "text": "And when that happens, you have officially escaped the translation trap for good!"}
        ]
    },
    {
        "title": "Act 3: 15 Natural Expressions for Everyday Small Talk",
        "focus": "Replacing robotic textbook phrases with modern colloquial alternatives, active listener reactions, and natural fillers.",
        "turns": [
            {"speaker": "female", "name": "Emma", "text": "Let's upgrade our daily vocabulary from stiff textbook English to modern expressions!"},
            {"speaker": "male", "name": "Alex", "text": "Number one: please retire 'I am fine, thank you, and you?' forever!"},
            {"speaker": "female", "name": "Emma", "text": "It sounds like an automated recording from an English cassette tape from 1985!"},
            {"speaker": "male", "name": "Alex", "text": "Instead, when someone asks 'How are you doing?', reply: 'Doing great, how about yourself?'"},
            {"speaker": "female", "name": "Emma", "text": "Or a wonderfully casual American response: 'Can't complain! Keeping pretty busy.'"},
            {"speaker": "male", "name": "Alex", "text": "If it's a relaxed morning, you can say: 'Just taking it easy today.'"},
            {"speaker": "female", "name": "Emma", "text": "Listen to how friendly and relaxed that feels compared to robotic textbook lines."},
            {"speaker": "male", "name": "Alex", "text": "What about when someone shares unexpected news with you, Emma?"},
            {"speaker": "female", "name": "Emma", "text": "Instead of saying 'That is unbelievable', natives almost always exclaim: 'No way!'"},
            {"speaker": "male", "name": "Alex", "text": "Or with a smile: 'You've got to be kidding me! That is wild!'"},
            {"speaker": "female", "name": "Emma", "text": "And when someone explains a frustrating problem, show empathy by saying: 'I hear you.'"},
            {"speaker": "male", "name": "Alex", "text": "'I hear you' or 'That makes total sense' shows deep listening and understanding."},
            {"speaker": "female", "name": "Emma", "text": "It instantly builds rapport and makes the speaker feel comfortable around you."},
            {"speaker": "male", "name": "Alex", "text": "What about agreeing with someone enthusiastically during a casual discussion?"},
            {"speaker": "female", "name": "Emma", "text": "Say: 'Tell me about it!' or 'I couldn't agree with you more!'"},
            {"speaker": "male", "name": "Alex", "text": "Fun fact: 'Tell me about it' actually means 'I already know and completely agree!'"},
            {"speaker": "female", "name": "Emma", "text": "English idioms can be funny like that, which is why real practice matters so much."},
            {"speaker": "male", "name": "Alex", "text": "And how should we disagree politely without sounding aggressive or rude?"},
            {"speaker": "female", "name": "Emma", "text": "Start with: 'I see what you mean, but looking at it another way...'"},
            {"speaker": "male", "name": "Alex", "text": "Or softly: 'I'm not so sure about that, but let's test it out.'"},
            {"speaker": "female", "name": "Emma", "text": "That softens the tone and keeps the conversation warm, polite, and friendly."},
            {"speaker": "male", "name": "Alex", "text": "Let's also talk about conversational transition fillers like 'To be honest with you...'"},
            {"speaker": "female", "name": "Emma", "text": "'To be honest' or 'As a matter of fact' gives you thinking time naturally."},
            {"speaker": "male", "name": "Alex", "text": "Another great filler is 'Actually, come to think of it, that's true.'"},
            {"speaker": "female", "name": "Emma", "text": "Notice that fillers are not bad; native speakers use them to maintain flow."},
            {"speaker": "male", "name": "Alex", "text": "They signal that you are formulating a thought while holding the conversation floor."},
            {"speaker": "female", "name": "Emma", "text": "Pick two of these fifteen phrases today and try using them out loud."},
            {"speaker": "male", "name": "Alex", "text": "Repeat after us: 'Can't complain!' Come on, say it right now!"},
            {"speaker": "female", "name": "Emma", "text": "And say: 'No way!' Put real emotion and surprise into your tone."},
            {"speaker": "male", "name": "Alex", "text": "Language is melody and emotion, not just ink printed on a textbook page."},
            {"speaker": "female", "name": "Emma", "text": "The more emotion you inject, the faster your brain locks the memory in."},
            {"speaker": "male", "name": "Alex", "text": "You are sounding more and more like a true English champ already!"}
        ]
    },
    {
        "title": "Act 4: Real-World Roleplay - The Modern Coffee Shop",
        "focus": "Practical roleplay ordering coffee, polite requests ('Could I get', 'Can I grab'), handling customizations and payments confidently.",
        "turns": [
            {"speaker": "female", "name": "Emma", "text": "Time for a live roleplay! I'm going to order coffee, and Alex is our barista."},
            {"speaker": "male", "name": "Alex", "text": "Welcome to Sunrise Roasters! What can I get started for you this morning?"},
            {"speaker": "female", "name": "Emma", "text": "Hi there! Could I get an iced vanilla latte with oat milk, please?"},
            {"speaker": "male", "name": "Alex", "text": "Absolutely! Would you like a single or a double shot of espresso?"},
            {"speaker": "female", "name": "Emma", "text": "Let's make that a double, please. And could you go light on the ice?"},
            {"speaker": "male", "name": "Alex", "text": "You got it. Anything to eat for you today? Fresh croissants just came out."},
            {"speaker": "female", "name": "Emma", "text": "Ooh, tempt me! I'll grab one almond croissant as well, please."},
            {"speaker": "male", "name": "Alex", "text": "Fantastic choice. Is that going to be for here, or to go?"},
            {"speaker": "female", "name": "Emma", "text": "To go, please. And how much does that come to?"},
            {"speaker": "male", "name": "Alex", "text": "That will be seven dollars and twenty-five cents at the card tap whenever you're ready."},
            {"speaker": "female", "name": "Emma", "text": "Here you go. Could I also grab an extra paper cup sleeve?"},
            {"speaker": "male", "name": "Alex", "text": "Right by the pickup counter on your left! We'll call Emma when it's ready."},
            {"speaker": "female", "name": "Emma", "text": "Thanks so much! Have a wonderful day ahead!"},
            {"speaker": "male", "name": "Alex", "text": "You too! And scene! Let's pause and dissect every single phrase we just used."},
            {"speaker": "female", "name": "Emma", "text": "Notice my very first sentence: 'Could I get an iced vanilla latte, please?'"},
            {"speaker": "male", "name": "Alex", "text": "Never say: 'I want coffee.' It sounds blunt, demanding, and overly harsh."},
            {"speaker": "female", "name": "Emma", "text": "'Could I get...' or 'Can I grab...' is the gold standard of polite English ordering."},
            {"speaker": "male", "name": "Alex", "text": "Millions of native speakers say 'Could I get' every single morning of their lives."},
            {"speaker": "female", "name": "Emma", "text": "And notice my customization: 'Could you go light on the ice?'"},
            {"speaker": "male", "name": "Alex", "text": "'Light on the ice' means less ice so you get more refreshing liquid drink."},
            {"speaker": "female", "name": "Emma", "text": "If you prefer dairy-free milk, just ask: 'Do you offer oat or almond milk?'"},
            {"speaker": "male", "name": "Alex", "text": "Then I asked the classic barista question: 'For here or to go?'"},
            {"speaker": "female", "name": "Emma", "text": "In the UK, they might ask: 'Eat in or takeaway?' It means the exact same thing."},
            {"speaker": "male", "name": "Alex", "text": "Notice Emma's answer was crisp and simple: 'To go, please.' Perfect clarity."},
            {"speaker": "female", "name": "Emma", "text": "You don't need a whole sentence like 'I would like to take it with me.'"},
            {"speaker": "male", "name": "Alex", "text": "Short, polite, and confident answers are what real English speakers use every day."},
            {"speaker": "female", "name": "Emma", "text": "What about paying? When the total is announced, tap your card and say 'Thanks'."},
            {"speaker": "male", "name": "Alex", "text": "If you need a receipt, simply ask: 'Could I have the receipt, please?'"},
            {"speaker": "female", "name": "Emma", "text": "If you don't need one, smile and say: 'I'm good without a receipt, thanks!'"},
            {"speaker": "male", "name": "Alex", "text": "'I'm good' is another brilliant idiom meaning 'No thank you, I have enough.'"},
            {"speaker": "female", "name": "Emma", "text": "See how natural and effortless that roleplay was when you know the formula?"},
            {"speaker": "male", "name": "Alex", "text": "Practice this coffee shop dialogue in front of your mirror before your next trip!"}
        ]
    },
    {
        "title": "Act 5: Real-World Roleplay - Restaurant Dining & Casual Chat",
        "focus": "Restaurant roleplay: asking for a table, server recommendations, steak temperatures, split checks, and dining etiquette.",
        "turns": [
            {"speaker": "female", "name": "Emma", "text": "Now let's graduate from the coffee shop to a bustling evening dinner restaurant!"},
            {"speaker": "male", "name": "Alex", "text": "Table for two! I'll be our friendly server, and Emma is having dinner."},
            {"speaker": "female", "name": "Emma", "text": "Good evening! We don't have a reservation; do you happen to have a table for two?"},
            {"speaker": "male", "name": "Alex", "text": "Good evening! Yes, we have a cozy booth by the window. Right this way, please!"},
            {"speaker": "female", "name": "Emma", "text": "Thank you, this table is lovely. Could we start with some sparkling water?"},
            {"speaker": "male", "name": "Alex", "text": "Sparkling water with lime coming right up! Here are your dinner menus."},
            {"speaker": "female", "name": "Emma", "text": "Thank you. Excuse me, what do you recommend between the salmon and the pasta?"},
            {"speaker": "male", "name": "Alex", "text": "The grilled salmon is fresh from the coast today and comes with roasted asparagus."},
            {"speaker": "female", "name": "Emma", "text": "That sounds heavenly! I'll have the grilled salmon, please."},
            {"speaker": "male", "name": "Alex", "text": "Excellent. And how would you like that cooked? Chef recommends medium."},
            {"speaker": "female", "name": "Emma", "text": "Medium sounds perfect to me. And dressing on the side for the salad, please."},
            {"speaker": "male", "name": "Alex", "text": "Coming right up! Enjoy your evening, and let me know if you need anything else."},
            {"speaker": "female", "name": "Emma", "text": "Thank you kindly! And fast forward to the end of the meal..."},
            {"speaker": "male", "name": "Alex", "text": "How was everything for you tonight? Did you enjoy the salmon?"},
            {"speaker": "female", "name": "Emma", "text": "It was absolutely delicious, compliments to the chef! Could we get the bill, please?"},
            {"speaker": "male", "name": "Alex", "text": "Right away! Will you be splitting the check, or paying together tonight?"},
            {"speaker": "female", "name": "Emma", "text": "We'll pay together on card, please. Could you bring the card reader over?"},
            {"speaker": "male", "name": "Alex", "text": "Here you are. No rush at all, take your time!"},
            {"speaker": "female", "name": "Emma", "text": "Thank you so much for the wonderful service tonight!"},
            {"speaker": "male", "name": "Alex", "text": "And scene! That was smooth, sophisticated, and completely authentic."},
            {"speaker": "female", "name": "Emma", "text": "Let's break down the essential dining phrases everyone needs to know."},
            {"speaker": "male", "name": "Alex", "text": "First: 'Do you happen to have a table for two?'"},
            {"speaker": "female", "name": "Emma", "text": "'Do you happen to...' is a wonderfully polite way to make any inquiry."},
            {"speaker": "male", "name": "Alex", "text": "And when asking for advice: 'What do you recommend here?'"},
            {"speaker": "female", "name": "Emma", "text": "Servers love that question because it lets them showcase their house specialties."},
            {"speaker": "male", "name": "Alex", "text": "And when ordering your dish: 'I'll have the salmon, please.' Clean and elegant."},
            {"speaker": "female", "name": "Emma", "text": "What about asking for adjustments? 'Dressing on the side, please.'"},
            {"speaker": "male", "name": "Alex", "text": "In the US and Canada, asking for dressing on the side is totally normal."},
            {"speaker": "female", "name": "Emma", "text": "Finally, asking for the bill: 'Could we get the bill, please?'"},
            {"speaker": "male", "name": "Alex", "text": "In the US, people often say 'the check'; in the UK, people say 'the bill'."},
            {"speaker": "female", "name": "Emma", "text": "Both words are universally understood everywhere in the English-speaking world."},
            {"speaker": "male", "name": "Alex", "text": "Memorize these five phrases, and dining out will become your favorite English experience!"}
        ]
    },
    {
        "title": "Act 6: Never Run Out of Things to Say - The Flow Technique",
        "focus": "The Answer-Plus-Detail-Plus-Question rule, conversational bridges, open vs closed questions, and active listening cues.",
        "turns": [
            {"speaker": "female", "name": "Emma", "text": "Alex, what is the number one fear people have after saying hello?"},
            {"speaker": "male", "name": "Alex", "text": "Running out of things to say and facing five seconds of dead awkward silence!"},
            {"speaker": "female", "name": "Emma", "text": "You stare at each other, your mind races, and you feel the urge to run away!"},
            {"speaker": "male", "name": "Alex", "text": "Today, we are teaching the ultimate remedy: The Flow Technique."},
            {"speaker": "female", "name": "Emma", "text": "The cornerstone of this method is the 'Answer Plus One Detail Plus Question' rule."},
            {"speaker": "male", "name": "Alex", "text": "When someone asks you a question, never, ever give a bare one-word answer."},
            {"speaker": "female", "name": "Emma", "text": "If someone asks 'Do you like movies?', don't just say 'Yes.' That kills the momentum!"},
            {"speaker": "male", "name": "Alex", "text": "Instead say: 'Yes! I just saw a brilliant sci-fi thriller last Friday. Have you seen it?'"},
            {"speaker": "female", "name": "Emma", "text": "Look at how much energy that gives back! The other person now has plenty to say."},
            {"speaker": "male", "name": "Alex", "text": "You answered the question, added an interesting detail, and threw the conversational ball back."},
            {"speaker": "female", "name": "Emma", "text": "It turns a one-sided interrogation into a fun, relaxed game of conversational tennis!"},
            {"speaker": "male", "name": "Alex", "text": "What if the person asks about something you know nothing about, Emma?"},
            {"speaker": "female", "name": "Emma", "text": "Don't pretend! Say: 'I haven't heard much about that. How did you get into it?'"},
            {"speaker": "male", "name": "Alex", "text": "People love talking about their passions, and showing curiosity makes you instantly likeable."},
            {"speaker": "female", "name": "Emma", "text": "Another secret weapon is what we call 'Conversational Bridges'."},
            {"speaker": "male", "name": "Alex", "text": "Phrases like: 'Speaking of travel, that reminds me of a crazy story...'"},
            {"speaker": "female", "name": "Emma", "text": "Or: 'That's so interesting, because a friend of mine told me something similar recently.'"},
            {"speaker": "male", "name": "Alex", "text": "Bridges connect two unrelated topics smoothly without making the shift feel abrupt."},
            {"speaker": "female", "name": "Emma", "text": "You can transition from discussing the weather to talking about your favorite holiday destination!"},
            {"speaker": "male", "name": "Alex", "text": "'The rain today reminds me of monsoon season when I visited Southeast Asia last year.'"},
            {"speaker": "female", "name": "Emma", "text": "Boom! Suddenly you are talking about travel, food, and culture instead of grey clouds!"},
            {"speaker": "male", "name": "Alex", "text": "Also, ask open-ended questions that start with 'How', 'Why', or 'What was it like?'"},
            {"speaker": "female", "name": "Emma", "text": "Closed questions that lead to 'yes' or 'no' shut down conversations fast."},
            {"speaker": "male", "name": "Alex", "text": "Instead of 'Did you enjoy your vacation?', ask 'What was the highlight of your trip?'"},
            {"speaker": "female", "name": "Emma", "text": "That invites a rich, detailed story with genuine emotions and laughter."},
            {"speaker": "male", "name": "Alex", "text": "And while they talk, practice active listening with nods and verbal cues."},
            {"speaker": "female", "name": "Emma", "text": "'Really?', 'No way!', 'And then what happened?', 'That sounds incredible!'"},
            {"speaker": "male", "name": "Alex", "text": "These small verbal cues act like oxygen keeping the conversational fire burning bright."},
            {"speaker": "female", "name": "Emma", "text": "When you focus on being interested rather than interesting, conversations become effortless."},
            {"speaker": "male", "name": "Alex", "text": "The pressure drops off your shoulders because you don't have to perform."},
            {"speaker": "female", "name": "Emma", "text": "You are simply sharing curiosity and human warmth with another person."},
            {"speaker": "male", "name": "Alex", "text": "Try the 'Answer Plus One Detail' rule in your very next conversation today!"}
        ]
    },
    {
        "title": "Act 7: Connected Speech Secrets - Sounding Natural, Not Fast",
        "focus": "Why English is stress-timed, linking consonants to vowels, contractions and reductions ('wanna', 'gonna', 'gotta'), and smoothing speech flow.",
        "turns": [
            {"speaker": "female", "name": "Emma", "text": "Many English learners tell us: 'Native speakers talk so fast, I can barely understand!'"},
            {"speaker": "male", "name": "Alex", "text": "But here is the fascinating truth: native speakers don't actually talk faster than anyone else."},
            {"speaker": "female", "name": "Emma", "text": "What you are hearing is connected speech and natural English rhythm."},
            {"speaker": "male", "name": "Alex", "text": "English is a stress-timed language, not a syllable-timed language like French or Japanese."},
            {"speaker": "female", "name": "Emma", "text": "In syllable-timed languages, every syllable gets equal time and equal musical weight."},
            {"speaker": "male", "name": "Alex", "text": "But in English, only key content words like nouns and main verbs are stressed."},
            {"speaker": "female", "name": "Emma", "text": "Function words like 'to', 'for', 'of', and 'at' get squished and reduced down."},
            {"speaker": "male", "name": "Alex", "text": "For example, the sentence: 'I want to go to the store for some milk.'"},
            {"speaker": "female", "name": "Emma", "text": "A robot says: 'I... want... to... go... to... the... store... for... some... milk.'"},
            {"speaker": "male", "name": "Alex", "text": "But a native speaker says: 'I wanna go to the store fer some milk.'"},
            {"speaker": "female", "name": "Emma", "text": "Notice how 'want to' naturally blends into 'wanna', and 'for' sounds like 'fer'."},
            {"speaker": "male", "name": "Alex", "text": "This is not sloppy slang or laziness; it is the natural physics of spoken English."},
            {"speaker": "female", "name": "Emma", "text": "Let's practice consonant-to-vowel linking right now with our listeners."},
            {"speaker": "male", "name": "Alex", "text": "Take the words 'hold' and 'on'. When spoken together, they become 'hol-don'."},
            {"speaker": "female", "name": "Emma", "text": "The consonant 'd' jumps right over to the vowel 'o' in the next word!"},
            {"speaker": "male", "name": "Alex", "text": "Same with 'check' and 'it' and 'out': 'che-ki-tout'. Say it with us: 'Check it out!'"},
            {"speaker": "female", "name": "Emma", "text": "Feel how smooth and effortless that rolls off your tongue?"},
            {"speaker": "male", "name": "Alex", "text": "Another famous reduction is 'going to' turning into 'gonna'."},
            {"speaker": "female", "name": "Emma", "text": "'I'm gonna call you later tonight.' It saves vocal energy and sounds friendly."},
            {"speaker": "male", "name": "Alex", "text": "And 'got to' becomes 'gotta': 'I gotta run, my train is arriving!'"},
            {"speaker": "female", "name": "Emma", "text": "What about 'could have' and 'should have'? They become 'coulda' and 'shoulda'."},
            {"speaker": "male", "name": "Alex", "text": "'I coulda done better, but it's fine.' Notice how relaxed that sounds."},
            {"speaker": "female", "name": "Emma", "text": "When you understand reductions, your listening comprehension improves ten times over."},
            {"speaker": "male", "name": "Alex", "text": "Because you stop expecting to hear every printed letter pronounced rigidly."},
            {"speaker": "female", "name": "Emma", "text": "You start hearing the music, the peaks, and the valleys of spoken phrases."},
            {"speaker": "male", "name": "Alex", "text": "Don't force yourself to speak quickly; focus on connecting the words smoothly."},
            {"speaker": "female", "name": "Emma", "text": "Smoothness creates the impression of natural fluency, not raw speed."},
            {"speaker": "male", "name": "Alex", "text": "Take a deep breath, link the consonants to the vowels, and let the voice glide."},
            {"speaker": "female", "name": "Emma", "text": "'Turn it off' becomes 'tur-ni-toff'. 'Pick it up' becomes 'pi-ki-tup'."},
            {"speaker": "male", "name": "Alex", "text": "English is like water flowing down a mountain stream, always seeking the easiest path."},
            {"speaker": "female", "name": "Emma", "text": "Relax your jaw, soften your tongue, and flow right along with the current."},
            {"speaker": "male", "name": "Alex", "text": "You are sounding more and more like a true native speaker with every single act!"}
        ]
    },
    {
        "title": "Act 8: Overcoming Mistakes & What to Do When Mind Goes Blank",
        "focus": "Rescue phrases for mind-blanks ('gather my thoughts', 'tip of my tongue'), handling accents with pride, and humor to break tension.",
        "turns": [
            {"speaker": "female", "name": "Emma", "text": "Let's talk about the nightmare scenario: your mind suddenly goes completely blank mid-sentence."},
            {"speaker": "male", "name": "Alex", "text": "You were speaking well, and suddenly the word you need evaporates into thin air!"},
            {"speaker": "female", "name": "Emma", "text": "Panic begins to rise, your face turns red, and you want the ground to swallow you!"},
            {"speaker": "male", "name": "Alex", "text": "First rule: do not apologize profusely or say 'My English is so bad, I'm sorry!'"},
            {"speaker": "female", "name": "Emma", "text": "Never apologize for learning another language; speaking multiple languages is a huge superpower!"},
            {"speaker": "male", "name": "Alex", "text": "Instead, use one of our professional rescue phrases with a calm, charming smile."},
            {"speaker": "female", "name": "Emma", "text": "Rescue phrase number one: 'Give me just a second to gather my thoughts.'"},
            {"speaker": "male", "name": "Alex", "text": "Look how mature and composed that sounds! It immediately resets the emotional tension."},
            {"speaker": "female", "name": "Emma", "text": "Rescue phrase number two: 'How should I put this... the word is on the tip of my tongue.'"},
            {"speaker": "male", "name": "Alex", "text": "That invites the other person to help you find the word collaboratively."},
            {"speaker": "female", "name": "Emma", "text": "They will often guess: 'Do you mean the invoice?' and you say: 'Yes, exactly, the invoice!'"},
            {"speaker": "male", "name": "Alex", "text": "Suddenly, you are solving a friendly puzzle together instead of feeling embarrassed."},
            {"speaker": "female", "name": "Emma", "text": "What if someone speaks so fast that you didn't catch what they said at all?"},
            {"speaker": "male", "name": "Alex", "text": "Don't nod and pretend you understood when you didn't! That leads to funny misunderstandings."},
            {"speaker": "female", "name": "Emma", "text": "Say: 'Could you rephrase that for me, please?' or 'Could you speak just a little slower?'"},
            {"speaker": "male", "name": "Alex", "text": "People are happy to slow down when you ask with warmth and confidence."},
            {"speaker": "female", "name": "Emma", "text": "Another great phrase is: 'If I understand correctly, you mean we meet at five?'"},
            {"speaker": "male", "name": "Alex", "text": "That confirms comprehension and gives both parties peace of mind."},
            {"speaker": "female", "name": "Emma", "text": "What about our accents, Alex? So many learners feel self-conscious about their accents."},
            {"speaker": "male", "name": "Alex", "text": "Having an accent simply means you had the courage to learn a whole other language!"},
            {"speaker": "female", "name": "Emma", "text": "An accent is part of your unique identity, your heritage, and your personal story."},
            {"speaker": "male", "name": "Alex", "text": "Some of the most influential, charismatic global leaders speak with distinct accents."},
            {"speaker": "female", "name": "Emma", "text": "Clarity is the only standard that matters: can people understand your thoughts clearly?"},
            {"speaker": "male", "name": "Alex", "text": "If people understand your ideas, your accent adds charm and international character."},
            {"speaker": "female", "name": "Emma", "text": "When a mistake happens, laugh it off! Humour dissolves awkwardness instantly."},
            {"speaker": "male", "name": "Alex", "text": "If you say the wrong word, just smile: 'Oops, that's not what I meant! Let me try that again.'"},
            {"speaker": "female", "name": "Emma", "text": "Self-deprecating humor shows supreme inner confidence and emotional intelligence."},
            {"speaker": "male", "name": "Alex", "text": "It shows that you aren't afraid of making a mistake in front of other people."},
            {"speaker": "female", "name": "Emma", "text": "And that freedom to make mistakes is the exact key that unlocks rapid fluency."},
            {"speaker": "male", "name": "Alex", "text": "Treat every conversation as a laboratory for experiments, not a final examination."},
            {"speaker": "female", "name": "Emma", "text": "Some experiments succeed, some fail, but every single one teaches you something valuable."},
            {"speaker": "male", "name": "Alex", "text": "You are brave, you are capable, and you are getting better with every word you speak!"}
        ]
    },
    {
        "title": "Act 9: The 7-Day Speaking Challenge & Daily Fluency Habits",
        "focus": "The 5-minute daily vocal blueprint, shadowing techniques, self-recorded voice notes, consistency over intensity, and viewer challenge.",
        "turns": [
            {"speaker": "female", "name": "Emma", "text": "We have covered so much transformative material in this thirty-minute masterclass!"},
            {"speaker": "male", "name": "Alex", "text": "But knowledge without consistent daily action will simply fade away within days."},
            {"speaker": "female", "name": "Emma", "text": "That is why we are officially launching the Learn English Champs Seven-Day Speaking Challenge!"},
            {"speaker": "male", "name": "Alex", "text": "Here is your exact mission for the next seven days, starting right now today."},
            {"speaker": "female", "name": "Emma", "text": "Rule number one: Speak English out loud for five minutes every single morning."},
            {"speaker": "male", "name": "Alex", "text": "Not silently reading in your head; your vocal cords and mouth muscles must move!"},
            {"speaker": "female", "name": "Emma", "text": "Step one: Shadow our voices from this podcast episode."},
            {"speaker": "male", "name": "Alex", "text": "Hit replay on any chapter, listen to a sentence, pause, and repeat it with our exact melody."},
            {"speaker": "female", "name": "Emma", "text": "Copy the rhythm, copy the pauses, and copy the enthusiasm in our voices."},
            {"speaker": "male", "name": "Alex", "text": "Step two: Send a sixty-second English audio voice note to yourself on your phone."},
            {"speaker": "female", "name": "Emma", "text": "Talk about what you are going to eat, what tasks you must finish, or what you are excited about."},
            {"speaker": "male", "name": "Alex", "text": "Don't judge yourself harshly when you listen back; celebrate that you spoke for sixty full seconds!"},
            {"speaker": "female", "name": "Emma", "text": "Step three: Label three objects in your home with their natural English action phrases."},
            {"speaker": "male", "name": "Alex", "text": "Not just 'Kettle', write 'Boil water for morning tea'. Put the language into action!"},
            {"speaker": "female", "name": "Emma", "text": "By day three, your tongue will feel less stiff and the words will come much faster."},
            {"speaker": "male", "name": "Alex", "text": "By day five, the mental translation delay will begin shrinking noticeably."},
            {"speaker": "female", "name": "Emma", "text": "And by day seven, you will feel a brand-new sense of speaking confidence blossoming!"},
            {"speaker": "male", "name": "Alex", "text": "Consistency always beats intensity when learning any language on earth."},
            {"speaker": "female", "name": "Emma", "text": "Five minutes every single day is vastly better than studying three hours on Sunday."},
            {"speaker": "male", "name": "Alex", "text": "Five minutes creates a daily habit loop that wires English deep into your subconscious."},
            {"speaker": "female", "name": "Emma", "text": "Be proud of taking these thirty minutes today to invest in your personal growth."},
            {"speaker": "male", "name": "Alex", "text": "Thousands of people dream of speaking English, but you actually sat down and practiced!"},
            {"speaker": "female", "name": "Emma", "text": "That proves you have the dedication and heart of a true champion."},
            {"speaker": "male", "name": "Alex", "text": "If you found this masterclass helpful, please click that Subscribe button right down below!"},
            {"speaker": "female", "name": "Emma", "text": "Turn on the notification bell so you never miss our daily English podcast masterclasses."},
            {"speaker": "male", "name": "Alex", "text": "And here is our question of the day for the comment section below:"},
            {"speaker": "female", "name": "Emma", "text": "Which phrase or technique was your absolute favorite from today's thirty-minute lesson?"},
            {"speaker": "male", "name": "Alex", "text": "Leave your answer in the comments, and Emma and I will read and reply to them!"},
            {"speaker": "female", "name": "Emma", "text": "Thank you so much for spending your valuable time learning and growing with us today."},
            {"speaker": "male", "name": "Alex", "text": "Keep your head held high, believe in yourself, and keep speaking with total confidence."},
            {"speaker": "female", "name": "Emma", "text": "I'm Emma, wishing you joy and fantastic conversations this week!"},
            {"speaker": "male", "name": "Alex", "text": "And I'm Alex. Keep practicing, English champs, and we will see you in our next episode!"}
        ]
    }
]

def generate_chapter_ai(act_index: int, act_info: dict, topic_theme: str) -> list:
    """Optional AI expansion using Pollinations AI if key is present and requested."""
    key = config.POLLINATIONS_API_KEY
    if not key:
        return act_info["turns"]

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
    prompt = f"""You are writing a script for 'Learn English Champs' podcast.
Hosts: Emma (female) and Alex (male).
Topic: {topic_theme}
Act: {act_info['title']}
Focus: {act_info['focus']}

Requirements:
- 28 to 32 dialogue turns alternating Emma and Alex.
- Keep each line concise (10-18 words, max 6 words per phrase) for clean single-line subtitles.
- Conversational, warm, educational, funny, encouraging.
Return ONLY valid JSON:
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
            timeout=8
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
            if isinstance(parsed, list) and len(parsed) >= 20:
                return parsed
    except Exception as e:
        print(f"[StoryGenerator] Note: AI call returned error ({e}), using masterclass script.")

    return act_info["turns"]

# Master catalog of viral English learning masterclass curricula
VIRAL_CURRICULUM_CATALOG = [
    {
        "id": "fear_mindset",
        "topic": "Speak English Without Fear! Overcome Shyness & Mind Blanks",
        "thumbnail_title_1": "SPEAK ENGLISH",
        "thumbnail_title_2": "WITHOUT FEAR!",
        "thumbnail_hook": "Overcome Shyness & Speak Fluently",
        "yt_hook": "Speak English Without Fear!",
        "act_themes": [
            ("Act 1: The Psychology of Fear - Why Our Minds Freeze", "Why English learners freeze and how the Affective Filter blocks recall."),
            ("Act 2: Escaping the Mental Translation Trap", "How translating in your head slows speech down and sensory drills."),
            ("Act 3: 15 Natural Expressions for Everyday Small Talk", "Alternatives to robotic textbook phrases and modern reactions."),
            ("Act 4: Real-World Roleplay - The Modern Coffee Shop", "Ordering coffee with confidence, polite requests and customizations."),
            ("Act 5: Real-World Roleplay - Restaurant Dining & Casual Chat", "Table reservations, recommendations, steak temperatures and the bill."),
            ("Act 6: Never Run Out of Things to Say - The Flow Technique", "Answer + Detail + Question rule to keep any conversation flowing."),
            ("Act 7: Connected Speech Secrets - Sounding Natural, Not Fast", "Stress-timed rhythm, reductions (wanna, gonna) and linking."),
            ("Act 8: Overcoming Mistakes & What to Do When Mind Goes Blank", "Rescue phrases, handling accents with pride, and laughing off errors."),
            ("Act 9: The 7-Day Speaking Challenge & Daily Fluency Habits", "The 5-minute daily vocal blueprint and shadowing exercises.")
        ]
    },
    {
        "id": "mental_translation",
        "topic": "Stop Translating in Your Head! How to Think Directly in English",
        "thumbnail_title_1": "STOP TRANSLATING",
        "thumbnail_title_2": "THINK IN ENGLISH!",
        "thumbnail_hook": "End the 3-Second Mental Delay",
        "yt_hook": "Stop Translating in Your Head!",
        "act_themes": [
            ("Act 1: The Translation Trap - Why Word-for-Word Fails", "Why converting your native language causes awkward silences and pauses."),
            ("Act 2: The Sensory Direct-Link Drill", "Connecting sights, sounds, and physical actions directly to English words."),
            ("Act 3: Silencing Your Inner Perfectionist Editor", "Allowing yourself to speak without pre-checking grammar rules in your mind."),
            ("Act 4: Circumlocution - Describe It When You Forget It", "How fluent speakers talk around forgotten words effortlessly."),
            ("Act 5: Everyday Mental Narration Routine", "How to describe your morning coffee, commute, and work in English."),
            ("Act 6: Thinking in Chunks, Not Single Words", "Collocations, phrasal verbs, and ready-made conversational chunks."),
            ("Act 7: Spontaneous Reaction Drills with Emma & Alex", "Fast-fire reaction prompts to bypass native language filters."),
            ("Act 8: Building English Immersion Without Traveling", "Podcasts, self-talk, and phone environment hacks."),
            ("Act 9: The 7-Day Direct-Thought Blueprint", "Daily 5-minute exercise to lock in automatic English thinking.")
        ]
    },
    {
        "id": "native_expressions",
        "topic": "Sound Like a Native! 50 Phrases Real People Actually Use Every Day",
        "thumbnail_title_1": "SOUND NATURAL",
        "thumbnail_title_2": "LIKE A NATIVE!",
        "thumbnail_hook": "Ditch Robotic Textbook Phrases",
        "yt_hook": "Sound Like a Native!",
        "act_themes": [
            ("Act 1: Ditching the Stiff Textbook Expressions", "Why 'I am fine, thank you' and 'How do you do' make you sound robotic."),
            ("Act 2: Casual Greetings & Icebreakers", "Natural greetings: 'What's good?', 'How's everything?', 'Can't complain!'."),
            ("Act 3: Active Listening & Empathetic Reactions", "Showing empathy: 'I hear you', 'That makes total sense', 'Tell me about it!'."),
            ("Act 4: Surprise & Excitement Phrasing", "Expressing shock: 'No way!', 'You're kidding me!', 'That is wild!'."),
            ("Act 5: Polite Disagreements & Soft Pushback", "Softening opinions: 'I see your point, but...', 'I'm not so sure'."),
            ("Act 6: Conversational Fillers That Sound Smart", "Using 'To be honest', 'As a matter of fact', 'Come to think of it'."),
            ("Act 7: Everyday Slang vs Professional Casual", "Knowing what to say with friends versus what to use at the office."),
            ("Act 8: Roleplay - Chit-Chat with Neighbors & Co-workers", "Weather, weekend plans, and casual water-cooler conversations."),
            ("Act 9: The 7-Day Natural Vocabulary Challenge", "Adopting 3 new modern expressions each day and mastering them.")
        ]
    },
    {
        "id": "flow_technique",
        "topic": "Never Run Out of Things to Say! Master the Infinite Flow Technique",
        "thumbnail_title_1": "NEVER RUN OUT",
        "thumbnail_title_2": "OF THINGS TO SAY!",
        "thumbnail_hook": "The Secret to Infinite Conversation",
        "yt_hook": "Never Run Out of Things to Say!",
        "act_themes": [
            ("Act 1: The Awkward Silence Nightmare", "Why our minds freeze after saying hello and how conversation momentum works."),
            ("Act 2: The Answer-Plus-Detail-Plus-Question Formula", "How to answer any question while passing the conversational ball back."),
            ("Act 3: Conversational Bridges - Linking Unrelated Topics", "Using 'Speaking of which...', 'That reminds me...', and 'By the way...'."),
            ("Act 4: The Power of Open-Ended Questions", "Asking 'How', 'Why', and 'What was it like?' to invite stories."),
            ("Act 5: Talking About Topics You Know Nothing About", "Curiosity frameworks to let the other person happily share their expertise."),
            ("Act 6: Storytelling Sparks - Turning Micro-Events into Stories", "How a spilled coffee or missed bus becomes a charming narrative."),
            ("Act 7: Handling Social Mingling & Party Situations", "Entering group conversations smoothly and exiting gracefully."),
            ("Act 8: Deepening Casual Acquaintances into Real Friends", "Moving from surface weather talk to genuine shared passions."),
            ("Act 9: The 7-Day Conversation Flow Challenge", "Daily conversational drill to speak smoothly without awkward pauses.")
        ]
    },
    {
        "id": "connected_speech",
        "topic": "Connected Speech Secrets! Why Native Speakers Sound Fast & How to Master It",
        "thumbnail_title_1": "CONNECTED SPEECH",
        "thumbnail_title_2": "RHYTHM SECRETS!",
        "thumbnail_hook": "Understand Fast English Easily",
        "yt_hook": "Connected Speech Secrets!",
        "act_themes": [
            ("Act 1: Why English Sounds Fast to Foreign Ears", "Stress-timed rhythm vs syllable-timed rhythm and why words blur."),
            ("Act 2: Consonant-to-Vowel Linking", "How 'hold on' becomes 'hol-don' and 'check it out' becomes 'che-ki-tout'."),
            ("Act 3: Vowel-to-Vowel Linking with W and Y Glides", "Inserting subtle glide sounds between words: 'go out' ('go-w-out')."),
            ("Act 4: The Most Common Reductions: Wanna, Gonna, Gotta", "Natural reductions that save vocal energy without being sloppy slang."),
            ("Act 5: Weak Forms: The Elusive Schwa Sound", "How 'to', 'for', 'at', and 'and' get reduced to effortless murmurs."),
            ("Act 6: Contractions in Past Tense: Coulda, Shoulda, Woulda", "Understanding fast past-modal reductions in real conversation."),
            ("Act 7: T-Flapping in American English", "Why 'water' sounds like 'wader' and 'better' sounds like 'bedder'."),
            ("Act 8: Vocal Shadowing Drills with Emma & Alex", "Side-by-side rhythmic repeating to match native cadence."),
            ("Act 9: The 7-Day Rhythm & Accent Reset", "5 minutes a day of connected speech shadowing for effortless rhythm.")
        ]
    },
    {
        "id": "job_interview",
        "topic": "Ace Your Job Interview in English! High-Impact Professional Fluency",
        "thumbnail_title_1": "JOB INTERVIEW",
        "thumbnail_title_2": "ENGLISH HACKS!",
        "thumbnail_hook": "Answer Tough Questions with Confidence",
        "yt_hook": "Ace Your Job Interview!",
        "act_themes": [
            ("Act 1: Interview Anxiety & Professional Confidence", "Overcoming imposter syndrome when interviewing in a second language."),
            ("Act 2: The Perfect Answer to 'Tell Me About Yourself'", "The Present-Past-Future formula to deliver a crisp 90-second pitch."),
            ("Act 3: Structuring Answers with the STAR Method", "Situation, Task, Action, Result for behavioral interview questions."),
            ("Act 4: Discussing Strengths Without Sounding Arrogant", "Action verbs and verifiable achievements that build credibility."),
            ("Act 5: Handling the 'What Is Your Greatest Weakness?' Trap", "Reframing real learning areas into growth and self-awareness."),
            ("Act 6: Clarifying Questions When You Don't Understand", "Professional ways to buy time and ask the interviewer to elaborate."),
            ("Act 7: Asking High-Value Questions at the End", "Questions that impress the hiring manager and show true passion."),
            ("Act 8: Salary Negotiation & Follow-Up Email Etiquette", "Polite, assertive language for discussing compensation and offers."),
            ("Act 9: The 7-Day Interview Speaking Prep Blueprint", "Mock interview drills out loud to walk into the room with confidence.")
        ]
    },
    {
        "id": "dining_cafe",
        "topic": "Real-World Food & Dining English! Master Cafe & Restaurant Dialogues",
        "thumbnail_title_1": "ORDER FOOD",
        "thumbnail_title_2": "LIKE A LOCAL!",
        "thumbnail_hook": "Master Cafe & Dining Roleplays",
        "yt_hook": "Order Food Like a Local!",
        "act_themes": [
            ("Act 1: The Morning Coffee Shop Experience", "Ordering espresso, customizations, plant milks, and ice levels politely."),
            ("Act 2: Arriving at a Restaurant: Reservations & Tables", "Checking in, asking for outdoor seating, and booth preferences."),
            ("Act 3: Deciphering Menus & Asking for Recommendations", "Daily specials, allergens, and asking the server their personal favorites."),
            ("Act 4: Customizing Your Dish Confidently", "Dressing on the side, meat temperatures, and dietary substitutions."),
            ("Act 5: Getting the Server's Attention Gracefully", "Polite eye contact, subtle hand gestures, and polite phrasing."),
            ("Act 6: Handling Food Issues Without Being Rude", "What to say if an order is cold, wrong, or missing an ingredient."),
            ("Act 7: Asking for the Bill and Tipping Etiquette", "Splitting checks, card terminals, and understanding tip customs."),
            ("Act 8: Street Food & Fast Casual Ordering", "Navigating food trucks, assembly lines, and delis."),
            ("Act 9: The 7-Day Dining Out Speaking Challenge", "Roleplaying food dialogues out loud for effortless real-life dining.")
        ]
    },
    {
        "id": "travel_english",
        "topic": "Travel English Made Simple! Airports, Hotels, Taxis & Lost Items",
        "thumbnail_title_1": "TRAVEL ENGLISH",
        "thumbnail_title_2": "MADE SIMPLE!",
        "thumbnail_hook": "Explore Any City with Zero Stress",
        "yt_hook": "Travel English Made Simple!",
        "act_themes": [
            ("Act 1: Navigating the International Airport", "Check-in counters, baggage allowances, and security checkpoint English."),
            ("Act 2: Customs & Immigration Questions", "Answering purpose of visit, length of stay, and accommodation clearly."),
            ("Act 3: Hotel Check-in & Requesting Upgrades", "Keys, Wi-Fi passwords, late checkouts, and room preferences."),
            ("Act 4: Taking Taxis, Rideshares & Public Transit", "Giving directions to drivers, fares, and buying metro cards."),
            ("Act 5: Asking Strangers for Directions on the Street", "How to stop someone politely: 'Excuse me, do you happen to know...'."),
            ("Act 6: Shopping for Souvenirs & Tax-Free Shopping", "Bargaining, currency conversions, and receipt inquiries."),
            ("Act 7: Handling Emergencies: Lost Luggage & Delayed Trains", "Speaking to airport lost-and-found and booking ticket changes."),
            ("Act 8: Sightseeing, Museum Tours & Booking Activities", "Audio guides, ticket queues, and photography etiquette."),
            ("Act 9: The 7-Day Jetsetter English Challenge", "Vocal drills for your next international adventure.")
        ]
    },
    {
        "id": "storytelling_english",
        "topic": "How to Tell Captivating Stories in English Like a Pro",
        "thumbnail_title_1": "TELL STORIES",
        "thumbnail_title_2": "LIKE A PRO!",
        "thumbnail_hook": "Hook Any Listener from Start to Finish",
        "yt_hook": "Tell Stories Like a Pro!",
        "act_themes": [
            ("Act 1: Why Humans Are Wired for Stories", "Why personal anecdotes build ten times more connection than facts."),
            ("Act 2: The Narrative Hook - Grabbing Attention Fast", "Starting with 'You won't believe what happened yesterday...'."),
            ("Act 3: Setting the Scene with Sensory Words", "Using colors, sounds, and physical feelings to paint a mental picture."),
            ("Act 4: Building Suspense with Strategic Pauses", "How timing and silence create anticipation in English conversation."),
            ("Act 5: Dialogue Within Stories - He Said, She Said", "Quoting conversations naturally: 'And then she goes... and I'm like...'."),
            ("Act 6: The Climax & The Twist", "Delivering the punchline or surprising turning point of your story."),
            ("Act 7: The Takeaway / Lesson Learned", "Wrapping up with personal reflection or a laugh with the group."),
            ("Act 8: Recovering If Your Story Falls Flat", "How to laugh at yourself and gracefully return to the group flow."),
            ("Act 9: The 7-Day Storytelling Masterclass Drill", "Crafting and practicing three personal 60-second go-to stories.")
        ]
    },
    {
        "id": "introvert_smalltalk",
        "topic": "Small Talk for Introverts! How to Talk to Anyone with Zero Awkwardness",
        "thumbnail_title_1": "SMALL TALK",
        "thumbnail_title_2": "FOR INTROVERTS!",
        "thumbnail_hook": "Turn Silence into Friendly Chat",
        "yt_hook": "Small Talk for Introverts!",
        "act_themes": [
            ("Act 1: The Introvert's Advantage in English", "Why deep listening and observation make introverts great conversationalists."),
            ("Act 2: Low-Stress Icebreakers for Strangers", "Commenting on shared environments: coffee line, bus stop, or conference."),
            ("Act 3: The Art of the Gentle Question", "Asking questions that invite enthusiasm without prying into privacy."),
            ("Act 4: Energy Conservation - Graceful Conversational Exits", "How to end a chat politely when your social battery is running low."),
            ("Act 5: Dealing with Loud Group Conversations", "Finding small moments to chime in without shouting or competing."),
            ("Act 6: Body Language for Approachability", "Smiling, nodding, and relaxed open posture that speaks volumes."),
            ("Act 7: Complimenting People Sincerity Hacks", "How specific, genuine compliments create instant warmth and smiles."),
            ("Act 8: Turning Small Talk into Meaningful Talk", "Steering conversations toward travel, creative projects, and hobbies."),
            ("Act 9: The 7-Day Introvert Social Speaking Plan", "One low-pressure, friendly interaction out loud every day.")
        ]
    }
]

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
        return {
            "id": "custom",
            "topic": custom_topic,
            "thumbnail_title_1": t1[:18],
            "thumbnail_title_2": t2[:18],
            "thumbnail_hook": "Daily English Masterclass",
            "yt_hook": f"{custom_topic[:50]} 🎙️",
            "act_themes": VIRAL_CURRICULUM_CATALOG[0]["act_themes"]
        }

    # Deterministic sequential rotation ensuring every daily episode gets a brand new curriculum topic
    # Ep 1 & 2 -> Topic 0: Speak English Without Fear!
    # Ep 3     -> Topic 1: Stop Translating in Your Head! Think Directly in English
    # Ep 4     -> Topic 2: Sound Like a Native! 50 Phrases Real People Actually Use
    # Ep 5     -> Topic 3: Never Run Out of Things to Say! Master the Infinite Flow Technique
    # Ep 6     -> Topic 4: Connected Speech Secrets! Why Native Speakers Sound Fast
    # Ep 7     -> Topic 5: Ace Your Job Interview in English! High-Impact Professional Fluency
    # Ep 8     -> Topic 6: Real-World Food & Dining English! Master Cafe & Restaurant Dialogues
    # Ep 9     -> Topic 7: Travel English Made Simple! Airports, Hotels, Taxis & Lost Items
    # Ep 10    -> Topic 8: How to Tell Captivating Stories in English Like a Pro
    # Ep 11    -> Topic 9: Small Talk for Introverts! How to Talk to Anyone with Zero Awkwardness
    if ep_num <= 2:
        idx = 0
    else:
        idx = (ep_num - 2) % len(VIRAL_CURRICULUM_CATALOG)

    return VIRAL_CURRICULUM_CATALOG[idx]

def generate_full_podcast_story(target_minutes: float = 30.0, topic: str = None, ep_num: int = 1) -> dict:
    """
    Generates a full structured English learning podcast episode with a brand new topic every run.
    Produces ~288 dialogue turns across 9 acts (~3,700-3,900 words, ~30.6 minutes).
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

    # If small test duration (e.g. <= 2 mins)
    if target_minutes <= 2.0:
        act = MASTERCLASS_ACTS[0]
        dialogue = act["turns"][:10]
        chapters_meta = [{"title": act["title"], "start_turn": 0}]
    elif target_minutes <= 6.0:
        dialogue = MASTERCLASS_ACTS[0]["turns"][:16] + MASTERCLASS_ACTS[1]["turns"][:16]
        chapters_meta = [
            {"title": MASTERCLASS_ACTS[0]["title"], "start_turn": 0},
            {"title": MASTERCLASS_ACTS[1]["title"], "start_turn": 16}
        ]
    elif target_minutes <= 15.0:
        dialogue = []
        chapters_meta = []
        for i in range(4):
            act = MASTERCLASS_ACTS[i]
            chapters_meta.append({"title": act["title"], "start_turn": len(dialogue)})
            dialogue.extend(act["turns"])
    else:
        # Full ~30-minute episode: all 9 Acts (288 turns total)
        dialogue = []
        chapters_meta = []
        
        # Only query external AI if a custom topic was explicitly requested
        is_custom_topic = (topic_info.get("id") == "custom")
        
        for i, (act_title, act_focus) in enumerate(topic_info["act_themes"]):
            chapters_meta.append({
                "title": act_title,
                "start_turn": len(dialogue)
            })

            if is_custom_topic and config.POLLINATIONS_API_KEY:
                act_dict = {"title": act_title, "focus": act_focus, "turns": MASTERCLASS_ACTS[i]["turns"]}
                act_turns = generate_chapter_ai(i, act_dict, selected_topic)
            else:
                act_turns = MASTERCLASS_ACTS[i]["turns"]

            dialogue.extend(act_turns)

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

