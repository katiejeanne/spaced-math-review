import src.math_class as math_class

def print_menu():
    print()
    print("Enter option to proceed. \n"
          "1 - Print exercises due today\n"
          "2 - Add next exercise to rotation\n"
          "3 - Generate worksheet\n"
          "4 - Mark today's reviews as done\n"
          "5 - Print status of all exercises\n"
          "6 - Add new exercise to class\n"
          "q - Quit\n")

current_class = math_class.MathClass()

print_menu()
menu_choice = input()
while menu_choice != 'q':
    if menu_choice == '1':
        # Prints only exercises due today
        pass
    elif menu_choice == '2':
        # Adds the next exercise to rotation by setting due date as today
        pass
    elif menu_choice == '3':
        # Generates worksheet
        pass
    elif menu_choice == '4':
        # Updates all exercises due today as done today and advances them to the next stage
        pass
    elif menu_choice == '5':
        current_class.print_all_exercises()

    elif menu_choice == '6':
        #Add new exercise to class
        exercise_id = input("Enter exercise number\n")
        name = input("Enter exercise name\n")
        web_link = input("Enter web link to exercises\n")
        current_class.add_exercise(exercise_id, name, web_link)
        print(f"Exercise {exercise_id} added to current class\n")
    elif menu_choice == 'm':
        #Reprints the menu
        print_menu()
    else:
        print("Input not valid")
        print_menu()
    menu_choice = input("Enter next option or q to quit. Enter m for menu.")

