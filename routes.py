from flask import Blueprint, render_template, request, redirect, url_for, flash
from data import db, Transaction, Split, Account, Slot, TransactionAutoUpdate
from forms import TransactionAutoUpdateForm

# Create a Blueprint for the main routes
main = Blueprint('main', __name__)

@main.route('/')
def index():
    transaction_auto_updates = TransactionAutoUpdate.query.all()
    return render_template('index.html', transaction_auto_updates=transaction_auto_updates)

@main.route('/add', methods=['GET', 'POST'])
def add_transaction_auto_update():
    form = TransactionAutoUpdateForm()
    form.bank_account.choices = [(a.guid, a.name) for a in Account.query.order_by(Account.name).all()]
    form.other_account.choices = [(a.guid, a.name) for a in Account.query.order_by(Account.name).all()]
    
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
        return redirect(url_for('main.index'))
    
    return render_template('add_transaction_auto_update.html', form=form)

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_transaction_auto_update(id):
    update = TransactionAutoUpdate.query.get_or_404(id)
    form = TransactionAutoUpdateForm(obj=update)
    form.bank_account.choices = [(a.guid, a.name) for a in Account.query.order_by(Account.name).all()]
    form.other_account.choices = [(a.guid, a.name) for a in Account.query.order_by(Account.name).all()]
    
    if form.validate_on_submit():
        update.bank_account = form.bank_account.data
        update.description = form.description.data
        update.notes = form.notes.data
        update.memo_bank_split = form.memo_bank_split.data
        update.memo_other_split = form.memo_other_split.data
        update.other_account = form.other_account.data
        update.search_term = form.search_term.data
        db.session.commit()
        flash('Transaction Auto Update updated successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('edit_transaction_auto_update.html', form=form, update=update)

@main.route('/delete/<int:id>', methods=['POST'])
def delete_transaction_auto_update(id):
    update = TransactionAutoUpdate.query.get_or_404(id)
    db.session.delete(update)
    db.session.commit()
    flash('Transaction Auto Update deleted successfully!', 'success')
    return redirect(url_for('main.index'))

@main.route('/update_transactions', methods=['POST'])
def update_transactions():
    # Retrieve date range and process transactions based on search terms
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    if not start_date or not end_date:
        flash('Please provide both start and end dates.', 'danger')
        return redirect(url_for('main.index'))
    
    total_updated_transactions = 0

    # Iterate over all transaction auto updates
    transaction_auto_updates = TransactionAutoUpdate.query.all()
    for update in transaction_auto_updates:
        # Sort and concatenate bank_account and other_account GUIDs with a hyphen
        update_guids = sorted([update.bank_account, update.other_account])
        update_guid_str = '-'.join(update_guids)

        # Filter transactions based on search term and date range
        transactions = Transaction.query.filter(
            Transaction.post_date >= start_date, 
            Transaction.post_date <= end_date, 
            Transaction.description.ilike(f"%{update.search_term}%")
            ).all()

        # Iterate over the filtered transactions
        for txn in transactions:
             # Get all splits for the transaction
            splits = Split.query.filter_by(tx_guid=txn.guid).all()

            # Sort and concatenate the account_guid of each split with a hyphen
            split_guids = sorted([split.account_guid for split in splits])
            split_guid_str = '-'.join(split_guids)

            # Compare the concatenated GUID string from TransactionAutoUpdate with the one from the splits
            if update_guid_str == split_guid_str:
                # If the concatenated strings match, proceed with updating the transaction
                txn.description = update.description
                note = Slot.query.filter_by(obj_guid=txn.guid, name='notes').first()
                if note:
                    note.string_val = update.notes

                # Update split memos only for non-reconciled transactions
                for split in splits:
                    if split.account_guid == update.bank_account:
                        if split.reconcile_state == 'c': # Only update if checked
                            split.memo = update.memo_bank_split
                    elif split.account_guid == update.other_account:
                        if split.reconcile_state == 'n':  # Only update if not reconciled
                            split.memo = update.memo_other_split

                # Update updated transactions count            
                total_updated_transactions += 1

                # Commit changes to the transaction and its splits
                db.session.commit()
    
    # Flash message indicating how many transactions were updated
    flash(f'Total number of transactions updated: {total_updated_transactions}', 'success')

    return redirect(url_for('main.index'))