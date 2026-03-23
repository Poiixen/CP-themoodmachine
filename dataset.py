"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    # Slang with positive meaning in modern usage
    "sick",   # "that was sick" = impressive
    "fire",   # "this is fire" = excellent
    "lit",    # "last night was lit" = exciting
    "dope",   # "that's dope" = cool
    "goated", # "she's goated" = the greatest
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    "ngl this hits different 😭🔥",
    "ugh another Monday... at least coffee exists I guess",
    "lowkey stressed but it's whatever lol",
    "just got the job offer!!! I'm literally shaking rn 🥹",
    "idk man everything feels kinda meh lately",
    "had such a good time w the squad tonight 💙",
    "this is genuinely the worst thing that's happened to me all week",
    "not gonna lie I'm kinda proud of myself for once",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "mixed",     # "ngl this hits different 😭🔥"
    "mixed",     # "ugh another Monday... at least coffee exists I guess"
    "mixed",     # "lowkey stressed but it's whatever lol"
    "positive",  # "just got the job offer!!! I'm literally shaking rn 🥹"
    "negative",  # "idk man everything feels kinda meh lately"
    "positive",  # "had such a good time w the squad tonight 💙"
    "negative",  # "this is genuinely the worst thing that's happened to me all week"
    "positive",  # "not gonna lie I'm kinda proud of myself for once"
]

# TODO: Add 5-10 more posts and labels.
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)
