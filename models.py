from app import db


class Task (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    title = db.Column(db.String(250), index=True)
    description = db.Column(db.String(250), index=True)
    status = db.Column(db.Boolean)

    def __repr__(self):
        return  self.taskTitle

