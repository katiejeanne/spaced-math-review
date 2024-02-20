import datetime
import sqlite3

class Exercise:
    def __init__(self, exercise_id, name, web_link, class_id=0, current_stage=0, last_review_date=None, due_date=None) -> None:
        self.exercise_id = exercise_id
        self.name = name
        self.web_link = web_link
        self.class_id = class_id
        self.current_stage = current_stage
        self.last_review_date = self._return_date_or_none(last_review_date)
        self.due_date = self._return_date_or_none(due_date)
        
    
    def print_exercise(self):
        print(self.exercise_id, self.name, self.web_link, self.class_id, self.current_stage, self._return_datestring_or_nastring(self.last_review_date), self._return_datestring_or_nastring(self.due_date))

    def _return_date_or_none(self, date_string):
        if not date_string:
            return None
        else:
            return self._date_string_to_object(date_string)
        

    def _date_string_to_object(self, date_string):
        try: 
            return datetime.datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"Invalid date format for {date_string}, expected format: YYYY-MM-DD") from e
    
    def _return_datestring_or_nastring(self, date):
        # Converts date object to string for printing. If no date value is assigned "n/a" is printed.
        if not date:
            return "n/a"
        else:
            return date.strftime("%Y-%m-%d")

class MathClass:

    def __init__(self, class_id=0, class_name="Default") -> None:
        self.exercises = []
        self.class_id = class_id
        self.class_name = class_name

    def add_exercise(self, exercise_id, name, web_link):
        new_exercise = Exercise(exercise_id, name, web_link, self.class_id)
        self.exercises.append(new_exercise)

    def print_all_exercises(self):
        for exercise in self.exercises:
            exercise.print_exercise()

    def save_to_db(self, db_path='spaced-math-review.db'):
        try: 
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Ensure the table exists
            cursor.execute('''CREATE TABLE IF NOT EXISTS exercises (
                                id TEXT PRIMARY KEY,
                                name TEXT,
                                web_link TEXT,
                                class_id INTEGER,
                                current_stage INTEGER,
                                last_review_date TEXT,
                                due_date TEXT)''')

            # Insert or update exercises in the database
            for exercise in self.exercises:
                cursor.execute('''INSERT OR REPLACE INTO exercises 
                                (id, name, web_link, class_id, current_stage, last_review_date, due_date) 
                                VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                            (exercise.exercise_id, exercise.name, exercise.web_link, exercise.class_id, exercise.current_stage, 
                                exercise.last_review_date, exercise.due_date))

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            print(f"An error occurred while saving to the database: {e}")
        
        finally:
            if conn:
                conn.close()

    def prompt_and_add_exercise(self):
        exercise_id = input("Enter exercise number\n")
        name = input("Enter exercise name\n")
        web_link = input("Enter web link to exercises\n")
        self.add_exercise(exercise_id, name, web_link)
        print(f"Exercise {exercise_id} added to current class\n")

    def add_exercises_until_done_then_save(self):
        menu_choice = "y"
        while menu_choice == "y":
            self.prompt_and_add_exercise()
            menu_choice = input('Add another? Type "y" to continue.')
        self.save_to_db()


            

