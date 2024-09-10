import random

class ChatBot:
    def __init__(self):
        self.bot_name = "TravelAssistantBot"

    def respond(self, user_input):
        responses = {
            'greeting': f"Hello! I'm {self.bot_name}. How can I assist you today?",
            'farewell': "Goodbye! Have a great day!",
            'default': "Sorry, I didn't understand that. Could you please clarify?",
        }
        if 'hello' in user_input or 'hi' in user_input:
            return responses['greeting']
        elif 'bye' in user_input or 'goodbye' in user_input:
            return responses['farewell']
        else:
            return responses['default']

class TravelAssistantBot(ChatBot):
    negative_res = ("no", "nope", "nah", "naw", "not a chance", "sorry")
    positive_res = ("yes", "yeah", "yep", "sure", "absolutely", "definitely", "of course")
    exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later", "thanks", "thank you")

    def __init__(self):
        super().__init__()
        self.destinations = {
            'paris': {
                'attractions': ['Eiffel Tower', 'Louvre Museum', 'Notre-Dame Cathedral', 'Montmartre'],
                'itinerary': 'Day 1: Eiffel Tower and Seine River Cruise. Day 2: Louvre Museum and Montmartre. Day 3: Notre-Dame Cathedral and Champs-Élysées.',
                'hotels': ['Hotel Lutetia', 'Le Meurice', 'Shangri-La Hotel'],
                'flights': ['Air France', 'Delta', 'United Airlines']
            },
            'new york': {
                'attractions': ['Statue of Liberty', 'Central Park', 'Times Square', 'Empire State Building'],
                'itinerary': 'Day 1: Statue of Liberty and Ellis Island. Day 2: Central Park and Times Square. Day 3: Empire State Building and Broadway Show.',
                'hotels': ['The Plaza', 'Mandarin Oriental', 'Four Seasons'],
                'flights': ['American Airlines', 'JetBlue', 'United Airlines']
            },
            'tokyo': {
                'attractions': ['Tokyo Tower', 'Senso-ji Temple', 'Shibuya Crossing', 'Meiji Shrine'],
                'itinerary': 'Day 1: Tokyo Tower and Senso-ji Temple. Day 2: Shibuya Crossing and Meiji Shrine. Day 3: Tsukiji Market and Odaiba.',
                'hotels': ['The Ritz-Carlton', 'Park Hyatt', 'Aman Tokyo'],
                'flights': ['Japan Airlines', 'ANA', 'Delta']
            },
            'london': {
                'attractions': ['Big Ben', 'London Eye', 'Tower of London', 'Buckingham Palace'],
                'itinerary': 'Day 1: Big Ben and London Eye. Day 2: Tower of London and Tower Bridge. Day 3: Buckingham Palace and British Museum.',
                'hotels': ['The Savoy', 'The Ritz London', 'Claridge’s'],
                'flights': ['British Airways', 'Virgin Atlantic', 'American Airlines']
            },
            'sydney': {
                'attractions': ['Sydney Opera House', 'Sydney Harbour Bridge', 'Bondi Beach', 'Taronga Zoo'],
                'itinerary': 'Day 1: Sydney Opera House and Sydney Harbour Bridge. Day 2: Bondi Beach and Taronga Zoo. Day 3: Darling Harbour and The Rocks.',
                'hotels': ['Park Hyatt Sydney', 'Shangri-La Hotel', 'The Langham'],
                'flights': ['Qantas', 'Emirates', 'United Airlines']
            },
            'maldives': {
                'attractions': ['Malé Atoll', 'Banana Reef', 'Maafushi', 'Hinnavaru'],
                'itinerary': 'Day 1: Malé Atoll and local exploration. Day 2: Snorkeling at Banana Reef. Day 3: Relaxation at Maafushi and Hinnavaru.',
                'hotels': ['Soneva Fushi', 'Conrad Maldives Rangali Island', 'Anantara Veli Maldives Resort'],
                'flights': ['Emirates', 'Qatar Airways', 'SriLankan Airlines']
            },
            'malaysia': {
                'attractions': ['Petronas Towers', 'Langkawi Sky Bridge', 'George Town', 'Kinabalu National Park'],
                'itinerary': 'Day 1: Petronas Towers and Kuala Lumpur City Tour. Day 2: Langkawi Sky Bridge and Island Exploration. Day 3: George Town and Kinabalu National Park.',
                'hotels': ['The Ritz-Carlton Kuala Lumpur', 'Four Seasons Resort Langkawi', 'Shangri-La Hotel Kuala Lumpur'],
                'flights': ['Malaysia Airlines', 'AirAsia', 'Singapore Airlines']
            },
            'istanbul': {
                'attractions': ['Hagia Sophia', 'Topkapi Palace', 'Blue Mosque', 'Grand Bazaar'],
                'itinerary': 'Day 1: Hagia Sophia and Topkapi Palace. Day 2: Blue Mosque and Bosphorus Cruise. Day 3: Grand Bazaar and local markets.',
                'hotels': ['Ciragan Palace Kempinski', 'Four Seasons Hotel Istanbul', 'The Marmara Taksim'],
                'flights': ['Turkish Airlines', 'Pegasus', 'Lufthansa']
            },
            'italy': {
                'attractions': ['Colosseum', 'Venice Canals', 'Leaning Tower of Pisa', 'Florence Cathedral'],
                'itinerary': 'Day 1: Colosseum and Roman Forum. Day 2: Venice Canals and St. Mark\'s Basilica. Day 3: Leaning Tower of Pisa and Florence Cathedral.',
                'hotels': ['Hotel Hassler Rome', 'Gritti Palace Venice', 'Four Seasons Florence'],
                'flights': ['Alitalia', 'Delta', 'British Airways']
            }
        }
        self.seasonal_destinations = {
            'winter': ['New York', 'Tokyo', 'Paris'],
            'spring': ['Paris', 'Tokyo', 'London'],
            'summer': ['Maldives', 'Malaysia', 'Istanbul', 'Italy'],
            'fall': ['Tokyo', 'Paris', 'Sydney']
        }
        self.current_destination = None
        self.prompt_shown = False
        self.destination_info_shown = False

    def greet(self):
        self.name = input("What is your name?\n")
        print(f"Hi {self.name}, I am {self.bot_name}. How can I assist you with your travel plans today?")
        self.chat()

    def make_exit(self, reply):
        for command in self.exit_commands:
            if reply == command:
                print("Goodbye! Have a nice trip!")
                return True
        return False

    def chat(self):
        reply = input().lower()
        while not self.make_exit(reply):
            response = self.match_reply(reply)
            if response:
                print(response)
                if self.current_destination and not self.destination_info_shown:
                    self.destination_info_shown = True
                    reply = input(f"What else would you like to know about {self.current_destination.title()}? Here are some options: 'attractions', 'itinerary', 'hotels', 'flights'.\n").lower()
                elif not self.prompt_shown:
                    print("What else would you like to know? Here are some options: 'best destinations in summer', 'best destinations in winter', etc.")
                    self.prompt_shown = True
                    reply = input().lower()
                else:
                    reply = input().lower()
            else:
                break

    def match_reply(self, reply):
        if 'best destinations' in reply:
            if 'summer' in reply or 'winter' in reply or 'spring' in reply or 'fall' in reply:
                season = self.extract_season(reply)
                if season:
                    return self.provide_seasonal_destinations(season)
                else:
                    return "Please specify a season (e.g., winter, spring, summer, fall)."
            else:
                return self.list_all_destinations()
        elif reply in self.destinations:
            return self.provide_destination_info(reply)
        elif 'itinerary' in reply:
            return self.provide_itinerary()
        elif 'hotels' in reply:
            return self.provide_hotels()
        elif 'flights' in reply:
            return self.provide_flights()
        elif 'attractions' in reply:
            return self.provide_attractions()
        elif reply in self.positive_res:
            return self.handle_positive_response()
        else:
            return self.no_match_intent()

    def extract_season(self, reply):
        seasons = ['winter', 'spring', 'summer', 'fall']
        for season in seasons:
            if season in reply:
                return season
        return None

    def provide_destination_info(self, destination):
         self.current_destination = destination
         self.destination_info_shown = False
         info = f"You have chosen {destination.title()}."
         return info


    def provide_itinerary(self):
        if self.current_destination:
            itinerary = self.destinations[self.current_destination]['itinerary']
            return f"Here's a suggested itinerary for {self.current_destination.title()}:\n{itinerary}\nWould you like information on hotels or flights?"
        else:
            return "Please specify a destination first."

    def provide_hotels(self):
        if self.current_destination:
            hotels = ', '.join(self.destinations[self.current_destination]['hotels'])
            return f"Recommended hotels in {self.current_destination.title()} are: {hotels}. Would you like information on flights or attractions?"
        else:
            return "Please specify a destination first."

    def provide_flights(self):
        if self.current_destination:
            flights = ', '.join(self.destinations[self.current_destination]['flights'])
            return f"Flights available to {self.current_destination.title()} are: {flights}. Would you like information on hotels or attractions?"
        else:
            return "Please specify a destination first."

    def provide_attractions(self):
        if self.current_destination:
            attractions = ', '.join(self.destinations[self.current_destination]['attractions'])
            return f"Top attractions in {self.current_destination.title()} are: {attractions}. Would you like to know about the itinerary or hotels?"
        else:
            return "Please specify a destination first."

    def provide_seasonal_destinations(self, season):
        if season in self.seasonal_destinations:
            destinations = ', '.join(self.seasonal_destinations[season])
            return f"Based on the {season.title()}, here are some of the best destinations: {destinations}. Please choose one to get more information."
        else:
            return "I don't have information on that season. Please choose from winter, spring, summer, or fall."

    def handle_positive_response(self):
        return "Great! What would you like to know about your travel destination? Here are some options: 'attractions', 'itinerary', 'hotels', 'flights'."

    def no_match_intent(self):
        available_destinations = ', '.join([destination.title() for destination in self.destinations])
        responses = (
            f"Sorry, I didn't understand that. Please ask about a specific destination or type 'best destinations' to get a list of options.",
            f"I'm afraid I don't have information on that. You can ask me about these destinations: {available_destinations}.",
            f"I can help with the following destinations: {available_destinations}. Please select one or ask about specific details."
        )
        return random.choice(responses)

    def list_all_destinations(self):
        destinations = ', '.join([dest.title() for dest in self.destinations])
        return f"I can help with the following destinations: {destinations}. Please select one or ask about specific details."

if __name__ == "__main__":
    bot = TravelAssistantBot()
    bot.greet()
