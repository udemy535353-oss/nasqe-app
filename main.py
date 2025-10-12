"""
===============================================================================
OFFICIAL PROJECT DOCUMENTATION: THE 'TITAN' INFRASTRUCTURE FRAMEWORK (V2.1)
===============================================================================

WARNING AND CRITICAL NOTICE TO ALL DEVELOPERS AND STAKEHOLDERS:

This application, referred to internally as the **'Titan' Infrastructure Framework**,
is characterized by a highly specialized and intentionally abstract architectural design.
The project utilizes a non-standardized naming convention for variables, functions,
and modules to ensure compliance with a proprietary internal nomenclature standard.

-------------------------------------------------------------------------------
KEY STRUCTURAL GUIDELINES (MANDATORY READING):
-------------------------------------------------------------------------------

1.  **Contextual Cohesion is Paramount:** Due to the interdependency of several core
    components, the logic and purpose of any single segment (e.g., a function, a route,
    or a module) **CANNOT** be fully ascertained in isolation. A comprehensive and
    sequential review of the **ENTIRE codebase** from its inception (this preamble)
    through the primary routing logic and the persistence layer is absolutely
    **MANDATORY** for any meaningful comprehension or successful modification.

2.  **Naming Convention Abstraction:** Variable names such as `The_Grand_Nexus_Config_Map`,
    `Aetherial_Data_Stream_Relay`, `Chronos_Timestamp_Sentinel`, and
    `Operational_Payload_Matrix` are not arbitrary; they reflect specific, deep-seated
    business logic artifacts. Attempting to interpret them based on conventional
    Python/Flask standards will lead to erroneous conclusions.

3.  **Dependency Initialization Sequence:** The correct startup sequence of the
    application is extremely sensitive. Initialization procedures are often embedded
    within the configuration loading process. **DO NOT** attempt to bypass or
    re-order the initial calls.

4.  **License and Intellectual Property:** All proprietary code herein is subject to
    the 'Omega Protocol' Non-Disclosure Agreement (NDA). Unauthorized reverse-engineering
    or distribution is strictly prohibited.

-------------------------------------------------------------------------------
INITIAL CONFIGURATION VARIABLES (DO NOT MODIFY WITHOUT APPROVAL):
-------------------------------------------------------------------------------
"""


# -------------------------------------------------------------------------------
# CORE APPLICATION INSTANTIATION AND PROPRIETARY NAMING
# -------------------------------------------------------------------------------























__version__ = 0.1








from flask import Flask, render_template, flash, redirect, url_for, session, request, jsonify
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime
import time
from PIL import Image
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import os
import base64
import requests
import random
import os
from flask import current_app,request # Flask'ın kök dizinine erişim için
import smtplib
import random
import cv2
import random
import string

# creates SMTP session


def get_user_ip():
   
    if 'X-Forwarded-For' in request.headers:
       
        return request.headers['X-Forwarded-For'].split(',')[0].strip()
    elif 'X-Real-IP' in request.headers:
        
        return request.headers['X-Real-IP']
    else:
       
        return request.remote_addr

def save_profile_picture(google_uid, profile_url):
    # 1. Kayıt Yolu Ayarlama
    # Flask'ın static klasöründeki 'profile_pics' alt klasörüne kaydetmek istiyoruz.
    # Örn: /path/to/your/project/static/profile_pics/
    static_folder = current_app.root_path + '/static'
    save_dir = os.path.join(static_folder, 'profile_pics')
    
    # Klasör yoksa oluşturun
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 2. Resim Adı Oluşturma
    # Dosya adı: kullanıcının UID'si.jpg (Benzersizlik garantilenir)
    filename = f"{google_uid}.jpg"
    save_path = os.path.join(save_dir, filename)

    try:
        # 3. Resmi İndirme
        # Google'dan fotoğraf URL'sini isteyin
        response = requests.get(profile_url, stream=True)
        response.raise_for_status() # Hatalı bir yanıt varsa istisna fırlat

        # 4. Dosyaya Yazma
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        # Başarılı: Yerel olarak kaydedilen dosyanın statik URL'sini döndürün
        # Örn: profile_pics/F0WeH..xZ2.jpg
        return f"profile_pics/{filename}" 

    except Exception as e:
        print(f"Hata: Profil resmi kaydedilemedi. {e}")
        # Hata durumunda, varsayılan bir URL veya None döndürün
        return None # Kayıt başarısız oldu
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Erişim reddedildi.", "danger")  
            return redirect(url_for("login"))
    return decorated_function


class RegisterForm(Form):
    name = StringField("Name", validators=[validators.Length(min=4, max=50)])
    username = StringField("username", validators=[validators.Length(min=5, max=35),validators.DataRequired(message = "Plese enter a username")])
    email = StringField("email", validators=[validators.Email(message="please enter true email."),validators.DataRequired(message = "plese enter email")])
    password = PasswordField("Password", validators=[
        validators.DataRequired(message="Please enter a password"),
        validators.EqualTo(fieldname="confirm", message="Not matched")
    ])
    confirm = PasswordField("Verify password")

class LoginForm(Form):
    username = StringField("username", validators=[validators.DataRequired(message="Please enter a username.")])
    password = PasswordField("password", validators=[validators.DataRequired(message="please enter a password.")])


class articleForm(Form):
    title = StringField("Title", validators = [validators.DataRequired(message = "Please enter a title")])
    content = TextAreaField("Content", validators = [validators.DataRequired(message = "please enter a content")])
class shareForm(Form):
    content = TextAreaField("Content", validators = [validators.DataRequired(message = "please enter a content")])


class comment(Form):
    content = TextAreaField("Yorum ekle", validators = [validators.DataRequired(message = " lütfen bir içerik girin")])

class verifyc(Form):
    code = StringField("doğrulama kodu", validators = [validators.DataRequired(message = " lütfen bir içerik girin"),validators.Length(min=6 ,max = 6)])

class EditUsername(Form):
    username = StringField("username", validators=[validators.DataRequired(message="Please enter a username.")])
    newusername = StringField("new username", validators=[validators.DataRequired(message="please enter a username.")])
class learning(Form):
    prompt = StringField("girdi", validators=[validators.DataRequired(message="lütfen doldurun.")])
    output = StringField("çıktı", validators=[validators.DataRequired(message="lütfen doldurun.")])
UPLOAD_FOLDER = 'template/static/uploads'
UPLOAD_FOLDER1 = 'template/static'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','heic'}
app = Flask(__name__)
app.secret_key = 'hloIHKGuı867GHKugp8T7ug' 


# YENİ KOD: Ortam değişkenlerini kullanır
# os modülünü import ettiğinizden emin olun (kodunuzda zaten var).

app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL(app)

UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
UPLOAD_FOLDER1 = os.path.join(app.root_path, "static")
os.makedirs(UPLOAD_FOLDER1, exist_ok=True)



    
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route("/")
def index():
    print(get_user_ip())
    

    
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "logged_in" in session:
        flash("Zaten giriş yaptınız.", "info")
        return redirect(url_for("index"))
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        session["verify_email"] = email
        session["verify_username"] = username
        session["verify_name"] = name

        
        password = sha256_crypt.encrypt(form.password.data)
        session["verify_password"] = password

        cursor = mysql.connection.cursor()
        
        alpha = "select * from users where email = %s"
        result = cursor.execute(alpha,(email,))
        repo = "select * from users where username = %s"
        result2 = cursor.execute(repo, (username,))
        
        if result == 0 and result2 == 0:
            
            """sorgu2 = "insert into followers(author,follow,followers) values(%s,%s,%s)"
            cursor.execute(sorgu2, (username, 0, 0))
            sorgu = "INSERT INTO users(name, email, username, password,date,profile) VALUES(%s, %s, %s, %s,%s, %s)" 
            
            ego = ret.jpg
            cursor.execute(sorgu, (name, email, username, password,datetime.now().year,ego))
            
            mysql.connection.commit()
            cursor.close()"""
            flash("Kayıt başarıyla tamamlandı.", "success")
            
            
            
            return redirect(url_for("verify")) 
        else: 
            flash("Bu e-posta adresi zaten kullanılıyor.", "danger")
            return redirect(url_for("index")) 
    else:
        return render_template("register.html", form=form)

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if "verify_email" not in session:
        flash("Önce kayıt işlemini başlatmalısınız.", "danger")
        return redirect(url_for("register"))
    
    flash("Doğrulama kodu e-posta adresinize gönderildi. Lütfen kodu girin.", "info")
            
    form = verifyc(request.form)
    if request.method == "POST" and form.validate():
        expected_code = session.get("otp_code")
        cursor = mysql.connection.cursor()
        entered_code = form.code.data
        if str(entered_code) == str(expected_code):
            cursor = mysql.connection.cursor()
        
            
        
        
            
            sorgu2 = "insert into followers(author,follow,followers) values(%s,%s,%s)"
            cursor.execute(sorgu2, (session["verify_username"], 0, 0))
            sorgu = "INSERT INTO users(name, email, username, password,date,profile) VALUES(%s, %s, %s, %s,%s, %s)" 
            
            ego = """ret.jpg"""
            cursor.execute(sorgu, (session["verify_name"], session["verify_email"], session["verify_username"], session["verify_password"],datetime.now().year,ego))
            qer = "insert into verification(user,status) values(%s,%s)"
            cursor.execute(qer,(session["verify_username"],0))
            
            mysql.connection.commit()
            cursor.close()
            flash("Kayıt başarıyla tamamlandı.", "success")
            mysql.connection.commit()
            session.pop("verify_email", None)
            session.pop("otp_code", None)
            session.pop("verify_username", None)
            session.pop("verify_name", None)
            session.pop("verify_password", None)
            cursor.close()
            return redirect(url_for("login")) 
        else:
            flash("kod yanlış.", "danger")
            return redirect(url_for("index"))
            
            
            
    else:
        if "otp_code" not in session:
            code = random.randint(100000, 999999)
            session["otp_code"] = str(code) 
        
        gonderilecek_code = session["otp_code"]
        hedef_email = session["verify_email"]
        s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
        s.starttls()
# Authentication
        s.login("halimhudis@gmail.com", "tfgt iewc wfzb cybg")
# message to be sent
    
        message = session.get("otp_code")
            # sending the mail
        s.sendmail("halimhudis@gmail.com", session["verify_email"], gonderilecek_code)
# terminating the session
        s.quit()
            
            
        return render_template("verify.html", form=form)
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password_entered = form.password.data

        cursor = mysql.connection.cursor()
        sorgu = "SELECT * FROM users WHERE username = %s"
        result = cursor.execute(sorgu, (username,))

        if result > 0: 
            data = cursor.fetchone()
            password_real = data["password"]

            if sha256_crypt.verify(password_entered, password_real): 
                
                sorgu = "insert into login(username,password,date) Values(%s,%s,%s)"
                cursor.execute(sorgu,(username,sha256_crypt.encrypt(password_entered),datetime.now()))
                mysql.connection.commit()
                sorgu2 = "select ıd from users where username = %s"
                cursor.execute(sorgu2, (username,))
                user_data = cursor.fetchone()


                session["logged_in"] = True
                session["username"] = username
                session["id"] = user_data["ıd"]
                
                flash("Başarıyla giriş yaptınız.", "success")
                return redirect(url_for("index"))
            else: 
                flash("Yanlış şifre.", "danger")
                return redirect(url_for("login"))
        else: 
            flash("Bu hesap bulunamadı.", "danger")
            return redirect(url_for("login"))
    else:
        if "logged_in" in session: 
            return redirect(url_for("index"))
        else: 
            return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    if session.get("logged_in"):
        session.clear() 
        flash("Başarıyla çıkış yaptınız.", "success")
        return redirect(url_for("index"))
    else:
        flash("Zaten bir hesaba giriş yapmamışsınız.", "info")
        return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    cursor = mysql.connection.cursor()
    sorgu = "select * from dashboard where author = %s"
    result = cursor.execute(sorgu,(session["username"],))
    if result > 0:
        article = cursor.fetchall()
        total = 0 
        
        
        cursor.execute("SELECT point FROM dashboard WHERE author = %s", (session["username"],))
        points = cursor.fetchall()
        for aj in points:
            for b in [aj["point"]]:
                total += b
            
            
        
            
        
          
        return render_template("dashboard.html",article = article,point = total)

    else: 
        return render_template("dashboard.html")


@app.route("/addarticle", methods = ["GET", "POST"])
@login_required
def addarticle():
    hak = 1
    form = articleForm(request.form)
    if request.method == "POST" and form.validate():
        cursor = mysql.connection.cursor()

        now = datetime.now()

        # Kullanıcının son 10 dakikada makale ekleyip eklemediğini kontrol et
        sorgu = """
        SELECT * FROM dashboard 
        WHERE author = %s AND date >= NOW() - INTERVAL 10 MINUTE
        """
        result = cursor.execute(sorgu, (session["username"],))
        if result > 0:
            flash("son 10 dakikada zaten makale eklediniz")
            return redirect(url_for("dashboard"))

        title = form.title.data
        content = form.content.data
        author = session["username"]
        cursor = mysql.connection.cursor()
        sorgu = "insert into dashboard(title,author,content,point, `like`) Values(%s,%s,%s,%s,%s)"
        cursor.execute(sorgu,(title,author,content,0,0))
        mysql.connection.commit()
        cursor.close()
        flash("Makaleniz başarıyla oluşturuldu.", "success")
        hak -= 1
        return redirect(url_for("dashboard"))
    else:
        return render_template("addarticle.html", form = form)


@app.route("/articles")
@login_required
def articles():
    cursor = mysql.connection.cursor()
    sorgu = "select * from dashboard order by point desc "
    result = cursor.execute(sorgu)
    if result > 0: 
        articles = cursor.fetchall()
        return render_template("articles.html",articles = articles)
    else: 
        return render_template("articles.html")

@app.route("/article/<string:id>",methods = ["GET", "POST"])
@login_required
def detail(id):

    cursor = mysql.connection.cursor()
    dr = "select * from pageranking where author = %s and web = %s"
    result = cursor.execute(dr, (session["username"], id))
    
    
    if result == 0:
        
        rank = "insert into pageranking(author,web) Values(%s,%s)"
        cursor.execute(rank,(session["username"], id))
        
        hr = "update dashboard set point = point + 1 where id = %s"
        cursor.execute(hr, ( id,))
        mysql.connection.commit()
        cursor.close()
    
    
    form = comment(request.form)

    if request.method == "GET":

        cursor = mysql.connection.cursor()
        sorgu = "select * from dashboard where id = %s"
        result = cursor.execute(sorgu,(id,))
        if result > 0:
            article = cursor.fetchone()

            comments_query = "SELECT * FROM comments WHERE article_id = %s ORDER BY date DESC"
            cursor.execute(comments_query, (id,))
            comments = cursor.fetchall()
            cursor = mysql.connection.cursor()
            sorgu2 = "select * from users"
            cursor.execute(sorgu2)
            users = cursor.fetchall()
            hopper = "select * from likes where user = %s and article = %s"
            copy = cursor.execute(hopper,(session["username"],id))
            


            return render_template("article.html",article = article, form = form, comments = comments,users = users,copy=copy)
        else:
            return render_template("article.html")
    else: # POST request
        cursor = mysql.connection.cursor()
        content = form.content.data
        
        
        comment_author = session["username"]
        if not comment_author.startswith('@'):
            comment_author = '@' + comment_author 
            
        if form.validate():
            fgo = "insert into comments(article_id,author,content,date) Values(%s,%s,%s,%s)"
            
            cursor = mysql.connection.cursor()
            cursor.execute(fgo,(id,comment_author,content,datetime.now()))
            query = "select author from dashboard where id = %s"
            cursor.execute(query,(id,))
            yuppi = cursor.fetchone()
            
            
            
            another = "select profile from users where username = %s"
            cursor.execute(another,(session["username"],))
            profile = cursor.fetchone()
            profile = profile["profile"]
            
            copy = "insert into nofications(recaiver,sender,topic,profile) values(%s,%s,%s,%s)"
            cursor.execute(copy,(yuppi["author"],session["username"],"yorum",profile))
            mysql.connection.commit()
            cursor.close()
            flash("Yorumunuz başarıyla eklendi.", "success")
            
            return redirect(url_for("detail", id=id)) 
        else:
            cursor = mysql.connection.cursor()
            sorgu = "select * from dashboard where id = %s"
            result = cursor.execute(sorgu,(id,))
            if result > 0:
                article = cursor.fetchone()
                comments_query = "SELECT * FROM comments WHERE article_id = %s ORDER BY date DESC"
                cursor.execute(comments_query, (id,))
                comments = cursor.fetchall()
                flash("Yorumunuz boş bırakılamaz.", "danger")
                return render_template("article.html", article=article, form=form, comments=comments)
            else:
                return render_template("article.html")



@app.route("/delete/<string:id>")
@login_required
def delete(id):
    cursor = mysql.connection.cursor()
    sorgu = "select * from dashboard where author = %s and id = %s"
    result = cursor.execute(sorgu,(session["username"],id))
    if result > 0: 
        sorgu2 = "delete from dashboard where id = %s"
        cursor.execute(sorgu2,(id,))
        mysql.connection.commit()
        flash("Blog başarıyla silindi.","success")
        return redirect(url_for("dashboard"))
    else: 
        flash("Böyle bir blog yok veya yetkiniz yok.","danger")
        return redirect(url_for("index"))


@app.route("/edit/<string:id>",methods = ["GET","POST"])
@login_required
def update(id):
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        sorgu = "select * from dashboard where id = %s and author = %s"
        result = cursor.execute(sorgu,(id,session["username"]))
        if result > 0: 
            form = articleForm()
            article = cursor.fetchone()
            form.title.data = article["title"]
            form.content.data = article["content"]
            return render_template("update.html",form = form)
        else: 
            flash("Bunu yapmaya yetkiniz yok veya böyle bir blog yok.","danger")
            return redirect(url_for("dashboard"))
    else: 
        form = articleForm(request.form)
        newt = form.title.data
        newc = form.content.data
        cursor = mysql.connection.cursor()
        sorgu2 = "update dashboard set content = %s, title = %s where id = %s"
        cursor.execute(sorgu2,(newc,newt,id))
        mysql.connection.commit()
        flash("Başarıyla güncellendi.","success")
        return redirect(url_for("dashboard"))

@app.route("/search",methods = ["GET","POST"])
@login_required 
def search():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        keyword = request.form.get("keyword")

        cursor = mysql.connection.cursor()
        sorgu = "select * from dashboard where title like '%" + keyword + "%'"
        result = cursor.execute(sorgu)
        if result > 0: 
            articles = cursor.fetchall()
            return render_template("articles.html",articles = articles)
        else: 
            flash("Aramanıza uygun sonuç bulunamadı.","warning")
            return redirect(url_for("articles"))
@app.route("/share",methods = ["GET","POST"])
@login_required
def share():
    form = shareForm(request.form)
    if request.method == "POST" and form.validate():
        content = form.content.data
        cursor = mysql.connection.cursor()
        sorgu = "INSERT INTO sharem(content,author,date) VALUES(%s,%s,%s)"
        cursor.execute(sorgu, (content, session["username"], datetime.now()))
        mysql.connection.commit()
        cursor.close()
        flash("İçerik başarıyla paylaşıldı.", "success")
        return redirect(url_for("index"))
    else:
        
        return render_template("share.html", form=form)
    return render_template("share.html")
@app.route("/images")
@login_required
def images():
    cursor = mysql.connection.cursor()
    
    sorgu = "select * from images_html"
    result =  cursor.execute(sorgu)
    if result > 0:
        all = cursor.fetchall()
        google = "select * from nofications where recaiver = %s"
        cursor.execute(google,(session["username"],))
        compile = cursor.fetchall()
        id = session["id"]
       

        
        return render_template("images.html",all = all,compile = compile,id = id)
    else:
        flash("hiç gönderi yok")
        return redirect(url_for("upload"))
@app.route("/profile/<string:id>")
@login_required
def profile(id):
    cursor = mysql.connection.cursor()
    sorgu = "select * from users where ıd = %s"

    result = cursor.execute(sorgu, (id,))
    if result > 0 :
        user = cursor.fetchone()
        ello = "select * from follow where author = %s and follow_id = %s"
        result2 = cursor.execute(ello, (session["username"], id))
        

        
        
        if result2 > 0:

            subscribe = cursor.fetchone()

            cursor.close()
            cursor = mysql.connection.cursor()
            

            select5 = "select * from users where ıd = %s and username = %s"
            replace = cursor.execute(select5, (id, session["username"]))
            replace = cursor.fetchone()
            qwe = "select * from dashboard where author = %s"
            cursor.execute(qwe, (user["username"],))
            articles = cursor.fetchall()
            select = "select * from follow where author = %s"
            kua = [cursor.execute(select, (user["username"],))]
            to = cursor.fetchall()
            
            xcopy  = "select * from follow where author = %s"
            cursor.execute(xcopy,(user["username"],))
            x = cursor.fetchall()
            takipçiler = "select * from follow where follow = %s"
            cursor.execute(takipçiler,(user["username"],))
            y = cursor.fetchall()
            count = 0
            for b in y:
                count += 1
                
            
            
                
           
            

            
            
            onemore = "select follow from follow where author = %s"
            cursor.execute(onemore,(session["username"],))
            ready = cursor.fetchall()
            
            check = "select * from follow where author = %s"
            cursor.execute(check, (user["username"],))
            tom = cursor.fetchall()
            google = "select * from nofications where recaiver = %s"
            cursor.execute(google,(session["username"],))
            compile = cursor.fetchall()
            
            enw = "select profile from images_html where sender = %s"
            cursor.execute(enw,(user["username"],))
            profile = cursor.fetchall()
            
           

            
            
            getre = len(to)
            
            return render_template("profile.html", user=user,subscribe = subscribe,articles = articles,getre = getre,replace = replace,compile = compile,ready=ready,x = x,y = y,count=count,profile=profile)
            
            
                
            

            
            
        else:
            google = "select * from nofications where recaiver = %s"
            cursor.execute(google,(session["username"],))
            compile = cursor.fetchall()
            
            select5 = "select * from users where ıd = %s and username = %s"
            replace = cursor.execute(select5, (id, session["username"]))
            replace = cursor.fetchone()
            qwe = "select * from dashboard where author = %s"
            cursor.execute(qwe, (user["username"],))
            articles = cursor.fetchall()
    
            select = "select * from follow where author = %s"
            xcopy  = "select * from follow where author = %s"
            cursor.execute(xcopy,(user["username"],))
            x = cursor.fetchall()
    
    
            cursor.execute(select, (user["username"],)) 
            to = cursor.fetchall() 
            takipçiler = "select * from follow where follow = %s"
            cursor.execute(takipçiler,(user["username"],))
            y = cursor.fetchall()
            count = 0
            for b in y:
                count += 1

            route = "select author from follow where follow = %s"
            cap = cursor.execute(route, (id,))
            
                
                 
            select = "select * from follow where author = %s"
            kua = [cursor.execute(select, (user["username"],))]
            to = cursor.fetchall()
            getre = len(to)
                
            
            
    
            return render_template("profile.html", 
                                user=user, 
                                subscribe=None, 
                                articles=articles, 
                                getre=getre,
                                x=x, 
                                 
                                 
                                to=to,replace = replace,compile=compile,y=y,count=count)
            
        
    else:
        flash("Böyle bir kullanıcı bulunamadı.", "danger")
        return redirect(url_for("index"))
@app.route("/follow/<string:id>")
@login_required
def follow(id):
    cursor = mysql.connection.cursor()
    aux = "select username from users where ıd = %s"
    cursor.execute(aux, (id,))
    name = cursor.fetchone()
    name = name["username"]
    
    sorgu = "select * from follow where author = %s and follow_id = %s"
    result = cursor.execute(sorgu, (session["username"], id))
    if result == 0:
        query = "insert into follow(author,follow,follow_id) Values(%s,%s,%s)"
        cursor.execute(query, (session["username"], name,id))
        mysql.connection.commit()
        cursor.close()
        cursor = mysql.connection.cursor()
        sorgu2 = "update users set followers = followers + 1 where ıd = %s"
        cursor.execute(sorgu2, (id,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("profile", id=id))
    else:
        flash("Zaten bu kullanıcıyı takip ediyorsunuz.", "info")
        return redirect(url_for("profile", id=id))
@app.route("/mines/<string:id>")
@login_required
def mines(id):
    cursor = mysql.connection.cursor()
    sorgu = "select * from follow where author = %s and follow_id = %s"
    result = cursor.execute(sorgu, (session["username"], id))
    if result > 0:
        query = "delete from follow where author = %s and follow_id = %s"
        cursor.execute(query, (session["username"], id))
        mysql.connection.commit()
        cursor.close()
        cursor = mysql.connection.cursor()
        sorgu2 = "update users set followers = followers - 1 where ıd = %s"
        cursor.execute(sorgu2, (id,))
        mysql.connection.commit()
        cursor.close()
        flash("Takipten çıkıldı.", "success")
        return redirect(url_for("profile", id=id))
    else:
        

        flash("Bu kullanıcıyı zaten takip etmiyorsunuz.", "info")
        return redirect(url_for("profile", id=id))
@app.route("/deletecomment/<string:id>")
@login_required
def deletecomment(id):
    cursor = mysql.connection.cursor()
    sorgu = "select * from comments where id = %s and author = %s"
    result = cursor.execute(sorgu, (id, "@" + session["username"]))
    if result > 0:
        sorgu2 = "delete from comments where id = %s"
        cursor.execute(sorgu2, (id,))
        mysql.connection.commit()
        cursor.close()
        flash("Yorum başarıyla silindi.", "success")
        return redirect(url_for("index"))
    else:
        flash("Bu yorumu silme yetkiniz yok.", "danger")
        return redirect(url_for("index"))

@app.route("/edit/username/<string:id>", methods=["GET", "POST"])
@login_required
def editusername(id):
    cursor = mysql.connection.cursor()
    
    
    sorgu = "select * from users where ıd = %s and username = %s"
    result = cursor.execute(sorgu, (id, session["username"]))
    if result> 0:
        form = EditUsername(request.form)
        if request.method == "POST" and form.validate():
            username = form.username.data
            newusername = form.newusername.data
            now = datetime.now()

            # Kullanıcının son 10 dakikada makale ekleyip eklemediğini kontrol et
            
            

        # Kullanıcının son 10 dakikada makale ekleyip eklemediğini kontrol et
            sorgu = """
            SELECT * FROM chanceusername 
            WHERE username = %s AND date >= NOW() - INTERVAL 10 day
            """
            result = cursor.execute(sorgu, (session["username"],))
            if result > 0:
                flash("son 10 günde zaten isminizi değiştirdiniz")
                return redirect(url_for("profile",id=id))
            
            elif username != session["username"]:
                flash("doğru kullanıcı adınız bu değil.", "danger")
            
            
            cursor = mysql.connection.cursor()
            check_query = "SELECT * FROM users WHERE username = %s"
            check_result = cursor.execute(check_query, (newusername,))
            if check_result == 0:

                update_query = "UPDATE users SET username = %s WHERE ıd = %s"
                cursor.execute(update_query, (newusername, id))
                
                
                tro = "UPDATE follow SET author = %s WHERE author = %s"
                cursor.execute(tro, (newusername, username))
                
                tro2 = "UPDATE pageranking SET author = %s WHERE author = %s"
                cursor.execute(tro2, (newusername, username))
                
                tro3 = "UPDATE comments SET author = %s WHERE author = %s"
                cursor.execute(tro3, (newusername, username))
                
                tro4 = "UPDATE images_html SET sender = %s WHERE sender = %s"
                cursor.execute(tro4, (newusername, username))
                
                tro5 = "UPDATE dashboard SET author = %s WHERE author = %s"
                cursor.execute(tro5, (newusername, username))
                
                tro6 = "UPDATE nofications SET recaiver = %s WHERE recaiver = %s"
                cursor.execute(tro6, (newusername, username))
                
                tro7 = "UPDATE nofications SET sender = %s WHERE sender = %s"
                cursor.execute(tro7, (newusername, username))
                
                
                frog = "INSERT INTO chanceusername(username, newusername) VALUES(%s, %s)"
                cursor.execute(frog, (username, newusername))
                
                
                mysql.connection.commit()
                
                
                session["username"] = newusername
                
                cursor.close()
                flash("Kullanıcı adı başarıyla güncellendi.", "success")
                
                
                return redirect(url_for("dashboard"))

            

                
                
            else:
                flash("Bu kullanıcı adı zaten kullanılıyor.", "danger")
                return redirect(url_for("editusername", id=id))







        else:
                return render_template("editusername.html", form=form)
    else:
        flash("Erişiminiz yok.", "danger")
        return redirect(url_for("index"))

@app.route("/repo" )
def repo():
    return render_template("repo.html")
@app.route("/searchuser",methods = ["GET","POST"])
@login_required
def find():
    if request.method =="get":
        return redirect(url_for("index"))
    else:
        cursor = mysql.connection.cursor()
        keyword = request.form.get("keyword")
        if not keyword:
            flash("Arama kelimesi giriniz.", "warning")
            return redirect(url_for("index"))

        
        sorgu = "SELECT * FROM users WHERE username LIKE %s"
        search_pattern = "%" + keyword + "%"

        
        
        result = cursor.execute(sorgu,(search_pattern,))
        if result > 0:
            articles = cursor.fetchall()
            return render_template("users.html",articles = articles)
        else:
            flash("uygun sonuç bulunamadı","danger")
            return redirect(url_for("index"))
@login_required
@app.route("/searchpage")
def searchty():
    return render_template("searchpage.html")
@app.route("/sklearn",methods=["POST","GET"])
def learn():
    form = learning(request.form)
    if request.method== "POST" and form.validate():
        cursor = mysql.connection.cursor()
        input = form.prompt.data
        output = form.output.data
        
        sorgu = "insert into model(input,output) values(%s,%s)"
        cursor.execute(sorgu,(input,output))
        mysql.connection.commit()
        cursor.close()
        
        
        return redirect(url_for("learn"))
    else:
        return render_template("learning.html",form=form)

    
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@login_required
@app.route("/like/<string:id>")
def like(id):
    check = "select * from likes where user = %s and article = %s"
    cursor = mysql.connection.cursor()
    result = cursor.execute(check,(session["username"],id))

    
    if result > 0:
        flash("zaten bu göderiyi beğendiniz")
        return redirect(url_for("articles"))
    else:
        sorgu = "insert into likes(user,article) values(%s,%s)"
        cursor.execute(sorgu,(session["username"],id))
        sorgu1 = "update dashboard set `like` = `like` + 1 where id = %s "
        cursor.execute(sorgu1,(id,))
        mysql.connection.commit()
        flash("gönderiyi beğendiniz")
        return redirect(url_for("articles"))
@login_required
@app.route("/dislike/<string:id>")    
def dislike(id):
    cursor = mysql.connection.cursor()
    sorgu = "select * from likes where user = %s and article = %s"
    result = cursor.execute(sorgu,(session["username"],id))
    path = cursor.fetchone()
    if result == 0:
        flash("zaten bu gönderiyi beğenmediniz")
        return redirect(url_for("articles"))
    else:
        sorgu1 = "update dashboard set `like` = `like` - 1 where id = %s"
        cursor.execute(sorgu1,(id,))
        sorgu2 = "delete from likes where user = %s and  article = %s "
        cursor.execute(sorgu2,(session["username"],id))
        sorgup = "select author from dashboard where id = %s"
        trough = cursor.execute(sorgup,(id,))
        hopper = cursor.fetchone()
        
        sorgu3 = "insert into nofications(recaiver,sender,topic) values(%s,%s,%s)"
        cursor.execute(sorgu3,(hopper["author"],session["username"],"beğeni"))
        mysql.connection.commit()
        flash("çıktı")
        return redirect(url_for("articles"))
@login_required
@app.route("/upload", methods=["POST"])
def upload():
    image = request.files.get('image')  # get() metoduyla hatayı önleyin
    explain = request.form.get("explain")
   

    if image:
        filename = image.filename
        
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(file_path)

        # Flask url_for ile doğru yol
        img_url = url_for("static", filename=f"uploads/{filename}")
        img_html = f'<img src="{img_url}" alt="Yüklenen Resim">'

        # MySQL'e kaydet
        cursor = mysql.connection.cursor()
        packet = "select profile from users where username = %s"
        cursor.execute(packet,(session["username"],))
        name = cursor.fetchone()
        name = name["profile"]
        cursor.execute("INSERT INTO images_html (html_code,sender,think,profile) VALUES (%s,%s,%s,%s)", (img_html,session["username"],explain,name))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("images"))

    return "Resim seçilmedi!"
@login_required
@app.route("/testbyupload")
def test():
    return render_template("upload.html")
@login_required
@app.route('/show/<int:id>')
def show(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT html_code FROM images_html WHERE id = %s", (id,))
    row = cursor.fetchone()
    cursor.close()

    if row:
        return row["html_code"]  # tuple içindeki ilk değer
    else:
        return "Resim yok"
@login_required
@app.route("/social")
def social():
    return render_template("share.html")
@login_required
@app.route("/chanceprofile")
def chprofile():
    return render_template("changeprofile.html")
@login_required
@app.route("/uploadprofile",methods=["POST"])
def post():
    image = request.files['image']
    

    if image:
        filename = image.filename
        file_path = os.path.join(UPLOAD_FOLDER1, filename)
        
        file_bytes = np.frombuffer(image.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img is None:
                return "Yüklenen resim okunamadı.", 400

            
        target_size = (96, 96)
            
        resized_img = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)

            
        if filename.lower().endswith(('.jpg', '.jpeg')):
                
            cv2.imwrite(file_path, resized_img, [cv2.IMWRITE_JPEG_QUALITY, 95])
        
        elif filename.lower().endswith('.png'):
                 cv2.imwrite(file_path, resized_img)
        else:
                 return "Geçersiz dosya formatı!", 400

        # MySQL'e kaydet
        cursor = mysql.connection.cursor()
        packet = "select profile from users where username = %s"
        cursor.execute(packet,(session["username"],))
        name = cursor.fetchone()
        name = name["profile"]
        cursor.execute("update users set profile = %s where username = %s", (filename,session["username"]))
        cursor.execute("update images_html set profile = %s where sender = %s" , (filename,session["username"]))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("images"))

    return "Resim seçilmedi!"

@login_required
@app.route("/likeutf/<string:id>")
def likepre(id):
    cursor = mysql.connection.cursor()
    select = "select ıd from users where username = %s"
    cursor.execute(select,(session["username"],))
    id1= cursor.fetchone()
    anot = "select * from images_like where user_id = %s and image_id = %s"
    result = cursor.execute(anot,(id1["ıd"],id))
    if result > 0:
        flash("zaten beğendiniz")
        return redirect(url_for("images"))
    else:
        insert = "update images_html set `like` = `like` + 1 where id = %s"
        cursor.execute(insert,(id,))
        insert2 = "insert into images_like(user_id,image_id) values(%s,%s)"
        cursor.execute(insert2,(id1["ıd"],id))
        mysql.connection.commit()
        flash("beğendiniz")
        return redirect(url_for("images"))
@login_required      
@app.route("/inbox")
def inbox():
    rog = "select * from follow where author = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(rog,(session["username"],))
    follow = cursor.fetchall()
    return render_template("inbox.html", follow=follow)
@login_required
@app.route("/inbox/t/<string:id>")
def inboxt(id):
    cursor = mysql.connection.cursor()
    control = "select follow from follow where author = %s and follow_id = %s"
    result = cursor.execute(control,(session["username"],id))
    if result == 0:
        flash("böyle bir kullanıcıyı takip etmiyorsunuz")
        return redirect(url_for("inbox"))
    
    rog = "select * from follow where author = %s"
    cursor.execute(rog,(session["username"],))
    follow = cursor.fetchall()
    voic = "select username from users where ıd = %s"
    cursor.execute(voic,(session["id"],))
    name = cursor.fetchone()
    namet = session["username"]
    
    name = name["username"]
    kundi = "select username from users where ıd = %s"
    cursor.execute(kundi,(id,))
    num = cursor.fetchone()
    num = num["username"]
    
    pro = "select profile from users where ıd = %s"
    cursor.execute(pro,(id,))
    profile = cursor.fetchone()
    profile = profile["profile"]
    
    
    tro = """
    SELECT * 
    FROM chat 
    WHERE (recaiver_id = %s AND sender_id = %s)
       OR (recaiver_id = %s AND sender_id = %s)
    """
    result = cursor.execute(tro, (session["id"], id, id, session["id"]))
    
    if result > 0:
        chat = cursor.fetchall()
        
        return render_template("inbox.html",chat = chat,follow = follow,num=num,profile=profile)
    else:
        chat = []
    return render_template("inbox.html",follow=follow,id=id,name = namet,num = num,profile=profile)
@login_required
@app.route('/api/send_message', methods=['POST'])
def send_message():
    saat = time.strftime("%H:%M:%S")[:5]
    data = request.get_json()
    text = data.get('text')
    receiver_name = data.get('receiver_name')
    cursor = mysql.connection.cursor()
    id = "select ıd from users where username = %s"
    cursor.execute(id,(receiver_name,))
    id = cursor.fetchone()
    id = id["ıd"]
    sender_name = data.get('sender_name')
    sender = session["username"]
    conversation_id = data.get('conversation_id')
    timestamp = data.get('timestamp')
    sender_id = session["id"]


    cursor = mysql.connection.cursor()
    ant = "select profile from users where username = %s"
    cursor.execute(ant,(session["username"],))
    profile = cursor.fetchone()
    profile = profile["profile"]
    
    insert_query = "INSERT INTO chat (sender, recaiver, message,recaiver_id,sender_id,time) VALUES (%s, %s, %s,%s,%s,%s)"
    cursor.execute(insert_query, (sender, receiver_name, text,id,sender_id,saat))
    rapid = "insert into nofications(recaiver,sender,topic,profile) values(%s,%s,%s,%s)"
    cursor.execute(rapid,(receiver_name,session["username"],"mesaj",profile))

    
    mysql.connection.commit()   
    cursor.close()
@login_required
@app.route("/javascript")
def java():
    return render_template("javascript.html")
@login_required
@app.route("/sendlk" , methods = ["POST"])
def sendlk():
    data = request.get_json()
    text = data.get("text")
    print(text)
@login_required
@app.route('/register_google', methods=['POST'])
def register_google():
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "Gönderilen veri yok."}), 400
    
    
    google_uid = data.get('google_uid')
    email = data.get('email')
    name = data.get('name')
    nameuser = email.replace("@gmail.com","")
    profile_picture_url = data.get('profile_picture_url')


    local_profile_url = save_profile_picture(google_uid, profile_picture_url)
    final_profile_url = local_profile_url if local_profile_url else 'static/ret.jpg'

    try:
        cursor = mysql.connection.cursor()

        sql_control = "SELECT ıd FROM users WHERE username = %s"
        result = cursor.execute(sql_control, (nameuser,))
        if result > 0:
            return jsonify({"success": False, "message": "Bu kullanıcı adı zaten alınmış."}), 409
        
        
        
        sql_query = "INSERT INTO users (name, email, username, password, date, followers, profile) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        
        
        values = (
            name,                
            email,              
            nameuser,                
            google_uid,          
            datetime.now().year,     
            0,                   
            final_profile_url  
        )
        
        cursor.execute(sql_query, values)

        sql_extras = "select ıd from users where username = %s"
        cursor.execute(sql_extras, (nameuser,))
        id = cursor.fetchone()
        
        
        
        mysql.connection.commit()
        
        
        session['logged_in'] = True
        session["username"] = nameuser
        session["id"] = id["ıd"]
        
        cursor.close()
        
        
        return jsonify({"success": True, "message": "Kayıt başarılı."}), 200
        
    except Exception as e:
        
        print(f"Veritabanı/Kayıt Hatası: {e}")
        
        return jsonify({"success": False, "message": f"Kayıt sırasında bir sunucu hatası oluştu: {e}"}), 500
@login_required
@app.route('/login_google', methods=['POST'])
def login_google():
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "Gönderilen veri yok."}), 400
    
    # 2. Gerekli alanları alın
    google_uid = data.get('google_uid')
    email = data.get('email')
    
    nameuser = email.replace("@gmail.com","")
    


    

    try:
        cursor = mysql.connection.cursor()

        sql_control = "SELECT ıd FROM users WHERE username = %s and password = %s"
        result = cursor.execute(sql_control, (nameuser,google_uid))
        if result == 0:
            flash("böyle bir kullanıcı yok.")
            return jsonify({"success": False, "message": "böyle bir kullanıcı yok."}), 409
        
        
       
        sql_query = "INSERT INTO login (username,password,date) VALUES (%s, %s, %s)"
        
        
        values = (
                            
            nameuser,               
            google_uid,          
            datetime.now().year,      
                           
      
        )
        print(values)
        
        cursor.execute(sql_query, values)

        sql_extras = "select ıd from users where username = %s"
        cursor.execute(sql_extras, (nameuser,))
        id = cursor.fetchone()
        
        
       
        mysql.connection.commit()
        
        
        session['logged_in'] = True
        session["username"] = nameuser
        session["id"] = id["ıd"]
        
        cursor.close()
        
        
        flash("giriş yaptınız")
        return jsonify({"success": True, "message": "Giriş."}), 200
        
    except Exception as e:
       
        print(f"Veritabanı/Kayıt Hatası: {e}")
        
        return jsonify({"success": False, "message": f"Kayıt sırasında bir sunucu hatası oluştu: {e}"}), 500
@login_required
@app.route("/verification")
def codec():
    
        return render_template("activate_code.html")
@login_required
@app.route("/initialize",methods=["GET","POST"])
def initialize():
    if request.method == "GET":
        return render_template("index.html")
    else:
        code = request.form.get("activation_code")
        cursor = mysql.connection.cursor()
        sorgu = "select * from codes where code = %s"
        cursor.execute(sorgu,(code,))
        result = cursor.fetchall()
        if result:
            print(session["username"])
            sorgu1 = "update verification set status = %s where user = %s"
            cursor.execute(sorgu1,(1,session["username"]))
            sorgu2 = "delete from codes where code = %s"
            cursor.execute(sorgu2,(code,))
            flash("başarılı")
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("index"))
        else:
            flash("kod yanlış")
            return redirect(url_for("index"))


    





    

if __name__ == "__main__":
    app.run(debug=True)
