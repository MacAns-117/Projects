import pyttsx3 
import speech_recognition as sr 
import datetime
import wikipedia 
import webbrowser
import random
import os
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
        print("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   
        print("Good Afternoon!")   

    else:
        speak("Good Evening!")
        print("Good Evening!")   

    speak("Hi!, I am Stella a virtual assistant. What can i do for you today?")
    print("Hi!, I am Stella a virtual assistant. What can i do for you today?")         

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query


if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()
        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            print('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print("According to Wikipedia")
            print(results)
            speak(results)
        
        elif 'what can you do' in query:
            speak("I can do many things such as opening apps, entertain you with jokes, gather information from wiki...")
            print("I can do many things such as opening apps, entertain you with jokes, gather information from wiki...")
            speak("Well the list is kind of limited for now but can be extended in future for sure as technology advances")
            print("Well the list is kind of limited for now but can be extended in future for sure as technology advances")

        elif 'open youtube' in query:
            speak('Processing!!')
            print('Processing!!')
            webbrowser.open("youtube.com")
            speak('Here you go!.')
            print('Here you go!.')

        elif 'open google' in query:
            speak('Processing!!')
            print('Processing!!')
            webbrowser.open("google.com")
            speak('Here you go!.')
            print('Here you go!.')

        elif 'open github' in query:
            speak('Processing!!')
            print('Processing!!')
            webbrowser.open("https://www.github.com")
            speak('Here you go!.')
            print('Here you go!.')

        elif 'open facebook' in query:
            speak('Processing!!')
            print('Processing!!')
            webbrowser.open("https://www.facebook.com")
            speak('Here you go!.')
            print('Here you go!.')
      
        elif 'open instagram' in query:
            speak('Processing!!')
            print('Processing!!')
            webbrowser.open("https://www.instagram.com")
            speak('Here you go!.')
            print('Here you go!.')


        elif 'open stackoverflow' in query:
            speak('Processing!!')
            print('Processing!!')
            webbrowser.open("stackoverflow.com")
            speak('Here you go!.')
            print('Here you go!.')

        elif 'open amazon' in query:
            speak('Processing!!')
            print('Processing!!')
            webbrowser.open("https://www.amazon.in")
            speak('Here you go!.')
            print('Here you go!.')

        elif 'open flipkart' in query:
            speak('Processing!!')
            print('Processing!!')
            webbrowser.open("https://www.flipkart.com")
            speak('Here you go!.')
            print('Here you go!.')

        elif 'open ebay' in query:
            speak('Processing!!')
            print('Processing!!')
            webbrowser.open("https://www.ebay.com")
            speak('Here you go!.')
            print('Here you go!.')  

        # elif 'play music' in query:
        #     music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
        #     songs = os.listdir(music_dir)
        #     print(songs)    
        #     os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")
            print(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            speak('Processing!!')
            print('Processing!!')
            codePath = "D:\\Installs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
            speak('Here you go!.')
            print('Here you go!.')  
            
        elif 'Tell me a joke!' in query or "Tell me something funny!" in query or "Do you know a joke?" in query or "say a joke" in query: 
            jokes = [
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
            "Why did the scarecrow get a promotion? Because he was out-standing in his field."
          ]
            c = random.choice(jokes)
            speak(c)
            print(c)

        elif 'exit' in query:
            speak("Good bye. Have a nice day")
            exit()

