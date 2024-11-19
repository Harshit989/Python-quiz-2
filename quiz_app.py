import random
import json
import os

# File paths
QUIZ_FILE = "quiz_questions.json"
USERS_FILE = "users_db.json"

# Ensure files exist
if not os.path.exists(QUIZ_FILE):
    with open(QUIZ_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

# Load data from files
def load_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# Function to register a student
def register_student():
    users_db = load_data(USERS_FILE)
    print("\n--- Registration ---")
    name = input("Enter your name: ")
    reg_id = input("Create a registration ID: ")
    password = input("Create a password: ")

    if reg_id in users_db:
        print("Registration ID already exists. Please try again.")
        return register_student()

    users_db[reg_id] = {"name": name, "password": password, "attempted_quizzes": {}}
    save_data(USERS_FILE, users_db)
    print(f"Registration successful. Your registration ID is {reg_id}.")

# Function to log in a student
def login_student():
    users_db = load_data(USERS_FILE)
    print("\n--- Login ---")
    reg_id = input("Enter your registration ID: ")
    password = input("Enter your password: ")

    if reg_id in users_db and users_db[reg_id]["password"] == password:
        print(f"Login successful. Welcome, {users_db[reg_id]['name']}!")
        return reg_id
    else:
        print("Invalid registration ID or password. Please try again.")
        return login_student()

# Function to take a quiz
def take_quiz(subject, reg_id):
    quiz_questions = load_data(QUIZ_FILE)
    users_db = load_data(USERS_FILE)
    questions = quiz_questions[subject]
    already_attempted = users_db[reg_id]["attempted_quizzes"].get(subject, [])

    # Get 5 random questions
    while True:
        selected_questions = random.sample(questions, 5)
        if selected_questions != already_attempted:
            break

    print(f"\n--- {subject} Quiz ---")
    score = 0

    for i, (question, options, answer) in enumerate(selected_questions, 1):
        print(f"Q{i}: {question}")
        for option in options:
            print(option)
        user_answer = input("Your answer (A/B/C/D): ").strip().upper()
        if user_answer == answer:
            score += 1

    # Store the attempted questions for reattempt prevention
    users_db[reg_id]["attempted_quizzes"][subject] = selected_questions
    save_data(USERS_FILE, users_db)

    print(f"\nYou scored {score}/5 in the {subject} quiz.")
    return score

# Function to choose a subject
def choose_subject():
    print("\n--- Choose Subject ---")
    print("1. Operating System")
    print("2. Database Management System")
    print("3. Computer Network")
    subject_choice = input("Enter your choice (1/2/3): ")

    if subject_choice == "1":
        return "Operating System"
    elif subject_choice == "2":
        return "Database Management System"
    elif subject_choice == "3":
        return "Computer Network"
    else:
        print("Invalid choice. Please try again.")
        return choose_subject()

# Main function to handle registration, login, and quiz
def main():
    while True:
        print("\n--- Welcome to the Quiz Application ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            register_student()
        elif choice == "2":
            reg_id = login_student()
            while True:
                subject = choose_subject()
                take_quiz(subject, reg_id)
                reattempt = input("Do you want to reattempt the quiz? (yes/no): ").strip().lower()
                if reattempt != "yes":
                    break
        elif choice == "3":
            print("Thank you for using the Quiz Application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
