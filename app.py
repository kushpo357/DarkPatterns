# app.py
from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('popup.html')

@app.route('/run_hello')
def run_hello():
    try:
        # Run the hello.py file using subprocess
        subprocess.run(['python', 'hello.py'])
        return 'Python file executed successfully!'

    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)