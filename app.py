# app.py
from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_hello')
def run_hello():
    url = request.args.get('url', '')
    try:
        subprocess.run(['python', 'backend.py', '--url', url])
        return 'Python file executed successfully!'
    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
