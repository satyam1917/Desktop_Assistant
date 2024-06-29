import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import random

# sapi5 microsoft API for voice
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# voices[] the number can be changed and you can look into the voices stored in the system
# print(voices[0].id)
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning")
    elif hour >= 12 and hour < 17:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
        
    speak("I am your assistant Friday, How may I help you?")

def takecommand():
    # Taking input from user's microphone and returning a string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Friday is Listening BE CAREFUL!!!!")
        # r.pause_threshold =1 the gap shows a pause between your voice
        r.pause_threshold = 1
        r.energy_threshold = 500
        audio = r.listen(source)
        
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "None"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "None"

def play_music():
    speak("Which song would you like to play?")
    song = takecommand()
    if song == "none":
        return
    webbrowser.open(f"https://music.youtube.com/search?q={song}")
    speak(f"Playing {song} on YouTube Music")

# smtplib used less secured app in Gmail --> google search
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your_email@gmail.com', 'password_generated_by_google_app_password')
    server.sendmail('your_email@gmail.com', to, content)
    server.close()
    
def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't some couples go to the gym? Because some relationships don't work out!",
        "What do you get when you cross a snowman with a vampire? Frostbite."
    ]
    return random.choice(jokes)

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board, player):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    return [player, player, player] in win_conditions

def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    human_player = random.choice(players)
    computer_player = "O" if human_player == "X" else "X"
    current_player = "X"
    moves = 0
    
    def computer_move(board):
        available_moves = [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]
        return random.choice(available_moves)

    while moves < 9:
        print_board(board)
        if current_player == human_player:
            print(f"Your turn ({human_player}). Enter row and column (0, 1, or 2).")
            try:
                command = input("Enter row and column (0, 1, or 2): ")
                row, col = map(int, command.split())
                if board[row][col] != " ":
                    print("Cell already taken, try again.")
                    continue
            except (ValueError, IndexError):
                print("Invalid input, try again.")
                continue
        else:
            print(f"Computer's turn ({computer_player}).")
            row, col = computer_move(board)
            print(f"Computer chose: {row} {col}")

        board[row][col] = current_player
        moves += 1

        if check_winner(board, current_player):
            print_board(board)
            print(f"{current_player} wins!")
            return
        
        current_player = human_player if current_player == computer_player else computer_player

    print_board(board)
    print("It's a draw!")

def get_computer_choice():
    return random.choice(["rock", "paper", "scissors"])

def get_winner(player, computer):
    if player == computer:
        return "It's a tie!"
    elif (player == "rock" and computer == "scissors") or \
         (player == "scissors" and computer == "paper") or \
         (player == "paper" and computer == "rock"):
        return "You win!"
    else:
        return "Computer wins!"

def rock_paper_scissors():
    choices = ["rock", "paper", "scissors"]
    
    while True:
        print("Enter rock, paper, or scissors (or 'quit' to stop playing):")
        player_choice = input().lower()
        if player_choice == 'quit':
            print("Thanks for playing!")
            break
        elif player_choice not in choices:
            print("Invalid choice, try again.")
            continue
        
        computer_choice = get_computer_choice()
        print(f"Computer chose: {computer_choice}")
        result = get_winner(player_choice, computer_choice)
        print(result)

if __name__ == "__main__":
    wishme()
    while True:
        query = takecommand()
        if query == "none":
            continue
        
        if 'wikipedia' in query:
            speak('Opening Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                summary = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(summary)
                speak(summary)
                break
            except wikipedia.exceptions.DisambiguationError as e:
                speak("There are multiple results for this topic. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("I could not find any information on this topic.")
            except wikipedia.exceptions.WikipediaException as e:
                speak(f"An error occurred while accessing Wikipedia: {e}")
            except Exception as e:
                speak(f"An unexpected error occurred: {e}")
        elif 'how ' in query and 'you' in query:
            speak('I am fine, thank you')
        elif 'youtube' in query: 
            webbrowser.open("https://www.youtube.com")
           
        elif 'google'  in query: 
            webbrowser.open("https://www.google.co.in")
           
        elif 'codeforce' in query or 'cf' in query:
            webbrowser.open("https://codeforces.com")
        
        elif 'music' in query:
            play_music()
            
        elif 'playlist' in query:
            music_dir ='path\\add\\here'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
        
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        
        elif 'email' in query:
            try:
                speak("What should I say?")
                content = takecommand()
                speak("Who do you want to send the email to?")
                print("Please Type The Email ID")
                to = input()
                sendEmail(to, content)
                speak("Email has been sent")
            except Exception as e:
                speak("Sorry, unable to send email")
                
        elif 'joke' in query or 'funny' in query:
            joke = tell_joke()
            print(joke)
            speak(joke)
        elif 'play' in query or 'game' in query:   
            speak("Which game would you like to play: tic tac toe or rock paper scissors? Enter 1 for tic tac toe and 2 for rock paper scissors.")
            game_choice = input("Enter 1 for tic tac toe and 2 for rock paper scissors or  0 to exit: ")
            if game_choice == "1":
                tic_tac_toe()
            elif game_choice == "2":
                rock_paper_scissors()
            elif game_choice == "0":
                break
            else:
                speak("Invalid choice. Please enter 1 for tic tac toe or 2 for rock paper scissors.")
        elif 'exit' in query or 'quit' in query:
            speak("Goodbye!")
            break
