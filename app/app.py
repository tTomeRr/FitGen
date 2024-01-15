from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/workout')
def workout():
    return render_template('workout.html')


@app.route('/workout/run')
def run():
    return render_template('run.html')


@app.route('/workout/strength')
def strength():
    return render_template('strength.html')


if __name__ == "__main__":
    app.run()
