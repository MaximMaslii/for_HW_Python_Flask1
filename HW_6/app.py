from pydantic import BaseModel
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from typing import List

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float

class ProductRead(ProductCreate):
    id: int

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    order_date: str
    status: str

class OrderRead(OrderCreate):
    id: int

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UserRead(UserCreate):
    id: int


# Модель для таблицы товаров
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

# Модель для таблицы заказов
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    order_date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)

# Модель для таблицы пользователей
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Создание таблиц в базе данных
db.create_all()

# CRUD операции для каждой таблицы
# Create
def create_item(model, data):
    try:
        item = model(**data)
        db.session.add(item)
        db.session.commit()
        return item
    except IntegrityError:
        db.session.rollback()
        return None

# Read All
def get_all_items(model):
    items = model.query.all()
    return items

# Read One
def get_item_by_id(model, item_id):
    item = model.query.get(item_id)
    return item

# Update
def update_item(model, item_id, data):
    item = model.query.get(item_id)
    if item:
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        return item
    return None

# Delete
def delete_item(model, item_id):
    item = model.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return item
    return None

# Маршруты для товаров
@app.route('/products', methods=['GET'])
def get_all_products():
    products = get_all_items(Product)
    return jsonify([ProductRead.from_orm(product).dict() for product in products])

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = get_item_by_id(Product, product_id)
    if product:
        return jsonify(ProductRead.from_orm(product).dict())
    return jsonify({'error': 'Product not found'}), 404

@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    product = create_item(Product, data)
    if product:
        return jsonify(ProductRead.from_orm(product).dict()), 201
    return jsonify({'error': 'Product creation failed'}), 400

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    product = update_item(Product, product_id, data)
    if product:
        return jsonify(ProductRead.from_orm(product).dict())
    return jsonify({'error': 'Product not found'}), 404

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = delete_item(Product, product_id)
    if product:
        return jsonify(ProductRead.from_orm(product).dict())
    return jsonify({'error': 'Product not found'}), 404

# Маршруты для заказов
@app.route('/orders', methods=['GET'])
def get_all_orders():
    orders = get_all_items(Order)
    return jsonify([OrderRead.from_orm(order).dict() for order in orders])

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = get_item_by_id(Order, order_id)
    if order:
        return jsonify(OrderRead.from_orm(order).dict())
    return jsonify({'error': 'Order not found'}), 404

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    order = create_item(Order, data)
    if order:
        return jsonify(OrderRead.from_orm(order).dict()), 201
    return jsonify({'error': 'Order creation failed'}), 400

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.json
    order = update_item(Order, order_id, data)
    if order:
        return jsonify(OrderRead.from_orm(order).dict())
    return jsonify({'error': 'Order not found'}), 404

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = delete_item(Order, order_id)
    if order:
        return jsonify(OrderRead.from_orm(order).dict())
    return jsonify({'error': 'Order not found'}), 404

# Маршруты для пользователей
@app.route('/users', methods=['GET'])
def get_all_users():
    users = get_all_items(User)
    return jsonify([UserRead.from_orm(user).dict() for user in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_item_by_id(User, user_id)
    if user:
        return jsonify(UserRead.from_orm(user).dict())
    return jsonify({'error': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = create_item(User, data)
    if user:
        return jsonify(UserRead.from_orm(user).dict()), 201
    return jsonify({'error': 'User creation failed'}), 400

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = update_item(User, user_id, data)
    if user:
        return jsonify(UserRead.from_orm(user).dict())
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = delete_item(User, user_id)
    if user:
        return jsonify(UserRead.from_orm(user).dict())
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)