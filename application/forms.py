from flask_wtf import Form
from wtforms import TextField, validators

class EnterSecAnswer(Form):
    answer = TextField(label='Security Question answer:', description="answer_enter", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])

