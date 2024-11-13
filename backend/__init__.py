from flask import Flask, render_template
import os

app = Flask(__name__, template_folder= 'templates')

@app.route('/')
def home():
    # Sample data that will be passed to the template
    user = {'name': 'Alice', 'age': 30}
    return render_template('home.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)