from email import message
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
api = Api(app)
db = SQLAlchemy(app)

class VideoModels(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Video( name = {name}, views = {views}, likes = {likes})"

# the resource fields is used to serialize the data into a json object
# this is done by importing fields and marshal with from flask_restful
resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer
}

# video_put_args is used to ensure that proper data is sent to the 
# api as arguement, if not the help message would be sent as error
video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument(
    "views", type=int, help="video id is required", required=True)
video_put_args.add_argument(
    "likes", type=int, help="number of likes of the video is required",
    required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str)
video_update_args.add_argument("views", type=int)
video_update_args.add_argument("likes", type=int)

        
class Video(Resource):
    # the marshal_with decorator ensures that the returned value is serialized
    @marshal_with(resource_fields)
    def get(self, video_id):
        video = VideoModels.query.get(video_id)
        if video == None:
            abort(404, message="could not find video with that id")
        return video
    
    @marshal_with(resource_fields)
    def put(self, video_id):
        check = VideoModels.query.get(video_id)
        if check:
            abort(409, message="video id taken")
        args = video_put_args.parse_args()
        video = VideoModels(
            id = video_id,
            name = args["name"],
            views = args["views"],
            likes = args["likes"]
        )
        db.session.add(video)
        db.session.commit()
        
        return video, 201
    
    @marshal_with(resource_fields)
    def patch(self, video_id):
        video = VideoModels.query.get(video_id)
        if video == None:
            abort(404, message="video does not exist")
        args = video_update_args.parse_args()
        if args.get("name"):
            video.name = args.get("name")
        if args.get("likes"):
            video.likes = args["likes"]
        if args.get("views"):
            video.views = args["views"]
            
        db.session.add(video)
        db.session.commit()
        
        return video, 200
    
    def delete(self, video_id):
        abort_if_video_id_does_not_exist(video_id)
        del videos[video_id]
        return {"message": "deleted"}, 204
        
api.add_resource(Video, '/video/<int:video_id>')

if __name__ == '__main__':
    app.run(debug=True)