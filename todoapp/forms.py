"""

"""
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    STATUS_CHOICES = [
        (1, 'TODO'),
        (2, 'In Process'),
        (3, 'Complete'),
    ]
    PRIORITY_CHOICES = [
        (0, 'not-set'),
        (1, 'low'),
        (2, 'normal'),
        (3, 'high'),
        (4, 'top')
    ]

    description = TextAreaField(
        label='Description',
        validators=[DataRequired()]
    )
    status = SelectField(
        label='Status',
        choices=STATUS_CHOICES,
        coerce=int
    )
    priority = SelectField(
        label='Priority',
        choices=PRIORITY_CHOICES,
        coerce=int
    )
    submit = SubmitField(
        label='Create'
    )
