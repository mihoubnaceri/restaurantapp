from flask import Flask,render_template,url_for,request,redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databasesetup import Base,Restaurant,MenuItem

app = Flask(__name__)
engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



@app.route("/")
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


if __name__ =="__main__":
    app.debug=True
    app.run(host='0.0.0.0',port=5000)
