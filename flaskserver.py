# TODO
# create a web server using Flask to provide a GUI on top of the CLI interface
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run()
