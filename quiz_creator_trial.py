import time
import random
import os


# --- Step 1: Load quiz data from a file with multiple choice questions ---
def load_quiz(filename):
    # Open the file and split questions by blank lines
    with open(filename, 'r') as file:
        raw_entries = file.read().strip().split('\n\n')

    quiz_data = []
    for entry in raw_entries:
        lines = entry.strip().split('\n')
        # Extract question, correct answer, and choices
        question = lines[0][3:]  # Skip "Q: "
        answer = lines[1][3:]  # Skip "A: "
        choices = lines[2][3:].split(';')  # Split choices by semicolon
        # Store the question, correct answer, and choices in a list
        quiz_data.append((question, answer, choices))
    return quiz_data


# --- Step 2: Ask one question and return score earned and correctness ---
def ask_question(quiz_data):
    # Define bonus conditions
    bonus_time_limit = 15
    bonus_points = 2
    normal_points = 1

    # Randomly select a question from the quiz data
    question, correct_answer, choices = random.choice(quiz_data)

    # Shuffle the answer choices so it's not predictable
    random.shuffle(choices)

    # Display the question and all the choices numbered
    print("\n🧠 Question:", question)
    for idx, choice in enumerate(choices, start=1):
        print(f"  {idx}. {choice}")

    # Start the timer when user sees the question
    start_time = time.time()
    try:
        # Get the user's answer (number corresponding to a choice)
        user_input = int(input("Enter the number of your answer: ").strip())
        end_time = time.time()
    except ValueError:
        # If input is invalid (e.g., letters), count it as wrong
        print("⚠️ Invalid input. Counting as incorrect.")
        return 0, False

    # Check if the input is a valid choice number
    if not (1 <= user_input <= len(choices)):
        print("⚠️ Choice out of range.")
        return 0, False

    # Map the number input to the actual answer
    user_answer = choices[user_input - 1]
    time_taken = end_time - start_time

    print(f"⏱️ You answered in {time_taken:.2f} seconds.")

    # --- Step 2.1: Check if answer is correct and assign score ---
    if user_answer.lower() == correct_answer.lower():
        if time_taken <= bonus_time_limit:
            # Fast and correct: give bonus
            print("✅ Correct! 🎉 Bonus points for speed!")
            return normal_points + bonus_points, True
        else:
            # Correct, but no bonus
            print("✅ Correct!")
            return normal_points, True
    else:
        # Wrong answer
        print(f"❌ Incorrect. The correct answer was: {correct_answer}")
        return 0, False


# --- Step 3: Save high score to a file if it's a new high ---
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
        print("🎉 New High Score!")
    else:
        # Show current high score to beat
        print(f"🏅 High Score to Beat: {high_score}")


# --- Step 4: Run the quiz game loop ---
def start_quiz(quiz_data):
    total_score = 0
    wrong_count = 0
    max_wrong = 3  # Game ends after 3 wrong answers

    # Welcome message
    print("🎯 Welcome to the Quiz! Pick the correct answer to earn points.")
    print("💥 Answer within 5 seconds for bonus points.")
    print("🚫 Game ends after 3 incorrect answers.")

    # Keep asking questions until the user gets 3 wrong
    while wrong_count < max_wrong:
        # Ask one question and get the result
        points, correct = ask_question(quiz_data)
        total_score += points

        # Track incorrect answers
        if not correct:
            wrong_count += 1
            print(f"⚠️ Wrong Answers: {wrong_count}/{max_wrong}")

        # Show updated score
        print(f"⭐ Current Score: {total_score} point(s)")

    # Game over message
    print("\n🚫 Game Over! You reached 3 incorrect answers.")
    print(f"🏁 Final Score: {total_score} point(s)")

    # Save score if it's a high score
    save_high_score(total_score)


# --- Step 5: Start the game ---
quiz_data = load_quiz("quiz.txt")
start_quiz(quiz_data)