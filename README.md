# Summerative: Workout Tracker API

A RESTful backend API for tracking workouts and exercises, built with Flask, SQLAlchemy, and Marshmallow.

## Description

Personal trainers, and health nuts, will be able to use this API to manage reusable exercises and log workouts. Each workout can include multiple exercises with reps, sets, or duration data attached via a join table.

## Installation

```bash
# Install dependencies
pipenv install

# Enter virtual environment
pipenv shell

# Navigate to server directory
cd server

# Initialize the database
flask db init
flask db migrate -m "initial migration"
flask db upgrade head

# Seed the database with sample data
python3 seed.py
```

## Run

```bash
# From the server/ directory with the virtual environment active
export FLASK_APP=app.py
export FLASK_RUN_PORT=5555
flask run
```

The API will be available at `http://localhost:5555`

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Get a single workout with its exercises |
| POST | `/workouts` | Create a new workout |
| DELETE | `/workouts/<id>` | Delete a workout and its associated exercises |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Get a single exercise with its workouts |
| POST | `/exercises` | Create a new exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

## Example curl Commands

```bash
# Get all workouts
curl http://localhost:5555/workouts

# Get a single workout
curl http://localhost:5555/workouts/1

# Create a workout
curl -X POST http://localhost:5555/workouts \
  -H "Content-Type: application/json" \
  -d '{"date": "2025-01-15", "duration_minutes": 45, "notes": "Morning session"}'

# Delete a workout
curl -X DELETE http://localhost:5555/workouts/1

# Get all exercises
curl http://localhost:5555/exercises

# Create an exercise
curl -X POST http://localhost:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{"name": "Pull Up", "category": "Strength", "equipment_needed": false}'

# Add an exercise to a workout (with reps and sets)
curl -X POST http://localhost:5555/workouts/1/exercises/1/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{"reps": 10, "sets": 3}'

# Add an exercise to a workout (with duration)
curl -X POST http://localhost:5555/workouts/1/exercises/2/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{"duration_seconds": 300}'
```

## Validations

### Table Constraints
- Exercise `name` is required and unique
- Exercise `category` is required
- Exercise `equipment_needed` is required
- Workout `date` is required
- Workout `duration_minutes` is required
- WorkoutExercise `workout_id` and `exercise_id` are required foreign keys

### Model Validations
- Exercise name cannot be blank
- Exercise category must be one of: Strength, Cardio, Flexibility, Balance, HIIT
- Workout duration must be a positive integer
- Workout date cannot be null

### Schema Validations
- Exercise name cannot be blank in request body
- Exercise category must be one of the accepted values
- Reps must be a positive integer if provided
- Sets must be a positive integer if provided
- Duration seconds must be a positive integer if provided
- Workout duration must be positive in request body
