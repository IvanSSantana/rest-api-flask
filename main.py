from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app, template_file='docs.yml') # Configurating the documentation

# Configurating the database for our API
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)
   views = db.Column(db.Integer, nullable=False)
   likes = db.Column(db.Integer, nullable=False)

   # For avoid errors in Code Editor
   def __init__(self, id, name, views, likes):
      self.id = id
      self.name = name
      self.views = views
      self.likes = likes

   def __repr__(self):
      return f"Video(name={self.name}, views={self.views}, likes={self.likes})"

# Creating database
with app.app_context():
    db.create_all()

# Creating the request object for methods
video_put_args = reqparse.RequestParser()
video_patch_args = reqparse.RequestParser()

# Adding the arguments for some request from above
video_put_args.add_argument("likes", type=int, help="Number of video likes is required!", required=True)
video_put_args.add_argument("name", type=str, help="Name of the video is required!", required=True)
video_put_args.add_argument("views", type=int, help="Number of video views is required!", required=True)

video_patch_args.add_argument("likes", type=int, help="Number of video likes")
video_patch_args.add_argument("name", type=str, help="Name of the video")
video_patch_args.add_argument("views", type=int, help="Number of video views")

# Serializing the database
resource_fields = {
   'id': fields.Integer,
   'name': fields.String,
   'views': fields.Integer,
   'likes': fields.Integer
}

# Exceptions
def abort_if_video_doesnt_exists(video_id):
   result = VideoModel.query.get(ident=video_id)

   if not result:
      abort(404, message="Video not found...")

def abort_if_video_exists(video_id):
   result = VideoModel.query.get(ident=video_id)
   
   if result:
      abort(409, message="Video already exists with this Id...")

# API Methods
class Video(Resource):
   @marshal_with(resource_fields) # Configurates the serialization for return from this function
   def get(self, video_id: int):
      abort_if_video_doesnt_exists(video_id)
      result = VideoModel.query.get(ident=video_id)
      return result
   
   @marshal_with(resource_fields)
   def put(self, video_id: int):
      abort_if_video_exists(video_id)

      # Parsing to request args according to the indicated variable
      args = video_put_args.parse_args()
      video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])

      # Sending changes to database
      db.session.add(video)
      db.session.commit()
      return video, 201

   @marshal_with(resource_fields)
   def patch(self, video_id):
      abort_if_video_doesnt_exists(video_id)

      # Parsing to request args according to the indicated variable
      args = video_patch_args.parse_args()
      result = VideoModel.query.filter_by(id=video_id).first()

      # Guard Clause for empty inserts
      if args["likes"] is None and args["name"] is None and args["views"] is None:
         abort(400, message="No arguments provided for update...")

      # Updating the video attributes if they are provided in the request
      if args['name']:
         result.name = args['name'] # type: ignore
      if args['views']:
         result.views = args['views'] # type: ignore
      if args['likes']:
         result.likes = args['likes'] # type: ignore

      # Sending changes to database
      db.session.commit()
      return result

   def delete(self, video_id:int):
      abort_if_video_doesnt_exists(video_id)
      result = VideoModel.query.get(ident=video_id)
      db.session.delete(result)
      db.session.commit()
      return '', 204      

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
   app.run(debug=True)

