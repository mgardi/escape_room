'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''

from flask import Flask, render_template, request
from application.forms import EnterSecAnswer

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'

branding = {
    "gpt" : "Girls-Power-Tech_Lockup---Large.png",
    "tacc" : "esacpe_room_tacc_branding.png"
}

current_event = 'tacc'

answer_dict = {
    "othersme":
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
}


@application.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', event=branding[current_event])


@application.route('/<question_arg>', methods=['GET', 'POST'])
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
