# Import difflib to catch typos in user input
import difflib
# Import requests to call websites and APIs
import requests
# Import random to pick a random reply from a list
import random
# Import datetime to get the current time
from datetime import datetime
# Import BeautifulSoup to read text off of web pages
from bs4 import BeautifulSoup

class ChatBot:
    def __init__(self, bot_name="Yudhi"):
        # Save the bot name
        self.bot_name = bot_name
        # Start an empty list to save the chat history
        self.history = []

        # List of topics and the words that trigger them
        self.intents = [
            ("gratitude", ["thank you", "thanks", "appreciate", "great", "cool", "awesome"]),
            ("humor", ["funny", "humor", "laugh", "joke"]),
            ("weather", ["weather", "temperature", "hot", "cold", "humidity", "rain", "wind"]),
            ("time", ["time", "date", "clock", "year", "month"]),
            ("identity", ["who are you", "what is your name", "your name"]),
            ("help", ["help", "commands", "options", "what can you do"]),
            ("farewell", ["bye", "goodbye", "exit", "quit"]),
            ("greeting", ["hello", "hi", "yo", "hey"])
        ]

        # Connect each topic to a function or a list of replies
        self.responses = {
            "humor": self.get_joke,
            "weather": self.get_weather,
            "time": self.get_time,
            "identity": ["I am a python chatbot made in CodeHS."],
            "help": ["I can tell you the weather, time, or look something up!"],
            "farewell": ["See you later!", "Goodbye!", "Adios!"],
            "greeting": ["Hello! What would you like to do today?"],
            "gratitude": ["No problem!", "Happy to help!"]
        }

    def get_city(self):
        # Try to find what city the user is in using their IP address
        try:
            reply = requests.get("http://ip-api.com/json/", timeout=3)
            data = reply.json()
            # Return the city name if it worked
            if data.get("status") == "success":
                return data.get("city")
        except:
            pass
        # Use New York as a backup if the lookup fails
        return "New York"

    def get_time(self, words):
        try:
            # Get the current time from the computer
            now = datetime.now()

            # Return the right format based on what the user asked
            if "year" in words:
                return "The current year is " + now.strftime('%Y') + "."
            elif "month" in words:
                return "The current month is " + now.strftime('%B') + "."
            elif "date" in words:
                return "Today is " + now.strftime('%A, %B %d, %Y') + "."
            else:
                return "The current time is " + now.strftime('%I:%M %p') + "."
        except:
            pass
        return "I could not read the time."

    def get_joke(self, words):
        try:
            # Grab a two part joke from a joke website
            url = "https://v2.jokeapi.dev/joke/Any?safe-mode&type=twopart"
            data = requests.get(url, timeout=5).json()
            setup = data["setup"]
            punchline = data["delivery"]
            # Return both parts as a list so main.py can add a pause between them
            return [setup, punchline]
        except:
            pass
        # Use a backup joke if the website is down
        return ["Why did the chicken cross the road?", "To get to the other side!"]

    def get_weather(self, words):
        try:
            # Get the user's city
            city = self.get_city()
            # Build the weather URL for that city
            url = "https://wttr.in/" + city.replace(' ', '+') + "?format=%C,%t,%h,%w"
            reply = requests.get(url, timeout=5)

            if reply.status_code == 200:
                # Split the weather data into separate pieces
                parts = reply.text.strip().split(",")
                sky = parts[0]
                temp = parts[1]
                humidity = parts[2]
                wind = parts[3]

                # Return the piece the user asked about
                if "humidity" in words or "humid" in words:
                    return "The humidity in " + city + " is " + humidity + "."
                elif "rain" in words or "raining" in words:
                    if "rain" in sky.lower() or "drizzle" in sky.lower():
                        return "Yes, it looks like it is raining in " + city + "."
                    else:
                        return "No rain today in " + city + "."
                elif "temperature" in words or "temp" in words or "hot" in words:
                    return "The temperature in " + city + " is " + temp + "."
                elif "wind" in words or "windspeed" in words:
                    return "The wind speed in " + city + " is " + wind + "."
                else:
                    return "It is " + sky + " in " + city + " at " + temp + "."
        except:
            pass
        return "I could not get the weather right now."

    def web_search(self, words):
        try:
            # Turn the word list back into a search sentence
            query = " ".join(words) + " fact summary short"

            # Set up the search request
            url = "https://lite.duckduckgo.com/lite/"
            payload = {"q": query}
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

            # Send the search and check if it worked
            reply = requests.post(url, headers=headers, data=payload, timeout=5)
            if reply.status_code == 200:
                # Read the results off the page
                soup = BeautifulSoup(reply.text, 'html.parser')
                results = soup.find_all(class_='result-snippet')

                # Loop through each result and find a good sentence to return
                for result in results:
                    text = result.text.strip()

                    # Skip results that start with a month name
                    if text.startswith("Jan") or text.startswith("Feb"):
                        continue

                    # Split into sentences and return the first clean one
                    for sentence in text.split(". "):
                        sentence = sentence.strip()
                        if len(sentence) > 25 and "click here" not in sentence.lower():
                            if not sentence.endswith("."):
                                sentence = sentence + "."
                            return "According to the web: " + sentence
        except:
            pass
        return "I could not find anything on that topic."

    def get_reply(self, user_input):
        # Lowercase and clean up the input
        cleaned = user_input.lower().strip()

        # Remove punctuation so it doesn't break word matching
        for mark in [".", "?", "!", ",", ";"]:
            cleaned = cleaned.replace(mark, " ")

        # Split the input into individual words
        words = cleaned.split()

        # Words that suggest the user is referring to something they said before
        pointer_words = ["it", "that", "they", "there", "him", "her", "again", "then"]

        # Check if the user used any pointer words
        used_pointer = False
        for word in words:
            if word in pointer_words:
                used_pointer = True

        # If they used a pointer word, pull words from the last message
        if used_pointer and len(self.history) > 0:
            last_message = self.history[-1]["user"]
            if "weather" in last_message or "wind" in last_message or "joke" in last_message:
                for old_word in last_message.lower().split():
                    # Add old topic words back into the current word list
                    if old_word not in words and len(old_word) > 3:
                        words.append(old_word)

        # Check each word against every topic's trigger words
        for topic, triggers in self.intents:
            for word in words:

                # Check for an exact match
                if word in triggers:
                    action = self.responses[topic]

                    # Run the function if it is one, otherwise pick a random reply
                    if callable(action):
                        reply = action(words)
                    else:
                        reply = random.choice(action)

                    # Use a backup message if the reply came back empty
                    if reply is None:
                        reply = "I got an empty response. Please try again!"

                    # Save and return the reply
                    self.history.append({"user": user_input, "bot": reply})
                    return reply

                # Check for a close match in case of a typo
                close = difflib.get_close_matches(word, triggers, n=1, cutoff=0.7)
                if close:
                    action = self.responses[topic]

                    if callable(action):
                        reply = action(words)
                    else:
                        reply = random.choice(action)

                    if reply is None:
                        reply = "I got an empty response. Please try again!"

                    self.history.append({"user": user_input, "bot": reply})
                    return reply

        # Nothing matched so return a default message
        fallback = "I do not understand. Try asking me about the weather, time, or a joke!"
        self.history.append({"user": user_input, "bot": fallback})
        return fallback