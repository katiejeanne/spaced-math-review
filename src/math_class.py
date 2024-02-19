
class Exercise:
    def __init__(self, exercise_id="000", name="Unnamed exercise", current_stage=0, last_review_date=0, due_date=0) -> None:
        self.exercise_id = exercise_id
        self.name = name
        self.current_stage = current_stage
        self.last_review_date = last_review_date
        self.due_date = due_date


class MathClass:

    def __init__(self) -> None:
        self.exercises = []

    def add_exercise(self, exercise_id, name, stage=0, last_review_date=0, due_date=0):
        new_exercise = Exercise(exercise_id, name, stage, last_review_date, due_date)
        self.exercises.append(new_exercise)

