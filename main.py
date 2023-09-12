
from flask import Flask, request, render_template, url_for, redirect,session
from Flask_Uploads import UploadSet, configure_uploads, IMAGES

import Functions as func


import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)
success= False



app = Flask(__name__)
app.secret_key = 'nobodyknowssamerlr123'  # Set a secret key for the session


photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)




"""""""""


***********************************************************************************************


"""""""""

def fetch_Goal(email):
    cursor = db.cursor()
    cursor.execute("SELECT goal FROM users WHERE email = %s", (email,))
    userGoal = cursor.fetchone()
    cursor.close()

    return userGoal



#register page

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        goal = request.form['goal']
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users ( email, fullName, password, goal) VALUES ( %s, %s, %s, %s)", ( email, name, password, goal))
        db.commit()
        success = True
        return render_template('login.html', success=success)
    return render_template('register.html')


#Authenticate for logging in

@app.route('/Authenticate', methods=['POST'])
def Authenticate():
    email = request.form['email']
    password = request.form['password']
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    session['email'] = email
    session['password'] = password
    cursor.close()

    if user:
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
   filename = photos.save(img)
   FoodName= func.processing_image(img)
   calories= func.fetch_calories2(FoodName)
   userGoal1=userGoal[2:-3]
   print(userGoal1)
   advice=func.provide_advice(userGoal1,int(calories))

   return render_template('result.html', FoodName=FoodName, calories=calories, filename=filename,advice=advice,userGoal1=userGoal1)





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

