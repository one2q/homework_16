import json

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JSON_AS_ASCII'] = False

# ????
app.url_map.strict_slashes = False

db = SQLAlchemy(app)

db.init_app(app)
app.app_context().push()

path_users = './data/users.json'
path_orders = './data/orders.json'
path_offers = './data/offers.json'


class User(db.Model):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String)
	last_name = db.Column(db.String)
	age = db.Column(db.Integer)
	email = db.Column(db.String)
	role = db.Column(db.String)
	phone = db.Column(db.Integer)


class Order(db.Model):
	__tablename__ = "order"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	description = db.Column(db.String)
	start_date = db.Column(db.Integer)
	end_date = db.Column(db.Integer)
	address = db.Column(db.String)
	price = db.Column(db.Integer)
	customer_id = db.Column(db.Integer)
	executor_id = db.Column(db.Integer)

# offer = db.relationship("Offer")


class Offer(db.Model):
	__tablename__ = "offer"
	id = db.Column(db.Integer, primary_key=True)
	order_id = db.Column(db.Integer)  # , db.ForeignKey("order.id"))
	executor_id = db.Column(db.Integer)  # , db.ForeignKey("order.executor_id"))

# order = relationship("Order")


db.create_all()  # Создать таблицы
# db.drop_all()  # Удалить таблицы


def table_filler(path: str, cls):
	"""
	Функция заполнения таблиц
	:param path: путь к файлу json с данными
	:param cls: укажите название класса таблицы
	"""
	with open(path, 'r', encoding='utf-8') as file:
		data = json.load(file)
		for user_data in data:
			user = cls(**user_data)
			# user = User(id=user_data.id, first_name=user_data.first_name,
			#             last_name=user_data.last_name, age=user_data.age,
			#             email=user_data.email, role=user_data.role, phone=user_data.phone)
			db.session.add(user)
		db.session.commit()

	# print(data)
	# print(type(data[0]))


@app.get('/users')
def get_all_users():
	users = User.query.all()
	result = []
	for user in users:
		result.append({
			"id": user.id,
			"first_name": user.first_name,
			"last_name": user.last_name,
			"age": user.age,
			"email": user.email,
			"role": user.role,
			"phone": user.phone
		})

	return json.dumps(result)


@app.get('/users/<int:pk>')
def get_user_by_pk(pk):
	user = User.query.get(pk)
	if user is None:
		return "Thi user is not found"
	return json.dumps({
		"id": user.id,
		"first_name": user.first_name,
		"last_name": user.last_name,
		"age": user.age,
		"email": user.email,
		"role": user.role,
		"phone": user.phone
	})


@app.get('/orders')
def get_orders():
	orders = Order.query.all()
	result = []
	for order in orders:
		result.append({
			"id": order.id,
			"name": order.name,
			"description": order.description,
			"start_date": order.start_date,
			"end_date": order.end_date,
			"address": order.address,
			"price": order.price,
			"customer_id": order.customer_id,
			"executor_id": order.executor_id
		})
	return json.dumps(result, ensure_ascii=False)


@app.get('/orders/<int:pk>')
def get_order_by_pk(pk):
	order = Order.query.get(pk)
	if order is None:
		return "Thi order is not found"
	return json.dumps({
			"id": order.id,
			"name": order.name,
			"description": order.description,
			"start_date": order.start_date,
			"end_date": order.end_date,
			"address": order.address,
			"price": order.price,
			"customer_id": order.customer_id,
			"executor_id": order.executor_id
	}, ensure_ascii=False)


@app.get('/offers')
def get_all_offers():
	offers = Offer.query.all()
	result = []
	for offer in offers:
		result.append({
			"id": offer.id,
			"order_id": offer.order_id,
			"executor_id": offer.executor_id,
			})
	return json.dumps(result)


@app.get('/offers/<int:pk>')
def get_offer_by_pk(pk):
	offer = Offer.query.get(pk)
	if offer is None:
		return "Thi offer is not found"
	return json.dumps({
			"id": offer.id,
			"order_id": offer.order_id,
			"executor_id": offer.executor_id,
	})


if __name__ == '__main__':
	app.run(debug=True)
