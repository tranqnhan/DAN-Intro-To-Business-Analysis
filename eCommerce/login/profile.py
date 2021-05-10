from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db
from models import Item, OrderItem, Order

user_profile = Blueprint('user_profile', __name__)

@user_profile.route('/profile')
@login_required
def profile():
    firstname = current_user.firstname
    lastname = current_user.lastname
    credits = current_user.credits

    #Reading item name, current stock, revenue
    inventorylist = []
    inventory = Item.query.filter_by(merchant_id=current_user.id).all()
    #Calculates revenue by orders
    for item in inventory:
        revenue = 0
        
        orderitems = OrderItem.query.filter_by(item_id=item.id).all()
        for orderitem in orderitems:
            revenue += orderitem.cost

        inventorylist.append([item.id, item.itemname, item.qty, revenue])

    orderhistorylist = []
    orders = Order.query.filter_by(buyer_id=current_user.id).all()
    for order in orders:
        grandtotalcost = 0

        orderitems = OrderItem.query.filter_by(order_id=order.id).all()
        for orderitem in orderitems:
            grandtotalcost += orderitem.cost
        
        orderhistorylist.append([order.id, grandtotalcost])

    return render_template('login/profile.html', firstname=firstname, lastname=lastname, credits=credits, inventory=inventorylist, orderhistory=orderhistorylist)

@user_profile.route('/profile/history/<order_id>')
def view_order_history(order_id):
    order = Order.query.filter_by(id=order_id).first()
    if (order.buyer_id != current_user.id):
        return render_template('permission_error.html')
    
    orderitemlist = []
    grandtotalcost = 0

    orderitems = OrderItem.query.filter_by(order_id=order.id).all()
    for orderitem in orderitems:
        grandtotalcost += orderitem.cost
        orderitemlist.append([orderitem.name, orderitem.qty_ordered, orderitem.cost])

    return render_template('order/order_history.html', order_id=order.id, address=order.shipaddress, grandtotalcost=grandtotalcost, orderitems=orderitemlist)


