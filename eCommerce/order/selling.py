from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from models import Item

selling = Blueprint('selling', __name__)

@selling.route('/create-listing')
@login_required
def listing():
    return render_template('order/listing.html')

@selling.route('/create-listing', methods=['POST'])
@login_required
def listing_post():
    itemname = request.form.get('itemname')
    price = request.form.get('price')
    imageurl = request.form.get('imageurl')
    description = request.form.get('description')
    qty = request.form.get('qty')

    item = Item(itemname=itemname, merchant_id=current_user.id, price=price, imageurl=imageurl, description=description, qty=qty)
    db.session.add(item)    
    db.session.commit()
    
    return redirect(url_for('user_profile.profile'))

@selling.route('/inventory/item/<item_id>')
@login_required
def view_item(item_id):
    item = Item.query.filter_by(id=item_id).first()

    if (current_user.id == item.merchant_id):
        return render_template('order/inventory.html',
            itemname=item.itemname,
            imageurl=item.imageurl,
            description=item.description,
            price="{:,.2f}".format(item.price),
            qty=item.qty
        )
    else:
        return render_template('permission_error.html')

@selling.route('/inventory/item/<item_id>/edit')
@login_required
def edit_item(item_id):
    item = Item.query.filter_by(id=item_id).first()

    if (current_user.id == item.merchant_id):
        return render_template('order/inventory.html',
            itemname=item.itemname,
            imageurl=item.imageurl,
            description=item.description,
            price="{:,.2f}".format(item.price),
            qty=item.qty
        )
    else:
        return render_template('permission_error.html')