from src import db
from sqlalchemy import exc
from flask import current_app


class Posts(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.BIGINT)
    image_url = db.Column(db.String(256))
    caption = db.Column(db.String(128))

    def __repr__(self):
        return "<Post {id} {user_id} {image_url}>".format(
            id=self.id, user_id=self.user_id, image_url=self.image_url)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'image_url': self.image_url,
            'caption': self.caption,
        }

    """
    A class method is a method that is bound to a class rather than its object. It doesn't require creation of a class instance, much like staticmethod.
    The difference between a static method and a class method is:

    Static method knows nothing about the class and just deals with the parameters
    Class method works with the class since its parameter is always the class itself.
    """

    @classmethod
    def get_posts_by_user_id(cls, user_id):
        try:
            #TODO: Fill this method
            pass

        except exc.SQLAlchemyError as e:
            current_app.logger.error(str(e))
            raise e

    @classmethod
    def insert(cls, post_obj):
        try:
            # TODO: Fill this method
            pass

        except exc.SQLAlchemyError as e:
            current_app.logger.error(str(e))
            raise e

    @classmethod
    def update(cls, post_obj):
        try:
            # TODO: Fill this method
            pass

        except exc.SQLAlchemyError as e:
            current_app.logger.error(str(e))
            raise e

    @classmethod
    def delete(cls, post_id):
        try:
            # TODO: Fill this method
            pass

        except exc.SQLAlchemyError as e:
            current_app.logger.error(str(e))
            raise e
