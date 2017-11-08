from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/categories')
def showCategories():
    return 'This page displays all categories.'


@app.route('/category/add')
def addCategory():
    return 'This page is to add a new category'


@app.route('/category/<int:category_id>/edit')
def editCategory(category_id):
    return 'This page is to edit the category {}'.format(category_id)


@app.route('/category/<int:category_id>/delete')
def deleteCategory(category_id):
    return 'This page is to delete the category {}'.format(category_id)

@app.route('/category/<int:category_id>')
@app.route('/category/<int:category_id>/items')
def showItems(category_id):
    return 'This page is to display all items of the category {}'\
           .format(category_id)


@app.route('/category/<int:category_id>/item/add')
def addItem(category_id):
    return 'This page is to add an item to the category {}'\
           .format(category_id)


@app.route('/category/<int:category_id>/item/<int:item_id>')
@app.route('/category/<int:category_id>/item/<int:item_id>/details')
def showItemDetails(category_id, item_id):
    return 'This page is to show details of item {} of the category {}'\
           .format(category_id, item_id)


@app.route('/category/<int:category_id>/item/<int:item_id>/edit')
def editItem(category_id, item_id):
    return 'This page is to edit item {} of the category {}'\
           .format(category_id, item_id)


@app.route('/category/<int:category_id>/item/<int:item_id>/delete')
def deleteItem(category_id, item_id):
    return 'This page is to delete item {} of the category {}'\
           .format(category_id, item_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8100)
