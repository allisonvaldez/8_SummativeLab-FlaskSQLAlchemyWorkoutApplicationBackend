#!/usr/bin/env python3

# Import utilites and modules
from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

# Required component for the interaction of the database
with app.app_context():
    # Delete all previously existing data 
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    # Make sure to commit the deletions
    db.session.commit()

    # Create sample exercises for the various implemented categories
    e1 = Exercise(name='Push Up', category='Strength', equipment_needed=False)
    e2 = Exercise(name='Squat', category='Strength', equipment_needed=False)
    e3 = Exercise(name='Treadmill Run', category='Cardio', equipment_needed=True)
    e4 = Exercise(name='Yoga Flow', category='Flexibility', equipment_needed=False)
    e5 = Exercise(name='Plank', category='Balance', equipment_needed=False)
    e6 = Exercise(name='Burpee', category='HIIT', equipment_needed=False)

    # Add exercises to sessions
    db.session.add_all([e1, e2, e3, e4, e5, e6])
    # Make sure to commit
    db.session.commit()

    # Create new workouts 
    w1 = Workout(date=date(2025, 1, 6), duration_minutes=45, notes='Morning strength session')
    w2 = Workout(date=date(2025, 1, 8), duration_minutes=30, notes='Quick cardio day')
    w3 = Workout(date=date(2025, 1, 10), duration_minutes=60, notes='Full body workout')

    # Add workouts
    db.session.add_all([w1, w2, w3])
    # Make sure to commit
    db.session.commit()

    # Create the link between workouts and exercises
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=e1.id, reps=15, sets=3)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=e2.id, reps=12, sets=4)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=e3.id, duration_seconds=1800)
    we4 = WorkoutExercise(workout_id=w2.id, exercise_id=e6.id, reps=10, sets=5)
    we5 = WorkoutExercise(workout_id=w3.id, exercise_id=e4.id, duration_seconds=600)
    we6 = WorkoutExercise(workout_id=w3.id, exercise_id=e5.id, duration_seconds=60, sets=3)
    we7 = WorkoutExercise(workout_id=w3.id, exercise_id=e1.id, reps=20, sets=2)

    # Add the join records
    db.session.add_all([we1, we2, we3, we4, we5, we6, we7])
    # Make sure to commit
    db.session.commit()

    # Provide print message
    print("Database seeded successfully!")