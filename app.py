from flask import Flask,render_template,request,redirect,url_for
from models import db,Model


app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model.db'
db.init_app(app)
  

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
    task.complete = not task.complete
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