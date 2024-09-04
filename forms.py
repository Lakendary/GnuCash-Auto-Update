from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class TransactionAutoUpdateForm(FlaskForm):
    bank_account = SelectField('Bank Account', choices=[], validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    notes = StringField('Notes')
    memo_bank_split = SelectField('Memo for Bank Split', choices=[('Payment', 'Payment'), ('Receipt', 'Receipt')], validators=[DataRequired()])
    memo_other_split = StringField('Memo for Other Split', validators=[DataRequired()])
    other_account = SelectField('Other Account', choices=[], validators=[DataRequired()])
    search_term = StringField('Search Term', validators=[DataRequired()])
    submit = SubmitField('Save')
