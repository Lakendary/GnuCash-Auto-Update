from flask import Flask, render_template, request, redirect, url_for, flash
from data import db, Transaction, Split, Account, Slot, TransactionAutoUpdate
from forms import TransactionAutoUpdateForm
from configparser import ConfigParser

def get_config():
    config = ConfigParser()
    config.read('config.ini')
    return config

config = get_config()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['database']['uri']
app.config['SECRET_KEY'] = config['secret']['key']
db.init_app(app)

@app.route('/')
def index():
    transaction_auto_updates = TransactionAutoUpdate.query.all()
    return render_template('index.html', transaction_auto_updates=transaction_auto_updates)

@app.route('/add', methods=['GET', 'POST'])
def add_transaction_auto_update():
    form = TransactionAutoUpdateForm()
    form.bank_account.choices = [(a.guid, a.name) for a in Account.query.all()]
    form.other_account.choices = [(a.guid, a.name) for a in Account.query.all()]
    
    if form.validate_on_submit():
        new_transaction_auto_update = TransactionAutoUpdate(
            bank_account=form.bank_account.data,
            description=form.description.data,
            notes=form.notes.data,
            memo_bank_split=form.memo_bank_split.data,
            memo_other_split=form.memo_other_split.data,
            other_account=form.other_account.data,
            search_term=form.search_term.data
        )
        db.session.add(new_transaction_auto_update)
        db.session.commit()
        flash('Transaction Auto Update added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_transaction_auto_update.html', form=form)

@app.route('/update_transactions', methods=['POST'])
def update_transactions():
    # Retrieve date range and process transactions based on search terms
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    
    transaction_auto_update = TransactionAutoUpdate.query.all()
    for update in transaction_auto_update:
        # Filter transactions based on search term and date range
        transactions = Transaction.query.filter(Transaction.post_date.between(start_date, end_date),
                                                Transaction.description.ilike(f"%{update.search_term}%")).all()
        for txn in transactions:
            txn.description = update.description
            note = Slot.query.filter_by(obj_guid=txn.guid, name='notes').first()
            if note:
                note.string_val = update.notes

            splits = Split.query.filter_by(tx_guid=txn.guid, reconcile_state='n').all()
            for split in splits:
                if split.account_guid == update.bank_account:
                    split.memo = update.memo_bank_split
                elif split.account_guid == update.other_account:
                    split.memo = update.memo_other_split
            
            db.session.commit()
    
    flash('Transactions updated successfully!', 'success')
    return redirect(url_for('index'))
