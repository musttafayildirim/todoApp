from flask import Flask,render_template,redirect,url_for,request
#kullanmamız gereken kütüphaneleri import ediyoruz...
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#sqlalchemy veritabanını ayarlıyoruz.
#buradaki url bloğuna satırına sizin todo.db'niz hangi dizindeyse onu yerleştirmeniz gerekiyor....
url = 'sqlite:////Users/MustafaY/Desktop/todoApp/todo.db'
app.config['SQLALCHEMY_DATABASE_URI'] = url
db = SQLAlchemy(app)

#index. html sayfasına gitmek için gerekenler
@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html",todos = todos)

#burada yeni bir todo ekleme yapmak için gerekenler
@app.route("/add", methods = ["post"])
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title = title,complete = False)
    #veri tabanına ekliyoruz..
    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for("index"))

#burada ise eklenilen todo tamamlanmışsa onu tamamla demeyi ayarlıyoruz
@app.route("/complete/<string:id>")
def todoComplete(id):
    todo = Todo.query.filter_by(id = id).first()
    if todo.complete == False:
        todo.complete = True
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))
    
    
#burası silme işlemimizin gerçekleştiği alan
@app.route("/delete/<string:id>")
def todoDelete(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))



#orm ile veritabanımızı class şeklinde oluşturuyoruz...
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)




if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
