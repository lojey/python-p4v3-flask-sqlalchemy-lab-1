from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

# Add models here


class Earthquake(db.Model, SerializerMixin):
    __tablename__ = 'earthquakes'

    # Define the columns
    id = db.Column(db.Integer, primary_key=True)
    magnitude = db.Column(db.Float, nullable=False)
    location = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    # Define the serialization rules (optional)
    serialize_rules = ('-earthquakes',)

    def __repr__(self):
        return f"<Earthquake {self.id}, {self.magnitude}, {self.location}, {self.year}>"
