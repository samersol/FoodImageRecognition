
from flask import Flask, request, render_template, url_for, redirect,session
from flask_uploads import UploadSet, configure_uploads, IMAGES
import Functions as func
from flask_pymongo import PyMongo
from bson.binary import Binary
import io
import base64

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://soliman775:samersamer123@food30.pr9yqh3.mongodb.net/userFood?retryWrites=true&w=majority&appName=food30"
mongo = PyMongo(app)





app.secret_key = 'nobodyknowssamerlr123'  # Set a secret key for the session


# photos = UploadSet('photos', IMAGES)

# app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
# configure_uploads(app, photos)




"""""""""


***********************************************************************************************


"""""""""

def fetch_Goal(email):
    users = mongo.db.userFood
    user = users.find_one({"email": email})
    userGoal = user['goal'] if user else None
    session['userGoal'] = userGoal  # Store userGoal in session
    return userGoal



#register page

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        goal = request.form['goal']
        users = mongo.db.userFood
        users.insert_one({
            "email": email,
            "fullName": name,
            "password": password,
            "goal": goal
        })
        success = True
        return render_template('login.html', success=success)
    return render_template('register.html')


#Authenticate for logging in

@app.route('/Authenticate', methods=['POST'])
def Authenticate():
    email = request.form['email']
    password = request.form['password']
    users = mongo.db.userFood
    user = users.find_one({"email": email, "password": password})
    if user:
        session['email'] = email
        session['password'] = password
        return redirect('/home')
    else:
        return redirect('/login')

# Define the route for the login page
@app.route('/login')
def login():
    js_files = [
        url_for('static', filename='js/bootstrap.js'),
        url_for('static', filename='js/jquery-3.4.1.min.js')
    ]
    return render_template('login.html', js_files=js_files)



"""""""""

***********************************************************************************************

"""""""""

#uploading image and knowing its Label and corresponding calories

@app.route('/upload/<userGoal>', methods=['GET', 'POST'])
def upload(userGoal):
   img = request.files['image']
   img_read = io.BytesIO(img.read())
   img_binary = Binary(img_read.read())
   FoodName= func.processing_image(img)
   calories= func.fetch_calories2(FoodName)
   advice=func.provide_advice(userGoal,int(calories))
   users = mongo.db.userFood
   users.insert_one({
            "image": img_binary,
        })
   img_base64 = base64.b64encode(img_binary).decode()

   return render_template('result.html', FoodName=FoodName, calories=calories,img_data=img_base64,advice=advice,userGoal=userGoal)





"""""""""

***********************************************************************************************

"""""""""


@app.route('/')
def hello_world():
    js_files = [
        url_for('static', filename='js/bootstrap.js'),
        url_for('static', filename='js/jquery-3.4.1.min.js')
    ]
    return render_template('home.html', js_files=js_files)




@app.route('/home')
def home():

    js_files = [
        url_for('static', filename='js/bootstrap.js'),
        url_for('static', filename='js/jquery-3.4.1.min.js')
    ]
    email=session.get('email')
    userGoal= fetch_Goal(email)
    return render_template('home.html', js_files=js_files,userGoal=userGoal)

    return render_template('home.html')


@app.route('/sample')
def sample():

   return render_template('sample.html')



@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route('/food')
def food():
    return render_template('food.html')

@app.route('/image')
def image():
    return render_template('Upload.html')










if __name__ == '__main__':
    app.run(host="127.0.0.1",port=8080,debug=True)

