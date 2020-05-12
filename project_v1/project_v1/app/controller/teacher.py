
from flask import Blueprint,render_template, request
from app.models.base import db
from app.models.teacher import Teacher

teacherBP = Blueprint('teacher',__name__)

@teacherBP.route('', methods=['GET'])
def get_teacher():
    # with db.auto_commit():
    #     teacher = Teacher('Nina',18,'CST','nina@uic.edu.hk','123456')
    #     # 数据库的insert操作
    #     db.session.add(teacher)
    # return 'hello teacher'

    return render_template('teacher_templates/teacher.html')

@teacherBP.route("/display",methods=['GET'])
def teacherDisplay():
    return render_template('teacher_templates/teacherdisplay.html')



@teacherBP.route("/edit/item",methods=["GET"])
def EditItem():
    return render_template('teacher_templates/edititems.html')



@teacherBP.route("/form/group",methods=['GET'])
def FormGroups():
    return render_template("teacher_templates/enternumofgroup.html")

@teacherBP.route("/export",methods=['GET'])
def Export():
    return render_template("teacher_templates/selectstudents.html")
@teacherBP.route('/import',methods=["GET"])
def Import():
    return render_template("teacher_templates/import.html")



@teacherBP.route('/import/class',methods=["GET"])
def ImportClass():
    return render_template("teacher_templates/importclassinfo.html")