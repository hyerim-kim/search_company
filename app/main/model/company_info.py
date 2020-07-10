# -- coding: utf-8 --
from sqlalchemy import PrimaryKeyConstraint

from app.main import db


class CompanyInfo(db.Model):
    """ Company Model for storing details of a company. """
    __tablename__ = "company_info"
    __table_args__ = (PrimaryKeyConstraint('company_id', 'language_id'),)

    company_id = db.Column(db.String(255), db.ForeignKey('company.company_id'), nullable=False)
    language_id = db.Column(db.String(5), db.ForeignKey('language.language_id'), nullable=False)
    name = db.Column(db.String(255))
    tag = db.Column(db.String(255))

    def __str__(self):
        return f"{{company_id:'{self.company_id}', language_id:'{self.language_id}', " \
               f"name:'{self.name}', tag: '{self.tag}'}}"
