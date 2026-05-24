# Import Flask utilities and modules
from flask import Flask, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from datetime import date

from models import db, Exercise, Workout, WorkoutExercise

# Import all schemas to serialize and deserialize data
from schemas import (
    exercise_schema, exercises_schema,
    workout_schema, workouts_schema,
    workout_exercise_schema
)

# Create the Flask app and configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Create migrate app to link db
migrate = Migrate(app, db)

# Create db
db.init_app(app)


# Create index route
@app.route('/')
def index():
    return make_response({'message': 'Workout Tracker API'}, 200)


# PART 1: WORKOUT ENDPOINTS

# Create functionality to return all workouts
@app.route('/workouts', methods=['GET'])
def get_workouts():
    # Search all rows in the workouts table
    workouts = Workout.query.all()
    # Serialize the list and return as JSON with 200 status
    return make_response(workouts_schema.dump(workouts), 200)


# Create functionality to return a single workout by its ID
@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    # Find workout by primary key
    workout = db.session.get(Workout, id)
    # Provide error handling if workout is not found
    if not workout:
        return make_response({'error': 'Workout not found'}, 404)
    # Return the serialized workout with 200 status
    return make_response(workout_schema.dump(workout), 200)


# Create functionality to create a new workout from request data
@app.route('/workouts', methods=['POST'])
def create_workout():
    # Get JSON body from request
    data = request.get_json()

    # Validate the incoming data and perform error handling
    try:
        validated = workout_schema.load(data)
    except ValidationError as e:
        return make_response({'errors': e.messages}, 400)
    
    # Create a workout to add to the database
    try:
        workout = Workout(
            date=validated['date'],
            duration_minutes=validated['duration_minutes'],
            notes=validated.get('notes')
        )
        db.session.add(workout)
        # Make sure to commit changes
        db.session.commit()

    # Perform error handling   
    except ValueError as e:
        db.session.rollback()
        return make_response({'error': str(e)}, 400)
    return make_response(workout_schema.dump(workout), 201)


# Create functionality to delete a workout by its ID
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    # Look up workout by primary key
    workout = db.session.get(Workout, id)
    # Provide error handling if workout is not found
    if not workout:
        return make_response({'error': 'Workout not found'}, 404)
    # Delete the workout
    db.session.delete(workout)
    db.session.commit()
    # Provide a message if successful
    return make_response({}, 204)


# PART 2: EXERCISE ENDPOINTS

# Create functionality to return all exercises
@app.route('/exercises', methods=['GET'])
def get_exercises():
    # Search rows from exercises table
    exercises = Exercise.query.all()
    # Serialize the list and return data as JSON
    return make_response(exercises_schema.dump(exercises), 200)

# Create functionality to return a single exercise by its ID
@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    # Look up exercise by primary key
    exercise = db.session.get(Exercise, id)
    # Provide error handling if exercise is not found
    if not exercise:
        return make_response({'error': 'Exercise not found'}, 404)
    # Return the serialized exercise with message
    return make_response(exercise_schema.dump(exercise), 200)


# Create functionality to create a new exercise from request data
@app.route('/exercises', methods=['POST'])
def create_exercise():
    # Get JSON 
    data = request.get_json()

    # Validate data with the schema
    try:
        validated = exercise_schema.load(data)
    except ValidationError as e:
        # Return error messages if failure
        return make_response({'errors': e.messages}, 400)
    
    # Create an exercise for the database
    try:
        exercise = Exercise(
            name=validated['name'],
            category=validated['category'],
            equipment_needed=validated.get('equipment_needed', False)
        )
        db.session.add(exercise)
        db.session.commit()

    except ValueError as e:
        db.session.rollback()
        return make_response({'error': str(e)}, 400)
    # Return the new exercise serialized as JSON with 201 Created status
    return make_response(exercise_schema.dump(exercise), 201)


# Create functionality to delete an exercise by its ID
@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    # Look up exercise by primary key
    exercise = db.session.get(Exercise, id)
    # Provide error handling if exercise is not found
    if not exercise:
        return make_response({'error': 'Exercise not found'}, 404)
    # Delete exercise 
    db.session.delete(exercise)
    db.session.commit()
    # Return message for successful deletion
    return make_response({}, 204)


# PART 3: WORKOUT EXERCISE ENDPOINT

# Create functionality to add an exercise to a workout with reps, sets, or duration
@app.route(
    '/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
    methods=['POST']
)
def add_exercise_to_workout(workout_id, exercise_id):
    # Look up the workout by primary key
    workout = db.session.get(Workout, workout_id)
    # Provide error handling if workout is not found
    if not workout:
        return make_response({'error': 'Workout not found'}, 404)

    # Look up the exercise by primary key
    exercise = db.session.get(Exercise, exercise_id)
    # Provide error handling if exercise is not found
    if not exercise:
        return make_response({'error': 'Exercise not found'}, 404)

    # Get JSON 
    data = request.get_json() or {}
    # Validate
    try:
        workout_exercise_schema.load(data)
    except ValidationError as e:
        return make_response({'errors': e.messages}, 400)

    # Create the join record linking the workout to the exercise
    workout_exercise = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        # Use .get() so these return None if not included in request
        reps=data.get('reps'),
        sets=data.get('sets'),
        duration_seconds=data.get('duration_seconds')
    )
    db.session.add(workout_exercise)
    db.session.commit()
    # Return the new join record serialized as JSON
    return make_response(workout_exercise_schema.dump(workout_exercise), 201)

if __name__ == '__main__':
    app.run(port=5555, debug=True)