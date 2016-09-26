from flask import Flask, render_template, flash, request
from wtforms import Form, FloatField, SelectField, validators, SubmitField

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class BMIForm(Form):
    height = FloatField('Height (metres):', validators=[validators.required()])
    weight = FloatField('Weight (kg):', validators=[validators.required()])
    bmi = 0
    types = ''
    tips = 0

class WorkoutForm(Form):
	workout_type = SelectField('Select your workout type:', choices = [(1, 'Cardio'), (2, 'Chest'), \
		(3, 'Arms'), (4, 'Legs')], validators=[validators.required()])

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/bmi', methods=['GET', 'POST'])
def health_check():
	types = {1 : 'Severe Thinness', 2 : 'Moderate thinness', 3 : 'Mild Thinness', 4 : 'Normal', \
			5 : 'Overweight', 6 : 'Obese class I', 7 : 'Obese class II', 8 : 'Obese class III'}
	form = BMIForm(request.form)

	print(form.errors)
	if request.method == 'POST':
		height=float(request.form['height'])
		weight=float(request.form['weight'])

		flash('Height: {}; Weight: {}'.format(height, weight))

		if form.validate():
			form.bmi = bmi(height, weight)
			form.types = types[classify(form.bmi)]
			form.tips = tips(form.bmi)

		else:
			flash('All the form fields are required. ')
	return render_template('health_check.html', form=form)

def bmi(height, weight):
	return weight/(height*height)

def classify(bmi_score):
	if (bmi_score < 16):
		return 1
	elif (bmi_score < 17):
		return 2
	elif (bmi_score < 18.5):
		return 3
	elif (bmi_score < 25):
		return 4
	elif (bmi_score < 30):
		return 5
	elif (bmi_score < 35):
		return 6
	elif (bmi_score < 40):
		return 7
	else:
		return 8

def tips(bmi_score):
	if (bmi_score < 18.5):
		return 1
	elif (bmi_score < 25):
		return 2
	else:
		return 3

@app.route('/workouts', methods=['GET', 'POST'])
def workouts():
	form = WorkoutForm(request.form)
	print(form.errors)
	if request.method == 'POST':
		form.workout_type=int(request.form['workout_type'])
		if (not form.validate()):
			flash('All the form fields are required. ')
	return render_template('workouts.html', form=form)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')