from flask import Blueprint,render_template, request, jsonify,redirect,make_response,session
from app.models.base import db
from app.models.student import Student
from app.models.teacher import Teacher
from sqlalchemy import or_,and_,all_,any_
from flask_login import login_user

userBP = Blueprint('user',__name__)

@userBP.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html',title='Sample Login',header='Sample Case')
    else:

        email = request.form.get('email')
        _password = request.form.get('password')



        if '@mail.uic.edu.hk' in email: # 并不严谨，仅作测试，应该用正则
            result = Student.query.filter(and_(Student.email == email,Student.password == _password)).first()
            # tr = TimetableRecord.query.filter(and_(TimetableRecord.tid==tid, TimetableRecord.day == day,TimetableRecord.status!=2)).first()
            if result:
                response=make_response("set_cookie")
                response.set_cookie("name",result.name,36000)
                session["id"]=result.id

                return redirect("/student")
            else:
                return render_template('login.html', title='Sample Login', header='Sample Case', message="用户名和密码错误")

        elif '@uic.edu.hk' in email:
            result = Teacher.query.filter(and_(Teacher.email == email,Teacher.password == _password)).first()

            if result:
                response=make_response("set_cookie")


                response.set_cookie("name", result.name, 36000)
                session["id"] = result.id
                session["name"] = result.name
                return redirect("/teacher")
            else:
                return render_template('login.html', title='Sample Login', header='Sample Case', message="用户名和密码错误")


        else:
            return render_template('login.html', title='Sample Login', header='Sample Case', message="invalid email")



@userBP.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('id') #删除session
    session.pop('name') #删除session


    return redirect('/user/login')