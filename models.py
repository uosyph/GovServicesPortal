from app import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(14), primary_key=True)
    password = db.Column(db.String(64))
    name = db.Column(db.String(128))
    phone = db.Column(db.String(16))
    email = db.Column(db.String(48))
    address = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)


class Department(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.String(14), primary_key=True)
    name = db.Column(db.String(128))


class Service(db.Model):
    __tablename__ = "services"
    id = db.Column(db.String(14), primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.String(8192))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    is_done = db.Column(db.Boolean)
    user_id = db.Column(db.String(14))


if __name__ == "__main__":
    from app import app

    with app.app_context():
        db.create_all()
