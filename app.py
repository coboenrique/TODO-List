import os
from flask import Flask, request, redirect, render_template
from datetime import datetime
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

'''
config = configparser.ConfigParser()
config.read(".ini")
'''

app = Flask(__name__)
#app.config['MONGO_URI'] = config['PROD']['DB_URI']
app.config['MONGO_URI'] = os.environ.get("MONGODB_URI")
mongo = PyMongo(app)

'''
class Todo(mongo.db.Model):
    id = mongo.db.Column(mongo.db.Integer, primary_key=True)
    content = mongo.db.Column(mongo.db.String(200), nullable=False)
    completed = mongo.db.Column(mongo.db.Integer, default=0)
    date_created = mongo.db.Column(mongo.db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return '<Task %r>' % self.id
'''

def get_tasks():
    tasks = mongo.db.tasks.find().sort("date_created", -1)
    return list(tasks)

def get_task(id):
    try:
       return mongo.db.tasks.find_one_or_404({"_id": ObjectId(id)}) 
    except:
        return
    
def add_task(content):
    task_doc = {'content' : content, 'completed' : 0,'date_created' : datetime.now()}
    return mongo.db.tasks.insert_one(task_doc)

def update_task(id, content):
    response = mongo.db.tasks.update_one(
        { "_id": ObjectId(id) },
        { "$set": { "content": content } }
    )

    return response

def delete_task(id):
    response = mongo.db.tasks.delete_one( { "_id": ObjectId(id) } )
    return response
    

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        
        if not task_content:
            return 'The content cannot be empty'
        
        try:
            add_task(task_content)
            return redirect('/')
        
        except:
            return 'There was a problem adding the task'
        
    else:
        tasks = get_tasks()
        return render_template('index.html', tasks=tasks)
    
    
@app.route('/delete/<string:id>')
def delete(id):
    try:
        delete_task(id)
        return redirect('/')
    except:
        return 'There was a problem deleting the task'
    
    
@app.route('/update/<string:id>', methods=['POST', 'GET'])
def update(id):
    task = get_task(id)
    
    if request.method == 'POST':
        new_content = request.form['content']
        
        if not new_content:
            return 'The content cannot be empty'
        
        try:
            update_task(id, new_content)
            return redirect('/')
        except:
            return 'There was a problem updating the task'
    
    else:
        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)


