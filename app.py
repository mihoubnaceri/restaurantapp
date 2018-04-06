from flask import Flask,render_template,url_for,request,redirect,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databasesetup import Base,Restaurant,MenuItem

app = Flask(__name__)
engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



@app.route("/")
@app.route("/restaurants/")
def index():
    restaurants = session.query(Restaurant).all()

    return render_template("index.html",restaurants=restaurants)


@app.route("/restaurants/add",methods=['GET', 'POST'])
def add_resto():
    if request.method == "POST":

        name = request.form.get('resto')
        if name:
            print(name)
            restaurant = Restaurant(name=name)
            session.add(restaurant)
            session.commit()
            return redirect(url_for('index'))
        else:
            return render_template("add_resto_form.html")
    else:
        return render_template("add_resto_form.html")
@app.route("/restaurants/<int:restaurant_id>/edit",methods=['GET', 'POST'])
def edit_resto(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":

        name = request.form.get('resto')
        if name:
            print(name)
            restaurant.name = name
            session.add(restaurant)
            session.commit()
            return redirect(url_for('index'))
        else:
            return render_template("edit_resto.html",restaurant=restaurant)
    else:
        return render_template("edit_resto.html",restaurant=restaurant)

@app.route("/restaurants/<int:restaurant_id>/delete",methods=['GET', 'POST'])
def delete_resto(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        session.delete(restaurant)
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template("delete_resto.html",restaurant=restaurant)

@app.route("/restaurants/<int:restaurant_id>/",methods=['GET', 'POST'])
@app.route("/restaurants/<int:restaurant_id>/menu/",methods=['GET', 'POST'])
def resto_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()

    return render_template("restaurant_detail.html",restaurant=restaurant,items=items)
@app.route("/restaurants/<int:restaurant_id>/menu/add",methods=['GET', 'POST'])
def add_to_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        name = request.form.get("name")
        course = request.form.get("course")
        price = request.form.get("price")
        restaurant_id = restaurant.id
        description = request.form.get("description")
        newitem = MenuItem(name=name,course=course,price=price,restaurant_id=restaurant_id,description=description)
        session.add(newitem)
        session.commit()
        return redirect(url_for('resto_menu',restaurant_id=restaurant_id))
    else:

        return render_template("add_to_menu.html",restaurant=restaurant)

@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit",methods=['GET', 'POST'])
def edit_menu_item(restaurant_id,menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(restaurant=restaurant,id=menu_id).one()
    if request.method == "POST":
        item.name = request.form.get("name")
        item.course = request.form.get("course")
        item.price = request.form.get("price")
        item.description = request.form.get("description")
        session.add(item)
        session.commit()
        return redirect(url_for('resto_menu',restaurant_id=restaurant.id))
    return render_template("edit_menu_item.html",item=item,restaurant=restaurant)
@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete",methods=['GET', 'POST'])
def delete_menu_item(restaurant_id,menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(restaurant=restaurant,id=menu_id).one()
    if request.method == "POST":
        session.delete(item)
        session.commit()
        return redirect(url_for('resto_menu',restaurant_id=restaurant.id))
    return render_template("delete_menu_item.html",item=item,restaurant=restaurant)
@app.route("/restaurants/<int:restaurant_id>/menu/JSON",methods=['GET', 'POST'])
def resto_menu_JSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])
@app.route("/restaurants/JSON",methods=['GET', 'POST'])
def restoJSON():
    restaurants = session.query(Restaurant).all()

    return jsonify(Restaurants=[i.serialize for i in restaurants])


@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON",methods=['GET', 'POST'])
def menuitemJSON(restaurant_id,menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(restaurant=restaurant,id=menu_id).one()
    return jsonify(Menuitem=item.serialize)
if __name__ =="__main__":
    app.debug=True
    app.run(host='0.0.0.0',port=5000)
