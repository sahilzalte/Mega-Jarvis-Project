import speech_recognition as sr
import webbrowser
from gtts import gTTS
import pygame
import os
import musiclibrary
import time
import cv2
import playlistlibrary
import threading
import screeninfo 
import client 
import pyjokes 

# Global control variables 
video_stopped = False
listening_active = True
video_thread = None

def play_intro_video():
    # Play introduction video in full screen 
    cap = cv2.VideoCapture("../Frontend/Video.mp4")
    pygame.mixer.init()
    pygame.mixer.music.load("../Frontend/Video.mp3")
    pygame.mixer.music.play()
    
    cv2.namedWindow("Intro", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Intro", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Intro', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyWindow("Intro")
    pygame.mixer.music.stop()


def play_background_video():
    global video_stopped
    video_stopped = False

    try:
        # Get screen resolution
        screen = screeninfo.get_monitors()[0]
        screen_width, screen_height = screen.width, screen.height

        # Window size
        win_width, win_height = 840, 360

        # Calculate bottom-center position
        x_pos = (screen_width - win_width) // 2
        y_pos = screen_height - win_height - 50  # 50px from bottom

        # Create persistent window
        cv2.namedWindow("Jarvis", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Jarvis", win_width, win_height)
        cv2.moveWindow("Jarvis", x_pos, y_pos)
        
        # Set window properties after creation
        cv2.setWindowProperty("Jarvis", cv2.WND_PROP_TOPMOST, 1)
        cv2.setWindowProperty("Jarvis", cv2.WND_PROP_VISIBLE, 1)

        cap = cv2.VideoCapture("../Frontend/bg.mp4")
        fps = cap.get(cv2.CAP_PROP_FPS)
        delay = int(1000 / fps) if fps > 0 else 33


        while not video_stopped:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
                
            cv2.imshow('Jarvis', frame)
            key = cv2.waitKey(delay)
            if key == ord('q'):
                break

    except Exception as e:
        print(f"Video error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()



def restart_video():
    global video_thread
    if video_thread and video_thread.is_alive():
        video_thread.join()
    video_thread = threading.Thread(target=play_background_video)
    video_thread.start()



def speak(text):
    tts = gTTS(text=text, lang ='en')
    tts.save('temp.mp3')
    
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    pygame.mixer.music.unload()
    os.remove('temp.mp3')



def process_command(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com") 
    
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com") 
    
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com") 
    
    elif "open github" in c.lower():
        webbrowser.open("https://github.com") 
        
    elif "open website" in c.lower():
        webbrowser.open("https://partfolio-website.vercel.app/") 
    
    elif "open college" in c.lower():
        webbrowser.open("https://www.sndpoly.com/") 
    
    elif "open chat gpt" in c.lower():
        webbrowser.open("https://chatgpt.com/") 
    
    elif "open ai" in c.lower():
        webbrowser.open("https://chatgpt.com/") 
    
    elif "open figma" in c.lower():
        webbrowser.open("https://www.figma.com/") 
    
    elif "open whatsapp" in c.lower():
        webbrowser.open("https://web.whatsapp.com/")

    elif "open twitter" in c.lower():
        webbrowser.open("https://twitter.com/")
    
    elif "open microsoft" in c.lower():
        webbrowser.open("https://www.microsoft.com/")
    
    elif "open sololearn" in c.lower():
        webbrowser.open("https://www.sololearn.com/")
    
    elif "open news" in c.lower():
        webbrowser.open("https://timesofindia.indiatimes.com/news")
    
    


    # About Jarvis
    elif any(greeting in c.lower() for greeting in ("hey", "hello")):
        speak("Hello! How can I help you ?") 

    elif any(greeting in c.lower() for greeting in ("who are you", "hu r u")):
        speak("I am Jarvis, your personal assistant.")
    
    elif "your name" in c.lower():
        speak("My name is Jarvis.")
    
    elif "how are you" in c.lower():
        speak("I'm doing great, thank you for asking!")

    elif "what can you do" in c.lower():
        speak("I can help you with a variety of tasks. Try asking me to play a song or search for something.")

    elif "who made you" in c.lower():
        speak("I was created by a team of Student developers at SND College. The names of students are Sahil, Akash, Tejaswini, and Anushka.")
    
    elif any(joke in c.lower() for joke in ("tell me a joke", "joke", "funny")):
        joke = pyjokes.get_joke()  # Fetches a random joke
        print(joke)
        speak(joke)
    
    
    elif c.lower().startswith("play"):
        song_name = c.lower().split(" ", 1)[1]  # Extract song name after "play"
        link = musiclibrary.music.get(song_name, None)

        if link:
            print(f"Playing song: {song_name}")
            speak(f"Playing song: {song_name}")
            webbrowser.open(link)  # Open the song link (e.g., YouTube URL)
        else:
            speak(f"Sorry, I couldn't find the song named {song_name}.")



    elif c.lower().startswith(("get", "gate")):  # Use a tuple for multiple prefixes
        words = c.lower().split(" ", 1)  

        if len(words) > 1:
            song_name = words[1]  # Extract Playlist name after "get" or "gate"
            link = playlistlibrary.playlist.get(song_name, None)

            if link:
                print(f"Playing Playlist: {song_name}")
                speak(f"Playing Playlist: {song_name}")
                webbrowser.open(link)  # Open the Playlist link (e.g., YouTube URL)
            else:
                speak(f"Sorry, I couldn't find the Playlist named {song_name}.")
        
        else:
            speak("Please specify a Playlist name after 'get' or 'gate'.")



    elif "exit" in c.lower() or "quit" in c.lower() or "stop" in c.lower():
        speak("Exiting Jarvis. Goodbye!")
        print("Exiting Jarvis. Goodbye!")
        exit()  # Terminate the program

    else:
        client.google_search(c)


def voice_listener():
    global video_stopped, listening_active, video_thread
    recognizer = sr.Recognizer()
    
    speak("Initializing Jarvis....")
    last_command_time = time.time()

    restart_video()  # Initial video start

    while listening_active:
        try:
            with sr.Microphone() as source:
                print("Listening for your command...")
                recognizer.adjust_for_ambient_noise(source, duration=2)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            # Process command
            command = recognizer.recognize_google(audio)
            print(f"Command recognized: {command}")
            
            # Bring window back if minimized
            cv2.setWindowProperty("Jarvis", cv2.WND_PROP_VISIBLE, 1)
            
            # Stop current video processing
            video_stopped = True
            if video_thread.is_alive():
                video_thread.join()
            
            # Process command
            process_command(command)
            
            # Reset timer and restart video immediately
            last_command_time = time.time()
            restart_video()

        except sr.UnknownValueError:
            pass

        except sr.RequestError as e:
            print(f"Recognition service error: {e}")
            speak("There was an error with the recognition service." )
            last_command_time = time.time()

        except Exception as e:
            print(f"Speak Again: {e}")
            speak("Please Speak Again.")
            last_command_time = time.time()

        # 30-second timeout check
        if time.time() - last_command_time > 30:
            print("No command received for 30 seconds. Exiting...")
            speak("No command received for 30 seconds. Exiting program, Thank You!")
            listening_active = False
            video_stopped = True
            break

    # Cleanup
    if video_thread.is_alive():
        video_thread.join()
    cv2.destroyAllWindows()
    os._exit(0)


if __name__ == "__main__":
    play_intro_video()
    voice_listener()