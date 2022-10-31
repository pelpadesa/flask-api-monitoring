from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from waitress import serve
from dotenv import load_dotenv
from datetime import datetime
from functools import cache
import os
import getopt
import sys
 

load_dotenv()
api = Flask(__name__)

api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/data/tag-data.db'
api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(api)

class DataModel(db.Model):
    tag = db.Column(db.String, primary_key=True)
    use_count = db.Column(db.Integer)
    @cache
    def update(self) -> int:
        self.use_count += 1
        return self.use_count

class Change(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.String)

@api.before_first_request
def create_all():
    db.create_all()
    
@api.route('/update', methods=["GET"])
def update_tag():
    tag = request.args.get("tag")
    description = request.headers.get("description")
    if tag is not None:
        tag_model = DataModel.query.filter_by(tag = tag).first()
        if tag_model is not None:
            change_model = Change(tag=tag, description=description, date=datetime.utcnow())
            use_count = tag_model.update()

            db.session.add(change_model)
            db.session.commit()

            return make_response(f'{use_count}', 200)
        else:
            return make_response(f"Tag does not exist!", 404)
    return make_response("Invalid Data", 400)

@api.route('/get', methods=["GET"])
def get_tag():
    tag = request.args.get("tag")
    if tag is not None:
        tag_model = DataModel.query.filter_by(tag = tag).first()
        if tag_model is not None:
            return make_response(f"{tag_model.use_count}", 200)
        else:
            return make_response(f"Tag does not exist!", 404)
    return make_response("Invalid Data", 400)

@api.route('/create', methods=["GET"])
def create_tag():
    tag = request.args.get("tag")
    if tag is not None:
        tag_model = DataModel(tag=tag, use_count=0)
        db.session.add(tag_model)
        db.session.commit()

        return make_response("Tag Created Successfully", 200)
    return make_response("Invalid Data", 400)

@api.route('/history', methods=["GET"])
def tag_history():
    tag = request.args.get("tag")
    if tag is not None:
        changes = Change.query.filter_by(tag=tag).all()
        if changes is None: return make_response("Invalid Data!", 403)

        change_data = {}
        for change in changes:
            change_data[change.id] = {"description": change.description, "date": change.date}
        return jsonify(change_data)
    return make_response("Invalid Data!", 404)

if __name__ == "__main__":
    try:
        portValue = 80 # Default Value
        argumentList = sys.argv[1:]
        if len(argumentList) > 0:
            portValue = int(sys.argv[1:][0])
    except getopt.error as err:
        print(str(err))
    print(f"Serving on http://0.0.0.0:{portValue}")
    serve(app=api, host="0.0.0.0", port=portValue)