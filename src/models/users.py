from src import db
from sqlalchemy import exc
from flask import current_app


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))

    def __repr__(self):
        return "<User {id} {first_name} {email}>".format(
            id=self.id, first_name=self.first_name, email=self.email)

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password
        }

    """
    A class method is a method that is bound to a class rather than its object. It doesn't require creation of a class instance, much like staticmethod.
    The difference between a static method and a class method is:
    
    Static method knows nothing about the class and just deals with the parameters
    Class method works with the class since its parameter is always the class itself.
    """
    @classmethod
    def get(cls, user_id):
        try:
            #TODO: Fill this method
            pass

        except exc.SQLAlchemyError as e:
            current_app.logger.error(str(e))
            raise e

    @classmethod
    def insert(cls, user_obj):
        try:
            #TODO: Fill this method
            pass

        except exc.SQLAlchemyError as e:
            current_app.logger.error(str(e))
            raise e


    @classmethod
    def update(cls, user_obj):
        try:
            #TODO: Fill this method
            pass

        except exc.SQLAlchemyError as e:
            current_app.logger.error(str(e))
            raise e


    @classmethod
    def delete(cls, user_id):
        try:
            #TODO: Fill this method
            pass

        except exc.SQLAlchemyError as e:
            current_app.logger.error(str(e))
            raise e

