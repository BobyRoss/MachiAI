import json
import nltk
from nltk.corpus import wordnet

nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)


try:
    with open("memory.json", "r") as f:
        memory = json.load(f)
except FileNotFoundError:
    memory = {}


def normalize(text):
    tet = text.lower()
    for p in ["!", ".", "?", ",", "'"]:
        text = text.replace(p, "")
    return text.strip()


def word_similarity(word1, word2):
    synsets1 = wordnet.synsets(word1)
    synsets2 = wordnet.synsets(word2)
    if synsets1 and synsets2:
        return synsets1[0].wup_similarity(synsets2[0]) or 0
    return 0

def sentence_similarity(s1, s2):
    words1 = s1.split()
    words2 = s2.split()
    scores = []
    for w1 in words1:
        for w2 in words2:
            scores.append(word_similarity(w1, w2))
    scores = [s for s in scores if s is not None]
    return sum(scores)/len(scores)if scores else 0

#def get_synonym(word):
#    synonymset = wordnet.synsets(word)
#    if synonymset:
#        return synonymset[0].lemmas()[0].name().lower()
#    return word


while True:
    user_input = input("You: ")

    if user_input.lower() == "bye":
        print("AI: Bye!")
        with open("memory.json", "w") as f:
            json.dump(memory, f)
        break

    norm_input = normalize(user_input)

    best_match = None
    best_score = 0
    for known in memory:
        score = sentence_similarity(norm_input, known)
        if score > best_score:
            best_score = score
            best_match = known

    if best_match and best_score > 0.5:
        print("AI:", memory[best_match])
    else:
        reply = input("I don't know what to say. How should I respond?")
        memory[norm_input] = reply
        print("AI: Got it! I'll remember that.")

