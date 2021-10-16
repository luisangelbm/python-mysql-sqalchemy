from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Task(db.Model):
        id = db.Column(db.Integer, primary_key=True)           #propidades(intero, llave primary)
        title = db.Column(db.String(70), unique=True)          #propidades(texto(70caracteres), Dato unico
        description = db.Column(db.String(100))                #propidades(texto(100caracteres)

        def __init__(self,title,description):                  #definimos la tarea que van a cambiar en la db(title,description)
            self.title = title
            self.description = description

db.create_all()                                                 #metodo para leer toda la class y crear las tablas

class TaskSchema(ma.Schema):                                    #crear un Schema para interactuar, esto con "ma=marshmallow"
    class Meta:
        fields = ('id','title', 'description')                  #campos que voy a interactuar 

task_schema= TaskSchema()
tasks_schema= TaskSchema(many=True)                             #para interactuar con muchas tablas

@app.route('/tasks', methods=['POST'])              #CREAR TAREA
def create_task():

    title = request.json['title']
    description = request.json['description']
    
    new_task = Task(title, description)
    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)

@app.route('/tasks', methods=['GET'])               #OBTENER TAREA
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)


@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['PUT'])          #ACTUALIZAR TAREA
def update_task(id):
    task = Task.query.get(id)

    title = request.json['title']
    description = request.json['description']

    task.title = title
    task.description = description

    db.session.commit()
    return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['DELETE'])          #ELIMINAR TAREA
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to my API'})


if __name__=="__main__":
    app.run(debug=True)