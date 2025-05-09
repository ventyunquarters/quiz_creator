import time
import random
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

#Define the quiz function to load it. It will come from a file with multiple choice questions
def load_quiz(filename):
    with open(filename, 'r') as file:
        raw_entries = file.read().strip().split('\n\n')
    quiz_data = []
    for entry in raw_entries:
        lines = entry.strip().split('\n')
        question = lines[0][3:]
        answer = lines[1][3:]
        choices = lines[2][3:].split(';')
        quiz_data.append((question, answer, choices))
    return quiz_data

#Ask one question and return the score earned and correctness
def ask_question(quiz_data):
    #Add a timer to give bonuses for early answers
    #Define bonus conditions
    bonus_time_limit = 15
    bonus_points = 2
    normal_points = 1

    #Randomly select a question from the quiz data
    question, correct_answer, choices = random.choice(quiz_data)

    #Shuffle the answer choices for unpredictability
    random.shuffle(choices)

    #Display the question and all the choices numbered and colored
    print(Fore.CYAN + "\nQuestion: " + Style.BRIGHT + question)
    choice_labels = ['A', 'B', 'C', 'D']
    label_to_choice = {}

    for idx, choice in enumerate(choices):
        label = choice_labels[idx]
        label_to_choice[label] = choice
        print(Fore.YELLOW + f"  {label}. {choice}")

    #Starting the timer when the user sees the question
    start_time = time.time()
    try:
        # Get the user's answer
        user_input = input(Fore.WHITE + "Enter the letter of your answer: ").strip().upper()
        end_time = time.time()
    except ValueError:
        # If input is invalid (e.g., letters), count it as wrong
        print(Fore.RED + " Invalid input. Counting as incorrect.")
        return 0, False

    #Check if the input is valid choice of number
    if user_input not in label_to_choice:
        print(Fore.RED + "Choice is invalid.")
        return 0, False

    #Track the number input to the actual answer
    user_answer = label_to_choice[user_input]
    time_taken = end_time - start_time

    print(f"You answered in {time_taken:.2f} seconds.")

    #Check if the answer is correct and assigns the score
    if user_answer.lower() == correct_answer.lower():
        if time_taken <= bonus_time_limit:
            # The user is fast and correct: Will give bonus
            print(Fore.GREEN + "Correct! Bonus points for speed!")
            return normal_points + bonus_points, True
        else:
            # Correct, but no bonus
            print(Fore.GREEN + "Correct!")
            return normal_points, True
    else:
        # Wrong answer
        print(Fore.RED + f"Incorrect. The correct answer was: {correct_answer}")
        return 0, False

#Save the high score to a file if it's a new high
def save_high_score(score, filename="highscore.txt"):
    high_score = 0

    # Check if a high score file already exists. Reads file
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                high_score = int(file.read().strip())
            except ValueError:
                high_score = 0
    # Compare the current score to the saved high score
    if score > high_score:
        with open(filename, 'w') as file:
            file.write(str(score))
        print(Fore.MAGENTA + "🎉 New High Score!")
    else:
        # If current score is higher, update the file
        print(Fore.BLUE + f"High Score to Beat: {high_score}")