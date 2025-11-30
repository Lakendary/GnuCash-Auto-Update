from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class TransactionAutoUpdateForm(FlaskForm):
    bank_account = SelectField('Bank Account', choices=[], validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    notes = StringField('Notes')
    memo_bank_split = SelectField('Memo for Bank Split', choices=[
        ('Payment', 'Payment'), 
        ('Receipt', 'Receipt'),
        ('Transfer from BWK Current', 'Transfer from BWK Current'),
        ('Transfer to BWK Current', 'Transfer to BWK Current'),
        ('Transfer from FNB Current', 'Transfer from FNB Current'),
        ('Transfer to FNB Current', 'Transfer to FNB Current'),
        ('Transfer from FNB Credit Card', 'Transfer from FNB Credit Card'),
        ('Transfer to FNB Credit Card', 'Transfer to FNB Credit Card'),
        ('Transfer from BWK Savings', 'Transfer from BWK Savings'),
        ('Transfer to BWK Savings', 'Transfer to BWK Savings'),
        ('Transfer from FNB Savings', 'Transfer from FNB Savings'),
        ('Transfer to FNB Savings', 'Transfer to FNB Savings'),
        ('Transfer from FNB Habit Tracker', 'Transfer from FNB Habit Tracker'),
        ('Transfer to FNB Habit Tracker', 'Transfer to FNB Habit Tracker'),
        ('Transfer from FNB OLT', 'Transfer from FNB OLT'),
        ('Transfer to FNB OLT', 'Transfer to FNB OLT'),
        ('Transfer from FNB Big Savings', 'Transfer from FNB Big Savings'),
        ('Transfer to FNB Big Savings', 'Transfer to FNB Big Savings')
        ], validators=[DataRequired()])
    memo_other_split = StringField('Memo for Other Split', validators=[DataRequired()])
    other_account = SelectField('Other Account', choices=[], validators=[DataRequired()])
    search_term = StringField('Search Term', validators=[DataRequired()])
    submit = SubmitField('Save')
