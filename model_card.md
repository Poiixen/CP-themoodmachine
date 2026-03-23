# Model Card: Mood Machine

This model card covers **two** versions of the Mood Machine classifier:

1. A **rule-based model** in `mood_analyzer.py`
2. A **machine learning model** in `ml_experiments.py` using scikit-learn

---

## 1. Model Overview

**Model type:**
Both models were built and compared. The rule-based model was the primary development focus; the ML model was run as a comparison experiment on the same dataset.

**Intended purpose:**
Classify short, informal text messages (social media style) into one of four mood labels: `positive`, `negative`, `neutral`, or `mixed`.

**How it works (brief):**
The rule-based model assigns a numeric score to each post by scanning tokens for matches against positive and negative word lists. Negation words (`not`, `don't`, `never`, etc.) flip the signal of the following token. Emojis are mapped to fixed scores. The final score is converted to a label using thresholds, with a `mixed` label assigned when both positive and negative signals are detected in the same post.

The ML model uses a bag-of-words representation (`CountVectorizer`) and trains a `LogisticRegression` classifier on the labeled examples in `SAMPLE_POSTS` / `TRUE_LABELS`. It learns which word patterns correlate with each label from the training data rather than from hand-written rules.

---

## 2. Data

**Dataset description:**
The dataset contains 14 short posts in `SAMPLE_POSTS`. The original 6 starter examples were extended with 8 new posts written to reflect realistic informal language — slang, emojis, hedging phrases, and mixed emotional signals.

**Labeling process:**
Labels were assigned by reading each post and choosing the label that best matched the dominant tone. Posts with clear single-emotion language (e.g. `"So excited for the weekend"`) were easy. Posts with hedging or contrast were harder:

- `"lowkey stressed but it's whatever lol"` — "stressed" is negative but "whatever lol" is dismissive/resigned, not purely negative. Labeled `mixed` because the dismissal softens the stress without canceling it.
- `"ngl this hits different 😭🔥"` — `😭` signals sadness but `🔥` signals excitement; the phrase "hits different" implies strong feeling without a clear valence. Labeled `mixed`.
- `"ugh another Monday... at least coffee exists I guess"` — complaint followed by a grudging positive. Labeled `mixed`.

**Important characteristics of the dataset:**

- Contains informal slang: `ngl`, `lowkey`, `idk`, `rn`, `w the squad`
- Includes emojis: 😭🔥🥹💙
- Several posts express genuinely mixed feelings
- Posts are short (5–15 words), which limits context available to any model
- No sarcasm in the labeled dataset (though sarcasm was tested in breakers)

**Possible issues with the dataset:**

- 14 examples is extremely small — any accuracy number reflects memorization more than generalization
- 4 labels across 14 posts means some labels have very few examples (e.g., `neutral` appears only twice)
- The `mixed` label is the hardest to apply consistently; different annotators might disagree on the same post
- All posts were written in one session with similar vocabulary, which limits linguistic diversity

---

## 3. How the Rule-Based Model Works

**Scoring rules:**

1. **Tokenization:** Input is lowercased, split on whitespace, and ASCII punctuation is stripped from token edges using `string.punctuation`. This preserves emojis (e.g., `🥹`) while removing trailing commas and exclamation marks.

2. **Positive/negative word matching:** Each token is looked up in `POSITIVE_WORDS` and `NEGATIVE_WORDS` (defined in `dataset.py`). A match in `POSITIVE_WORDS` adds +1 to the score; a match in `NEGATIVE_WORDS` subtracts 1.

3. **Negation handling:** If the token immediately before a matched word is in the negation set (`not`, `never`, `don't`, `doesn't`, `didn't`, `won't`, `can't`, `isn't`, `aren't`), the effect is flipped: a positive word subtracts 1, a negative word adds 1.
   - Example: `"I am not happy about this"` → `happy` is negated → score = -1 → `negative` ✓

4. **Emoji scoring:** A small lookup table (`EMOJI_SCORES`) maps individual emoji tokens to fixed scores (e.g., `😭` → -1, `🔥` → +1, `🥹` → +1, `💙` → +1).

5. **Slang vocabulary (added after breaker testing):** `sick`, `fire`, `lit`, `dope`, `goated` were added to `POSITIVE_WORDS` after observing that `"that party was sick"` and `"this beat is fire"` both scored 0.

6. **Label thresholds and mixed detection:**
   - Before applying score thresholds, the model counts effective positive and negative signals separately (after negation flipping).
   - If both counts > 0 → `mixed`
   - If only positive signals → use score: score > 0 → `positive`
   - If only negative signals → use score: score < 0 → `negative`
   - Otherwise → `neutral`

**Strengths of this approach:**

- Transparent: every prediction can be explained by pointing to specific tokens
- Negation handling correctly flips `"not happy"` to negative and `"don't hate it"` to positive
- Predictable: adding a word to the vocabulary has a clear, immediate effect
- Works without any training data

**Weaknesses of this approach:**

- Depends entirely on vocabulary coverage — any word not in the lists scores 0
- Cannot detect sarcasm (see Section 5)
- `mixed` detection requires both signal types to appear explicitly in the same post; implicit contrast is invisible
- Word-level matching misses multi-word expressions like "couldn't be better"

---

## 4. How the ML Model Works

**Features used:**
Bag-of-words representation using `CountVectorizer` (scikit-learn default settings). Each post becomes a sparse vector of word counts across the full vocabulary of the training corpus.

**Training data:**
Trained on all 14 examples in `SAMPLE_POSTS` with labels from `TRUE_LABELS`. No held-out test set — the evaluation is training accuracy only.

**Training behavior:**
With only 14 examples, the model memorized the training data and achieved 100% training accuracy. This is expected and does not indicate real generalization ability. The model is overfit by design: there is not enough data to do a proper train/test split and still have meaningful results.

**Strengths and weaknesses:**

Strengths:
- Learned the `mixed` label correctly for all four mixed posts — something the rule-based model mostly missed
- Did not require manually curated word lists
- Picked up on full word co-occurrence patterns (e.g., `"hits different"` co-occurring with the `mixed` label)

Weaknesses:
- 100% training accuracy on 14 examples is not meaningful — the model has seen every example it is tested on
- Extremely sensitive to label choices: changing one label in `TRUE_LABELS` can shift the decision boundary significantly
- Will fail on any vocabulary not present in the 14 training posts (e.g., input "this is awful" would score as unknown because "awful" never appeared in a negative post in training)
- The `CountVectorizer` treats emojis as unknown tokens since they appear too infrequently to contribute reliably

---

## 5. Evaluation

**How the models were evaluated:**
Both models were evaluated on the same 14 labeled posts from `dataset.py`. Because the ML model trains on the same data it is tested on, both accuracy numbers should be interpreted with caution — neither reflects performance on genuinely new examples.

**Rule-based accuracy: 0.50 (7/14)**
**ML model accuracy: 1.00 (14/14)** *(training accuracy — overfitted)*

**Examples of correct predictions (rule-based):**

| Post | Predicted | True | Why it worked |
|------|-----------|------|---------------|
| `"I am not happy about this"` | negative | negative | Negation correctly flipped `happy` from +1 to -1 |
| `"had such a good time w the squad tonight 💙"` | positive | positive | `good` (+1) and `💙` (+1) both fired → score = 2 |
| `"Today was a terrible day"` | negative | negative | `terrible` is in `NEGATIVE_WORDS` — direct match |

**Examples of incorrect predictions (rule-based):**

| Post | Predicted | True | Why it failed |
|------|-----------|------|---------------|
| `"idk man everything feels kinda meh lately"` | neutral | negative | `meh` signals low-grade negativity in common usage but isn't in any word list — score = 0 |
| `"this is genuinely the worst thing that's happened to me all week"` | neutral | negative | `worst` is absent from `NEGATIVE_WORDS` — a clear negative word the vocabulary simply doesn't cover |
| `"not gonna lie I'm kinda proud of myself for once"` | neutral | positive | `proud` is not in `POSITIVE_WORDS`; `not` before `gonna` triggered no flip; result was score = 0 |

---

## 6. Limitations

**Sarcasm is systematically misclassified.**
The breaker sentence `"I love getting stuck in traffic"` was predicted `positive` (score = 1) because `love` matched `POSITIVE_WORDS`. The model has no mechanism to detect that the following phrase — "getting stuck in traffic" — is a negative context that inverts the intended meaning. A word-list model cannot distinguish sincere and ironic uses of the same word without sentence-level context.

**Slang words silently score zero unless manually added.**
Before adding vocabulary, `"that party was sick"` and `"this beat is fire"` both scored 0 → `neutral`. The model did not raise an error or flag uncertainty — it simply returned a wrong answer quietly. This is a dangerous failure mode for any production system: silent, confident, wrong.

**Emoji sequences are not split.**
`"ngl this hits different 😭🔥"` produced the token `😭🔥` as a single string. Neither emoji was found in `EMOJI_SCORES` individually, so both were ignored. The model scored this post 0 → `neutral` when the true label was `mixed`. Any emoji pasted without spaces will be invisible to the current scoring logic.

**The `mixed` label is nearly unreachable for the rule-based model.**
Four of the 14 posts are labeled `mixed`, but the rule-based model correctly classified 0 of them. The `mixed` label requires both a positive and a negative effective signal in the same post. Most mixed posts in the dataset express ambivalence through *tone and word choice* (`"kinda meh"`, `"it's whatever"`, `"at least coffee exists"`) rather than through explicit positive + negative word pairs. The rule-based model is blind to this.

**Dataset size limits generalizability.**
Fourteen posts is not a dataset — it is a demonstration. Any accuracy figure from this project describes behavior on examples the model was explicitly built or trained to handle.

---

## 7. Ethical Considerations

**Language bias toward a specific dialect and demographic.**
The vocabulary and sample posts were written in a style reflecting informal American English, particularly Gen-Z internet slang (`ngl`, `lowkey`, `idk`, `fire`, `sick`, `goated`). This model will systematically underperform for:

- Users who express mood through different cultural idioms or dialects
- Non-native English speakers whose phrasing doesn't match the word lists
- Formal or older registers of English where words like `terrible` or `awful` appear but words like `hopeful` or `proud` are more common than the vocabulary covers

**Misclassifying distress as neutral.**
The sentence `"this is genuinely the worst thing that's happened to me all week"` was predicted `neutral` because `worst` is absent from the vocabulary. In any real application — a mental health check-in, a customer support triage tool, a content moderation system — a false neutral on a distress signal is a meaningful harm. Neutral is often interpreted as "nothing to act on."

**Passive emotional language is invisible.**
Posts like `"idk man everything feels kinda meh lately"` express low-energy, demotivated, or depressive tone through hedging and slang rather than strong negative words. This model cannot see those signals at all. Deploying a classifier like this in contexts where detecting low-grade negative mood matters would produce systematically worse results for people who communicate in understated ways.

**No privacy protections.**
This model processes raw text. If adapted to analyze real user messages, it would require careful attention to data handling, consent, and storage practices — none of which are addressed in this prototype.

---

## 8. Ideas for Improvement

**Short-term (word-list model):**
- Add `worst`, `horrible`, `dreadful`, `miserable` to `NEGATIVE_WORDS` — these are high-frequency negative words absent from the current list
- Add `proud`, `hopeful`, `grateful`, `relieved` to `POSITIVE_WORDS`
- Fix emoji tokenization: split emoji sequences character by character so `😭🔥` becomes `['😭', '🔥']` instead of one unknown token

**Medium-term:**
- Replace or supplement `CountVectorizer` with `TfidfVectorizer` to reduce the weight of high-frequency filler words
- Add a held-out test set (even 5 manually written posts not used in training) to get any honest accuracy estimate
- Expand `SAMPLE_POSTS` to 50–100 examples with more label diversity before re-running the ML model

**Longer-term:**
- Use a pre-trained sentence embedding model (e.g., `sentence-transformers`) to capture semantic similarity rather than exact word matches
- Add sarcasm as a label and build explicit detection: many sarcastic posts pair a positive word with a clearly negative context phrase
- Evaluate on posts from different communities, writing styles, and languages to measure demographic performance gaps before any real deployment
