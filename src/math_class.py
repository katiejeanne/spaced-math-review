import datetime
import sqlite3

class Exercise:
    # Class for saving all exercise information as an object. 
    def __init__(self, chapter, unit, number, name, web_link, class_id=0, current_stage=0, last_review_date=None, due_date=None) -> None:
        self.chapter = chapter
        self.unit = unit
        self.number = number
        self.name = name
        self.web_link = web_link
        self.class_id = class_id
        self.current_stage = current_stage
        self.last_review_date = self._return_date_or_none(last_review_date)
        self.due_date = self._return_date_or_none(due_date)
        
    
    def print_exercise(self):
        #Prints standard exercise info to screen. 
        #Truncates long names to fit into column
        #Does not print web link, class id because they aren't especially useful to the user and would clutter the display.
        exercise_id = self.get_exercise_id_string()
        print(f"{exercise_id:12}{self.name[:50]:50}{self.current_stage:<7}{self._return_datestring_or_nastring(self.last_review_date):12}{self._return_datestring_or_nastring(self.due_date):12}")

    def _return_date_or_none(self, date_string):
        #For classes not started date values will be null or None. This makes sure the right value is returned from the string.
        if not date_string:
            return None
        else:
            return self._date_string_to_object(date_string)
        

    def _date_string_to_object(self, date_string):
        #Takes what should be a date string and returns a datetime object. If not a valid datetime object, an error is raised.
        try: 
            return datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError(f"Invalid date format for {date_string}, expected format: YYYY-MM-DD") from e
    
    def _return_datestring_or_nastring(self, date):
        # Converts date object to string for printing. If no date value is assigned "n/a" is printed for the date.
        if not date:
            return "n/a"
        else:
            return date.strftime("%Y-%m-%d")
        
    def get_exercise_id_string(self):
        return f"{self.chapter}.{self.unit}.{self.number}"
    
    def advance_stage(self, review_date):
        self.current_stage += 1
        self.last_review_date = review_date
        if self.current_stage == 6:
            self.due_date = None
        else:
            due_date_modifier = self._get_due_date_modifier()
            self.due_date = review_date + datetime.timedelta(days=due_date_modifier)

    def _get_due_date_modifier(self):
        due_date_modifiers = {1:1, 2:3, 3:7, 4:14, 5:28}
        return due_date_modifiers[self.current_stage]
    
    def get_num_of_exercises(self):
        exercises_per_stage = {1:5, 2:3, 3:2, 4:1, 5:1}
        return exercises_per_stage[self.current_stage]
        

class MathClass:
    #Class for managing the class set of exercises.
    def __init__(self, class_id=0, class_name="Default") -> None:
        self.exercises = []
        self.class_id = class_id
        self.class_name = class_name

    def add_exercise(self, chapter, unit, number, name, web_link):
        #Creates a new exercise then adds it to the class.
        #Note that stage number and date values are assigned by the program, so only the ID, name, and web link are provided by the user.
        new_exercise = Exercise(chapter, unit, number, name, web_link, self.class_id)
        self.exercises.append(new_exercise)

    def print_all_exercises(self):
        #Prints all the exercises currently in the class. 
        
        if self.exercises:
            print(f'{"Number":12}{"Name":50}{"Stage":7}{"Last":12}{"Due":12}')
            for exercise in self.exercises:
                exercise.print_exercise()
        else:
            print("Class is empty. No exercises have been added. Type 6 to add exercises.")
    
    def print_due_exercises(self):
        #Prints only those exercises that are due or past due today. 
        due_exercises = self.get_due_exercises()
        if due_exercises:
            for exercise in due_exercises:
                exercise.print_exercise()
        else:
            print("No exercises due today")

    def get_due_exercises(self):
        #Creates a list of the exercises that are due or past due today.
        due_exercises = []
        today = datetime.datetime.today().date()
        for exercise in self.exercises:
            if exercise.due_date is None:
                continue

            if exercise.due_date <= today:
                due_exercises.append(exercise)

        return due_exercises

    def save_to_db(self, db_path='spaced-math-review.db'):
        #Saves current exercise data into the database
        try: 
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Ensure the table exists
            cursor.execute('''CREATE TABLE IF NOT EXISTS exercises (
                                chapter INTEGER,
                                unit INTEGER,
                                number INTEGER,
                                name TEXT,
                                web_link TEXT,
                                class_id INTEGER,
                                current_stage INTEGER,
                                last_review_date TEXT,
                                due_date TEXT,
                                PRIMARY KEY (chapter, unit, number, class_id),
                                FOREIGN KEY (class_id) REFERENCES classes(class_id))''')

            # Insert or update exercises in the database
            for exercise in self.exercises:
                cursor.execute('''INSERT OR REPLACE INTO exercises 
                                (chapter, unit, number, name, web_link, class_id, current_stage, last_review_date, due_date) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                            (exercise.chapter, exercise.unit, exercise.number, exercise.name, exercise.web_link, exercise.class_id, exercise.current_stage, 
                                exercise.last_review_date, exercise.due_date))

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            print(f"An error occurred while saving to the database: {e}")
        
        finally:
            if conn:
                conn.close()

    def prompt_and_add_exercise(self):
        #Prompts the user to input values for a single new exercise
        chapter = input("\nNOTE: Exercises will be scheduled in order of chapter, then unit, then number.\n"
                            "Enter chapter number. Must be an number.\n")
        chapter = self._user_input_to_int(chapter)

        unit = input("Enter unit number. Must be a number.\n")   
        unit = self._user_input_to_int(unit) 

        number = input("Enter number. Must be unique to chapter and unit.\n")
        number = self._user_input_to_int(number)
        number = self._verify_number_is_unique(chapter, unit, number)

        name = input("Enter exercise name\n")

        web_link = input("Enter web link to exercises\n")

        self.add_exercise(chapter, unit, number, name, web_link)

        exercise_id = f"{chapter}.{unit}.{number}"
        print(f"Exercise {exercise_id} added to current class\n")

    def _user_input_to_int(self, num):
        while not(num.isdigit()):
            num = input("Invalid. Please enter a number.")
        return int(num)

    def _verify_number_is_unique(self, chapter, unit, number):
        existing_exercise_numbers = self._get_list_of_existing_exercise_numbers_for_chapter_and_unit(chapter, unit)
        while number in existing_exercise_numbers:
            largest_num = max(existing_exercise_numbers)
            number = input(f"Number already exists. Please input new number. Largest existing number is {largest_num}.")
            number = self._user_input_to_int(number)
        return number
    
    def _get_list_of_existing_exercise_numbers_for_chapter_and_unit(self, chapter, unit):
        existing_exercise_numbers = []
        for exercise in self.exercises:
            if exercise.chapter == chapter and exercise.unit == unit:
                existing_exercise_numbers.append(exercise.number)
        return existing_exercise_numbers

    def add_exercises_until_done_then_save(self):
        #Allows user to continue adding exercises until they are finished then saves to the database when finished.
        menu_choice = "y"
        while menu_choice.lower() == "y":
            self.prompt_and_add_exercise()
            menu_choice = input('Add another? Type "y" to add another.')
        self.save_to_db()
        self.exercises.sort(key=lambda x: (x.chapter, x.unit, x.number)) #Sorts new values into exercise list

    def load_exercises_from_database(self, dbpath='spaced-math-review.db'):
        #Loads all the exercises for the chosen class from the database into the program.
        try: 
            conn = sqlite3.connect(dbpath)
            cursor = conn.cursor()

            query = "SELECT * FROM exercises WHERE class_id = ? ORDER BY chapter, unit, number"

            cursor.execute(query, (self.class_id,))

            exercises = cursor.fetchall()
           
            conn.close()
            
            for exercise in exercises:
                exercise_to_add = Exercise(*exercise)
                self.exercises.append(exercise_to_add)
                
        except sqlite3.OperationalError:
            # Silently handle the error if the 'exercises' table doesn't exist
            pass

        except sqlite3.Error as e:
            print(f"An error occurred while loading from the database: {e}")
        
        finally:
            if conn:
                conn.close()
    


    def delete_exercise(self):
        #Deletes an already existing exercise

        #Prompt for the number of the exercise to delete
        chapter = input("Enter the chapter, unit, and number of the exercise to delete.\n"
                        "Chapter:")
        chapter = self._user_input_to_int(chapter)
        unit = input("Unit:")
        unit = self._user_input_to_int(unit)
        number = input("Number:")
        number = self._user_input_to_int(number)

        #Verify that the exercise to delete is actually an exercise
        existing_exercises = self._get_list_of_existing_exercise_numbers_for_chapter_and_unit(chapter, unit)
        while number not in existing_exercises:
            number = input("Exercise number not found. Please enter again or type a to abort.")
            if number.lower() == "a":
                print("Delete exercise aborted.")
                return
            number = self._user_input_to_int(number)

        #Ask for confirmation before deleting
        exercise_id = f"{chapter}.{unit}.{number}"
        confirm = input(f"This will permanently delete exercise {exercise_id}. Do you wish to proceed? Type y to confirm.")    
        if confirm.lower() != "y":
            print("Delete exercise aborted.")
            return
        
        #Find the exercise's position in the exercise list
        for i in range(len(self.exercises)):
            if self.exercises[i].chapter == chapter and self.exercises[i].unit == unit and self.exercises[i].number == number:
                index = i

        #Delete the exercise first from the class then from the database
        del self.exercises[i]
        self.delete_exercise_from_db(chapter, unit, number)
        
            

    def delete_exercise_from_db(self, chapter, unit, number, dbpath='spaced-math-review.db'):
        #Deletes the specificed exercise from the database
        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()

        try:
            # Prepare and execute the DELETE statement
            cursor.execute("DELETE FROM exercises WHERE chapter = ? AND unit = ? AND number = ? AND class_id = ?", (chapter, unit, number, self.class_id))

            # Commit the changes
            conn.commit()
            exercise_id = f"{chapter}.{unit}.{number}"
            print(f"Exercise {exercise_id} has been deleted.")

        except sqlite3.Error as e:
            # Handle any database errors
            print(f"An error occurred: {e}")

        finally:
            # Ensure the connection is closed
            conn.close()

    def _find_next_stage_0_exercise(self):
        for i in range(len(self.exercises)):
            if self.exercises[i].current_stage == 0:
                return i
            
    def _find_number_of_stage_one_exercises(self):
        count = 0
        for exercise in self.exercises:
            if exercise.current_stage == 1:
                count += 1
        return count
    
    def _find_number_of_stage_zero_exercises(self):
        count = 0
        for exercise in self.exercises:
            if exercise.current_stage == 0:
                count += 1
        return count
            
    def start_next_exercise(self):
        #Takes the next exercise at stage 0 and sets the stage to 1 and the due date to today.
        
        #Check to make sure there are exercises to add
        num_stage0_exercises = self._find_number_of_stage_zero_exercises()
        if num_stage0_exercises == 0:
            print("No exercises available to add.")
            return


        #Gets information on the next exercise
        next_exercise_index = self._find_next_stage_0_exercise()
        next_exercise_id = self.exercises[next_exercise_index].get_exercise_id_string()
        next_exercise_name = self.exercises[next_exercise_index].name

        #Get number of exercises currently at stage 1 
        num_stage1_exercises = self._find_number_of_stage_one_exercises()

        #Confirm 
        print(f"\nExercise {next_exercise_id}: {next_exercise_name} will be changed to stage 1 and the due date will be set to today.")
        print(f"{num_stage1_exercises} exercises are currently at stage 1.\n")
        menu_choice = input("Would you like to proceed? Type y to proceed.")
        if menu_choice != "y":
            print("Adding next exercise aborted.")
            return
        
        #Set stage to 1
        self.exercises[next_exercise_index].current_stage = 1

        #Set due date to today
        today = datetime.datetime.today().date()
        self.exercises[next_exercise_index].due_date = today

        #Save new values to database
        self.save_to_db()

        #Notify user of success
        print(f"Exercise {next_exercise_id}: {next_exercise_name} added to rotation.")

    def get_review_date(self):
        date_choice = input("Enter date reviews were completed.\n"
                            "Type 0 for today, 1 for yesterday, or d to enter some other date.\n"
                            "Enter any other value to abort.\n")
        if date_choice == "0":
            review_date = datetime.datetime.today().date()
        elif date_choice == "1":
            review_date = datetime.datetime.today().date() - datetime.timedelta(days=1)
        elif date_choice == "d":
            user_date = input("Enter date in format YYYY-MM-DD\n")
            while not self.is_date_valid(user_date):
                user_date = input("Date format invalid. Enter date in format YYYY-MM-DD\n")
            review_date = datetime.datetime.strptime(user_date, "%Y-%m-%d").date()
        else:
            return
        return review_date

    def count_reviews_to_advance(self, review_date):
        count = 0
        for exercise in self.exercises:
            if exercise.due_date and exercise.due_date <= review_date:
                count += 1
        return count

    def is_date_valid(self, date_string):
        date_format = date_format = "%Y-%m-%d"
        try:
            datetime.datetime.strptime(date_string, date_format)
            return True
        except ValueError:
            return False
            
    def mark_reviews_done(self):
        #Mark all exercises due before the specified review date as complete and advances stage appropriately.
        review_date = self.get_review_date()

        #If the review date is None then the update is aborted.
        if not(review_date):
            print("Process aborted. No exercises advanced.")
            return
        
        #If there are no reviews due for this review date then no updates are attempted.
        num_exercises_to_advance = self.count_reviews_to_advance(review_date)
        if num_exercises_to_advance == 0:
            print("No exercises are due for this review date.")
            return
        
        #Confirm with user 
        confirm = input(f"\nUsing review date of {review_date}, {num_exercises_to_advance} will be advanced.\n"
                        "Do you wish to proceed? Type y to proceed.\n")
        
        if not(confirm.lower() == "y"):
            print("Advancement aborted.")
            return
        
        #Updates exercises due before review date.
        for exercise in self.exercises:
            if exercise.due_date and exercise.due_date <= review_date:
                exercise.advance_stage(review_date)
        print("All exercises due before review date have been advanced.")

        #Saves updates to the database
        self.save_to_db()
        





