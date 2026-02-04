import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import random
import requests
import subprocess
import json

class EnhancedVoiceAssistant:
    def __init__(self, name="Dev"):
        self.name = name
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.setup_voice()
        
        self.user_data = {
            'name': 'Boss',
            'favorite_sites': {},
            'reminders': []
        }
        
        self.command_history = []
        
    def setup_voice(self):
        """Voice settings"""
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 170)
        self.engine.setProperty('volume', 1.0)
        
    def speak(self, text):
        """Bolo"""
        print(f"\n🤖 {self.name}: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self, timeout=5):
        """Suno"""
        with sr.Microphone() as source:
            print("\n🎤 Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                print("⚙️ Processing...")
                
                text = self.recognizer.recognize_google(audio, language='en-in')
                print(f"👤 You: {text}")
                
                self.command_history.append({
                    'time': datetime.datetime.now().isoformat(),
                    'command': text
                })
                
                return text.lower()
                
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                self.speak("Internet connection issue. Please check your connection.")
                return None
    
    def greet(self):
        """Smart greeting"""
        hour = datetime.datetime.now().hour
        
        greetings = {
            (0, 6): "It's quite late! You should get some rest.",
            (6, 12): "Good Morning",
            (12, 17): "Good Afternoon", 
            (17, 21): "Good Evening",
            (21, 24): "Good Night"
        }
        
        for time_range, greeting in greetings.items():
            if time_range[0] <= hour < time_range[1]:
                self.speak(f"{greeting}, {self.user_data['name']}!")
                break
                
        self.speak(f"I am {self.name}. What can I do for you today?")
    
    def get_weather(self, city="Agra"):
        """Weather information (free API)"""
        try:
            
            response = requests.get(f"https://wttr.in/{city}?format=3", timeout=5)
            if response.status_code == 200:
                return response.text.strip()
            return None
        except:
            return None
    
    def get_news(self):
        """Top headlines (placeholder - ad533a04946a449d89115178d71ba53d)"""
        
        self.speak("To get news, ad533a04946a449d89115178d71ba53d.")
        
    def play_on_youtube(self, query):
        """YouTube pe search aur play karo"""
        try:
            import pywhatkit
            self.speak(f"Playing {query} on YouTube")
            pywhatkit.playonyt(query)
        except:
            
            self.speak(f"Searching {query} on YouTube")
            webbrowser.open(f"https://youtube.com/results?search_query={query}")
    
    def set_reminder(self, reminder_text):
        """Simple reminder save karo"""
        self.user_data['reminders'].append({
            'text': reminder_text,
            'time': datetime.datetime.now().isoformat()
        })
        self.speak(f"Reminder saved: {reminder_text}")
    
    def show_reminders(self):
        """Saved reminders dikhao"""
        if self.user_data['reminders']:
            self.speak("Your reminders are:")
            for i, reminder in enumerate(self.user_data['reminders'], 1):
                self.speak(f"{i}. {reminder['text']}")
        else:
            self.speak("You have no reminders.")
    
    def system_info(self):
        """System information"""
        import platform
        
        info = f"""
        Operating System: {platform.system()} {platform.release()}
        Machine: {platform.machine()}
        Processor: {platform.processor()}
        """
        self.speak(f"You are running {platform.system()} {platform.release()}")
    
    def take_screenshot(self):
        """Screenshot lo"""
        try:
            import pyautogui
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            self.speak(f"Screenshot saved as {filename}")
        except ImportError:
            self.speak("Please install pyautogui: pip install pyautogui")
    
    def process_command(self, command):
        """Command processing with more features"""
        
        if command is None:
            return True
        
        if any(word in command for word in ['hello', 'hi', 'hey']):
            responses = [
                f"Hello {self.user_data['name']}! How can I help?",
                "Hey there! What do you need?",
                "Hi! I'm here to assist you."
            ]
            self.speak(random.choice(responses))
        
        elif 'wikipedia' in command:
            self.speak("What should I search on Wikipedia?")
            query = self.listen()
            if query:
                try:
                    self.speak("Searching...")
                    results = wikipedia.summary(query, sentences=2)
                    self.speak("According to Wikipedia")
                    self.speak(results)
                except:
                    self.speak("Sorry, couldn't find that.")
        
        elif 'play' in command and ('youtube' in command or 'song' in command or 'music' in command):
            query = command.replace('play', '').replace('on youtube', '').replace('song', '').replace('music', '').strip()
            if query:
                self.play_on_youtube(query)
            else:
                self.speak("What should I play?")
                query = self.listen()
                if query:
                    self.play_on_youtube(query)
        
        elif 'open' in command:
            sites = {
                'youtube': 'https://youtube.com',
                'google': 'https://google.com',
                'github': 'https://github.com',
                'stackoverflow': 'https://stackoverflow.com',
                'stack overflow': 'https://stackoverflow.com',
                'facebook': 'https://facebook.com',
                'instagram': 'https://instagram.com',
                'twitter': 'https://twitter.com',
                'linkedin': 'https://linkedin.com',
                'reddit': 'https://reddit.com',
                'amazon': 'https://amazon.in',
                'flipkart': 'https://flipkart.com',
                'gmail': 'https://mail.google.com',
                'whatsapp': 'https://web.whatsapp.com'
            }
            
            apps = {
                'notepad': 'notepad',
                'calculator': 'calc',
                'cmd': 'cmd',
                'command prompt': 'cmd',
                'file explorer': 'explorer',
                'paint': 'mspaint',
                'word': 'winword',
                'excel': 'excel',
                'powerpoint': 'powerpnt',
                'chrome': 'chrome',
                'firefox': 'firefox',
                'edge': 'msedge'
            }
            
            opened = False
            
            for site_name, url in sites.items():
                if site_name in command:
                    self.speak(f"Opening {site_name}")
                    webbrowser.open(url)
                    opened = True
                    break
            
            if not opened:
                for app_name, app_cmd in apps.items():
                    if app_name in command:
                        self.speak(f"Opening {app_name}")
                        try:
                            os.system(app_cmd)
                        except:
                            subprocess.Popen(app_cmd, shell=True)
                        opened = True
                        break
            
            if not opened:
                self.speak("I couldn't find that application or website.")
        
        elif 'search' in command or 'google' in command:
            query = command.replace('search', '').replace('google', '').replace('for', '').strip()
            if query:
                self.speak(f"Searching for {query}")
                webbrowser.open(f"https://google.com/search?q={query}")
            else:
                self.speak("What should I search for?")
        
        elif 'weather' in command:
            
            city = "Agra"  
            words = command.split()
            if 'in' in words:
                idx = words.index('in')
                if idx + 1 < len(words):
                    city = words[idx + 1]
            
            self.speak(f"Getting weather for {city}")
            weather = self.get_weather(city)
            if weather:
                self.speak(weather)
            else:
                self.speak("Sorry, couldn't fetch weather information.")
        
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {current_time}")
            
        elif 'date' in command:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            self.speak(f"Today is {current_date}")
            
        elif 'day' in command:
            day = datetime.datetime.now().strftime("%A")
            self.speak(f"Today is {day}")
        
        elif 'remind' in command or 'reminder' in command:
            if 'show' in command or 'list' in command:
                self.show_reminders()
            else:
                self.speak("What should I remind you about?")
                reminder = self.listen()
                if reminder:
                    self.set_reminder(reminder)
        
        elif 'screenshot' in command:
            self.take_screenshot()
        
        elif 'system' in command and 'info' in command:
            self.system_info()
        
        elif 'volume' in command:
            if 'up' in command or 'increase' in command:
                self.speak("Increasing volume")
                
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                try:
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    current = volume.GetMasterVolumeLevelScalar()
                    volume.SetMasterVolumeLevelScalar(min(1.0, current + 0.2), None)
                except:
                   
                    import pyautogui
                    pyautogui.press('volumeup', presses=5)
                    
            elif 'down' in command or 'decrease' in command:
                self.speak("Decreasing volume")
                try:
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    current = volume.GetMasterVolumeLevelScalar()
                    volume.SetMasterVolumeLevelScalar(max(0.0, current - 0.2), None)
                except:
                    import pyautogui
                    pyautogui.press('volumedown', presses=5)
                    
            elif 'mute' in command:
                self.speak("Muting volume")
                try:
                    import pyautogui
                    pyautogui.press('volumemute')
                except:
                    pass
        
        elif 'joke' in command:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the programmer quit his job? Because he didn't get arrays!",
                "A SQL query walks into a bar, walks up to two tables and asks: Can I join you?",
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "There are only 10 types of people: those who understand binary and those who don't.",
                "Why was the JavaScript developer sad? Because he didn't Node how to Express himself!",
                "What's a programmer's favorite hangout place? Foo Bar!"
            ]
            self.speak(random.choice(jokes))
            
        elif 'how are you' in command:
            self.speak("I'm functioning perfectly! Thanks for asking. How are you?")
            
        elif "i am" in command or "i'm" in command:
            if any(word in command for word in ['good', 'fine', 'great', 'awesome', 'happy']):
                self.speak("That's wonderful to hear!")
            elif any(word in command for word in ['sad', 'bad', 'tired', 'bored']):
                self.speak("I'm sorry to hear that. Is there anything I can do to help?")
            else:
                self.speak("I see. How can I assist you today?")
                
        elif 'your name' in command:
            self.speak(f"I am {self.name}, your personal voice assistant!")
            
        elif 'who made you' in command or 'who created you' in command:
            self.speak("I was created by Dev Yadav")
            
        elif 'thanks' in command:
            self.speak("You're welcome! Happy to help!")
        
        elif 'shutdown' in command or 'shut down' in command:
            self.speak("Are you sure you want to shutdown the computer? Say yes to confirm.")
            confirm = self.listen()
            if confirm and 'yes' in confirm:
                self.speak("Shutting down in 5 seconds")
                os.system("shutdown /s /t 5")
            else:
                self.speak("Shutdown cancelled.")
                
        elif 'restart' in command:
            self.speak("Are you sure you want to restart? Say yes to confirm.")
            confirm = self.listen()
            if confirm and 'yes' in confirm:
                self.speak("Restarting in 5 seconds")
                os.system("shutdown /r /t 5")
            else:
                self.speak("Restart cancelled.")
        
        elif any(word in command for word in ['exit', 'quit', 'bye', 'goodbye', 'stop']):
            goodbyes = [
                f"Goodbye {self.user_data['name']}! Have a great day!",
                "See you later! Take care!",
                "Bye bye! Call me whenever you need help!"
            ]
            self.speak(random.choice(goodbyes))
            return False
        
        elif 'help' in command or 'what can you do' in command:
            help_text = """
            I can help you with:
            Opening websites like YouTube, Google, GitHub
            Opening apps like Notepad, Calculator, Chrome
            Playing songs on YouTube
            Searching on Google
            Telling time, date and weather
            Taking screenshots
            Setting reminders
            Controlling volume
            And having a friendly chat!
            """
            self.speak(help_text)
        
        else:
            responses = [
                "I'm not sure about that. Can you try rephrasing?",
                "I didn't catch that. Could you say it differently?",
                "Sorry, I don't understand. Say 'help' to know what I can do."
            ]
            self.speak(random.choice(responses))
        
        return True
    
    def run(self):
        """Main program loop"""
        print("=" * 50)
        print(f"   {self.name} - Voice Assistant")
        print("=" * 50)
        
        self.greet()
        
        running = True
        while running:
            command = self.listen()
            running = self.process_command(command)
        
        print("\nAssistant stopped.")


if __name__ == "__main__":
    assistant = EnhancedVoiceAssistant(name="Dev")
    assistant.run()
    
