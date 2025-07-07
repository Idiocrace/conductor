from conductor.rendering import viewmethod
from conductor.accessors import gvar, rvar
from flask import render_template, request


def validate_fruit(fruit: str) -> str:
    """Validate the favorite fruit field."""
    if not fruit or not fruit.strip():
        return "Favorite fruit is required."

    fruit = fruit.strip().lower()

    # Get valid fruits from global variable
    valid_fruits = gvar('choices')
    if not valid_fruits:
        return "No valid fruits available."

    # Convert to lowercase for comparison
    valid_fruits_lower = [f.lower() for f in valid_fruits]

    # Check if it's a valid fruit
    if fruit not in valid_fruits_lower:
        return (f"'{fruit}' is not a recognized fruit. "
                f"Please choose from: {', '.join(valid_fruits)}")

    return None


@viewmethod
def form_render_function() -> str:
    errors = {}
    form_data = {}
    success_message = None

    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        favorite_fruit = request.form.get('favorite_fruit', '').strip()

        # Store form data for re-display
        form_data = {
            'name': name,
            'favorite_fruit': favorite_fruit
        }

        # Validate fields
        fruit_error = validate_fruit(favorite_fruit)

        if fruit_error:
            errors['favorite_fruit'] = fruit_error

        # If no errors, show success
        if not errors:
            success_message = (
                f"Thank you {name}! Your favorite fruit "
                f"'{favorite_fruit.lower()}' has been recorded."
            )

    return render_template(
        rvar('template'),
        errors=errors,
        form_data=form_data,
        success_message=success_message
    )
