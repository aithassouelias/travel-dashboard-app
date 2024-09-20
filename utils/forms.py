from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FileField, SubmitField, SelectField, FloatField, DateTimeField
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
    visited = SelectField('Statut', choices=[(0, 'À visiter'), (1, 'Visité')], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Ajouter')

class ModifyProfileForm(FlaskForm):
    username = StringField('Nom', validators=[DataRequired()])
    profile_picture = FileField('Photo de profil')
    user_id = StringField("Nom d'utilisateur", validators=[DataRequired()])
    date_of_birth = DateField('Date de naissance', format='%Y-%m-%d', validators=[DataRequired()])
    email = StringField('Nom', validators=[DataRequired()])
    submit = SubmitField('Modifier mon profil')


class AddUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Mot de passe', validators=[DataRequired()])
    date_of_birth = DateField('Date de naissance', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Créer mon compte')

