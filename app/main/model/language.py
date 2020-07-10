# -- coding: utf-8 --
from app.main import db


class Language(db.Model):
    """ Language Model for storing the language to support multi-languages. """
    __tablename__ = "language"

    language_id = db.Column(db.String(5), primary_key=True, nullable=False, unique=True)
