# 13DGT Quiz
# API: https://opentdb.com/api_config.php

# SPECS

# Must use classes
# Settings must include: Topics, Levels of difficulty, number of users.
# At the end of the quiz the full results will be displayed.
# The results will be saved to a file.
# The results will be displayed in a table.
# If you have multiple users you may decide to display updated scores after a set number of, or each question.
# let the user decide how many questions they would like to do.
# Randomise the order of the questions from the full list.
# Different topic and difficulty Levels at the start of the program.
# The program must be able to allow for multiple users
# Read from a file and randomise the results
# Display the information in a meaningful way
# Comment code and appropriate variable names
# Evidence of debugging and error checking
# Flexible and robust.

# You must use:
# Object oriented Classes
# Multidimensional arrays
# Module(s)
# Strings, Numbers and Boolean data types

# use ╗ ╝ ╚ ╔ ═ ║ to draw boxes around the questions and text



# =================== VARIABLES ===================

welcome_text = """
 _ _____ ____   ____ _____ ___        _     
/ |___ /|  _ \ / ___|_   _/ _ \ _   _(_)____
| | |_ \| | | | |  _  | || | | | | | | |_  /
| |___) | |_| | |_| | | || |_| | |_| | |/ / 
|_|____/|____/ \____| |_| \__\_\\\__,_|_/___|
"""

topics = {
    "General Knowledge": 9,
    "Books": 10,
    "Film": 11,
    "Music": 12,
    "Musicals & Theatres": 13,
    "Television": 14,
    "Video Games": 15,
    "Board Games": 16,
    "Science & Nature": 17,
    "Computers": 18,
    "Mathematics": 19,
    "Mythology": 20,
    "Sports": 21,
    "Geography": 22,
    "History": 23,
    "Politics": 24,
    "Art": 25,
    "Celebrities": 26,
    "Animals": 27,
    "Vehicles": 28,
    "Comics": 29,
    "Gadgets": 30,
    "Japanese Anime & Manga": 31,
    "Cartoon & Animations": 32
}
difficulties = ["easy", "medium", "hard"]
default_topic = "General Knowledge"
default_difficulty = "easy" 
default_amount = 10

html_entities = {
    "&quot;": '"',
    "&amp;": "&",
    "&apos;": "'",
    "&lt;": "<", 
    "&gt;": ">",
    "&nbsp;": " ",
    "&rsquo;": "'",
    "&#039;": "'",
    "&oacute;": "ó",
}


# =================== IMPORTS ===================
import os
import json
import random
import time
import sys
from html import unescape
import base64

try:
    import requests
except ModuleNotFoundError:
    input("The requests module is not installed. Press enter to install it, else press ctrl+c to exit.")
    os.system("python -m pip install requests")
    import requests

# =================== CLASSES ===================


# This class is used to store the questions
class Question:
    def __init__(self, question, correct_answer, incorrect_answers):
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answers = incorrect_answers
        self.all_answers = incorrect_answers + [correct_answer]
        random.shuffle(self.all_answers)

    def __str__(self):
        return self.question

    def check_answer(self, answer):
        return answer == self.correct_answer

class User:
    def __init__(self, name):
        self.name = name    # Name of the user
        self.score = 0      # Score for the score board
        self.answers = []   # Will store the answers the user gave

    def __str__(self):
        return self.name

    def add_score(self, score):
        self.score += score

    def add_answer(self, answer):
        self.answers.append(answer)

    def get_score(self):
        return self.score


# This class is used to print colored text
# I got it from https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    


# =================== FUNCTIONS ===================


# This function gets the questions from the API
def get_questions(topic, difficulty, amount):
    url = f"https://opentdb.com/api.php?amount={amount}&category={topic}&difficulty={difficulty}&type=multiple&encode=base64"
    # print(url)
    response = requests.get(url)
    data = json.loads(response.text)
    questions = []
    for question in data["results"]:
        questions.append(Question(question["question"], question["correct_answer"], question["incorrect_answers"]))

    # replace html entities with the actual characters
    for question in questions:
        question.question = decode_response(question.question)
        question.correct_answer = decode_response(question.correct_answer)
        for i in range(len(question.incorrect_answers)):
            question.incorrect_answers[i] = decode_response(question.incorrect_answers[i])

    return questions

def decode_response(text):
    # decode the base64 encoded text
    text = base64.b64decode(text).decode("utf-8")
    return text


# This function verifies that the input is a number between the min and max
def verify_input(input_num, min, max):
    while True:
        try:
            input_num = int(input_num)
            if input_num < min or input_num > max:
                raise ValueError
            break
        except ValueError:
            input_num = input(f"Please enter a number between {min} and {max}: ")
    return input_num


# This function makes a box around the text
def box_print(text):
    terminal_size = os.get_terminal_size()
    output = "╔" + "═"*(terminal_size.columns-2) + "╗\n"
    
    if("\n" in text):
        lines = text.split("\n")
    else:
        lines = [text]

    for line in lines:
        words = line.split(" ")
        current_line = ""
        for word in words:
            if len(current_line + word) > terminal_size.columns-4:
                output += "║ " + current_line + " "*(terminal_size.columns-4-len(current_line)) + " ║\n"
                current_line = ""
            current_line += word 
            if(current_line != ""):
                if(len(current_line) < terminal_size.columns-4):
                    current_line += " "
        output += "║ " + current_line + " "*(terminal_size.columns-4-len(current_line)) + " ║\n"
        
    output += "╚" + "═"*(terminal_size.columns-2) + "╝"
    print(output)


# This function gets all the options from the user and returns them 
def get_options():
    

    # get the topic
    print("\nPlease select a topic:")
    for i, topic in enumerate(topics):
        print(f"{i+1}. {topic.title()}")
    topic = verify_input(input("Enter the number of the topic: "), 1, len(topics))
    topic = list(topics.keys())[topic-1]

    # get the difficulty
    print("\nPlease select a difficulty:")
    for i, difficulty in enumerate(difficulties):
        print(f"{i+1}. {difficulty.title()}")
    difficulty = verify_input(input("Enter the number of the difficulty: "), 1, len(difficulties))

    # get the amount of questions
    amount = verify_input(input("\nHow many questions do you want? "), 1, 50)

    # get the amount of players
    players = verify_input(input("\nHow many players are there? "), 1, 10)

    #users is a list of User objects
    users = []

    # get the players' names
    for i in range(players):
        name = input(f"\nWhat is the name of player {i+1}? ")
        while name == "":
            name = input(f"What is the name of player {i+1}? ")
        users.append(User(name))
            
    
    return topic, difficulty, amount, users


def quiz(questions, player_number, users):
    os.system("cls")
    print(f"Player {player_number+1}/{len(users)}, {users[player_number].name}")
    input(f"Press enter to start the game...")

    # start the quiz
    for i, question in enumerate(questions):
        os.system("cls")
        box_print(f"Question {i+1}/{len(questions)}\n{question.question}")
        
        correct_answer_position = random.randint(0, len(question.all_answers)-1)
        
        answers = question.incorrect_answers.copy()
        answers.insert(correct_answer_position, question.correct_answer)

        answers_to_print = []
        for i, answer in enumerate(answers):
            answers_to_print.append(f"{i+1}. {answer}")
            if i == 3: 
                break
            else:
                answers_to_print.append("\n")

        box_print("".join(answers_to_print))

        answer = verify_input(input("Enter the number of your answer: "), 1, len(question.all_answers))

        if correct_answer_position+1 == answer:
            users[player_number].add_score(1)
            print(bcolors.OKGREEN + "\nCorrect!" + bcolors.ENDC)
        else:
            print(bcolors.FAIL + "\nIncorrect!" + f"\nThe correct answer was {question.correct_answer}." + bcolors.ENDC)

        users[player_number].add_answer({"question": question.question, "correct_answer": answers_to_print[correct_answer_position], "user_answer": answers_to_print[answer-1], "correct": correct_answer_position+1 == answer})
        input("\nPress enter to continue...")




# This function prints the final results
def final_results(users, questions):
    os.system("cls")
    print("Final results:")
    # sort the users by score
    users.sort(key=lambda x: x.score, reverse=True)
    for i, user in enumerate(users):
        print(f"{i+1}. {user.name}: {user.score}/{len(questions)}.")

    input("\nPress enter to continue...")
    


# Welcome message
def welcome():
    os.system("cls")
    # print welcome text if the console is big enough
    terminal_size = os.get_terminal_size()
    if terminal_size.columns >= 44:
        print(welcome_text)
    else:
        print("\nWelcome to the quiz!")
    


# This is the main function
def main():

    # welcome the user
    welcome()

    # get the options
    topic, difficulty, amount, users = get_options()

    # get the questions and put them in a list of Question objects
    questions = get_questions(topics[topic], difficulties[difficulty-1], amount)

    # start the game
    print(f"Starting the game with {len(users)} players...")
    time.sleep(1)

    # start the quiz
    for i, user in enumerate(users):
        quiz(questions=questions, player_number=i, users=users)

    # print the final results
    final_results(users, questions)

    
    
    







# =================== MAIN ===================
if __name__ == "__main__":
    main()
    input("Press enter to exit...")
    sys.exit()