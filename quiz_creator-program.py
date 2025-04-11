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

#Stop the game when there's three incorrect answers

#Record the highscore