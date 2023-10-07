from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model.db'

db = SQLAlchemy(app)

#todos = [{"task" : "sample task", "done" : False}]

class Model(db.Model):
    
    id = db.Column(db.Integer, primary_key= True)
    content = db.Column(db.String(300), nullable = False)
    done = db.Column(db.Boolean , default = False)
    
    def __repr__(self):
        return f'<Task {self.id}>'
    
  

@app.route('/')
def index():
    tasks = Model.query.all()
    return render_template ("index.html", tasks = tasks)


@app.route("/add", methods=["POST"])
def add():
    
        content = request.form.get('content')
        new_task = Model(content = content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        
        except:
            return "error occur while adding task"

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):
    
    task = Model.query.get_or_404(id)
    
    if request.method == "POST":
        new_content = request.form.get("new_content")
        task.content = new_content
        
        try:
            db.session.commit()
            return redirect('/')
        
        except:
            return "error occur while editting"
    

    return render_template("edit.html", task = task)

@app.route("/check/<int:id>")
def check(id):
    
    task = Model.query.get(id)
    task.done = not task.done
    db.session.commit()
    return redirect('/')

@app.route("/delete/<int:id>")
def delete(id):
    
    delete_task = Model.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect ("/")
    
    except:
        return "error while deleting task"


if __name__ == '__main__':
    app.run(debug=True)