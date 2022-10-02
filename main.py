import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] =True

app.config['JSON_AS_ASCII'] = False


db = SQLAlchemy(app)

db.init_app(app)
app.app_context().push()

#  Путь к json файлам для заполнения таблиц.
path_users = './data/users.json'
path_orders = './data/orders.json'
path_offers = './data/offers.json'


class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String)
	last_name = db.Column(db.String)
	age = db.Column(db.Integer)
	email = db.Column(db.String)
	role = db.Column(db.String)
	phone = db.Column(db.String)


class Order(db.Model):
	__tablename__ = 'order'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	description = db.Column(db.String)
	start_date = db.Column(db.Integer)
	end_date = db.Column(db.Integer)
	address = db.Column(db.String)
	price = db.Column(db.Integer)
	customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	customer = db.relationship('User', foreign_keys=[customer_id])
	executor = db.relationship('User', foreign_keys=[executor_id])


class Offer(db.Model):
	__tablename__ = 'offer'
	id = db.Column(db.Integer, primary_key=True)
	order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
	executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	order = db.relationship('Order', foreign_keys=[order_id])
	executor = db.relationship('User', foreign_keys=[executor_id])


db.create_all()  # Создать таблицы
# db.drop_all()  # Удалить таблицы


def table_filler(path: str, cls: any):
	"""
	Функция заполнения таблиц
	:param path: путь к файлу json с данными
	:param cls: укажите название класса таблицы
	"""
	with open(path, 'r', encoding='utf-8') as file:
		data = json.load(file)
		for user_data in data:
			user = cls(**user_data)
			db.session.add(user)
		db.session.commit()


# # Заполняем таблицы
# table_filler(path_users, User)
# table_filler(path_orders, Order)
# table_filler(path_offers, Offer)


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


#  Создание нового пользователя
@app.post('/users')
def add_user_to_users():
	data = request.json
	try:
		user = User(**data)
		db.session.add(user)
		db.session.commit()
		return f'{user} added'
	except:
		return 'Can not add this user'


@app.put('/users/<int:pk>')
def update_user_by_pk(pk):
	data = request.json

	db.session.execute(db.update(User).where(User.id == pk).values(**data))
	db.session.commit()
	return 'User updated'


@app.delete('/users/<int:pk>')
def delete_user_by_pk(pk):
	try:
		user = User.query.get(pk)
		db.session.delete(user)
		db.session.commit()
		return f'User{pk} deleted'
	except:
		return 'Такой пользователь не найден'


@app.post('/orders')
def add_order_to_orders():
	data = request.json
	try:
		order = Order(**data)
		db.session.add(order)
		db.session.commit()
		return f'{order} added'
	except:
		return 'Can not add this order'


@app.put('/order/<int:pk>')
def update_order_by_pk(pk):
	data = request.json

	db.session.execute(db.update(Order).where(Order.id == pk).values(**data))

	db.session.commit()
	return 'Order updated'


@app.delete('/orders/<int:pk>')
def delete_order_by_pk(pk):
	try:
		order = Order.query.get(pk)
		db.session.delete(order)
		db.session.commit()
		return f'Order{pk} deleted'
	except:
		return 'Такой заказ не найден'


@app.post('/offers')
def add_offer_to_offers():
	data = request.json
	try:
		offer = Offer(**data)
		db.session.add(offer)
		db.session.commit()
		return f'{offer} added'
	except:
		return 'Can not add this offer'


@app.put('/offer/<int:pk>')
def update_offer_by_pk(pk):
	data = request.json

	db.session.execute(db.update(Offer).where(Offer.id == pk).values(**data))

	db.session.commit()
	return 'Offer updated'


@app.delete('/offers/<int:pk>')
def delete_offer_by_pk(pk):
	try:
		offer = Offer.query.get(pk)
		db.session.delete(offer)
		db.session.commit()
		return f'Offer{pk} deleted'
	except:
		return 'Такое предложение не найдено'


if __name__ == '__main__':
	app.run(debug=True)
