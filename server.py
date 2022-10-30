from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from waitress import serve
from dotenv import load_dotenv
import os

load_dotenv()
api = Flask(__name__)

api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(api)

class DataModel(db.Model):
    tag = db.Column(db.String, primary_key=True)
    use_count = db.Column(db.Integer)
    def update(self) -> int:
        self.use_count += 1
        db.session.commit()
        return self.use_count

@api.before_first_request
def create_all():
    db.create_all()
    
@api.route('/update_tag', methods=["GET"])
def update_tag():
    tag = request.args.get("tag")
    if tag is not None:
        tag_model = DataModel.query.filter_by(tag = tag).first()
        if tag_model is not None:
            return make_response(f"{tag_model.update()}", 200)
        else:
            return make_response(f"Tag does not exist!", 404)
    return make_response("Invalid Data", 400)

@api.route('/get_tag', methods=["GET"])
def get_tag():
    tag = request.args.get("tag")
    if tag is not None:
        tag_model = DataModel.query.filter_by(tag = tag).first()
        if tag_model is not None:
            return make_response(f"{tag_model.use_count}", 200)
        else:
            return make_response(f"Tag does not exist!", 404)
    return make_response("Invalid Data", 400)

@api.route('/create_tag', methods=["GET"])
def create_tag():
    tag = request.args.get("tag")
    if tag is not None:
        tag_model = DataModel(tag=tag, use_count=0)
        db.session.add(tag_model)
        db.session.commit()
        return make_response("Tag Created Successfully", 200)
    return make_response("Invalid Data", 400)

if __name__ == "__main__":
    serve(app=api, host=os.getenv('HOST'), port=os.getenv('PORT'))