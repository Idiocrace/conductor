from conductor.routing import Router
from flask import Flask

app = Flask(__name__)

app.config['DEBUG'] = True

choices = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape']

fruit_dict = {
    'apple': 'A sweet red fruit.',
    'banana': 'A long yellow fruit.',
    'cherry': 'A small red fruit.',
    'date': 'A sweet brown fruit.',
    'elderberry': 'A dark purple fruit.',
    'fig': 'A soft purple fruit.',
    'grape': 'A small green or purple fruit.'
}

router = Router("router.json")
router.activate_router(app)

# For development, use port 80
app.run(host='0.0.0.0', port=80)
