import datetime
import os
import random
import sys
import webbrowser

import pyttsx3
import speech_recognition as sr
import wikipedia

# Change this if VS Code is installed somewhere else.
VSCODE_PATH = r"D:\Installs\Microsoft VS Code\Code.exe"

JOKES = [
    "Why did the hipster burn his mouth? He drank the coffee before it was cool.",
    "What did the buffalo say when his son left for college? Bison.",
    "What did the confused egg say? I don't unda-stand.",
    "A magician was walking down the street and he turned into a grocery store.",
    "I bought a new boomerang… But I just can't throw the old one away.",
    "What did the green peas say? Nothing. They just mutter'ed.",
    "Sindhu threw butter out of the window. What did she see? Answer: Butter-fly.",
    "What did one math book say to the other? I don't know about you, but I've got a lot of problems.",
    "Maths teacher: What is a line? A genius answered : A line is a dot, going for a walk.",
    "Why did Micky Mouse go to outer space? He was looking for Pluto.",
    "An astronomer once told me a joke but it went way above my head and in no time, I was spaced out totally.",
    "Have you heard of the book about zero gravity, apparently you cannot put it down.",
    "What did the lonely banana say? I'm a kela.",
    "Why do scuba divers always fall backwards out of the boat? If they fell forwards, they'd still be in the boat.",
    "If I bought a balloon for Re.1/-, how much should I sell it for when I adjust for inflation?",
    "What is green and jumpy? A grasshopper with hiccups.",
    "There's a special place in he'll for autocorrect.",
    "This is my step ladder. I never knew my real ladder.",
    "You can catch it, you can pass it, you can get it, but you can't throw it. What is it? Answer: A cold.",
    "Where do sheep take a bath? In a baaaa-th tub.",
    "Did you hear about the two thieves who stole a calendar? They each got six months.",
    "What do computers eat for a snack? Microchips.",
    "What did the flower say to its girl-friend? Why do phools fall in love?",
    "What did the green grape say to the purple grape? Breathe, you idiot!",
    "Have you heard the rumour about butter? Never mind, I shouldn't spread it.",
    "Why are ghosts terrible liars? Because you can see right through them.",
    "How do you catch a runaway laptop? With an internet.",
    "Why can't your nose be 12 inches long? Because then it would be a foot!",
    "What did the confederate soldiers use to eat off of? Civil-ware. What did they use to drink with? Cups. Dixie cups.",
    "Do you want to hear a joke about pizza? Never mind, it was too cheesy.",
    "Do you know what's not right? left",
    "A moon rock tastes better than an earthly rock because it's meat-eor",
    "I tried to catch some fog earlier, I mist.",
    "A backwards poet writes inverse",
    "Bakers trade bread recipes on a knead to know basis.",
    "I stayed up all night wondering where the sun went, then it dawned on me.",
    "It doesn't matter how much you push the envelope, it'll still be stationary.",
    "A book just fell on my head, I only have my-shelf to blame.",
    "Why did the scarecrow get a promotion? Because he was out-standing in his field.",
]


def make_engine():
    # SAPI5 is Windows-only. Fall back to the default driver elsewhere.
    if sys.platform.startswith("win"):
        engine = pyttsx3.init("sapi5")
        voices = engine.getProperty("voices")
        if len(voices) > 1:
            engine.setProperty("voice", voices[1].id)
        return engine
    return pyttsx3.init()


engine = make_engine()


def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()


def wish_me():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Hi!, I am Stella a virtual assistant. What can i do for you today?")


def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")
        return query.lower()
    except Exception:
        print("Say that again please...")
        return "none"


def open_site(url):
    speak("Processing!!")
    webbrowser.open(url)
    speak("Here you go!.")


def tell_joke():
    speak(random.choice(JOKES))


def wants_joke(query):
    phrases = (
        "tell me a joke",
        "tell me something funny",
        "do you know a joke",
        "say a joke",
        "joke",
    )
    return any(p in query for p in phrases)


def open_vscode():
    speak("Processing!!")
    if os.path.exists(VSCODE_PATH):
        if hasattr(os, "startfile"):
            os.startfile(VSCODE_PATH)
        else:
            os.system(f'"{VSCODE_PATH}"')
        speak("Here you go!.")
        return
    speak("I could not find VS Code at the path in Stella.py.")


def main():
    wish_me()
    while True:
        query = take_command()

        if query == "none":
            continue

        if "wikipedia" in query:
            speak("Searching Wikipedia...")
            topic = query.replace("wikipedia", "").strip()
            if not topic:
                speak("What should I search on Wikipedia?")
                continue
            results = wikipedia.summary(topic, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif "what can you do" in query:
            speak(
                "I can do many things such as opening apps, entertain you with jokes, gather information from wiki..."
            )
            speak(
                "Well the list is kind of limited for now but can be extended in future for sure as technology advances"
            )

        elif "open youtube" in query:
            open_site("https://www.youtube.com")

        elif "open google" in query:
            open_site("https://www.google.com")

        elif "open github" in query:
            open_site("https://www.github.com")

        elif "open facebook" in query:
            open_site("https://www.facebook.com")

        elif "open instagram" in query:
            open_site("https://www.instagram.com")

        elif "open stackoverflow" in query:
            open_site("https://stackoverflow.com")

        elif "open amazon" in query:
            open_site("https://www.amazon.in")

        elif "open flipkart" in query:
            open_site("https://www.flipkart.com")

        elif "open ebay" in query:
            open_site("https://www.ebay.com")

        elif "the time" in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {str_time}")

        elif "open code" in query:
            open_vscode()

        elif wants_joke(query):
            tell_joke()

        elif "exit" in query:
            speak("Good bye. Have a nice day")
            break


if __name__ == "__main__":
    main()
