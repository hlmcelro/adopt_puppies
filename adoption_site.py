#import pymysql
import csv
import os
from forms import  AddForm , DelForm, AddOwnerForm
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import username, password

app = Flask(__name__)
# Key for Forms
app.config['SECRET_KEY'] = 'mysecretkey'

############################################

        # SQL DATABASE AND MODELS

##########################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:9hannah9ms@localhost/dogs_db' # DB connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # DB connection

db = SQLAlchemy(app)
Migrate(app,db)

class Puppy(db.Model):

    __tablename__ = 'puppies'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.Text)
    gender = db.Column(db.Text)
    age = db.Column(db.Text)
    color = db.Column(db.Text)
    size = db.column(db.Text)
    weight = db.column(db.Text)
    aptitude = db.column(db.Text)
    tricks = db.column(db.Text)
    favorite_food = db.column(db.Text)
    owner = db.relationship('Owner',backref='puppy',uselist=False)


    def __repr__(self):
        if self.owner:
            return f"Puppy name is {self.name} and owner is {self.owner.name}. They live at {self.owner.address}, {self.owner.city}, {self.owner.state} and can be contacted at {self.owner.phone}"
        else:
            return f"Puppy name is {self.name} and has no owner assigned yet."

class Owner(db.Model):

    __tablename__ = 'owners'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.Text)
    address = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    phone = db.Column(db.Text)

    # We use puppies.id because __tablename__='puppies'
    puppy_id = db.Column(db.Integer,db.ForeignKey('puppies.id'))


    def __repr__(self):
        return f"Owner Name: {self.name}"
############################################

        # VIEWS WITH FORMS

##########################################
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_pup():
    form = AddForm()

    if form.validate_on_submit():
        new_pup = Puppy(
            name=form.name.data,
            age=form.age.data,
            gender=form.gender.data,
            aptitude=form.aptitude.data,
            tricks=form.tricks.data)

        sql = (
            f"Insert into puppies (name, age, gender, color, size, weight, aptitude, tricks, favorite_food) "
            f"values ('{form.name.data}', '{form.age.data}', '{form.gender.data}', '{form.color.data}', "
            f"'{form.size.data}', '{form.weight.data}', '{form.aptitude.data}', "
            f"'{form.tricks.data}', '{form.favorite_food.data}');"
        )
        #repr(eval(sql))
        db.engine.execute(sql)

        return redirect(url_for("index"))
    else:
        return render_template('add.html', form=form)

@app.route('/add_owner', methods=['GET', 'POST'])
def add_owner():
    form = AddOwnerForm()

    if form.validate_on_submit():
        new_owner = Owner(
            name=form.name.data,
            puppy_id=form.puppy_id.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data)


        sql = (
            f"Insert into owners (name, puppy_id, address, city, state, phone) "
            f"values ('{form.name.data}', '{form.puppy_id.data}', '{form.address.data}', '{form.city.data}', "
            f"'{form.state.data}', '{form.phone.data}');"
        )
        db.engine.execute(sql)

        return redirect(url_for('list_pup'))
    else:
        return render_template('add_owner.html',form=form)

@app.route('/list')
def list_pup():
    # Grab a list of puppies from database.
    puppies = Puppy.query.all()
    return render_template('list.html', puppies=puppies)

@app.route('/delete', methods=['GET', 'POST'])
def del_pup():

    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        pup = Puppy.query.get(id)
        db.session.delete(pup)
        db.session.commit()

        return redirect(url_for('list_pup'))
    return render_template('delete.html',form=form)


@app.route("/pup-csv")
def pup_csv():

    with open("samplepup.csv", "rt") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row:
                continue
            name = row.get("name", "")
            gender = row.get("gender", "")
            age = row.get("age", "")
            color = row.get("color", "")
            size = row.get("size", "")
            weight = row.get("weight", "")
            aptitude = row.get("aptitude", "")
            tricks = row.get("tricks", "")
            favorite_food = row.get("favorite_food", "")

            sql = (
                f"Insert into puppies (name, age, gender, color, size, weight, aptitude, tricks, favorite_food) "
                f"values ('{name}', '{age}', '{gender}', '{color}', '{size}', '{weight}', '{aptitude}', '{tricks}', '{favorite_food}');"
            )
            db.engine.execute(sql)

    return redirect(url_for("index"))

@app.route("/owner-csv")
def owner_csv():

    with open("sampleowner.csv", "rt") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row:
                continue
            name = row.get("name", "")
            puppy_id = row.get("puppy_id", "")
            address = row.get("address", "")
            city = row.get("city", "")
            state = row.get("state", "")
            phone = row.get("phone", "")

            sql = (
                f"Insert into owners (name, puppy_id, address, city, state, phone) "
                f"values ('{name}', '{puppy_id}', '{address}', '{city}', '{state}', '{phone}');"
            )
            db.engine.execute(sql)

    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
