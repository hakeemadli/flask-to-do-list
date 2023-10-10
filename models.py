from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Model(db.Model):
    
    id = db.Column(db.Integer, primary_key= True)
    content = db.Column(db.String(300), nullable = False)
    complete = db.Column(db.Boolean , default = False)
    
    def __repr__(self):
        return f'<Task {self.id}>'