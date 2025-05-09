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

