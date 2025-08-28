import json
import nltk
from pathlib import Path
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer, util

lemmatizer = WordNetLemmatizer()

nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

MEM_FILE = Path("memory.json")


#try:
#    with open("memory.json", "r") as f:
#        memory = json.load(f)
#except FileNotFoundError:
#    memory = {}


def normalize(text):
    text = text.lower()
    for p in ["!", ".", "?", ",", "'"]:
        text = text.replace(p, "")
    return text.strip()


# def word_similarity(word1, word2):
#     synsets1 = wordnet.synsets(word1)
#     synsets2 = wordnet.synsets(word2)
#     if synsets1 and synsets2:
#         return synsets1[0].wup_similarity(synsets2[0]) or 0
#     return 0

# def sentence_similarity(s1, s2):
#     s1 = normalize(s1)
#     s2 = normalize(s2)
#     words1 = [lemmatizer.lemmatize(w) for w in s1.split()]
#     words2 = [lemmatizer.lemmatize(w) for w in s2.split()]
#     scores = []
#     for w1 in words1:
#         for w2 in words2:
#             scores.append(word_similarity(w1, w2))
#     scores = [s for s in scores if s is not None]
#     return sum(scores)/len(scores)if scores else 0

#def get_synonym(word):
#    synonymset = wordnet.synsets(word)
#    if synonymset:
#        return synonymset[0].lemmas()[0].name().lower()
#    return word


# while True:
#     user_input = input("You: ")

#     if user_input.lower() == "bye":
#         print("AI: Bye!")
#         with open("memory.json", "w") as f:
#             json.dump(memory, f)
#         break

#     norm_input = normalize(user_input)

#     best_match = None
#     best_score = 0
#     for known in memory:
#         score = sentence_similarity(norm_input, known)
#         if score > best_score:
#             best_score = score
#             best_match = known

#     if best_match and best_score > 0.01:
#         print("AI:", memory[best_match])
#     else:
#         reply = input("I don't know what to say. How should I respond?")
#         memory[norm_input] = reply
#         print("AI: Got it! I'll remember that.")



def load_memory():
    if MEM_FILE.exists():
        with open(MEM_FILE, "r") as f:
            return json.load(f)


    seed = [
        {"example": "hello", "response": "Hi!", "embedding":embedding_model.encode("hello", convert_to_tensor = True).tolist()},
        {"example": "goodbye", "response": "Bye!", "embedding":embedding_model.encode("hello", convert_to_tensor = True).tolist()},
        {"example": "tell me a joke", "response": "Why did the developer go broke? Because they used up all their cache.", "embedding":embedding_model.encode("hello", convert_to_tensor = True).tolist()}
    ]

    with open(MEM_FILE, "w") as f:
        json.dump(seed, f, ensure_ascii=False, indent=2)
    return seed
    
def save_memory(mem):
    with open(MEM_FILE, "w") as f:
        json.dump(mem, f, ensure_ascii=False, indent=2)

def add_memory(rootWord, response, memory):
    embedding = embedding_model.encode(rootWord, convert_to_tensor = True).tolist()
    memory.append({
        "examlple": rootWord,
        "response":response,
        "embedding": embedding
    })

def get_best_match(user_input, memory):
    if not memory:
        return None, 0.0
    
    input_embedding = embedding_model.encode(user_input, convert_to_tensor = True)

    scores = []
    for item in memory:
        score = util.cos_sim(input_embedding, item["embedding"]).item()
        scores.append(score)

    best_index = scores.index(max(scores))
    return memory[best_index], max(scores)

def chat():
    memory = load_memory()     

    print("AI: Hi, lets talk (type 'bye' to quit)")

    while True:
        text = input("You:").strip()
        if not text:
            continue
        if text.lower() == "bye":
            print("AI: Ending Conversation")
            save_memory(memory)
            break
        
        match, score = get_best_match(text, memory)
                
        THRESHHOLD = 0.55

        if match and score >= THRESHHOLD:
            print(f"AI (match {score:.2f}): {match["response"]}")

        else:
            print(f"AI: I don't know how to reply to that (best match {score:.2f}).")
            resp = input("How should I reply?").strip()
            if resp:
                add_memory(text, resp, memory)
                save_memory(memory)


chat()

