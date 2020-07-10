from app.main import db


def save_change(data):
    db.session.add(data)
    aa = db.session.commit()
    # print(f"commit+result:{aa}")


def save_all(data_list: list):
    for data in data_list:
        db.session.add(data)
    db.session.commit()


def delete(data):
    db.session.delete(data)
    db.session.commit()


def delete_all(data_list: list):
    for data in data_list:
        db.session.delete(data)
    db.session.commit()
