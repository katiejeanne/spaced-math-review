import src.math_class as math_class
import sqlite3

def get_classes(db_path='spaced-math-review.db'):
    #Fetches all classes from the database and returns them as a list of tuples.
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS classes (
                            class_id INTEGER PRIMARY KEY,
                            class_name TEXT NOT NULL)''')

        cursor.execute("SELECT class_id, class_name FROM classes ORDER BY class_id")
        classes = cursor.fetchall()
    return classes


def create_new_class(class_name, db_path='spaced-math-review.db'):
    #Creates a new class
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO classes (class_name) VALUES (?)", (class_name,))
        new_class_id = cursor.lastrowid
    print(f"New class '{class_name}' created successfully with ID {new_class_id}.")
    return new_class_id, class_name  # Return both ID and name


def print_menu():
    #Prints the main selection menu
    print()
    print("Enter option to proceed. \n"
        "1 - Print exercises due today\n"
        "2 - Add next exercise to rotation\n"
        "3 - Generate worksheet\n"
        "4 - Mark reviews as done\n"
        "5 - Print status of all exercises\n"
        "6 - Add new exercise to class\n"
        "7 - Delete exercise\n"
        "q - Quit\n")

if __name__ == "__main__":

    #Announce program and prompt to choose class.
    print("\n*****************************\n"
        "Welcome to Spaced Math Review!\n"
        "Start by choosing a class.\n")


    classes = get_classes()

    #Print currently available classes.
    if classes:
        print("Available classes:")
        for class_id, class_name in classes:
            print(f"{class_id}: {class_name}")
        # Further logic to select a class or create a new one
    else:
        print("No classes available.")
        # Logic to create a new class

    #Save class ids as a list to facilitate comparing with input.
    class_ids = [str(class_id) for class_id, _ in classes]  # Convert class IDs to strings for comparison

    #Allow users to choose a class by typing class ID or to create a new class.
    while True:
        class_choice = input("Choose class by entering class number. Or, type 'n' for a new class: ").strip()

        if class_choice in class_ids:
            selected_class_id = int(class_choice)  # Convert back to int as IDs in the database are likely integers
            selected_class_name = next(name for cid, name in classes if cid == selected_class_id)
            print(f"You selected: {selected_class_name}")
            break

        elif class_choice.lower() == "n":
            class_name = input("Enter the name of the new class: ")
            selected_class_id, selected_class_name = create_new_class(class_name)  # Assuming this function returns the new class ID
            break

        else:
            print("Invalid choice. Please try again.")


    #Load the class as a MathClass object
    current_class = math_class.MathClass(selected_class_id, selected_class_name)

    #Load exercises from the database
    current_class.load_exercises_from_database()


    #Main user menu
    print_menu()
    menu_choice = input()
    while menu_choice != 'q':
        if menu_choice == '1':
            # Prints only exercises due today
            current_class.print_due_exercises()
        elif menu_choice == '2':
            # Adds the next exercise to rotation by setting due date as today
            current_class.start_next_exercise()
        elif menu_choice == '3':
            # Generates worksheet
            pass
        elif menu_choice == '4':
            # Updates all exercises due before review date and advances them to the next stage
            current_class.mark_reviews_done()
        elif menu_choice == '5':
            #Print info for all exercises
            current_class.print_all_exercises()
        elif menu_choice == '6':
            #Add new exercise to class
            current_class.add_exercises_until_done_then_save()
        elif menu_choice == '7':
            #Delete an exercise
            current_class.delete_exercise()
        elif menu_choice == 'm':
            #Reprints the menu
            print_menu()
        else:
            print("Input not valid")
            print_menu()
        menu_choice = input("\nEnter next option or q to quit. Enter m for menu.")

