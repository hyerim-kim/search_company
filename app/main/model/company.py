# -- coding: utf-8 --
from app.main import db


class Company(db.Model):
    """ Company Model for storing the unique ID of a company. """
    __tablename__ = "company"

    company_id = db.Column(db.String(255), primary_key=True, nullable=False)

