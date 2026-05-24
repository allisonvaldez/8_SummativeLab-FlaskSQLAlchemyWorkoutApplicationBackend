# Import marshmallow tools for serialization and validation
from marshmallow import Schema, fields, validates, ValidationError


# Create a WorkoutExerciseSchema to serializes the join table rows
class WorkoutExerciseSchema(Schema):
    # This field is only included in output not input
    id = fields.Int(dump_only=True)

    # The workout_id and exercise_id are also included in output
    workout_id = fields.Int()
    exercise_id = fields.Int()

    # Allow for these variables to be null if not provided
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)

    # Provide a decorator and define a validator function for reps to be a positive number
    @validates('reps')
    def validate_reps(self, value):
        # Provide error handling
        if value is not None and value <= 0:
            raise ValidationError("Reps must be a positive integer.")

    # Provide a decorator and define a validator function that sets must be a positive number
    @validates('reps')
    def validate_sets(self, value):
        # Perform error handling
        if value is not None and value <= 0:
            raise ValidationError("Sets must be a positive integer.")

    # Provide a decorator and define a validator function that ensures duration_seconds is a positive number
    @validates('duration_seconds')
    def validate_duration_seconds(self, value):
        # Provide error handling
        if value is not None and value <= 0:
            raise ValidationError("Duration seconds must be a positive integer.")


# Create a ExerciseSchema to serializes Exercise objects
class ExerciseSchema(Schema):
    # Make sure its included in output
    id = fields.Int(dump_only=True)

    # This must be in the POST request
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool()

    # Provie list of workout_exercises
    workout_exercises = fields.List( 
        fields.Nested(lambda: WorkoutExerciseSchema(exclude=('exercise_id',))),
        dump_only=True
    )

    # Provide a decorator and define a validator function that ensures no blanks are entered
    @validates('name')
    def validate_name(self, value):
        # Perform error handling
        if not value or not value.strip():
            raise ValidationError("Exercise name cannot be blank.")

    # Provide a decorator and define a validator function that ensures that the category is proper
    @validates('category')
    def validate_category(self, value):
        # Provide the appropriate list of entries
        accepted = ['Strength', 'Cardio', 'Flexibility', 'Balance', 'HIIT']

        # Perform error handling
        if value not in accepted:
            raise ValidationError(f"Category must be one of: {', '.join(accepted)}")


# Create a WorkoutSchema to serializes Workout objects
class WorkoutSchema(Schema):
    # Make sure its included only as an output
    id = fields.Int(dump_only=True)

    # Date must be in the POST
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    # Notes will be allowed to be null
    notes = fields.Str(allow_none=True)

    # Provide a list of workout_exercises
    workout_exercises = fields.List(
        fields.Nested(lambda: WorkoutExerciseSchema(exclude=('workout_id',))),
        dump_only=True
    )

    # Provide a decorator and define a validator function that ensures the exercise duration is a valid number
    @validates('duration_minutes')
    def validate_duration(self, value):
        # Provide error handling
        if value is not None and value <= 0:
            raise ValidationError("Duration must be a positive number of minutes.")


# Create exercise variables necessary to run while serializing
exercise_schema = ExerciseSchema()
workout_schema = WorkoutSchema()
workout_exercise_schema = WorkoutExerciseSchema()

# Create lists that will be utilized when serializing multiple records at a time
exercises_schema = ExerciseSchema(many=True)
workouts_schema = WorkoutSchema(many=True)
workout_exercises_schema = WorkoutExerciseSchema(many=True)