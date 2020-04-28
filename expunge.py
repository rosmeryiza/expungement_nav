from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
application = app

# Flask-Bootstrap requires this line
Bootstrap(app)
#app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = ''

# the name of the database; add path if necessary
db_name = 'expunge.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

# each table in the database needs a class to be created for it
# db.Model is required - don't change it
# identify all columns by name and data type
class Expunge(db.Model):
    __tablename__ = 'Expungement'
    id = db.Column(db.Integer, primary_key=True)
    State = db.Column(db.String)
    Law = db.Column(db.String)
    StatuteLink = db.Column(db.String)
    FirstEffective = db.Column(db.String)
    LatestAmendment = db.Column(db.String)
    Fee = db.Column(db.String)
    FeeMin = db.Column(db.String)
    FeeMax = db.Column(db.String)
    DrugOffenses = db.Column(db.String)
    Misdemeanors = db.Column(db.String)
    Felonies = db.Column(db.String)
    ViolentFelonies = db.Column(db.String)
    SexTrafficking = db.Column(db.String)
    WaitTime = db.Column(db.String)

# get state IDs and names for the select menu BELOW
states = Expunge.query.order_by(Expunge.State).all()

# create the list of tuples needed for the choices value
pairs_list = []
for state in states:
    pairs_list.append( (state.id, state.State) )

# Flask-WTF form magic
# set up the quickform - select includes value, option text (value matches db)
# all that is in this form is one select menu and one submit button
class StateForm(FlaskForm):
    select = SelectField( 'Choose a state:', choices=pairs_list, validators=[DataRequired()])
    submit = SubmitField('Submit')

# first route

@app.route('/')
def index():
    # make an instance of the WTF form class we created, above
    form = StateForm()
    # pass it to the template
    return render_template('index.html', form=form)
    
# second route
# whichever id comes from the form, that one sock will be displayed
@app.route('/state', methods=['POST'])
def state_detail():
    state_id = request.form['select']
    # get all columns for the one sock with the supplied id
    the_state = Expunge.query.filter_by(id=state_id).first()
    # pass them to the template
    return render_template('state.html', the_state=the_state)

# keep this as is
if __name__ == '__main__':
    app.run(debug=True)