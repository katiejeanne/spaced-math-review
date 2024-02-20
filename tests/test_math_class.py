
import pytest
import datetime
import sqlite3
from src.math_class import MathClass, Exercise

# Define the parameter sets
@pytest.mark.parametrize("exercise_id, name, web_link", [
    ("ex1", "Addition Basics", "https://www.example.com/addition"),
    ("ex2", "Subtraction Basics", "https://www.example.com/subtraction"),
    ("000.000.000", "This is a very long title. It's all about how math exercies are so fascinating. Greebo loves math. Kalyn loves math. We all love math.", "https://www.khanacademy.org/math/pre-algebra")
])
def test_add_exercise(exercise_id, name, web_link):
    math_class = MathClass(0, "Test math class")

    # Add an exercise to the math_class
    math_class.add_exercise(exercise_id, name, web_link)

    # Check if the exercise was added correctly
    added_exercise = math_class.exercises[-1]  # Access the last added exercise

    # Assert that the added exercise has the correct attributes
    assert added_exercise.exercise_id == exercise_id
    assert added_exercise.name == name
    assert added_exercise.web_link == web_link
    assert added_exercise.class_id == 0


@pytest.fixture
def setup_math_class_with_exercises():
    math_class = MathClass(0,"Test math class")
    # Create mock exercises
    exercise1 = Exercise("001", "Exercise 1", "http://example.com/1", 0, 1, "2023-01-01", "2023-01-02")
    exercise2 = Exercise("002", "Exercise 2", "http://example.com/2", 0, 2, "2023-01-03", "2023-01-04")
    exercise3 = Exercise("123.123.123", "Exercise 3", "www.math.org", 1, 6, None, None)
    # Add mock exercises to MathClass instance
    math_class.exercises.extend([exercise1, exercise2, exercise3])
    return math_class

def test_save_to_db(setup_math_class_with_exercises, tmp_path):
    db_path = tmp_path / "test2_database.db"  # Use pytest's tmp_path fixture for a temporary database file
    math_class = setup_math_class_with_exercises

    # Invoke the method to test
    math_class.print_all_exercises()
    math_class.save_to_db(db_path=db_path.as_posix())

    # Connect to the temporary database and verify the inserted data
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exercises")
    rows = cursor.fetchall()

    # Verify the number of inserted rows and some specific data
    assert len(rows) == 3  # Assuming you added 2 exercises
    assert rows[0][0] == "001"  # Verify the first exercise's ID
    assert rows[1][1] == "Exercise 2"  # Verify the second exercise's name

    # Clean up by closing the database connection
    conn.close()


    
