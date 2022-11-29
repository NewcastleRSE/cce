from apps import db

class Entry(db.Model):
        
    __tablename__ = 'Entry'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    year = db.Column(db.Integer, nullable=False)
    manufactured = db.Column(db.Integer, nullable=False)
    acquired = db.Column(db.Integer, nullable=False)
    imported = db.Column(db.Integer, nullable=False)
    recycled = db.Column(db.Integer, nullable=False)
    untracked = db.Column(db.Integer, nullable=False)
    transferred = db.Column(db.Integer, nullable=False)
    exported = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.id)