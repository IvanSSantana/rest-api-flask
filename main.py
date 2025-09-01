from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# Create the request object
video_put_args = reqparse.RequestParser()

# Add the arguments for request above
video_put_args.add_argument("likes", type=int, help="Number of video likes")
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Number of video views")

videos = {}

class Video(Resource):
   def get(self, video_id: int):
      return videos[video_id]
   
   def put(self, video_id: int):
      # Parse to request args according to the indicated variable
      args = video_put_args.parse_args()
      videos[video_id] = args
      return {video_id: args}, 201

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
   app.run(debug=True)
