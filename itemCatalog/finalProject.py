from flask import Flask, render_template

app = Flask(__name__)

#Fake data
categories = [{'name':'Cricket', 'description':'Gentlemens Game', 'id':1}
              ,{'name':'Football', 'description':'Worlds top game', 'id':2}
              ,{'name':'Hockey', 'description':'Hockey desc', 'id':3}
              ,{'name':'Baseball', 'description':'Tall players', 'id':4}]

category = {'name':'Cricket', 'description':'Gentlemens Game', 'id':1}

items = [{'name':'Bat', 'description':'Gentlemens Game', 'id':1, 'category_id':1}
         ,{'name':'Ball', 'description':'Gentlemens Game', 'id':1, 'category_id':1}
         ,{'name':'Stumps', 'description':'Gentlemens Game', 'id':1, 'category_id':1}
         ,{'name':'Pads', 'description':'Gentlemens Game', 'id':1, 'category_id':1}]


@app.route('/')
@app.route('/categories')
def showCategories():
    #return 'This page displays all categories.'
    return render_template("categories.html", categories = categories)


@app.route('/category/add')
def addCategory():
    #return 'This page is to add a new category'
    return render_template("addCategory.html")


@app.route('/category/<int:category_id>/edit')
def editCategory(category_id):
    #return 'This page is to edit the category {}'.format(category_id)
    return render_template("editCategory.html", category = category)


@app.route('/category/<int:category_id>/delete')
def deleteCategory(category_id):
    #return 'This page is to delete the category {}'.format(category_id)
    return render_template("deleteCategory.html", category = category)

@app.route('/category/<int:category_id>')
@app.route('/category/<int:category_id>/items')
def showItems(category_id):
    #return 'This page is to display all items of the category {}'.format(category_id)
    return render_template("showItems.html", category = category, items = items)


@app.route('/category/<int:category_id>/item/add')
def addItem(category_id):
    #return 'This page is to add an item to the category {}'.format(category_id)
    return render_template("addItem.html", category = category)


@app.route('/category/<int:category_id>/item/<int:item_id>')
@app.route('/category/<int:category_id>/item/<int:item_id>/details')
def showItemDetails(category_id, item_id):
    #return 'This page is to show details of item {} of the category {}'.format(category_id, item_id)
    return render_template("items.html", category = category, items = items)


@app.route('/category/<int:category_id>/item/<int:item_id>/edit')
def editItem(category_id, item_id):
    #return 'This page is to edit item {} of the category {}'.format(category_id, item_id)
    return render_template("editItem.html", category = category, item = items[item_id])


@app.route('/category/<int:category_id>/item/<int:item_id>/delete')
def deleteItem(category_id, item_id):
    #return 'This page is to delete item {} of the category {}'.format(category_id, item_id)
    return render_template("deleteItem.html", category = category, item = items[item_id])


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8100)
