from flask import Flask, make_response, request, render_template, jsonify,redirect, url_for,send_file
import requests
from db import session,Users,Product
import json

app = Flask(__name__)


@app.route("/addUser", methods=["GET","POST"])
def addUser():
    try:
        data = request.json
        print(data["formInput"])
        if data["formInput"]["name"] != "" and data["formInput"]["username"] != "" and data["formInput"]["password"] != "" and data["formInput"]["access"] != "":
            name = data["formInput"]["name"]
            username = data["formInput"]["username"]
            password = data["formInput"]["password"]
            access = data["formInput"]["access"]
            try:
                user = Users(name=name,username=username,password=password,access=access)
                session.add(user)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e) 
            return jsonify({"msg":"success"})
        else:
            return jsonify({"msg":"Failed"})
    except Exception as e:
        print(e)
        return jsonify({"msg":"Failed"})

@app.route("/updateUser", methods=["GET","POST"])
def updateUser():
    try:
        data = request.json
        print(data["formInput"])
        if data["formInput"]["name"] != "" and data["formInput"]["username"] != "" and data["formInput"]["password"] != "" and data["formInput"]["access"] != "":
            name = data["formInput"]["name"]
            username = data["formInput"]["username"]
            password = data["formInput"]["password"]
            access = data["formInput"]["access"]
            try:
                user = session.query(Users).filter(Users.username == username).one()
                user.name = name
                user.username = username
                user.password = password
                user.access = access
                session.commit()
            except Exception as e:
                session.rollback()
                print(e) 
            return jsonify({"msg":"success"})
        else:
            return jsonify({"msg":"Failed"})
    except Exception as e:
        print(e)
        return jsonify({"msg":"Failed"})

@app.route("/userinfo", methods=["GET"])
def userinfo():
    try:
        user = session.query(Users).filter(Users.id == 1).one()
        return jsonify({"name":user.name,"username":user.username,"password":user.password,"access":user.access})
    except Exception as e:
        session.rollback()
        print(e)
        return jsonify({"msg":"Failed"}) 

@app.route('/displayimage/<name>')
def displayImage(name):
    image = "/home/mohamed/Desktop/Management-app/label/"+name
    return send_file(image)

@app.route('/displayfile/<name>')
def displayFile(name):
    pdf = "/home/mohamed/Desktop/Management-app/csd/"+name
    return send_file(pdf)

@app.route('/login',methods=["GET","POST"])
def login():
    try:
        data = request.json
        try:
            user = session.query(Users).filter(Users.username == data["username"]).one()
            user1 = session.query(Users).filter(Users.password == data["password"]).one()
            data = {"name":user.name,"username":user.username,"password":user.password,"access":user.access}
            return jsonify({"msg":"success","info": data})
        except Exception as e:
            print(e)
            return jsonify({"msg":"failed"})
    except Exception as e:
        print(e)

@app.route("/set-cookie", methods=["GET","POST"])
def set_cookie():
    try:
        token = request.json
        print(token)
        response = make_response("Here, take some cookie!")
        response.set_cookie(key="profile", value=json.dumps(token), httponly=True)
        return response
    except Exception as e:
        print(e)

@app.route("/get-profile", methods=["GET"])
def get_profile():
    profile = request.cookies.get('profile')
    return profile

@app.route("/add", methods=["GET","POST"])
def add():
    try:
         product_line = request.form['product_line']
         product_name = request.form['product_name']
         part_no = request.form['part_no']
         label = request.files['label']
         csd = request.files['csd']
         label.save("/home/mohamed/Desktop/Management_app/Management-app/label/"+label.filename)
         csd.save("/home/mohamed/Desktop/Management_app/Management-app/csd/"+csd.filename)
         try:
             product = Product(product_line=product_line,product_name=product_name,part_no=part_no,csd=csd.filename,label=label.filename)
             session.add(product)
             session.commit()
             return jsonify({"msg":"success"})
         except Exception as e:
             print(e)
             session.rollback()
             return jsonify({"msg":"failed"})
    except Exception as e:
         print(e)

@app.route("/productlist", methods=["GET","POST"])
def productlist():
    try:
        products = session.query(Product).all()
        result = {}
        for product in products:
            if product.product_line in result.keys():
                result[product.product_line].append(product.product_name)
            else:
                data = []
                data.append(product.product_name)
                result.update({product.product_line: data})
        return result
    except Exception as e:
        print(e)

@app.route("/productdisplay", methods=["GET","POST"])
def productdisplay():
    try:
        data = request.json
        print(data["product_line"])
        products = session.query(Product).filter(Product.product_line == data["product_line"]).all()
        for product in products:
            print(product.product_name)
            if product.product_name == data["product_name"]:
                result = {"product_line":product.product_line,"product_name":product.product_name,"part_no":product.part_no,"label":product.label,"csd":product.csd}
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({"msg":"Not found"})

@app.route("/", methods=["GET"])
def index():
    return "works !!!"


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug=True)
