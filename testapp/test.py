from conductor.rendering import viewmethod
from conductor.accessors import gvar, rvar
from flask import render_template
from random import choice


@viewmethod
def test_render_function() -> str:
    return render_template(rvar('template'), choice=choice(gvar('choices')))
