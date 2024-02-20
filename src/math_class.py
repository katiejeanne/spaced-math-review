import datetime
import sqlite3


class Exercise:
    def __init__(self, exercise_id="000", name="Unnamed exercise", web_link="0", current_stage="0", last_review_date="0", due_date="0") -> None:
        self.exercise_id = exercise_id
        self.name = name
        self.web_link = web_link
        self.current_stage = current_stage
        self.last_review_date = self._return_date_or_zero(last_review_date)
        self.due_date = self._return_date_or_zero(due_date)
        
    
    def print_exercise(self):
        print(self.exercise_id, self.name, self.current_stage, self.last_review_date, self.due_date)

    def _return_date_or_zero(self, date_string):
        try: 
            if date_string == "0":
                return "0"
            else:
                return self._date_string_to_object(date_string)
        except ValueError as e:
            raise ValueError(f"Invalid date format for {date_string}, expected format: YYYY-MM-DD") from e

    def _date_string_to_object(self, date_string):
        return datetime.datetime.strptime(date_string, "%Y-%m-%d")

class MathClass:

    def __init__(self) -> None:
        self.exercises = []

    def add_exercise(self, exercise_id, name, web_link, stage="0", last_review_date="0", due_date="0"):
        new_exercise = Exercise(exercise_id, name, web_link, stage, last_review_date, due_date)
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
                                current_stage INTEGER,
                                last_review_date TEXT,
                                due_date TEXT)''')

            # Insert or update exercises in the database
            for exercise in self.exercises:
                cursor.execute('''INSERT OR REPLACE INTO exercises 
                                (id, name, web_link, current_stage, last_review_date, due_date) 
                                VALUES (?, ?, ?, ?, ?, ?)''', 
                            (exercise.exercise_id, exercise.name, exercise.web_link, exercise.current_stage, 
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


            

