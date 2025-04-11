import time
import random
import os

#Define the quiz function to load it. It will come from a file with multiple choice questions
def load_quiz(filename):
    #Open the file and split questions by blank lines
    with open(filename, 'r') as file:
        raw_entries = file.read().strip().split('\n\n') #Splits the text at every double line for questions

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
    choice_labels = ['A', 'B', 'C', 'D']  # Can extend if needed
    label_to_choice = {}

    for idx, choice in enumerate(choices):
        label = choice_labels[idx]
        label_to_choice[label] = choice
        print(f"  {label}. {choice}")

    #Starting the timer when the user sees the question
    start_time = time.time()
    try:
        #Get the user's answer
        user_input = input("Enter the letter of your answer: ").strip().upper()
        end_time = time.time()
    except ValueError:
        # If input is invalid (e.g., letters), count it as wrong
        print(" Invalid input. Counting as incorrect.")
        return 0, False

    #Check if the input is valid choice of number
    if user_input not in label_to_choice:
        print("Choice is invalid.")
        return 0, False

    #Track the number input to the actual answer
    user_answer = label_to_choice[user_input]
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

#Run the quiz on the loop
def start_quiz(quiz_data):
    total_score = 0
    wrong_count = 0
    max_wrong = 3 #Stop the game when there's three incorrect answers

    # Welcome messages
    print("Welcome to the Quiz! Pick the correct letter of the answer to earn points.")
    print("Answer within 5 seconds for bonus points.")
    print("Game ends after 3 incorrect answers.")

    # Will keep asking questions until the user gets 3 wrong
    while wrong_count < max_wrong:
        # Ask one question and get the result
        points, correct = ask_question(quiz_data)
        total_score += points

        # Track incorrect answers
        if not correct:
            wrong_count += 1
            print(f"Wrong Answers: {wrong_count}/{max_wrong}")

        # Show updated score
        print(f"Current Score: {total_score} point(s)")

    # Game over message
    print("\n Game Over! You reached 3 incorrect answers.")
    print(f"Final Score: {total_score} point(s)")

    # Save score if it's a high score
    save_high_score(total_score)


# Start the game
quiz_data = load_quiz("quiz.txt")
start_quiz(quiz_data)
