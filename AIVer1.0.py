import json
try:
    with open("memory.json", "r") as f:
        memory = json.load(f)
except FileNotFoundError:
    memory = {}


def normalize(text):
    tet = text.lower()
    for p in ["!", ".", "?", ","]:
        text = text.replace(p, "")
    return text.strip()


while True:
    user_input = input("You: ")

    if user_input.lower() == "bye":
        print("AI: Bye!")
        with open("memory.json", "w") as f:
            json.dump(memory, f)
        break

    norm_input = normalize(user_input)

    if norm_input in memory:
        print("AI:", memory[norm_input])
    else:
        reply = input("I dont know what to say. how should I respond?")
        memory[norm_input] = reply
        print("AI: Got it! I will remember that.")