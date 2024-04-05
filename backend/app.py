from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app_code = os.environ.get('APP_CODE')

@app.route('/')
def hello():
    return f'Hello, Kubernetes! App Code: {app_code}'

if __name__ == '__main__':
    print(f'App Code: {app_code}')
    app.run(debug=True)
