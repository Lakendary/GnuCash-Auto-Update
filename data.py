from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transaction(db.Model):
    __tablename__ = 'transactions'
    guid = db.Column(db.String, primary_key=True)
    post_date = db.Column(db.Date)
    description = db.Column(db.String)
    splits = db.relationship('Split', backref='transaction', lazy=True)
    slot = db.relationship('Slot', backref='transaction', uselist=False)

class Split(db.Model):
    __tablename__ = 'splits'
    guid = db.Column(db.String, primary_key=True)
    tx_guid = db.Column(db.String, db.ForeignKey('transactions.guid'), nullable=False)
    account_guid = db.Column(db.String, db.ForeignKey('accounts.guid'), nullable=False)
    memo = db.Column(db.String)
    reconcile_state = db.Column(db.String)
    value_num = db.Column(db.Numeric)
    account = db.relationship('Account', backref='splits', lazy=True)

class Account(db.Model):
    __tablename__ = 'accounts'
    guid = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    code = db.Column(db.String)

class Slot(db.Model):
    __tablename__ = 'slots'
    id = db.Column(db.Integer, primary_key=True)
    obj_guid = db.Column(db.String, db.ForeignKey('transactions.guid'))
    name = db.Column(db.String)
    string_val = db.Column(db.String)
    
class TransactionAutoUpdate(db.Model):
    __tablename__ = 'transaction_auto_updates'
    id = db.Column(db.Integer, primary_key=True)
    bank_account = db.Column(db.String, db.ForeignKey('accounts.guid'))
    description = db.Column(db.String)
    notes = db.Column(db.String)
    memo_bank_split = db.Column(db.String)
    memo_other_split = db.Column(db.String)
    other_account = db.Column(db.String, db.ForeignKey('accounts.guid'))
    search_term = db.Column(db.String)