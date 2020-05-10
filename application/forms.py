from flask_wtf import Form
from wtforms import TextField, PasswordField, HiddenField, validators

class EnterSecAnswer(Form):
    answer = TextField(label='Security Question answer:', description="answer_enter", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])
class EnterLogin(Form):
    user = TextField(label='Username', description="username", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])
    password = PasswordField(label='Password', description="password", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])
class AcceptButtonForm(Form):
    action = HiddenField(label='Accept', description="", default="accept", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])
class DeclineButtonForm(Form):
    action = HiddenField(label='Decline', description="", default="decline",validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])
class ContinueButtonForm(Form):
    action = HiddenField(label='Continue', description="", default="continue",validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])