from . import db

class Video(db.Model):
    __tablename__ = "videos"
    id = db.Column(db.Integer, primary_key=True)
    youtube_id = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    likes = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "youtube_id": self.youtube_id,
            "title": self.title,
            "description": self.description,
            "likes": self.likes
        }
