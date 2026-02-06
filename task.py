"""
Task Tracker CLI
Author: Samuel Eduardo Polanco Lithgow
Description:
A command-line application to manage tasks using a JSON file for persistence.
"""


import json
import datetime
import sys
from pathlib import Path



class Task:
    """
    Represents a task in the task tracker
    Handles task creation and serialization to JSON

    """
    def __init__(self, description, status="todo"):
        self.id = idgenerator()
        self.description = description
        self.status = status
        self.createdAt = datetime.datetime.now()
        self.updatedAt = datetime.datetime.now()

    def add(self, taskfile):
        """
        Adds a new Task to the JSON file used for storage. Creates the file if it does not exists

        Args:
            taskfile (str): Path to the JSON file used for task storage.
        """
        file = Path(taskfile)

        # Avoid loading an empty JSON file which would raise JSONDecodeError
        if file.exists() and file.stat().st_size > 0:
            try:
                with open(taskfile, "r") as a:
                    tasklist = json.load(a)
                    tasklist.append({"id" : self.id, "description" : self.description, "status" : self.status, "createdAt" : self.createdAt.isoformat(), "updatedAt" : self.updatedAt.isoformat()})
                
                with open(taskfile, "w") as f:
                    json.dump(tasklist, f, indent=2)
                    print(f"task added succesfully (ID: {self.id})")


            except json.decoder.JSONDecodeError:
                print("There was an error while reading the json file")
            except TypeError:
                print("TypeError: may be that object of type datetime is not JSON serializable. Use isoformat()")

        # File does not exist or is empty → initialize storage
        else:
            with open(taskfile, "w") as f:
                thistask = [{"id" : self.id, "description" : self.description, "status" : self.status, "createdAt" : self.createdAt.isoformat(), "updatedAt" : self.updatedAt.isoformat()}]
                json.dump(thistask, f, indent=2)
                print(f"task added succesfully (ID: {self.id})")




        


def update(taskfile, task_id, field, new_value):
        """
        Update a task field (description or status) by task ID.

        Args:
            taskfile (str): Path to task storage file
            task_id (int): Id of the task to update
            field(str): Name of the field to update. must be the same name of the field in the JSON file
            new_value(str): Description or status to update.
        """
        file = Path(taskfile)

        # Avoid loading an empty JSON file which would raise JSONDecodeError
        if file.exists() and file.stat().st_size > 0:
            try: 
                with open(taskfile) as f:
                    uplist = json.load(f)
                    for i in uplist:
                        if i["id"] == task_id:
                            i[field] = new_value
                            i["updatedAt"] = datetime.datetime.now().isoformat()
                            if field == "description":
                                print(f"Task with the id {i['id']} was updated succesfully")
                            else:
                                print(f"Task with the id {i['id']} was marked succesfully as {new_value}")
                            # Stop after updating the matching task to avoid unnecessary iteration
                            break
                    else:
                        print("Could not find the task. Check the given id")

                with open(taskfile, "w") as f:
                    json.dump(uplist, f, indent=2)

            except json.decoder.JSONDecodeError:
                print("There was an error while reading the json file")
           
        else:
            print("There's no file to update")

def delete(taskfile, task_id):
    """
    Delete a task by its ID

    Args:
        taskfile (str): Path to the JSON file used for task storage
        task_id (int): ID of the task to delete
    """
    file = Path(taskfile)
    # Avoid loading an empty JSON file which would raise JSONDecodeError
    if file.exists() and file.stat().st_size > 0:
        try: 
            with open(taskfile) as f:
                delist = json.load(f)
                for index, task in enumerate(delist):
                    if task["id"] == task_id:
                        delist.pop(index)
                        print(f"successfully deleted the task with the id {task_id}")
                        # Stop after deleting the task to avoid unnecessary iteration
                        break
                else:
                    print("Could not find the task to delete. Check the given id")

        
            with open(taskfile, "w") as f:
                json.dump(delist, f, indent=2)

        except json.decoder.JSONDecodeError:
                print("There was an error while reading the JSON file")

    else:
        print("could not find the given file")




def list(taskfile,status):
    """
    Print all task to the CLI. Can filter on the basis of task status

    Args:
        taskfile (str): Path to the JSON file used for task storage
        status (str | None): Status to filter by (e.g., "todo", "done", "in-progress").
    """
    file = Path(taskfile)
    # Avoid loading an empty JSON file which would raise JSONDecodeError
    if file.exists() and file.stat().st_size > 0:
        try:
            with open(taskfile) as f:
                alltasks = json.load(f)
            if status:
                istask = False
                for i in alltasks:
                    if i["status"] == status:
                        istask = True
                        print(f"(ID:{i['id']})'{i['description']}' - - -({i["status"]})")
                else:
                    if not istask:
                        print(f"there are no tasks marked as {status}")
                    
            else:
                for i in alltasks:
                    print(f"(ID:{i['id']})'{i['description']}' - - -({i["status"]})")
        except json.decoder.JSONDecodeError:
            print("there was an error while reading the file")
    else:
        print("could not find the given file")
    
                


def idgenerator():
    """
    Generates a JSON file to store the current ID. Returns the current ID

    """

    # Use a separate file to persist task IDs between executions
    idFile = Path("idFile.json")

    if idFile.exists() and idFile.stat().st_size > 0:
        with open("idFile.json") as f:
            data = json.load(f)

        data["currentID"] += 1

        with open("idFile.json", "w") as f:
            json.dump(data, f)
        
        return data["currentID"]

    else:
        data = {"currentID" : 1}
        with open("idFile.json", "w") as f:
            json.dump(data, f)
        
        return data["currentID"]
    

"""
CLI entry point / command dispatcher.

Reads positional arguments from sys.argv and routes to the appropiate command.
Each command validates requered arguments and prints firendly errors on bad input
"""

try:
    # sys.argv[1] should be the command name: add, update, delete, list, etc.
    match sys.argv[1]:
        case "add":
            try:
                # sys.argv[2] = task description
                x = Task(sys.argv[2])
                x.add("task.json")
            except IndexError:
                print("Error: Missing a valid description")


        case "update":
            try:
                # Expected: update <id> <new_description>
                update("task.json", int(sys.argv[2]),"description", sys.argv[3])
            except IndexError:
                print("Error: Missing a valid id and description")
            except ValueError:
                print('Error: Missing a valid id or description. The correct order is {command} {id} {"description"}')

        case "delete":
            try:
                # Expected: delete <id>
                delete("task.json", int(sys.argv[2]))
            except ValueError:
                print("Error: Input a valid ID")
            except IndexError:
                print("Error: Input a valid ID")


        case "mark-in-progress":
            try:
                 # Expected: mark-in-progress <id>
                update("task.json", int(sys.argv[2]),"status", "in-progress")
            except ValueError:
                print("Error: Input a valid ID")
            except IndexError:
                print("Error: Input a valid ID")
                


        case "mark-done":
            try:
                # Expected: mark-done <id>
                update("task.json", int(sys.argv[2]),"status", "done")
            except ValueError:
                print("Error: Input a valid ID")
            except IndexError:
                print("Error: Input a valid ID")

        case "mark-todo":
            try:
                 # Expected: mark-todo <id>
                update("task.json", int(sys.argv[2]),"status", "todo")
            except ValueError:
                print("Error: Input a valid ID")
            except IndexError:
                print("Error: Input a valid ID")

        case "list":
                # list OR list <status>
                if len(sys.argv) > 2:
                     # sys.argv[2] is an optional filter
                    if sys.argv[2] == "done":
                        list("task.json", "done")
                    elif sys.argv[2] == "todo":
                        list("task.json", "todo")
                    elif sys.argv[2] == "in-progress":
                        list("task.json", "in-progress")
                    else:
                        print("Input a valid status to list")
                else:
                     # No filter: list all tasks
                    list("task.json", None)
            
        case _:
            # Unknown command
            print("Input a valid command")

except IndexError:
    # Happens when sys.argv[1] doesn't exist (user ran: python task.py with no args)
    print("Error: No input")







