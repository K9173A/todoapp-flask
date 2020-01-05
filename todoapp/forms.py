"""

"""
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired


class TaskCreateForm(FlaskForm):
    description = TextAreaField(
        label='Description',
        validators=[DataRequired()]
    )
    status = SelectField(
        label='Status',
        choices=[
            (1, 'TODO'),
            (2, 'In Process'),
            (3, 'Complete'),
        ],
        coerce=int
    )
    priority = SelectField(
        label='Priority',
        choices=[
            (0, 'Not set'),
            (1, 'Low'),
            (2, 'Normal'),
            (3, 'High'),
            (4, 'Top')
        ],
        coerce=int
    )
    submit = SubmitField(
        label='Create'
    )
