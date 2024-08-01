from datetime import datetime
import os

def login():
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        with open("user.txt", "r") as users_file:
            for line in users_file:
                stored_username, stored_password = line.strip().split(", ")
                if username == stored_username and password == stored_password:
                    print("")
                    print("--Successful Login--\n")
                    return username
                    
        print("Invalid username or password. Please try again.")

def reg_user():
    username = input("Enter username: ")
    
    # Check if the username already exists in user.txt
    with open("user.txt", "r") as file:
        existing_usernames = [line.split(", ")[0] for line in file.readlines()]

    if username in existing_usernames:
        print("Error: Username already exists. Please choose a different username.")
        reg_user()  # Recursively call reg_user to allow the user to try again
        return
    else:
        password = input("Enter password: ")

        # Add the new user to user.txt
        with open("user.txt", "a") as file:
            file.write(f"{username}, {password}\n")

        print("User registered successfully.\n")

def add_task():
    task_title = input("Enter task title: ")
    user_assigned = input("Enter username of the user assigned to this task: ")
    date_assigned = input("Enter date assigned (YYYY-MM-DD): ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    task_description = input("Enter task description: ")
       
    # Append the new task to tasks.txt
    with open("tasks.txt", "a") as file:
        file.write(f"ID: {get_next_task_id()}\n")
        file.write(f"Task title: {task_title}\n")
        file.write(f"User assigned to: {user_assigned}\n") 
        file.write(f"Date assigned: {date_assigned}\n")
        file.write(f"Due Date: {due_date}\n")
        file.write("Completed: No\n\n")
        file.write(f"Description: {task_description}\n\n")       
        
    print("Task added successfully.\n")

def get_next_task_id():
    try:
        with open("tasks.txt", "r") as file:
            lines = file.readlines()
            if not lines:
                return 1
            # Find the index of the first empty line to determine the number of lines per task
            # Find the last task ID in the file
            last_task_line = lines[-9]  # Assuming each task has 8 lines
            last_task_id = int(last_task_line.split(":")[1].strip())
            return last_task_id + 1  # Return the next task ID
    except (FileNotFoundError, IndexError, ValueError):
        return 1  # If file doesn't exist or format is invalid, return 1 as the next task ID

def view_all():
    try:
        with open("tasks.txt", "r") as file:
            tasks = file.readlines()
            if not tasks:
                print("No tasks found.\n")
                return

            print("All Tasks:")
            print("-----------")
            for i in range(0, len(tasks), 9):  # Assuming each task has 8 lines
                for line in tasks[i:i+9]:
                    print(line.strip())
                
    except FileNotFoundError:
        print("No tasks found.\n")

def view_mine(username):
    try:
        counter = 1
        start = 9999
        end = 0
        array = []
        tasks = "tasks.txt"
        singleTask = []

        with open(tasks, "r+") as fp:
            allTasks = fp.readlines()
            for position, line in enumerate(allTasks):
                if line.startswith("User assigned to: " + username): # if the line User assigned to starts with the input username when logging in, the relevant user's tasks are shown
                    start = position 
                    end = start + 5 # the position of the beginning and end of line is determined using indexing for each task
                if start != 9999:
                    for position, line in enumerate(allTasks):
                        noLines = line.strip("\n")                    
                        if position >= start -2 and position <= end:
                            array.append(noLines)
                    array.append("")
                start = 9999
            
            if array:
                print("Your Tasks:")
                print("-----------")
                for getData in array:
                    print(getData)
                
                print("-----------\n")
            else:
                print("No tasks assigned to you.\n")
                return False

            option = input("Enter the ID of the task to mark as complete or edit (-1 to return): ")
            if option == '-1':
                return False

            for position, line in enumerate(array):            
                if line.startswith("ID: " + option): # if the line ID starts with the input number choice the task with the relevant number is displayed           
                    start = position
                    end = start + 8
                if start != 9999:
                    for position, line in enumerate(array):
                        lineCheck = line.strip("\n")
                        if position >= start and position <= end:
                            singleTask.append(lineCheck)
                start = 9999
            
            print("\n-Task Chosen-")
            print("-----------") # used to create a seperation line
            for getSingleTaskData in singleTask:
                print(getSingleTaskData)

            print("-----------")

            isComplete = False
            completeArray = []
            tasksGet = allTasks 
            for i in tasksGet:
                completeArray.append(i)
            for position, line in enumerate(completeArray):
                    if line.startswith("ID: " + option):
                        start = position
                        end = start + 5
                    if start != 9999:
                        for position, line in enumerate(completeArray):
                            noLines = line.strip("\n")
                            if position == end:
                                if completeArray[end] == "Completed: Yes \n": # if the task is complete, the loop ends, if not then more options are displayed below
                                    isComplete = True
    
            for get in singleTask:            
                completeArray = []
            tasksGet = allTasks 
            for i in tasksGet:
                completeArray.append(i)
            
            if isComplete == True:
                print("This task is already marked as completed.\n")
            elif isComplete == False: # if the task is not complete
                choice = input("\nDo you want to mark this task as complete (Y/N)? ").strip().lower() # the user is allowed to change if the task is complete adn the relevant line is replaced to yes
                            
                if choice == "y":
                    isComplete = True 
                    for position, line in enumerate(completeArray):
                        if line.startswith("ID: " + option):
                            start = position
                            end = start + 5
                        if start != 9999:
                            for position, line in enumerate(completeArray):
                                noLines = line.strip("\n")
                                if position == end:
                                    completeArray[end] = "Completed: Yes \n"
                    fp.close()
                    with open(tasks, 'w') as filetowrite:
                        filetowrite.writelines(completeArray)
                    print("\nTask marked as complete.\n")

            if isComplete == False:
                for position, line in enumerate(completeArray):
                        if line.startswith("ID: " + option):
                            endNamePos = position + 2
                            endDueDatePos = endNamePos + 2
                choiceEdit = input("\nDo you want to edit the username (Y/N)? ").strip().lower() # the user is allowed to edit the name of the user on task if it is not complete
                if choiceEdit == "y":
                    editName = input("Enter new username: ").strip()
                    for position, line in enumerate(completeArray):
                        if position == endNamePos:
                            completeArray[endNamePos] = "User assigned to: " + editName + "\n" # the new username is replaced onto the User assigned to line
                            print("\nTask username updated.\n")
                elif choiceEdit =="n":
                    choiceEdit = input("\nDo you want to edit the due date (Y/N)? ").strip().lower() # the Due date is allowed to be changed
                    if choiceEdit == "y":
                        editDate = input("Enter new due date: ").strip()
                        for position, line in enumerate(completeArray):
                            if position == endDueDatePos:
                                completeArray[endDueDatePos] = "Due Date: " + editDate + "\n" # the Due date line is replaced with the new Due date
                                print("\nTask due date updated.\n")
                    elif choiceEdit =="n":
                        print("\nReturning to main menu.\n")
                fp.close()
                with open(tasks, 'w') as writeFile:
                    writeFile.writelines(completeArray)
                    writeFile.close()                               

    except FileNotFoundError:
        print("No tasks found.\n")
        return False

def generate_reports():
    try:
        # Read tasks from file
        with open("tasks.txt", "r") as file:
            tasks = file.readlines()

        # Count total tasks
        total_tasks = len(tasks) // 9  # Assuming each task has 9 lines

        # Count completed tasks
        completed_tasks = sum(1 for i in range(0, len(tasks), 9) if tasks[i+5].strip() == "Completed: Yes")

        # Count uncompleted tasks
        uncompleted_tasks = total_tasks - completed_tasks

        # Count overdue tasks
        current_date = datetime.now().date()
        overdue_tasks = sum(1 for i in range(0, len(tasks), 9) if datetime.strptime(tasks[i+3].split(": ")[1].strip(), "%Y-%m-%d").date() < current_date and tasks[i+5].strip() == "Completed: No")

        # Calculate percentages
        incomplete_percent = (uncompleted_tasks / total_tasks) * 100
        overdue_percent = (overdue_tasks / total_tasks) * 100

        # Write task overview to file
        with open("task_overview.txt", "w") as file:
            file.write(f"Total number of tasks: {total_tasks}\n")
            file.write(f"Total number of completed tasks: {completed_tasks}\n")
            file.write(f"Total number of uncompleted tasks: {uncompleted_tasks}\n")
            file.write(f"Total number of tasks overdue: {overdue_tasks}\n")
            file.write(f"Percentage of tasks that are incomplete: {round(incomplete_percent)}%\n")
            file.write(f"Percentage of tasks that are overdue: {round(overdue_percent)}%\n")

        # Read users from file
        with open("user.txt", "r") as file:
            users = file.readlines()

        # Count total users
        total_users = len(users)

        # Write user overview to file
        with open("user_overview.txt", "w") as file:
            file.write(f"Total number of users registered: {total_users}\n")
            file.write(f"Total number of tasks: {total_tasks}\n")
            for user_line in users:
                user = user_line.split(',')[0].strip()
                user_tasks = sum(1 for i in range(0, len(tasks), 9) if tasks[i+2].strip() == f"User assigned to: {user}")
                user_completed_tasks = sum(1 for i in range(0, len(tasks), 9) if tasks[i+2].strip() == f"User assigned to: {user}" and tasks[i+5].strip() == "Completed: Yes")
                user_incomplete_tasks = user_tasks - user_completed_tasks
                user_overdue_tasks = sum(1 for i in range(0, len(tasks), 9) if tasks[i+2].strip() == f"User assigned to: {user}" and datetime.strptime(tasks[i+3].split(": ")[1].strip(), "%Y-%m-%d").date() < current_date and tasks[i+5].strip() == "Completed: No")
                user_tasks_percent = (user_tasks / total_tasks) * 100 if total_tasks > 0 else 0
                user_completed_percent = (user_completed_tasks / user_tasks) * 100 if user_tasks > 0 else 0
                user_incomplete_percent = (user_incomplete_tasks / user_tasks) * 100 if user_tasks > 0 else 0
                user_overdue_percent = (user_overdue_tasks / user_tasks) * 100 if user_tasks > 0 else 0
                file.write(f"\nUser: {user}\n")
                file.write(f"Total number of tasks assigned: {user_tasks}\n")
                file.write(f"Percentage of total tasks assigned: {user_tasks_percent:.0f}%\n")
                file.write(f"Percentage of completed tasks: {user_completed_percent:.0f}%\n")
                file.write(f"Percentage of incomplete tasks: {user_incomplete_percent:.0f}%\n")
                file.write(f"Percentage of overdue tasks: {user_overdue_percent:.0f}%\n")

        print("Reports generated successfully.\n")

    except FileNotFoundError:
        print("Error: Task file or user file not found.")

def main_menu(is_admin):
    print("Please select one of the following options:\n")
    print("a - add task")
    print("va - view all tasks")
    print("vm - view my tasks")
    if is_admin:
        print("r - register user")
        print("gr - generate reports")
        print("ds - display statistics")
    print("e - exit\n")

def run():
    logged_in_user = login()  # Get the username of the logged-in user
    is_admin = logged_in_user == "admin"  # Check if the logged-in user is the admin
    
    while True:
        main_menu(is_admin)  # Pass the admin status to the main_menu function
        choice = input("Enter your choice: ")
        
        if choice == "r" and is_admin:
            print("")
            reg_user()
        elif choice == "a":
            print("")
            add_task()
        elif choice == "va":
            print("")
            view_all()
        elif choice == "vm":
            print("")
            view_mine(logged_in_user)
        elif choice == "gr" and is_admin:
            print("")
            generate_reports()
        elif choice == "ds" and is_admin:
            print("")
            display_statistics()
        elif choice == "e":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def display_statistics():
    # Check if the reports exist, if not, generate them first
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_reports()

    # Read and display task overview
    with open("task_overview.txt", "r") as task_file:
        print("Task Overview:")
        print(task_file.read())

    # Read and display user overview
    with open("user_overview.txt", "r") as user_file:
        print("User Overview:")
        print(user_file.read())

if __name__ == "__main__":
    run()
