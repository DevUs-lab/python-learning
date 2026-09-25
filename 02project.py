import datetime

responses = {
    "hi": "Hi, I am fine. How are you?",
    "who are you": "I am a chatbot.",
    "how are you": "I am fine.",
    "what you know": "I don't know.",
}


# Get current hour
currentHour = datetime.datetime.now().hour

# Ask user's name
name = input("Enter your name: ").strip()

# Time-based greeting
if 5 <= currentHour < 12:
    print("Good morning,", name)
elif 12 <= currentHour < 17:
    print("Good afternoon,", name)
elif 17 <= currentHour < 21:
    print("Good evening,", name)
else:
    print("Good night,", name)


# Chatbot
while True:
    userInput = input("Ask your question: ").lower().strip()

    if userInput == "bye":
        print("Bye, take care!")
        break

    if userInput in responses:
        print(responses[userInput])
    else:
        print("I don't know, I am learning.")
