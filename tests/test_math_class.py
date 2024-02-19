
import pytest

from src.math_class import MathClass

def test_add_exercise():
    # Create an instance of MathClass
    math_class = MathClass()

    # Define the exercise details
    exercise_id = "ex1"
    name = "Addition Basics"
    stage = 1
    last_review_date = "2023-02-20"
    due_date = "2023-02-27"

    # Add an exercise to the math_class
    math_class.add_exercise(exercise_id, name, stage, last_review_date, due_date)

    # Check if the exercise was added correctly
    added_exercise = math_class.exercises[0]  # Access the first (and only) exercise in the list

    # Assert that the added exercise has the correct attributes
    assert added_exercise.exercise_id == exercise_id
    assert added_exercise.name == name
    assert added_exercise.current_stage == stage
    assert added_exercise.last_review_date == last_review_date
    assert added_exercise.due_date == due_date

    # Optionally, you can also check the length of the exercises list to be 1
    assert len(math_class.exercises) == 1
