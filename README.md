## Task Tracker CLI

A simple command-line interface (CLI) application to track tasks you need to do, tasks in progress, and completed tasks.
This project stores tasks locally using a JSON file and is designed as a learning project for practicing Python fundamentals.

## ✨ Features

Add new tasks

Update task descriptions

Mark tasks as:

todo

in-progress

done

Delete tasks

List all tasks or filter them by status

Persistent storage using JSON files

## 🛠 Requirements

Python 3.10 or higher

No external libraries required

## ▶️ How to Run

Clone the repository and navigate into the project folder:

git clone https://github.com/samueleduardoPL/task-tracker-cli.git
cd task-tracker-cli


Run the program using Python:

python task.py <command> [arguments]

## 📖 Available Commands
Add a task
python task.py add "Buy groceries"

Update a task description
python task.py update 1 "Buy groceries and cook dinner"

Delete a task
python task.py delete 1

Mark task status
python task.py mark-in-progress 1
python task.py mark-done 1
python task.py mark-todo 1

List tasks
python task.py list
python task.py list todo
python task.py list in-progress
python task.py list done

## 💾 Data Storage

Tasks are stored in task.json.
Task IDs are persisted across executions using idFile.json.

Both files are created automatically if they do not exist.

## 🎯 Purpose of This Project

This project was built as a learning exercise to practice:

Python basics

File handling

JSON serialization

Command-line arguments

Error handling

Code documentation and comments

The goal is to show progress and understanding rather than perfection.

## 👤 Author

Samuel Eduardo Polanco Lithgow

