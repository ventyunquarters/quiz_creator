import time
import random
import os

#Define the quiz function to load it. It will come from a file with multiple choice questions
def load_quiz(filename):
    #Open the file and split questions by blank lines
    with open(filename, 'r') as file:
        raw_entries = file.read().strip().split('\n\n') #Splits the tet at every double line for questions

    quiz_data = []
    for entry in raw_entries:
        lines = entry.strip().split('\n')
        #Extract the question, correct answer, nad choices
        question  = lines[0][3:] # Skip the "Q: "
        answer  = lines[1][3:] # Skip the "A: "
        choices  = lines[2][3:].split(';') #Split choices by semicolon
        #Store the question, correct answer, and choices in a list
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

    #Display the question and all the choices numbered
    print("\n Question:", question)
    for idx, choice in enumerate(choices, start=1):
        print(f"  {idx}. {choice}")

    #Starting the timer when the user sees the question
    start_time = time.time()
    try:
        #Get the user's answer
        user_input = int(input("Enter the number of your answer: ").strip())
        end_time = time.time()
    except ValueError:
        # If input is invalid (e.g., letters), count it as wrong
        print(" Invalid input. Counting as incorrect.")
        return 0, False

    #Check if the input is valid choice of number
    if not (1 <= user_input <= len(choices)):
        print("Choice is out of range.")
        return 0, False

    #Track the number input to the actual answer
    user_answer = choices[user_input - 1]
    time_taken = end_time - start_time

    print(f"You answered in {time_taken:.2f} seconds.")

    #Check if the answer is correct and assigns the score
    if user_answer.lower() == correct_answer.lower():
        if time_taken <= bonus_time_limit:
            #The user is fast and correct: Will give bonus
            print("Correct! Bonus points for speed!")
            return normal_points + bonus_points, True
        else:
            # Correct, but no bonus
            print("Correct!")
            return normal_points, True

    else:
        #Wrong answer
        print(f"Incorrect. The correct answer was: {correct_answer}")
        return 0, False

#Save the high score to a file if it's a new high
def save_high_score(score, filename="highscore.txt"):
    high_score = 0

    # Check if a high score file already exists
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                high_score = int(file.read().strip())
            except ValueError:
                high_score = 0

    # Compare the current score to the saved high score
    if score > high_score:
        # If current score is higher, update the file
        with open(filename, 'w') as file:
            file.write(str(score))
        print(" New High Score!")
    else:
        # Show current high score to beat
        print(f" High Score to Beat: {high_score}")


#Stop the game when there's three incorrect answers

