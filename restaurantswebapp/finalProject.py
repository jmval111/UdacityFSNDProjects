from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template("restaurants.html", restaurants = restaurants)


@app.route('/restaurant/new', methods=['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'], location=request.form['location'], description=request.form['description'])
        session.add(newRestaurant)
        session.commit()
        flash("New Restaurant \"{}\" Created!".format(newRestaurant.name))
        return redirect(url_for('showRestaurants'))
    else:
        return render_template("newRestaurant.html")

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    if editedRestaurant is None:
            return render_template('404.html'),404
    if request.method == 'POST':
        print('in editRestaurant post')
        editedRestaurant.name=request.form['name']
        editedRestaurant.location=request.form['location']
        editedRestaurant.description=request.form['description']
        session.add(editedRestaurant)
        session.commit()
        flash("Restaurant \"{}\", Successfully Edited".format(editedRestaurant.name))
        return redirect(url_for('showRestaurants'))
    else:
        return render_template("editRestaurant.html", restaurant=editedRestaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    deletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    if deletedRestaurant is None:
            return render_template('404.html'),404
    if request.method == 'POST':
        session.delete(deletedRestaurant)
        session.commit()
        flash("Restaurant \"{}\", Successfully Deleted!".format(deletedRestaurant.name))
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant = deletedRestaurant)
    

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    if restaurant is None:
            return render_template('404.html'),404
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).order_by(MenuItem.course).all()
    if items is None:
        print("No items found!")
    return render_template("menu.html",restaurant = restaurant, items = items)


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    if restaurant is None:
            return render_template('404.html'),404
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'],
                           restaurant_id = restaurant_id,
                           description = request.form['description'],
                           course = request.form['course'])
        session.add(newItem)
        session.commit()
        flash("New Menu Item \"{}\" Created!".format(newItem.name))
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).first()
    if editedItem is None:
            return render_template('404.html'),404
    if request.method == 'POST':
        editedItem.name = request.form['name']
        editedItem.description = request.form['description']
        editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        flash("Menu Item \"{}\", Successfully Edited!".format(editedItem.name))
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template('editMenuItem.html', restaurant = restaurant, item = editedItem)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).first()
    if deletedItem is None:
            return render_template('404.html'),404
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("Menu Item \"{}\", Successfully Deleted!".format(deletedItem.name))
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template("deleteMenuItem.html",restaurant = restaurant, item = deletedItem)


@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def MenuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id = menu_id).one()
    return jsonify(MenuItem=item.serialize)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.debug = True
    app.secret_key="supersecret"
    app.run(host = '0.0.0.0', port = 8100)
