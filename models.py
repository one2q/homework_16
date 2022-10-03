from config import db


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
