from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db.init_app(app)

# Routes
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.order_by(Message.created_at).all()]
        return make_response(jsonify(messages), 200)

    elif request.method == 'POST':
        data = request.form
        new_message = Message(body=data.get('body'), username=data.get('username'))
        db.session.add(new_message)
        db.session.commit()
        message_dict = new_message.to_dict()
        return make_response(jsonify(message_dict), 201)

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def message_by_id(id):
    message = Message.query.get(id)

    if not message:
        return make_response(jsonify({'error': 'Message not found'}), 404)

    if request.method == 'PATCH':
        data = request.form
        message.body = data.get('body')
        db.session.commit()
        updated_message_dict = message.to_dict()
        return make_response(jsonify(updated_message_dict), 200)

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return make_response(jsonify({'message': 'Message deleted successfully'}), 200)

if __name__ == '__main__':
    app.run(port=5555)
