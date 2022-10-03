import json

from config import db

from models import User, Order, Offer

path_users = './data/users.json'
path_orders = './data/orders.json'
path_offers = './data/offers.json'


def table_filler(path: str, cls: any):
	"""
	Функция заполнения таблиц
	:param path: путь к файлу json с данными
	:param cls: укажите название класса таблицы
	"""
	with open(path, 'r', encoding='utf-8') as file:
		data = json.load(file)
		for row in data:
			db.session.add(cls(**row))
		db.session.commit()


def init_db():
	db.drop_all()
	db.create_all()
	table_filler(path_users, User)
	table_filler(path_orders, Order)
	table_filler(path_offers, Offer)