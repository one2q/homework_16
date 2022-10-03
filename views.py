import json

from config import app
from utils import init_db
from models import *
from flask import request


@app.route('/users', methods=['GET', 'POST'])
def users_page():
	if request.method == 'GET':
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
		return app.response_class(json.dumps(result),
		                          mimetype='application.json',
		                          status=200)
	elif request.method == 'POST':
		data = request.json
		try:
			user = User(**data)
			db.session.add(user)
			db.session.commit()
			return f'{user} added'
		except Exception as e:
			print(e)


@app.route('/users/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def user_page(pk):
	if request.method == 'GET':
		user = User.query.get(pk)
		if user is None:
			return app.response_class('No data 404', status=404)
		return app.response_class(json.dumps({
			"id": user.id,
			"first_name": user.first_name,
			"last_name": user.last_name,
			"age": user.age,
			"email": user.email,
			"role": user.role,
			"phone": user.phone
		}), mimetype='application.json', status=200)
	elif request.method == 'PUT':
		data = request.json
		db.session.execute(db.update(User).where(User.id == pk).values(**data))
		db.session.commit()
		return app.response_class(json.dumps(data),
		                          mimetype='application.json',
		                          status=200)
	elif request.method == 'DELETE':
		user = User.query.get(pk)
		db.session.delete(user)
		db.session.commit()
		return 200


if __name__ == "__main__":
	init_db()
	app.run(debug=True, port=8000)
