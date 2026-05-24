# Import utilities and models
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

# Create db for Flask app
db = SQLAlchemy()

# Create an exercise class for the model to add exercises for workouts
class Exercise(db.Model):

    # Detail what db this model maps to
    __tablename__ = 'exercises'

    # Create unique id for the primary key
    id = db.Column(db.Integer, primary_key=True)
    # Provide other attributes for the model
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    # One exercise will be apart of many workouts
    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise", cascade="all delete-orphan")

    # Provide a method to skip through workout_exercises to get to a specific workout
    workouts = association_proxy('workout_exercises', 'workout')

    # Provide a decorator and define a validator function to ensure exercise name is not blank
    @validates('name')
    def validate_name(self, key, value):
        # Perform error handling
        if not value or not value.strip():
            raise ValueError("Exercise must have a name.")
        # Removes any potential leading/trailing whitespace
        return value.strip()

    # Provide a decorator and define a validator function to ensure category is one of the accepted values
    @validates('category')
    def validate_category(self, key, value):
        # Create a list for acceptable categories
        accepted = ['Strength', 'Cardio', 'Flexibility', 'Balance', 'HIIT']
        # Provide error handling
        if value not in accepted:
            raise ValueError(f"Category must be one of: {', '.join(accepted)}")
        return value

    # Provide data as a string when exercise is printed
    def __repr__(self):
        return f'<Exercise {self.id}, {self.name}, {self.category}>'


# Create an workout class for the model to add a single exercise
class Workout(db.Model):
    # Detail what db this model maps to
    __tablename__ = 'workouts'

    # Create unique id for the primary key
    id = db.Column(db.Integer, primary_key=True)
    # Provide other attributes for the model
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # One workout will be apart of many exercises
    workout_exercises = db.relationship( "WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")

    # Provide a method to skip through workout_exercises to get to a specific exercise
    exercises = association_proxy('workout_exercises', 'exercise')

    # Provide a decorator and define a validator function to ensure duration is not 0
    @validates('duration_minutes')
    def validate_duration(self, key, value):
        # Perform error handling
        if value is None or value <= 0:
            raise ValueError("Duration must be a positive number of minutes.")
        return value

    # Provide a decorator and define a validator function to ensure a date is entered
    @validates('date')
    def validate_date(self, key, value):
        # Perform error handling
        if not value:
            raise ValueError("Workout must have a date.")
        return value

    # Provide data as a string when a workout is printed
    def __repr__(self):
        return f'<Workout {self.id}, {self.date}, {self.duration_minutes} mins>'


# Create an WorkoutExercise class for the model to join the tables linking both the Workouts and Exercises
class WorkoutExercise(db.Model):

    # Detail what db this model maps to
    __tablename__ = 'workout_exercises'

    # Create unique id for the primary key
    id = db.Column(db.Integer, primary_key=True)
    # Provide other attributes for the model
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # Each WorkoutExercise will have one Workout
    workout = db.relationship('Workout', back_populates='workout_exercises')
    # Each WorkoutExercise have one Exercise
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    # Provide data as a string when workout is printed
    def __repr__(self):
        return f'<WorkoutExercise workout={self.workout_id} exercise={self.exercise_id}>'