from conductor import viewmethod, gvar, rvar
from flask import render_template


@viewmethod
def example_render_function() -> str:
    # Implement your rendering logic here
    return render_template(
        'example_template.html',
        data=gvar('data'),
        other_data=rvar('other_data')
    )
