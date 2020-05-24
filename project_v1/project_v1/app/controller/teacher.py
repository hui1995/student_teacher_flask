
from flask import Blueprint,render_template, request,session,redirect,make_response
from app.models.base import db
from app.models.course import Course
from app.models.student import Student
from app.models.CourseAndStudent import CourseAndStudent
from app.models.member import Member

import xlrd
from io import BytesIO

teacherBP = Blueprint('teacher',__name__)
import io
import xlsxwriter





@teacherBP.route('', methods=['GET'])
def get_teacher():
    if session.get("id") is None:
        return redirect("/user/login")
    name=session.get("name")
    courselst = Course.query.filter_by(teacherId=session.get("id"))


    return render_template('teacher_templates/teacher.html',name=name,result=courselst)





@teacherBP.route("/form/group",methods=['GET'])
def FormGroups():
    if session.get("id") is None:
        return redirect("/user/login")
    name=session.get("name")

    return render_template("teacher_templates/enternumofgroup.html")

@teacherBP.route("/export",methods=['GET'])
def Export():
    if session.get("id") is None:
        return redirect("/user/login")
    name=session.get("name")
    courseId=request.args.get("id")

    return render_template("teacher_templates/selectstudents.html",name=name,courseId=courseId)


@teacherBP.route('/export_excel/', methods=['GET'])
def export_excel():
    if request.method == 'GET':
        courseId=request.args.get("courseId")
        studentlst=CourseAndStudent.query.filter_by(CourseId=courseId)
        output = BytesIO()
        # 创建Excel文件,不保存,直接输出
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        # 设置Sheet的名字为download
        worksheet = workbook.add_worksheet('download')
        # 列首
        title = ["Id","name", "email", "password","GPA","programme","contribution"]
        worksheet.write_row('A1', title)
        count=0
        for i in studentlst:
            count+=1
            i=Student.query.filter_by(id=i.studentId).first()
            member=Member.query.filter_by(studentId=i.id).first()
            if member is None:
                row = [i.id, i.name, i.email,i.password,i.GPA,i.programme,""]

            else:

                row = [i.id, i.name, i.email,i.password,i.GPA,i.programme,member.contribution]

            worksheet.write_row('A' + str(count + 2), row)
        workbook.close()
        response = make_response(output.getvalue())
        output.close()
        response.headers['Content-Type'] = "utf-8"
        response.headers["Cache-Control"] = "no-cache"
        response.headers["Content-Disposition"] = "attachment; filename=download.xlsx"
        return response

@teacherBP.route('/import',methods=["GET"])
def Import():
    if session.get("id") is None:
        return redirect("/user/login")
    name=session.get("name")
    id=request.args.get("id")

    return render_template("teacher_templates/import.html", name=name,id=id)



@teacherBP.route('/import/class',methods=["GET","POST"])
def ImportClass():
    if session.get("id") is None:
        return redirect("/user/login")
    name=session.get("name")
    courseId=request.args.get("courseId")

    if request.method=="GET":

        return render_template("teacher_templates/importclassinfo.html",name=name,courseId=courseId)
    else:
        file = request.files.get("files")
        f = file.read()  # 文件内容
        data = xlrd.open_workbook(file_contents=f)
        table = data.sheets()[0]
        names = data.sheet_names()  # 返回book中所有工作表的名字
        status = data.sheet_loaded(names[0])  # 检查sheet1是否导入完毕
        nrows = table.nrows  # 获取该sheet中的有效行数



        for  i in range(0,nrows):
            s = table.row_values(i)  # 第1列数据
            student = Student.query.filter_by(email=s[5]).first()
            if student:
                continue
            student = Student.query.filter_by(id=s[3]).first()
            if student:
                continue
            with db.auto_commit():
                # name password programme id gpa email contribution
                try:
                    student = Student(s[0], s[4],s[3],s[5], s[2], s[1])
                # 数据库的insert操作
                    db.session.add(student)
                except:
                    continue

            student = Student.query.filter_by(email=s[5]).first()
            if student is not None:
                with db.auto_commit():
                    courseAndStudent = CourseAndStudent()
                    courseAndStudent.CourseId = courseId
                    courseAndStudent.studentId = student.id

                    db.session.add(courseAndStudent)




        return render_template("teacher_templates/importclassinfo.html",message="添加成功",courseId=courseId,name=name)









@teacherBP.route("import/individual",methods=['GET',"POST"])
def ImportIndivaidual():
    if session.get("id") is None:
        return redirect("/user/login")
    name=session.get("name")
    courseId =request.args.get("id")

    if request.method=="GET":


        return render_template("teacher_templates/importindividual.html",courseId=courseId,name=name)
    else:
        name=request.form.get("name")
        password=request.form.get("password")
        gpa=request.form.get("gpa")
        email=request.form.get("email")
        programme=request.form.get("programme")
        id=request.form.get("id")

        if email =="" or password =="" or gpa=="" or programme=="" or name=="" or id=="":
            return render_template("teacher_templates/importindividual.html", courseId=courseId, name=name,message="参数不完全")

        student=Student.query.filter_by(email=email).first()
        if student:
            return render_template("teacher_templates/importindividual.html", courseId=courseId, name=name,message="该学生已经存在")
        student=Student.query.filter_by(id=id).first()
        if student:
            return render_template("teacher_templates/importindividual.html", courseId=courseId, name=name,message="该学生已经存在")



        with db.auto_commit():
            student = Student(name,id,gpa,email,password,programme)

            # 数据库的insert操作
            db.session.add(student)

        student=Student.query.filter_by(email=email).first()
        if student is not None:
            with db.auto_commit():
                courseAndStudent = CourseAndStudent()
                courseAndStudent.CourseId = courseId
                courseAndStudent.studentId = student.id
                db.session.add(courseAndStudent)

        return render_template("teacher_templates/importindividual.html", courseId=courseId, name=name, message="学生提交成功")






