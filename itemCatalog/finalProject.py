from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/categories')
def showCategories():
    categories = session.query(Category).all()
    return render_template("categories.html", categories = categories)


@app.route('/category/add', methods = ['GET', 'POST'])
def addCategory():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        if not name:
            flash('Add CategoryError: Name can\'t be empty')
            return redirect(url_for('showCategories'))
        newCategory = Category(name = name, description = description)
        session.add(newCategory)
        session.commit()
        flash('Added Category \'{}\' Successfully!'.format(newCategory.name))
        return redirect(url_for('showCategories'))
    else:
        return render_template("addCategory.html")


@app.route('/category/<int:category_id>/edit', methods=['GET','POST'])
def editCategory(category_id):
    editedCategory = session.query(Category).filter_by(id = category_id).first()
    if not editedCategory:
        flash('Attempt to edit non-existent category')
        return redirect(url_for('showCategories'))
    
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
    
        if request.form['description']:
            editedCategory.description = request.form['description']
        else:
            editedCategory.description = ''
        session.add(editedCategory)
        session.commit()
        flash('Edited Category \'{}\'  Successfully'.format(editedCategory.name))
        return redirect(url_for('showCategories'))
    else:
        return render_template("editCategory.html", category = editedCategory)


@app.route('/category/<int:category_id>/delete', methods=['GET','POST'])
def deleteCategory(category_id):
    deletedCategory = session.query(Category).filter_by(id = category_id).first()
    if not deletedCategory:
        flash('Attempt to delete non-existent category')
        return redirect(url_for('showCategories'))

    if request.method == 'POST':
        session.delete(deletedCategory)
        session.commit()
        flash('Deleted Category \'{}\'  Successfully'.format(deletedCategory.name))
        return redirect(url_for('showCategories'))
    else:
        return render_template("deleteCategory.html", category = deletedCategory)

@app.route('/category/<int:category_id>', methods = ['GET', 'POST'])
@app.route('/category/<int:category_id>/items', methods = ['GET', 'POST'])
def showItems(category_id):
    category = session.query(Category).filter_by(id = category_id).first()
    if not category:
        flash('Attempt to view non-existent category')
        return redirect(url_for('showCategories'))
    
    items = session.query(Item).filter_by(category_id = category_id).all()
    return render_template("showItems.html", category = category, items = items)


@app.route('/category/<int:category_id>/item/add', methods = ['GET', 'POST'])
def addItem(category_id):
    category = session.query(Category).filter_by(id = category_id).first()
    if not category:
        flash('Attempted operation on non-existent category')
        return redirect(url_for('showCategories'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        if not name:
            flash('Add ItemError: Name can\'t be empty')
            return redirect(url_for('showItems', category_id = category_id))
        newItem = Item(name = name, description = description, category_id = category_id)
        session.add(newItem)
        session.commit()
        flash('Added Item \'{}\' Successfully!'.format(newItem.name))
        return redirect(url_for('showItems', category_id = category_id))
    else:
        return render_template("addItem.html", category = category)


@app.route('/category/<int:category_id>/item/<int:item_id>/edit', methods = ['GET', 'POST'])
def editItem(category_id, item_id):
    category = session.query(Category).filter_by(id = category_id).first()
    if not category:
        flash('Attempted operation on non-existent category')
        return redirect(url_for('showCategories'))
    
    editedItem = session.query(Item).filter_by(id = item_id, category_id = category_id).first()
    if not editedItem:
        flash('Attempt to edit non-existent item')
        return redirect(url_for('showItems', category_id = category_id))
    
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
    
        if request.form['description']:
            editedItem.description = request.form['description']
        else:
            editedItem.description = ''
        session.add(editedItem)
        session.commit()
        flash('Edited Item \'{}\'  Successfully'.format(editedItem.name))
        return redirect(url_for('showItems', category_id = category_id))
    else:
        return render_template("editItem.html", category = category, item = editedItem)
    


@app.route('/category/<int:category_id>/item/<int:item_id>/delete', methods = ['GET', 'POST'])
def deleteItem(category_id, item_id):
    category = session.query(Category).filter_by(id = category_id).first()
    if not category:
        flash('Attempted operation on non-existent category')
        return redirect(url_for('showCategories'))
    
    deletedItem = session.query(Item).filter_by(id = item_id, category_id = category_id).first()
    if not deletedItem:
        flash('Attempt to delete non-existent item')
        return redirect(url_for('showItems', category_id = category_id))

    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash('Deleted Item \'{}\'  Successfully'.format(deletedItem.name))
        return redirect(url_for('showItems', category_id = category_id))
    else:
        return render_template("deleteItem.html", category = deletedItem.category, item = deletedItem)
    


if __name__ == '__main__':
    app.debug = True
    app.secret_key = '\x87{\xfc\xc9\x94\x10.\x12$R\x1b\x8d\x8a\xe2\x81\x82\xc9vD\x15\x95\x85\xb0\x16'
    app.run(host = '0.0.0.0', port = 8100)
