from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/receive')
def receive():
    """
    Expecting:
    {"message": ""}
    """
    json.loads(req.body)
    print('Contacting wit.ai...')
    print('Got from wit.ai')
    return 'This is a response from wit.ai'
