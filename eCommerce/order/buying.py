from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app import db
from models import Item, Order, OrderItem, User

import ast

buying = Blueprint('buying', __name__)

@buying.route('/checkout')
@login_required
def checkout():
    itemlist = request.args.getlist('itemlist')

    #Name, Qty, Total Cost, Grand Total Cost
    items = []
    grandtotalcost = 0
    for itemdata in itemlist:
        astdata = ast.literal_eval(itemdata)
        item = Item.query.filter_by(id=int(astdata["id"])).first()
        if (item == None):
            flash('Item ' + str(astdata["id"]) + ' does not exist. It may have been removed.')
        else:
            user = User.query.filter_by(id=item.merchant_id).first()
            if (user == None):
                flash('Supplier of this item no longer exist.')
            else:
                if (int(astdata["qty"]) > item.qty):
                    flash('Item ' + item.itemname + ' quantity ordered exceeds supply of ' + str(item.qty) + '.')
                else:
                    totalcost = item.price * int(astdata["qty"])
                    items.append({"id": item.id, "name": item.itemname, "qty": int(astdata["qty"]), "total": totalcost})
                    grandtotalcost += totalcost

    return render_template('order/checkout.html', items=items, grandtotalcost=grandtotalcost)


@buying.route('/receipt', methods=['POST'])
@login_required
def confirm_buy():
    address = request.form.get('address')
    checkoutlist = request.args.getlist('checkoutlist')

    items_bought = []
    grandtotalcost = 0

    order = Order(buyer_id=current_user.id, shipaddress=address)
    db.session.add(order)
    db.session.flush()

    for itemdata in checkoutlist:
        astdata = ast.literal_eval(itemdata)
    
        item = Item.query.filter_by(id=int(astdata["id"])).first()
        
        if (item == None):
            flash('Item ' + str(astdata["name"]) + ' no longer exist. It may have been removed.')
        else:
            user = User.query.filter_by(id=item.merchant_id).first()
            if (user == None):
                flash('Supplier of this item no longer exist.')
            else:
                if (int(astdata["qty"]) > item.qty):
                    flash('Item ' + item.itemname + ' quantity ordered exceeds supply of ' + str(item.qty) + '.')
                else:
                    qty_ordered = int(astdata["qty"])
                    totalcost = item.price * qty_ordered

                    if(totalcost <= current_user.credits):
                        current_user.credits -= totalcost
                        user.credits += totalcost
                        item.qty -= qty_ordered
                        db.session.flush()

                        items_bought.append({"id": item.id, "name": item.itemname, "qty": qty_ordered, "total": totalcost})
                        grandtotalcost += totalcost
                        
                        orderitem = OrderItem(item_id=item.id, order_id=order.id, qty_ordered=qty_ordered, cost=totalcost, name=item.itemname)
                        db.session.add(orderitem)
                        db.session.commit()
                    else:
                        flash('Item ' + item.itemname + ' x(' + str(qty_ordered) + ') cannot be bought because your credit is too low.')
    
    if (len(items_bought) == 0):
        db.session.delete(order)
        db.session.commit()
        return render_template('order/receipt.html', address="[Empty]", items_bought=items_bought, grandtotalcost=grandtotalcost)
    
    return render_template('order/receipt.html', address=order.shipaddress, items_bought=items_bought, grandtotalcost=grandtotalcost)


@buying.route('/order/item/<item_id>')
@login_required
def view_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    if (item == None):
        return render_template('purchase_error.html', itemid=item_id)

    return render_template('order/order.html',
        item_id = item_id,
        itemname=item.itemname,
        imageurl=item.imageurl,
        description=item.description,
        price="{:,.2f}".format(item.price),
        qty=item.qty
    )


@buying.route('/order/item/<item_id>', methods=['POST'])
@login_required
def buy_now(item_id):
    item = Item.query.filter_by(id=item_id).first()
    if (item == None):
        return render_template('purchase_error.html', itemid=item_id)

    merchant = User.query.filter_by(id=item.merchant_id).first()
    if (merchant == None):
        flash('Supplier for this item no longer exist.')
        return redirect(url_for('buying.view_item', item_id=item_id))

    qty = int(request.form.get('qty'))
    if (int(qty) > item.qty):
        flash('Quantity order exceeds the supply.')
        return redirect(url_for('buying.view_item', item_id=item_id))
    itemdata = {"id": item_id, "qty": qty}
    return redirect(url_for('buying.checkout', itemlist=[itemdata]))