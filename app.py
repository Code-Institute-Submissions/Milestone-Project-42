import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)


app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["MONGO_DBNAME"] = 'mad_libz'

mongo = PyMongo(app)


@app.route('/')
def hello():
    return 'Hello World'


@app.route('/create')
def create():
    return render_template('create.html',
                           skeletons=mongo.db.mad_libz_templates.find())


@app.route('/insert_words', methods=['GET'])
def insert_words():
    selected_id = request.args.get('mad_lib')
    mad_lib = mongo.db.mad_libz_templates.find_one(
                                                  {'_id': ObjectId(selected_id)})
    return render_template('insert-words.html', mad_lib=mad_lib)

        
@app.route('/push_data/<template_id>', methods=['POST'])
def push_data(template_id):
    user_input = list(request.form.values())
    mongo.db.mad_libs_input.insert_one({
        "mad_lib_id": ObjectId(template_id),
        "words": user_input
    })
    return redirect(url_for('/results'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
