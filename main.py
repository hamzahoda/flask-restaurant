from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
import json





with open('config.json','r') as c:
    params=json.load(c)["params"]

local_server=True

app=Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password'])

mail=Mail(app)

# security key set for session variable
app.secret_key='super-secret-key'

if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI']=params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI']=params['prod_uri']   


    
db=SQLAlchemy(app)


class Contact(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),nullable=False)
    email=db.Column(db.String(20),nullable=False)
    phone=db.Column(db.String(12),nullable=False)
    date=db.Column(db.String(12),nullable=False)
    message=db.Column(db.String(120),nullable=False)


class Reservation(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    date=db.Column(db.String(12),nullable=False)
    time=db.Column(db.String(12),nullable=False)
    people=db.Column(db.String(20),nullable=False)
    name=db.Column(db.String(80),nullable=False)
    phone=db.Column(db.String(12),nullable=False)
    email=db.Column(db.String(20),nullable=False)



class Starters(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    dish=db.Column(db.String(80),nullable=False)
    tagline=db.Column(db.String(50),nullable=False)
    price=db.Column(db.String(20),nullable=False)
    

class Drinks(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    drink_name=db.Column(db.String(80),nullable=False)
    tagline=db.Column(db.String(50),nullable=False)
    price=db.Column(db.String(20),nullable=False)

class Maindish(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    main_dish=db.Column(db.String(80),nullable=False)
    tagline=db.Column(db.String(50),nullable=False)
    price=db.Column(db.String(20),nullable=False) 

class Dessert(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    dessert_name=db.Column(db.String(80),nullable=False)
    tagline=db.Column(db.String(50),nullable=False)
    price=db.Column(db.String(20),nullable=False) 


class Lunch(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    lunch_dish=db.Column(db.String(80),nullable=False)
    tagline=db.Column(db.String(50),nullable=False)
    price=db.Column(db.String(20),nullable=False) 
    lunch_image=db.Column(db.String(20),nullable=False) 

class Dinner(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    dinner_dish=db.Column(db.String(80),nullable=False)
    tagline=db.Column(db.String(50),nullable=False)
    price=db.Column(db.String(20),nullable=False) 
    dinner_image=db.Column(db.String(20),nullable=False)

class Interiorgallery(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    interior=db.Column(db.String(80),nullable=False)

class Foodgallery(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    food=db.Column(db.String(80),nullable=False)


class Eventsgallery(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    event=db.Column(db.String(80),nullable=False)

class Guestsgallery(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    guest=db.Column(db.String(80),nullable=False)



class Blog(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(80),nullable=False)
    tagline=db.Column(db.String(20),nullable=False)
    content=db.Column(db.String(12),nullable=False)
    blog_slug=db.Column(db.String(12),nullable=False)
    date=db.Column(db.String(12),nullable=False)
    month=db.Column(db.String(12),nullable=False)
    blog_image=db.Column(db.String(120),nullable=False)


class Specialsignup(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(80),nullable=False)




@app.route('/',methods=['GET','POST'])
def home():
    blog=Blog.query.filter_by().all()[0:3]
    if request.method == 'POST':
        email=request.form.get('email-address')
        entry=Specialsignup(email=email)
        db.session.add(entry)
        db.session.commit()
    return render_template('index.html',blog=blog)



@app.route('/about')
def about():
    return render_template('about.html')







@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        # add entry to database
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        # entry ko fetch karliya ab add karonga database mei
        entry=Contact(name=name,email=email,phone=phone,message=message,date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message(
            'New message from '+name,
            sender=params['gmail-user'],
            recipients=[email],
            body=message+'\n' + '\n'+phone + '\n'+email
        )



    return render_template('contact.html')










@app.route('/reservation',methods=['GET','POST'])
def reservation():
    if request.method == 'POST':
        date=request.form.get('date')
        time=request.form.get('time')
        people=request.form.get('people')
        name=request.form.get('name')
        phone=request.form.get('phone')
        email=request.form.get('email')
        entry=Reservation(date=date,time=time,people=people,name=name,phone=phone,email=email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message(
            'New message from '+'Pato Resturant',
            sender=params['gmail-user'],
            recipients=[email],
            body="Your Reservation has been placed we look forward in seeing you"+'\n'+people + '\n'+phone + '\n'+email
        )


    return render_template('reservation.html')












@app.route('/menu')
def menu():
    starters=Starters.query.filter_by().all()
    drinks=Drinks.query.filter_by().all()
    maindish=Maindish.query.filter_by().all()
    dessert=Dessert.query.filter_by().all()
    lunch=Lunch.query.filter_by().all()
    dinner=Dinner.query.filter_by().all()
    return render_template('menu.html',starters=starters,drinks=drinks,maindish=maindish,dessert=dessert,lunch=lunch,dinner=dinner)




@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/dashboard')








@app.route('/gallery')
def gallery():
    interiorgallery=Interiorgallery.query.all()
    foodgallery=Foodgallery.query.all()
    eventsgallery=Eventsgallery.query.all()
    guestsgallery=Guestsgallery.query.all()
    return render_template('gallery.html',interiorgallery=interiorgallery,foodgallery=foodgallery,eventsgallery=eventsgallery,guestsgallery=guestsgallery)



# interiorgallery ko edit ka tareeka
@app.route("/edit-interiorgallery/<string:sno>",methods=["GET","POST"])
def edit_interiorgallery(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        if request.method == 'POST':
            form_photo=request.form.get('interior')
            if sno == '0': #if sno is zero add new photo and if not then edit exsisting photo
                interiorphoto=Interiorgallery(interior=form_photo)
                db.session.add(interiorphoto)
                db.session.commit()
            else:
                interiorphoto=Interiorgallery.query.filter_by(sno=sno).first()
                interiorphoto.interior=form_photo
                db.session.commit()    
                return redirect('/edit-interiorgallery/'+sno)
        interiorphoto=Interiorgallery.query.filter_by(sno=sno).first()    
        return render_template('edit-interiorgallery.html',interiorphoto=interiorphoto,sno=sno)
        # jab request post nahi thi isne get karke mje puran dikha diya phir sumbit kiya tou request 
       # post howi tou phir changes karke redirect woh dikhaya

# interiorgallery ko delete ka tareeka
@app.route("/delete-interiorgallery/<string:sno>",methods=["GET","POST"])
def delete_interiorgallery(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        interiorphoto=Interiorgallery.query.filter_by(sno=sno).first()
        db.session.delete(interiorphoto)
        db.session.commit()
    return redirect('/dashboard')


# foodgallery ko edit ka tareeka
@app.route("/edit-foodgallery/<string:sno>",methods=["GET","POST"])
def edit_foodgallery(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        if request.method == 'POST':
            form_photo=request.form.get('food')
            if sno == '0': #if sno is zero add new photo and if not then edit exsisting photo
                foodphoto=Foodgallery(food=form_photo)
                db.session.add(foodphoto)
                db.session.commit()
            else:
                foodphoto=Foodgallery.query.filter_by(sno=sno).first()
                foodphoto.food=form_photo
                db.session.commit()    
                return redirect('/edit-foodgallery/'+sno)
        foodphoto=Foodgallery.query.filter_by(sno=sno).first()    
        return render_template('edit-foodgallery.html',foodphoto=foodphoto,sno=sno)
        # jab request post nahi thi isne get karke mje puran dikha diya phir sumbit kiya tou request 
       # post howi tou phir changes karke redirect woh dikhaya

# interiorgallery ko delete ka tareeka
@app.route("/delete-foodgallery/<string:sno>",methods=["GET","POST"])
def delete_foodgallery(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        foodphoto=Foodgallery.query.filter_by(sno=sno).first()
        db.session.delete(foodphoto)
        db.session.commit()
    return redirect('/dashboard')



# eventgallery ko edit ka tareeka
@app.route("/edit-eventgallery/<string:sno>",methods=["GET","POST"])
def edit_eventgallery(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        if request.method == 'POST':
            form_photo=request.form.get('event')
            if sno == '0': #if sno is zero add new photo and if not then edit exsisting photo
                eventphoto=Eventsgallery(event=form_photo)
                db.session.add(eventphoto)
                db.session.commit()
            else:
                eventphoto=Eventsgallery.query.filter_by(sno=sno).first()
                eventphoto.event=form_photo
                db.session.commit()    
                return redirect('/edit-eventgallery/'+sno)
        eventphoto=Eventsgallery.query.filter_by(sno=sno).first()    
        return render_template('edit-eventgallery.html',eventphoto=eventphoto,sno=sno)
        # jab request post nahi thi isne get karke mje puran dikha diya phir sumbit kiya tou request 
       # post howi tou phir changes karke redirect woh dikhaya

# eventgallery ko delete ka tareeka
@app.route("/delete-eventgallery/<string:sno>",methods=["GET","POST"])
def delete_eventgallery(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        eventphoto=Eventsgallery.query.filter_by(sno=sno).first()
        db.session.delete(eventphoto)
        db.session.commit()
    return redirect('/dashboard')



# guestsgallery ko edit ka tareeka
@app.route("/edit-guestgallery/<string:sno>",methods=["GET","POST"])
def edit_guestgallery(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        if request.method == 'POST':
            form_photo=request.form.get('guest')
            if sno == '0': #if sno is zero add new photo and if not then edit exsisting photo
                guestphoto=Guestsgallery(guest=form_photo)
                db.session.add(guestphoto)
                db.session.commit()
            else:
                guestphoto=Guestsgallery.query.filter_by(sno=sno).first()
                guestphoto.guest=form_photo
                db.session.commit()    
                return redirect('/edit-guestgallery/'+sno)
        guestphoto=Guestsgallery.query.filter_by(sno=sno).first()    
        return render_template('edit-guestgallery.html',guestphoto=guestphoto,sno=sno)
        # jab request post nahi thi isne get karke mje puran dikha diya phir sumbit kiya tou request 
       # post howi tou phir changes karke redirect woh dikhaya

# guestgallery ko delete ka tareeka
@app.route("/delete-guestgallery/<string:sno>",methods=["GET","POST"])
def delete_guestgallery(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        guestphoto=Guestsgallery.query.filter_by(sno=sno).first()
        db.session.delete(guestphoto)
        db.session.commit()
    return redirect('/dashboard')












@app.route('/blog')
def blog():
    blog=Blog.query.all()
    return render_template('blog.html',blog=blog)




# dekh kar kiya blog detail page ka nahi araha tha kese hoga khali blog hogaya tha

@app.route('/blog-detail/<string:blog_slug>',methods=['GET'])
def blog_detail(blog_slug):
    blog=Blog.query.filter_by(blog_slug=blog_slug).first()
    return render_template('blog-detail.html',blog=blog)    




# Blog edit ka tareeka
@app.route("/edit-blog/<string:sno>",methods=["GET","POST"])
def edit_blog(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        if request.method == 'POST':
            form_title=request.form.get('title')
            form_tagline=request.form.get('tagline')
            form_content=request.form.get('content')
            form_slug=request.form.get('slug')
            form_date=request.form.get('date')
            form_month=request.form.get('month')
            form_image=request.form.get('image')
            if sno == '0': #if sno is zero add new dish and if not then edit exsisting dish
                blog=Blog(title=form_title,tagline=form_tagline,content=form_content,blog_slug=form_slug,date=form_date,month=form_month,blog_image=form_image)
                db.session.add(blog)
                db.session.commit()
            else:
                blog=Blog.query.filter_by(sno=sno).first()
                blog.title=form_title
                blog.tagline=form_tagline
                blog.content=form_content
                blog.blog_slug=form_slug
                blog.date=form_date
                blog.month=form_month
                blog.blog_image=form_image
                db.session.commit()    
                return redirect('/edit-blog/'+sno)
        blog=Blog.query.filter_by(sno=sno).first()
        return render_template('edit-blog.html',blog=blog,sno=sno)
# Lunch delete ka tareeka
@app.route("/delete-blog/<string:sno>",methods=["GET","POST"])
def delete_blog(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        blog=Blog.query.filter_by(sno=sno).first()
        db.session.delete(blog)
        db.session.commit()
    return redirect('/dashboard')












# starter ko edit ka tareeka
@app.route("/edit-starter/<string:sno>",methods=["GET","POST"])
def edit_starter(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        if request.method == 'POST':
            form_dish=request.form.get('dish')
            form_tagline=request.form.get('tagline')
            form_price=request.form.get('price')
            if sno == '0': #if sno is zero add new dish and if not then edit exsisting dish
                starters=Starters(dish=form_dish,tagline=form_tagline,price=form_price)
                db.session.add(starters)
                db.session.commit()
            else:
                starters=Starters.query.filter_by(sno=sno).first()
                starters.dish=form_dish
                starters.tagline=form_tagline
                starters.price=form_price
                db.session.commit()    
                return redirect('/edit-starter/'+sno)
        starters=Starters.query.filter_by(sno=sno).first()    
        return render_template('edit-starter.html',starters=starters,sno=sno)
        # jab request post nahi thi isne get karke mje puran dikha diya phir sumbit kiya tou request 
        # post howi tou phir changes karke redirect woh dikhaya
# starter ko delete ka tareeka
@app.route("/delete-starter/<string:sno>",methods=["GET","POST"])
def delete_starter(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        starters=Starters.query.filter_by(sno=sno).first()
        db.session.delete(starters)
        db.session.commit()
    return redirect('/dashboard')




# drink ko edit ka tareeka

@app.route("/edit-drink/<string:sno>",methods=["GET","POST"])
def edit_drink(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        if request.method == 'POST':
            form_dish=request.form.get('drink')
            form_tagline=request.form.get('tagline')
            form_price=request.form.get('price')
            if sno == '0': #if sno is zero add new dish and if not then edit exsisting dish
                drinks=Drinks(drink_name=form_dish,tagline=form_tagline,price=form_price)
                db.session.add(drinks)
                db.session.commit()
            else:
                drinks=Drinks.query.filter_by(sno=sno).first()
                drinks.dish=form_dish
                drinks.tagline=form_tagline
                drinks.price=form_price
                db.session.commit()    
                return redirect('/edit-drink/'+sno)
        drinks=Drinks.query.filter_by(sno=sno).first()
        return render_template('edit-drink.html',drinks=drinks,sno=sno)
# drink ko delete ka tareeka
@app.route("/delete-drink/<string:sno>",methods=["GET","POST"])
def delete_drink(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        drinks=Drinks.query.filter_by(sno=sno).first()
        db.session.delete(drinks)
        db.session.commit()
    return redirect('/dashboard')


# main dish ko edit ka tareeka

@app.route("/edit-maindish/<string:sno>",methods=["GET","POST"])
def edit_maindish(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        if request.method == 'POST':
            form_dish=request.form.get('maindish')
            form_tagline=request.form.get('tagline')
            form_price=request.form.get('price')
            if sno == '0': #if sno is zero add new dish and if not then edit exsisting dish
                maindish=Maindish(main_dish=form_dish,tagline=form_tagline,price=form_price)
                db.session.add(maindish)
                db.session.commit()
            else:
                maindish=Maindish.query.filter_by(sno=sno).first()
                maindish.main_dish=form_dish
                maindish.tagline=form_tagline
                maindish.price=form_price
                db.session.commit()    
                return redirect('/edit-maindish/'+sno)
        maindish=Maindish.query.filter_by(sno=sno).first()
        return render_template('edit-maindish.html',maindish=maindish,sno=sno)

# main dish ko delete ka tareeka
@app.route("/delete-maindish/<string:sno>",methods=["GET","POST"])
def delete_maindish(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        maindish=Maindish.query.filter_by(sno=sno).first()
        db.session.delete(maindish)
        db.session.commit()
    return redirect('/dashboard')


# dessert edit ka tareeka
@app.route("/edit-dessert/<string:sno>",methods=["GET","POST"])
def edit_dessert(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        if request.method == 'POST':
            form_dish=request.form.get('dessert')
            form_tagline=request.form.get('tagline')
            form_price=request.form.get('price')
            if sno == '0': #if sno is zero add new dish and if not then edit exsisting dish
                dessert=Dessert(dessert_name=form_dish,tagline=form_tagline,price=form_price)
                db.session.add(dessert)
                db.session.commit()
            else:
                dessert=Dessert.query.filter_by(sno=sno).first()
                dessert.dessert_name=form_dish
                dessert.tagline=form_tagline
                dessert.price=form_price
                db.session.commit()    
                return redirect('/edit-dessert/'+sno)
        dessert=Dessert.query.filter_by(sno=sno).first()
        return render_template('edit-dessert.html',dessert=dessert,sno=sno)

# dessert delete ka tareeka
@app.route("/delete-dessert/<string:sno>",methods=["GET","POST"])
def delete_dessert(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        dessert=Dessert.query.filter_by(sno=sno).first()
        db.session.delete(dessert)
        db.session.commit()
    return redirect('/dashboard')


# Lunch edit ka tareeka
@app.route("/edit-lunch/<string:sno>",methods=["GET","POST"])
def edit_lunch(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        if request.method == 'POST':
            form_dish=request.form.get('lunch')
            form_tagline=request.form.get('tagline')
            form_price=request.form.get('price')
            form_image=request.form.get('lunch_image')
            if sno == '0': #if sno is zero add new dish and if not then edit exsisting dish
                lunch=Lunch(lunch_dish=form_dish,tagline=form_tagline,price=form_price,lunch_image=form_image)
                db.session.add(lunch)
                db.session.commit()
            else:
                lunch=Lunch.query.filter_by(sno=sno).first()
                lunch.lunch_dish=form_dish
                lunch.tagline=form_tagline
                lunch.price=form_price
                lunch.lunch_image=form_image
                db.session.commit()    
                return redirect('/edit-lunch/'+sno)
        lunch=Lunch.query.filter_by(sno=sno).first()
        return render_template('edit-lunch.html',lunch=lunch,sno=sno)
# Lunch delete ka tareeka
@app.route("/delete-lunch/<string:sno>",methods=["GET","POST"])
def delete_lunch(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        lunch=Lunch.query.filter_by(sno=sno).first()
        db.session.delete(lunch)
        db.session.commit()
    return redirect('/dashboard')


# Dinner edit ka tareeka
@app.route("/edit-dinner/<string:sno>",methods=["GET","POST"])
def edit_dinner(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        if request.method == 'POST':
            form_dish=request.form.get('dinner')
            form_tagline=request.form.get('tagline')
            form_price=request.form.get('price')
            form_image=request.form.get('dinner_image')
            if sno == '0': #if sno is zero add new dish and if not then edit exsisting dish
                dinner=Dinner(dinner_dish=form_dish,tagline=form_tagline,price=form_price,dinner_image=form_image)
                db.session.add(dinner)
                db.session.commit()
            else:
                dinner=Dinner.query.filter_by(sno=sno).first()
                dinner.dinner_dish=form_dish
                dinner.tagline=form_tagline
                dinner.price=form_price
                dinner.dinner_image=form_image
                db.session.commit()    
                return redirect('/edit-dinner/'+sno)
        dinner=Dinner.query.filter_by(sno=sno).first()
        return render_template('edit-dinner.html',dinner=dinner,sno=sno)
# Lunch delete ka tareeka
@app.route("/delete-dinner/<string:sno>",methods=["GET","POST"])
def delete_dinner(sno):
    if ('user' in session and session['user'] == params['admin-username']):
        dinner=Dinner.query.filter_by(sno=sno).first()
        db.session.delete(dinner)
        db.session.commit()
    return redirect('/dashboard')














@app.route('/dashboard',methods=["GET","POST"])
def dashboard():
    # indentation ka khayaal warna kuch nahi chalega
    if ('user' in session and session['user'] == params['admin-username']):
        starters=Starters.query.all()
        drinks=Drinks.query.all()
        maindish=Maindish.query.all()
        dessert=Dessert.query.all()
        lunch=Lunch.query.all()
        dinner=Dinner.query.all()
        interiorgallery=Interiorgallery.query.all()
        foodgallery=Foodgallery.query.all()
        eventgallery=Eventsgallery.query.all()
        guestgallery=Guestsgallery.query.all()
        blog=Blog.query.all()
        return render_template('dashboard.html',starters=starters,drinks=drinks,maindish=maindish,dessert=dessert,lunch=lunch,dinner=dinner,interiorgallery=interiorgallery,foodgallery=foodgallery,eventgallery=eventgallery,guestgallery=guestgallery,blog=blog)
    if request.method == "POST":
        # redirect to admin panel
        username=request.form.get("username")
        password=request.form.get("password")
        if (username == params['admin-username'] and password == params['admin-password']):
            # set the session variable
            session['user']= username
            starters=Starters.query.all()
            drinks=Drinks.query.all()
            maindish=Maindish.query.all()
            dessert=Dessert.query.all()
            lunch=Lunch.query.all()
            dinner=Dinner.query.all()
            interiorgallery=Interiorgallery.query.all()
            foodgallery=Foodgallery.query.all()
            eventgallery=Eventsgallery.query.all()
            guestgallery=Guestsgallery.query.all()
            blog=Blog.query.all()
            return render_template('dashboard.html',starters=starters,drinks=drinks,maindish=maindish,dessert=dessert,lunch=lunch,dinner=dinner,interiorgallery=interiorgallery,foodgallery=foodgallery,eventgallery=eventgallery,guestgallery=guestgallery,blog=blog)        
    return render_template('login.html')






app.run(debug=True)