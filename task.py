import json
import datetime
import sys
from pathlib import Path



class Task:
    def __init__(self, description, status="todo"):
        self.id = idgenerator()
        self.description = description
        self.status = status
        self.createdAt = datetime.datetime.now()
        self.updatedAt = datetime.datetime.now()

    def add(self, taskfile):
        file = Path(taskfile)

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

        else:
            with open(taskfile, "w") as f:
                thistask = [{"id" : self.id, "description" : self.description, "status" : self.status, "createdAt" : self.createdAt.isoformat(), "updatedAt" : self.updatedAt.isoformat()}]
                json.dump(thistask, f, indent=2)
                print(f"task added succesfully (ID: {self.id})")




        


def update(taskfile, id, field, new):
        file = Path(taskfile)

        if file.exists() and file.stat().st_size > 0:
            try: 
                with open(taskfile) as f:
                    uplist = json.load(f)
                    for i in uplist:
                        if i["id"] == id:
                            i[field] = new
                            i["updatedAt"] = datetime.datetime.now().isoformat()
                            if field == "description":
                                print(f"Task with the id {i['id']} was updated succesfully")
                            else:
                                print(f"Task with the id {i['id']} was marked succesfully as {new}")
                            break
                    else:
                        print("Could not find the task. Check the given id")

                with open(taskfile, "w") as f:
                    json.dump(uplist, f, indent=2)

            except json.decoder.JSONDecodeError:
                print("There was an error while reading the json file")
           
        else:
            print("There's no file to update")

def delete(taskfile, id):
    file = Path(taskfile)

    if file.exists() and file.stat().st_size > 0:
        try: 
            with open(taskfile) as f:
                delist = json.load(f)
                for index, task in enumerate(delist):
                    if task["id"] == id:
                        delist.pop(index)
                        print(f"succesfully deleted the task with the id {id}")
                        break
                else:
                    print("Could not find the task to delete. Check the given id")

        
            with open(taskfile, "w") as f:
                json.dump(delist, f, indent=2)

        except json.decoder.JSONDecodeError:
                print("There was an error while reading the json file")

    else:
        print("could not find the given file")




def list(file,status):
    try:
        with open(file) as f:
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
                


def idgenerator():
    idFile = Path("idFile.json")

    if idFile.exists() and idFile.stat().st_size > 0:
        with open("idFile.json") as f:
            id = json.load(f)

        id["currentID"] += 1

        with open("idFile.json", "w") as f:
            json.dump(id, f)
        
        return id["currentID"]

    else:
        id = {"currentID" : 1}
        with open("idFile.json", "w") as f:
            json.dump(id, f)
        
        return id["currentID"]


try:
    match sys.argv[1]:
        case "add":
            try:
                x = Task(sys.argv[2])
                x.add("task.json")
            except IndexError:
                print("Error: Missing a valid description")


        case "update":
            try:
                update("task.json", int(sys.argv[2]),"description", sys.argv[3])
            except IndexError:
                print("Error: Missing a valid id and description")
            except ValueError:
                print('Error: Missing a valid id or description. The correct order is {command} {id} {"description"}')

        case "delete":
            try:
                int(sys.argv[2])
                delete("task.json", int(sys.argv[2]))
            except ValueError:
                print("Error: Input a valid ID")
            except IndexError:
                print("Error: Input a valid ID")


        case "mark-in-progress":
            try:
                update("task.json", int(sys.argv[2]),"status", "in-progress")
            except ValueError:
                print("Error: Input a valid ID")
            except IndexError:
                print("Error: Input a valid ID")
                


        case "mark-done":
            try:
                update("task.json", int(sys.argv[2]),"status", "done")
            except ValueError:
                print("Error: Input a valid ID")
            except IndexError:
                print("Error: Input a valid ID")

        case "mark-todo":
            try:
                update("task.json", int(sys.argv[2]),"status", "todo")
            except ValueError:
                print("Error: Input a valid ID")
            except IndexError:
                print("Error: Input a valid ID")

        case "list":
                if len(sys.argv) > 2:
                    if sys.argv[2] == "done":
                        list("task.json", "done")
                    elif sys.argv[2] == "todo":
                        list("task.json", "todo")
                    elif sys.argv[2] == "in-progress":
                        list("task.json", "in-progress")
                    else:
                        print("Input a valid status to list")
                else:
                    list("task.json", None)
            
        case _:
            print("Input a valid command")

except IndexError:
    print("Error: No input")







