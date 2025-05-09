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