memory = {}

while True:
    user_input = input("You: ")

    if user_input.lower() == "bye":
        print("AI: Bye!")
        break
    if user_input in memory:
        print("AI:", memory[user_input])
    else:
        reply = input("I dont know what to say. how should I respond?")
        memory[user_input] = reply
        print("AI: Got it! I will remember that.")