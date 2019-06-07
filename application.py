'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''

from flask import Flask, render_template, request, redirect, url_for
from application.forms import EnterSecAnswer

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'

answer_dict = {
    "others me":
        {"question": "What city were you born in?",
         "answer": "chicago",
         "place_holder": "Enter City of Birth",
         "solution": "othersme-ciphertext.png"},
    "own":
        {"question": "What was the name of your first pet?",
         "answer": "plumcot",
         "place_holder": "Enter Name of Pet",
         "solution": "own-ciphertext.png"},
    "backup":
        {"question": "What was the make and model of your first car?",
         "answer": "Toyota Rav4",
         "place_holder": "Enter Car Model",
         "solution": "backup-ciphertext.png"},
    "passwords":
        {"question": "What is your favorite food?",
         "answer": "potato",
         "place_holder": "Enter Food",
         "solution": "passwords-ciphertext.png"},
    "multi1":
        {"question": "What is your favorite food?",
         "answer": "potato",
         "place_holder": "Enter Food",
         "solution": "passwords-ciphertext.png"},
    "multi2":
        {"question": "What is your favorite food?",
         "answer": "potato",
         "place_holder": "Enter Food",
         "solution": "passwords-ciphertext.png"}
}


@application.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@application.route('/othersme', methods=['GET', 'POST'])
def othersme():
    question = answer_dict['othersme']['question']
    answer = answer_dict['othersme']['answer']
    place_holder = answer_dict['othersme']['place_holder']
    form = EnterSecAnswer(request.form)
    feedback = None

    if request.method == 'POST' and form.validate():
        data_entered = form.answer.data
        if data_entered.lower() == answer.lower():
            #return render_template('cipherkey1.html')
            return render_template('dynamic_key.html', solution=answer_dict['othersme']['solution'])
        feedback = ':-( wrong answer, try again'

    return render_template('secquestion.html', form=form, question=question,
                           place_holder=place_holder, feedback=feedback)


@application.route('/own', methods=['GET', 'POST'])
def own():
    question = answer_dict['own']['question']
    answer = answer_dict['own']['answer']
    place_holder = answer_dict['own']['place_holder']
    form = EnterSecAnswer(request.form)
    feedback = None

    if request.method == 'POST' and form.validate():
        data_entered = form.answer.data
        if data_entered.lower() == answer.lower():
            #return render_template('cipherkey1.html')
            return render_template('dynamic_key.html', solution=answer_dict['own']['solution'])
        feedback = ':-( wrong answer, try again'

    return render_template('secquestion.html', form=form, question=question,
                           place_holder=place_holder, feedback=feedback)


@application.route('/backup', methods=['GET', 'POST'])
def backup():
    question = answer_dict['backup']['question']
    answer = answer_dict['backup']['answer']
    place_holder = answer_dict['backup']['place_holder']
    form = EnterSecAnswer(request.form)
    feedback = None

    if request.method == 'POST' and form.validate():
        data_entered = form.answer.data
        if data_entered.lower() == answer.lower():
            #return render_template('cipherkey1.html')
            return render_template('dynamic_key.html', solution=answer_dict['backup']['solution'])
        feedback = ':-( wrong answer, try again'

    return render_template('secquestion.html', form=form, question=question,
                           place_holder=place_holder, feedback=feedback)


@application.route('/passwords', methods=['GET', 'POST'])
def passwords():
    question = answer_dict['passwords']['question']
    answer = answer_dict['passwords']['answer']
    place_holder = answer_dict['passwords']['place_holder']
    form = EnterSecAnswer(request.form)
    feedback = None

    if request.method == 'POST' and form.validate():
        data_entered = form.answer.data
        if data_entered.lower() == answer.lower():
            return render_template('dynamic_key.html', solution=answer_dict['passwords']['solution'])
        feedback = ':-( wrong answer, try again'

    return render_template('secquestion.html', form=form, question=question,
                           place_holder=place_holder, feedback=feedback)


@application.route('/multi/<question_arg>', methods=['GET', 'POST'])
def dynamic(question_arg):
    question = answer_dict[question_arg]['question']
    answer = answer_dict[question_arg]['answer']
    place_holder = answer_dict[question_arg]['place_holder']
    form = EnterSecAnswer(request.form)
    feedback = None

    if request.method == 'POST' and form.validate():
        data_entered = form.answer.data
        if data_entered.lower() == answer.lower():
            return render_template('dynamic_key.html', solution=answer_dict[question_arg]['solution'])
        feedback = ':-( wrong answer, try again'

    return render_template('secquestion.html', form=form, question=question,
                           place_holder=place_holder, feedback=feedback)




if __name__ == '__main__':
    application.run(host='0.0.0.0')
