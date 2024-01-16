from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['Message']

        print(name, email, phone, message)

    return render_template('index.html')


@app.route('/workout')
def workout():
    return render_template('workout.html')


@app.route('/workout/run', methods=['GET', 'POST'])
def run():

    if request.method == 'POST':
        duration = request.form['workout-duration']
        level = request.form['fitness-level']
        run_type = request.form['running-type']

        # Do something with the data
        print(duration, level, run_type)


    return render_template('run.html')


@app.route('/workout/strength', methods=['GET', 'POST'])
def strength():

    if request.method == 'POST':
        duration = request.form['workout-duration']
        level = request.form['fitness-level']
        goal = request.form['fitness-goal']
        equipment = request.form['equipment-access']
        print(duration, level, goal, equipment)

    return render_template('strength.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


if __name__ == "__main__":
    app.run()


