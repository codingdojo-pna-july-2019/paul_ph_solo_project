import requests
import math
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy	
from flask_migrate import Migrate
from sqlalchemy.sql import func  

app = Flask(__name__)

# database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///solo_project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# an instance of the ORM
db = SQLAlchemy(app)

# a tool for allowing migrations/creation of tables
migrate = Migrate(app, db)


#### ADDING THIS CLASS ####
# the db.Model in parentheses tells SQLAlchemy that this class represents a table in our database

class City(db.Model):
    __tablename__ = "city"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())   
    updated_at = db.Column(db.DateTime, server_default=func.now(), 
    onupdate=func.now())

@app.route("/")
def main():
    
    # open weather API
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={},us&units=imperial&APPID=23760f78fd0e8fb5253b54257367f070"

    weather_data =[]
    cities = City.query.all()
    for city in cities:
        response = requests.get(api_url.format(city.city)).json()
        weather = {
            'id': city.id,
            'city' : city.city,
            'temperature' : response['main']['temp'],
            'description' : response['weather'][0]['description'],
            'icon' : response['weather'][0]['icon'],
    }
        weather_data.append(weather)
    return render_template("index.html", weather_data=weather_data, cities=cities)

@app.route("/add_city", methods=['POST'])
def add_city():
    new_city = City(
        city=request.form['city_name'],
     )
    print("adding new city to db:")
    print(new_city)
    db.session.add(new_city)
    db.session.commit()
    return redirect("/")

@app.route("/delete_city/<id>")
def delete_city(id):
    print("deleting new city to db:")
    city_delete = City.query.get(id)
    db.session.delete(city_delete)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)