from flask import Flask , render_template  ,redirect ,url_for , request
from flask_sqlalchemy import SQLAlchemy
    
app = Flask(__name__)
# app configs
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite"

# db setings
db = SQLAlchemy(app)

# task class for sae in database
class task(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String,nullable=False)
    body = db.Column(db.String,nullable=False)
    do = db.Column(db.Integer,nullable=True,default=0)
    

@app.route('/',methods=["POST","GET"] )
def index():
    if request.method == "POST":
        title = request.form['title']
        if not title or title == "" :
            return render_template('index.html',massage = "وظیفه نمی تواند خالی باشد ")
        body = request.form['body']
        if not body or body == "" :
            return render_template('index.html',massage = "شرح وظیفه نمی تواند خالی بماند ")
        new_task  = task(title=title,body=body)
       
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')

    tasks = task.query.all()

    return render_template('index.html' , tasks = tasks )

@app.route("/delete/<int:id>")
def delete(id):
    taske = task.query.get_or_404(id)
    db.session.delete(taske)
    db.session.commit()
    return redirect('/')
    
@app.route("/update/<int:id>",methods=["POST","GET"])
def update(id):
    taske = task.query.get_or_404(id)

    if request.method == "POST":
        taske.title = request.form['title']
        taske.body = request.form['body']
        db.session.commit()

        return redirect('/')
    return render_template('update.html' , task=taske)

@app.route("/do/<int:id>")
def doed(id):
    taske = task.query.get_or_404(id)
    if taske.do == 0:
        taske.do = 1
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')
@app.route('/doc/<int:id>')
def doc(id):
    task = task.query.get_or_404(id)
if __name__ == "__main__":
    app.run(debug=True)

