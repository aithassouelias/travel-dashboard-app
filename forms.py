from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FileField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Optional

class AddTripForm(FlaskForm):
    title = StringField('Titre du voyage', validators=[DataRequired()])
    description = StringField('Résumé', validators=[Optional()])
    destination = StringField('Destination', validators=[DataRequired()])
    start_date = DateField('Début', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Fin', format='%Y-%m-%d', validators=[DataRequired()])
    image = FileField('Photo de couverture')
    submit = SubmitField('Ajouter le voyage')

class AddPOIForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    visit_date = DateField('Date de visite', format='%Y-%m-%d', validators=[DataRequired()])
    latitude = FloatField('Latitude', validators=[DataRequired()])
    longitude = FloatField('Longitude', validators=[DataRequired()])
    visited = SelectField('Statut', choices=[('0', 'À visiter'), ('1', 'Visité')], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Ajouter')
