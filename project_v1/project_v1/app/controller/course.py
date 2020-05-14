from flask import Blueprint,render_template, request,redirect,session
from app.models.base import db
from app.models.course import Course
from app.models.CourseAndStudent import CourseAndStudent
from app.models.student import Student
from app.models.team import Team
from app.models.member import Member

courseBP = Blueprint('course',__name__)

@courseBP.route('', methods=['GET','POST'])
def get_course():
    if session.get("id") is None:
        return redirect("/user/login")
    name2 = session.get("name")

    if request.method=="GET":


        return render_template('teacher_templates/importcourse.html',name=name2)

    else:
        name=request.form.get("name")
        if name=="" or name is None:
            return render_template('teacher_templates/importcourse.html', message="title不能为空")

        course =Course.query.filter_by(courseName=name).filter_by(teacherId=session.get("id")).first()
        if course:
            return render_template('teacher_templates/importcourse.html', message="该课程已经存在")

        with db.auto_commit():
            course = Course()
            course.courseName = name
            course.teacherId=session.get("id")
            db.session.add(course)
        return redirect("/course")


@courseBP.route("/display",methods=['GET'])
def teacherDisplay():
    if session.get("id") is None:
        return redirect("/user/login")
    name=session.get("name")

    id=request.args.get("id")

    course=Course.query.filter_by(CourseId=id).first()
    if course.teamType is None:
        isTeamType=False
    else:
        isTeamType=True




    return render_template('teacher_templates/teacherdisplay.html',name=name,id=id,isTeamType=isTeamType)


@courseBP.route("/method1", methods=["GET"])
def Method1():
    if session.get("id") is None:
        return redirect("/user/login")
    name = session.get("name")
    courseId = request.args.get("courseId")


    return render_template("teacher_templates/method2.html", name=name,courseId=courseId)


@courseBP.route("/method2", methods=["GET"])
def Method2():
    if session.get("id") is None:
        return redirect("/user/login")
    name = session.get("name")
    courseId = request.args.get("courseId")

    Course.query.filter(Course.CourseId == courseId).update({"teamType": 1})
    db.session.commit()


    return redirect("/course/display?id="+courseId)


@courseBP.route("/method3", methods=["GET"])
def Method3():
    if session.get("id") is None:
        return redirect("/user/login")
    name = session.get("name")

    return render_template("teacher_templates/method3.html")


@courseBP.route("by/gpa", methods=['GET'])
def byGPA():
    if session.get("id") is None:
        return redirect("/user/login")
    name = session.get("name")

    return render_template("teacher_templates/floatband.html")

import random

@courseBP.route("by/student",methods=['GET'])
def byStudent():
    if session.get("id") is None:
        return redirect("/user/login")
    name=session.get("name")
    courseId=request.args.get("courseId")

    studentList=CourseAndStudent.query.filter_by(CourseId=courseId).all()
    list=[]
    for i in studentList:

        student=Student.query.filter_by(id=i.studentId).first()
        list.append(student)


    #每组的人数
    totalNum=Course.query.filter_by(CourseId=courseId).first().numofmember


    #组的数量
    # teamNum=len(list)/totalNum+1
    # print(teamNum)
    #
    # if teamNum==1:
    #     list2=[]
    #     list2.append(list)
    #     pass
    # else:
    from random import shuffle

    shuffle(list)  # 重排序
    list2 = []
    for i in range(0, len(list), totalNum):
        list2.append(list[i:i + totalNum])

    result=[]

    for i in list2:
        dict1 = dict()

        nameTeam=random.randint(100,1000)
        dict1["name"]=str(nameTeam)
        dict1["value"]=i
        print(i)
        result.append(dict1)

        with db.auto_commit():
            team = Team()
            team.TeamName=str(nameTeam)
            team.courseId=courseId
            # 数据库的insert操作
            db.session.add(team)

        team=Team.query.filter(Team.courseId==courseId).filter(Team.TeamName==nameTeam).first()
        with db.auto_commit():
            for x in i:
                member=Member()
                member.teamId=team.TeamNumber
                member.studentId=x.id
                db.session.add(member)


    Course.query.filter(Course.CourseId == courseId).update({"teamType": 2})
    db.session.commit()
    return render_template("teacher_templates/displaygroup.html",name=name,courseId=courseId,result=result)



