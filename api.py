# from flask import Flask, request
# from flask_restful import Resource, Api, reqparse

# app = Flask(__name__)

# @app.route("/")
# def hello():
# 	return 'Welcome to Flask Tutorial'

from flask import  Flask, render_template, redirect, url_for
from flask import request
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os

client = MongoClient('localhost:27017')
db = client.pymongo_tut
UPLOAD_FOLDER = os.path.basename('uploads')


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# status = db.customers.insert_one({
#                 "name" : "Rohan",
#                 "city" : "Bokaro"
#             })

# db.customers.delete_many({})

# @app.route("/upload", methods = ['GET', 'POST'])
# def upload():
#     return """ 
#         <form action="" method="POST"  enctype="multipart/form-data">
#           <b> Image: </b><input type="file" placeholder="Image" name="mov_img" required = "True">
#           <input class="btn btn-default" type="submit" value="submit">
#         </form>
#       """

# @app.route("/see_file", methods = ['GET', 'POST'])
# def see():
#     if 'mov_img' in request.files:
#         mov_img = request.files['mov_img']
#         mongo.save_file(mov_img.filename, mov_img)
#         mongo.db.customers.insert({"mov_img_name":mov_img.filename})
#     return "Done"

@app.route("/add", methods = ['GET', 'POST'])
def add_contact():
    _id = request.values.get("_id")
    name = request.values.get("name")
    genre = request.values.get("genre")   
    if _id is not None:
        value = db.customers.insert({"name":name,"genre":genre})
        return render_template('add.html', value = value)
    else:
        return render_template('add.html')

    # else:
    #     # return render_template('contact.html', status=status)
    #     return  'Error submitting Data'

@app.route("/del", methods = ['GET', 'POST'])
def del_things():
    val = db.customers.find()
    nm = request.values.get("delname")
    db.customers.remove({"name":nm})
    return render_template("rem.html", val = val)

@app.route("/update", methods = ['GET', 'POST'])
def updt_things():
    val = db.customers.find()
    val_nm = request.values.get("valname")
    # val_ct = request.values.get("valcity")
    nm = request.values.get("n_name")
    ct = request.values.get("n_genre")
    print(nm)
    print(ct)
    if nm is not "":
        db.customers.update_one({"name":val_nm},{'$set':{"name":nm}})
    else:
        db.customers.update_one({"name":val_nm},{'$set':{"name":val_nm}})

    if ct is not None:
        db.customers.update_one({"name":val_nm},{'$set':{"genre":ct}})

    return render_template("upd.html", val = val)
    
@app.route("/", methods = ['GET', 'POST'])
def get_all_contact():
    try:
        contacts = db.customers.find()
        if db.customers.find() is None:
            db.coll.findAndModify({query :{}, sort: {"_id" : -1}, remove:true})
        else:
            return render_template('show.html', contacts=contacts)
    except Exception as e:
        flag = 1
      
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
