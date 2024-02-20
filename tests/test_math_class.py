
import pytest
import datetime
import sqlite3
from src.math_class import MathClass, Exercise

# Define the parameter sets
@pytest.mark.parametrize("exercise_id, name, web_link, stage, last_review_date, due_date", [
    ("ex1", "Addition Basics", "https://www.example.com/addition", 1, "2023-02-20", "2023-02-27"),
    ("ex2", "Subtraction Basics", "https://www.example.com/subtraction", 2, "2023-03-01", "2023-03-05"),
    ("000.000.000", "This is a very long title. It's all about how math exercies are so fascinating. Greebo loves math. Kalyn loves math. We all love math.", "https://www.khanacademy.org/math/pre-algebra", 20, "0", "0")
])
def test_add_exercise(exercise_id, name, web_link, stage, last_review_date, due_date):
    math_class = MathClass()

    # Convert string dates to datetime objects for comparison
    if last_review_date != "0":
        last_review_date_object = datetime.datetime.strptime(last_review_date, "%Y-%m-%d")
    else:
        last_review_date_object = last_review_date

    if due_date != "0":
        due_date_object = datetime.datetime.strptime(due_date, "%Y-%m-%d")
    else:
        due_date_object = due_date

    # Add an exercise to the math_class
    math_class.add_exercise(exercise_id, name, web_link, stage, last_review_date, due_date)

    # Check if the exercise was added correctly
    added_exercise = math_class.exercises[-1]  # Access the last added exercise

    # Assert that the added exercise has the correct attributes
    assert added_exercise.exercise_id == exercise_id
    assert added_exercise.name == name
    assert added_exercise.web_link == web_link
    assert added_exercise.current_stage == stage
    assert added_exercise.last_review_date == last_review_date_object
    assert added_exercise.due_date == due_date_object



def test_add_exercise_with_invalid_date_raises_value_error():
    
    # Create an instance of MathClass
    math_class = MathClass()

    # Define the exercise details with an invalid date
    exercise_id = "ex1"
    name = "Addition Basics"
    web_link = "https://www.khanacademy.org/math/pre-algebra"
    stage = 1
    invalid_last_review_date = "invalid-date"
    due_date = "2023-02-27"

    # Use pytest.raises to expect a ValueError
    with pytest.raises(ValueError) as excinfo:
        math_class.add_exercise(exercise_id, name, web_link, stage, invalid_last_review_date, due_date)

@pytest.fixture
def setup_math_class_with_exercises():
    math_class = MathClass()
    # Create mock exercises
    exercise1 = Exercise("001", "Exercise 1", "http://example.com/1", 1, "2023-01-01", "2023-01-02")
    exercise2 = Exercise("002", "Exercise 2", "http://example.com/2", 2, "2023-01-03", "2023-01-04")
    # Add mock exercises to MathClass instance
    math_class.exercises.extend([exercise1, exercise2])
    return math_class

def test_save_to_db(setup_math_class_with_exercises, tmp_path):
    db_path = tmp_path / "test_database.db"  # Use pytest's tmp_path fixture for a temporary database file
    math_class = setup_math_class_with_exercises

    # Invoke the method to test
    math_class.save_to_db(db_path=db_path.as_posix())

    # Connect to the temporary database and verify the inserted data
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exercises")
    rows = cursor.fetchall()

    # Verify the number of inserted rows and some specific data
    assert len(rows) == 2  # Assuming you added 2 exercises
    assert rows[0][0] == "001"  # Verify the first exercise's ID
    assert rows[1][1] == "Exercise 2"  # Verify the second exercise's name

    # Clean up by closing the database connection
    conn.close()


    
