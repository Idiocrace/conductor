from conductor.rendering import viewmethod
from conductor.accessors import gvar, rvar
from flask import render_template


@viewmethod
def test_render_function(fruit: str) -> str:
    return render_template(
        rvar('template'),
        fruit=fruit,
        definition=gvar('fruit_dict')[fruit]
    )
