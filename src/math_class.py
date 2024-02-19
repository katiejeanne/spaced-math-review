
class Exercise:
    def __init__(self, exercise_id="000", name="Unnamed exercise", web_link="0", current_stage="0", last_review_date="0", due_date="0") -> None:
        self.exercise_id = exercise_id
        self.name = name
        self.web_link = web_link
        self.current_stage = current_stage
        self.last_review_date = last_review_date
        self.due_date = due_date
        self.web_link = web_link
    
    def print_exercise(self):
        print(self.exercise_id, self.name, self.current_stage, self.last_review_date, self.due_date)


class MathClass:

    def __init__(self) -> None:
        self.exercises = []

    def add_exercise(self, exercise_id, name, web_link, stage="0", last_review_date="0", due_date="0"):
        new_exercise = Exercise(exercise_id, name, web_link, stage, last_review_date, due_date)
        self.exercises.append(new_exercise)

    def print_all_exercises(self):
        for exercise in self.exercises:
            exercise.print_exercise()


