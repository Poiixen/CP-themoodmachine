"""
Breaker sentences designed to expose weaknesses in the Mood Machine.
Run with: python -X utf8 breaker.py
"""

from mood_analyzer import MoodAnalyzer

BREAKERS = [
    # (sentence, expected_label, note)
    ("I love getting stuck in traffic",        "negative", "sarcasm — 'love' is ironic here"),
    ("that party was sick",                    "positive", "slang: 'sick' means awesome"),
    ("this beat is fire",                      "positive", "slang: 'fire' means great"),
    ("I'm fine 🙂",                            "negative", "passive-aggressive emoji — 'fine' + 🙂 reads as not fine"),
    ("I'm exhausted but so proud of myself",   "mixed",    "mixed: negative + positive, neither in word lists"),
    ("not gonna lie this is actually amazing", "positive", "negation before filler, real sentiment at the end"),
    ("I don't hate it",                        "positive", "double-flip: negated negative = positive"),
    ("wicked good time last night",            "positive", "regional slang: 'wicked' as intensifier, not negative"),
]

analyzer = MoodAnalyzer()

print("=" * 65)
print(f"{'SENTENCE':<42} {'PREDICTED':<10} {'EXPECTED':<10} {'PASS'}")
print("=" * 65)

for sentence, expected, note in BREAKERS:
    # Suppress the per-call debug prints for clean table output
    import io, sys
    buf = io.StringIO()
    sys.stdout = buf
    predicted = analyzer.predict_label(sentence)
    sys.stdout = sys.__stdout__

    captured = buf.getvalue()
    # Pull the score out of captured debug output
    score_line = next((l for l in captured.splitlines() if "[score_text]" in l), "")

    passed = "✓" if predicted == expected else "✗"
    print(f"{sentence:<42} {predicted:<10} {expected:<10} {passed}  ({note})")
    if score_line:
        print(f"  {score_line.strip()}")
print("=" * 65)
