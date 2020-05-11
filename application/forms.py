from flask_wtf import Form
from wtforms import TextField, PasswordField, HiddenField, validators, SubmitField

class EnterSecAnswer(Form):
    answer = TextField(label='Security Question answer:', description="answer_enter", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])
class EnterLogin(Form):
    user = TextField(label='Username', description="username", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])
    password = PasswordField(label='Password', description="password", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])
class AcceptOrDeclineForm(Form):
    accept = SubmitField(label='Accept', description="")
    decline = SubmitField(label='Decline', description="")
class ContinueButtonForm(Form):
    action = SubmitField(label='Continue', description="")