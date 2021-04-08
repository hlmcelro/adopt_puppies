from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField



class AddForm(FlaskForm):

    name = StringField('Name of Puppy:')
    gender = StringField('Gender:')
    age = IntegerField("Age:")
    color = StringField('Color:')
    size = StringField('Small/Medium/Large:')
    weight = IntegerField("Weight (lbs):")
    aptitude = StringField('Aptitude:')
    tricks = StringField('Tricks:')
    favorite_food = StringField('Favorite Food:')
    submit = SubmitField('Add Puppy')

class AddOwnerForm(FlaskForm):

    name = StringField('Name of Owner:')
    pup_id = IntegerField("Id of Puppy: ")
    address = StringField('Address:')
    city = StringField('City')
    state = StringField('State')
    phone = StringField('Phone Number')
    submit = SubmitField('Add Owner')

class DelForm(FlaskForm):

    id = IntegerField('Id Number of Puppy to Remove:')
    submit = SubmitField('Remove Puppy')
