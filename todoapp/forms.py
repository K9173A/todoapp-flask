"""
Module which defines forms
"""
from flask_wtf import FlaskForm
from wtforms import (
    TextAreaField,
    SubmitField,
    SelectField,
    StringField,
    FloatField,
)
from wtforms.validators import (
    DataRequired,
    Length
)


class TaskForm(FlaskForm):
    STATUS_CHOICES = [
        (1, 'todo'),
        (2, 'in-progress'),
        (3, 'complete'),
    ]
    PRIORITY_CHOICES = [
        (0, 'not-set'),
        (1, 'low'),
        (2, 'normal'),
        (3, 'high'),
        (4, 'top')
    ]

    title = StringField(
        label='Title',
        validators=[
            DataRequired(),
            Length(min=3, max=48)
        ]
    )
    date_added = FloatField(
        label='Added',
    )
    description = TextAreaField(
        label='Description'
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
