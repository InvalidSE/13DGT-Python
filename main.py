# 13DGT Quiz by InvalidSE - https://github.com/InvalidSE - 2023
# API: https://opentdb.com/api_config.php 

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

# =================== IMPORTS ===================
from random import randint, shuffle
from time import sleep
import os
import json
import sys
import base64

try:
    import requests
except ModuleNotFoundError:
    input("The requests module is not installed. Press enter to install it, else press ctrl+c to exit.")
    os.system("python -m pip install requests")
    try:
        import requests
    except ModuleNotFoundError:
        print("Failed to install requests module. Please install it manually.")
        input("Press enter to exit.")
        sys.exit()

# Get OS and the clear screen command
if os.name == "nt":
    clear_screen = "cls"
else:
    clear_screen = "clear"

# =================== CLASSES ===================


# This class is used to store the questions
class Question:
    def __init__(self, question, correct_answer, incorrect_answers):
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answers = incorrect_answers
        self.all_answers = incorrect_answers + [correct_answer]
        shuffle(self.all_answers)

    def __str__(self):
        return self.question

    def check_answer(self, answer):
        return answer == self.correct_answer


# This class is used to store the users
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


# This function gets the questions from the API and returns them as a list of Question objects
def get_questions(topic, difficulty, amount):
    url = f"https://opentdb.com/api.php?amount={amount}&category={topic}&difficulty={difficulty}&type=multiple&encode=base64"
    # print(url)
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        print("The API returned an error.")
        input("Check connection or try different settings. Press enter to exit.")
        sys.exit()
    # check for a valid response
    if(response.status_code != 200):
        print("The API returned an error. Code: " + str(response.status_code))
        input("Check connection or try different settings. Press enter to exit.")
        sys.exit()
    data = json.loads(response.text)
    if(data["response_code"] == 2 or data["response_code"] == 3 or data["response_code"] == 4):
        print("The API returned an error. Code: " + str(data["response_code"]))
        input("Check connection or try different settings. Press enter to exit.")
        sys.exit()
    if(data["response_code"] == 1):
        print("There are not enough questions to match your request. Retrying with less questions.")
        while data["response_code"] == 1:
            amount -= 1
            url = f"https://opentdb.com/api.php?amount={amount}&category={topic}&difficulty={difficulty}&type=multiple&encode=base64"
            response = requests.get(url)
            data = json.loads(response.text)
        print(f"Successfully got questions with {amount} questions.")
        sleep(1)
        
    questions = []
    for question in data["results"]:
        questions.append(Question(question["question"], question["correct_answer"], question["incorrect_answers"]))

    # Decode the Base64 encoding
    for question in questions:
        question.question = base64.b64decode(question.question).decode("utf-8")
        question.correct_answer = base64.b64decode(question.correct_answer).decode("utf-8")
        for i in range(len(question.incorrect_answers)):
            question.incorrect_answers[i] = base64.b64decode(question.incorrect_answers[i]).decode("utf-8")

    if(len(questions) == 0):
        print("No questions were returned by the API. Code: " + str(data["response_code"]))
        input("Check connection or try different settings. Press enter to exit.")
        sys.exit()

    return questions


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
    amount = verify_input(input("\nHow many questions do you want? "), 1, 25)

    # get the amount of players
    players = verify_input(input("\nHow many players are there? "), 1, 8)

    #users is a list of User objects
    users = []

    # get the players' names
    for i in range(players):
        name = input(f"\nWhat is the name of player {i+1}? ")
        while name == "":
            name = input(f"What is the name of player {i+1}? ")
        users.append(User(name))
            
    return topic, difficulty, amount, users


# The main quiz function
def quiz(questions, player_number, users):
    os.system(clear_screen)
    print(f"Player {player_number+1}/{len(users)}, {users[player_number].name}")
    input(f"Press enter to start the game...")

    # start the quiz
    for i, question in enumerate(questions):
        os.system(clear_screen)
        box_print(f"Question {i+1}/{len(questions)}\n{question.question}")
        
        correct_answer_position = randint(0, len(question.all_answers)-1)
        
        answers = question.incorrect_answers.copy()
        answers.insert(correct_answer_position, question.correct_answer)

        answers_to_print = []
        answers_list = []
        for i, answer in enumerate(answers):
            answers_to_print.append(f"{i+1}. {answer}")
            answers_list.append(answer)
            if i == 3: 
                break
            else:
                answers_to_print[-1] += "\n"

        box_print("".join(answers_to_print))

        answer = verify_input(input("Enter the number of your answer: "), 1, len(question.all_answers))

        if correct_answer_position+1 == answer:
            users[player_number].add_score(1)
            print(bcolors.OKGREEN + "\nCorrect!" + bcolors.ENDC)
        else:
            print(bcolors.FAIL + "\nIncorrect!" + f"\nThe correct answer was {question.correct_answer}." + bcolors.ENDC)


        users[player_number].add_answer({"question": question.question, "correct_answer": question.correct_answer, "user_answer": answers_list[answer-1], "correct": correct_answer_position+1 == answer})
        # print(question.correct_answer, str(answers_list))
        input("\nPress enter to continue...")


# This function prints the final results
def final_results(users, questions):
    os.system(clear_screen)
    print("Final results:")
    # sort the users by score
    users.sort(key=lambda x: x.score, reverse=True)

    for i, user in enumerate(users):
        answer_string = "["
        for j, question in enumerate(user.answers):
            if question["correct"]:
                answer_string += bcolors.OKGREEN + "•" + bcolors.ENDC
            else:
                answer_string += bcolors.FAIL + "•" + bcolors.ENDC
            if j == len(user.answers)-1:
                answer_string += "]"

        leaderboard_string = (f"{i+1}. {user.name}: {user.score}/{len(questions)} " + bcolors.ENDC)
        if(len(leaderboard_string) + len(questions) + 3 <= os.get_terminal_size().columns):
            leaderboard_string += answer_string

        print(leaderboard_string)


    input("\nPress enter to continue...")
    


# Welcome message
def welcome():
    os.system(clear_screen)
    # print welcome text if the console is big enough
    terminal_size = os.get_terminal_size()
    if terminal_size.columns >= 44:
        print(welcome_text)

     # ask the user if they want to play a quiz or view previous quizzes
    print("\nWelcome to the quiz!\nSelect an option:\n")
    print("1. Play a quiz")
    print("2. View previous quiz")
    print("3. Exit")

    # get the user's choice
    choice = verify_input(input("\nEnter the number of your choice: "), 1, 3)
    return choice
    

# Store previous quiz in a json file
def store_quiz(questions, users):
    # create a dictionary with all the questions and answers
    quiz = {}
    for i, question in enumerate(questions):
        quiz[i] = {"question": question.question, "correct_answer": question.correct_answer, "incorrect_answers": question.incorrect_answers}

    # create a dictionary with all the users and their answers
    users_answers = {}
    for i, user in enumerate(users):
        users_answers[i] = {"name": user.name, "answers": user.answers}

    # create a dictionary with the quiz and the users
    quiz_dict = {"quiz": quiz, "users": users_answers}

    # write the dictionary to a json file
    with open("quiz.json", "w") as file:
        json.dump(quiz_dict, file, indent=4)


# View previous quiz
def view_previous_quiz():

    # check if file exists
    if not os.path.exists("quiz.json") or os.stat("quiz.json").st_size == 0 :
        print("No previous quiz found.")
        input("\nPress enter to continue...")
        return
    
    # check if user answers exist
    with open("quiz.json", "r") as file:
        quiz_dict = json.load(file)
    if "users" not in quiz_dict:
        print("No previous quiz found.")
        input("\nPress enter to continue...")
        return

    # open the json file
    with open("quiz.json", "r") as file:
        quiz_dict = json.load(file)

    # get the quiz and the users
    quiz = quiz_dict["quiz"]
    users = quiz_dict["users"]

    # print the users
    for i, user in users.items():
        for j, answer in enumerate(user["answers"]):
            os.system(clear_screen)

            # count the amount of correct answers
            correct_answers = 0
            for k in user["answers"]:
                if k["correct"]:
                    correct_answers += 1
            total_questions = len(user["answers"])

            box_print(f"Name: {user['name']}\nScore: {correct_answers}/{total_questions}\nPress enter view next question.")

            print(f"{bcolors.BOLD}Question {j+1}: {answer['question']}{bcolors.ENDC}")
            if(answer["correct"]):
                print(bcolors.OKGREEN + "User answer: " + str({answer['user_answer']})[2:-2] + bcolors.ENDC)
            else:
                print(bcolors.FAIL + "User answer: " + str({answer['user_answer']})[2:-2] + bcolors.ENDC)
                print(f"{bcolors.OKCYAN}Correct answer: {answer['correct_answer']}{bcolors.ENDC}")
            
            input("\n")


# This is the main function
def main():

    # get the options
    topic, difficulty, amount, users = get_options()

    # get the questions and put them in a list of Question objects
    questions = get_questions(topics[topic], difficulties[difficulty-1], amount)

    # start the game
    print(f"Starting the game with {len(users)} players...")
    sleep(1)

    # start the quiz
    for i, user in enumerate(users):
        quiz(questions=questions, player_number=i, users=users)

    # print the final results
    final_results(users, questions)

    # store the quiz
    store_quiz(questions, users)


# =================== MAIN ===================
if __name__ == "__main__":
    while True:

        # welcome the user
        choice = welcome()

        # if the user wants to play a quiz
        if choice == 1:
            main()

        # if the user wants to view previous quizzes
        if choice == 2:
            view_previous_quiz()
        
        # if the user wants to exit
        if choice == 3:
            sys.exit()