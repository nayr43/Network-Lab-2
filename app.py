from flask import Flask, render_template, flash, request
from wtforms import Form, FloatField, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class BMIForm(Form):
    height = FloatField('Height:', validators=[validators.required()])
    weight = FloatField('Weight:', validators=[validators.required()])
    bmi = 0
    types = ''
    tips = 0

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/BMI.html', methods=['GET', 'POST'])
def health_check():
	types = {1 : 'Severe Thinness', 2 : 'Moderate thinness', 3 : 'Mild Thinness', 4 : 'Normal', \
			5 : 'Overweight', 6 : 'Obese class I', 7 : 'Obese class II', 8 : 'Obese class III'}
	form = BMIForm(request.form)

	print(form.errors)
	if request.method == 'POST':
		height=float(request.form['height'])
		weight=float(request.form['weight'])
		
		print(type(height))
		flash('Height: {}; Weight: {}'.format(height, weight))

		if form.validate():
			form.bmi = bmi(height, weight)
			form.types = types[classify(form.bmi)]
			form.tips = tips(form.bmi)

			# flash('Your BMI is {}'.format(bmi_score))
			# flash(types(classify(bmi_score)))
			# flash(tips(classify(bmi_score)))
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

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')