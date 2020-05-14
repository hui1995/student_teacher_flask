from flask import Blueprint,render_template, request,redirect,session
from app.models.student import Student
from app.models.member import Member
from app.models.team import Team
from app.models.course import Course
from app.models.base import db


memberBP = Blueprint('member',__name__)

@memberBP.route('', methods=['GET'])
def get_member():
    with Student.auto_commit():
        member = Member("Mario", 3.0,'aaa@mail.uic.edu.hk','A','123456')
        # 数据库的insert操作
        Student.session.add(member)
    
    return 'hello member'


@memberBP.route('edit', methods=['GET',"POST"])
def edit_member():
    if session.get("id") is None:
        return redirect("/user/login")
    name = session.get("name")
    courseId=request.args.get("id")
    if request.method=="GET":
        courselst=Course.query.all()



        return render_template('teacher_templates/enternumofgroup.html',result=courselst,name=name,courseId=courseId)
    courseId=request.args.get("id")
    total=request.form.get("total")
    Course.query.filter(Course.CourseId==courseId).update({"totalNum":total})
    db.session.commit()
    return redirect("/member/choose/method?courseId="+courseId)

@memberBP.route('choose/method', methods=['GET',"POST"])
def choosemethod():
    if session.get("id") is None:
        return redirect("/user/login")
    name = session.get("name")
    courseId=request.args.get("courseId")
    return render_template('teacher_templates/choosemethod.html',name=name,courseId=courseId)


@memberBP.route('list', methods=['GET',"POST"])
def list():
    if session.get("id") is None:
        return redirect("/user/login")
    name = session.get("name")

    member=Member.query.filter(Member.studentId==session.get("id")).first()

    memberlst=Member.query.filter(Member.teamId==member.teamId)
    result=[]
    for i in memberlst:
        if i.contribution is not None:
            continue
        if i.studentId==session.get("id"):
            continue
        dict={}
        dict['id']=i.id
        dict['name']=Student.query.filter(Student.id==i.studentId).first().name
        result.append(dict)

    courseId=request.args.get("courseId")
    return render_template('student_templates/member.html',name=name,courseId=courseId,result=result)






@memberBP.route('evaluate', methods=['GET', "POST"])
def evaluate():
    if session.get("id") is None:
        return redirect("/user/login")
    name = session.get("name")
    id =request.args.get("id")

    if request.method=="GET":
        return render_template('student_templates/setcontribution.html',name=name)

    else:
        con=request.form.get("con")

        if con is  None or con =="":
            return render_template('student_templates/setcontribution.html', name=name,message="请填写评分")

        Member.query.filter(Member.id == id).update({"contribution":con})
        db.session.commit()




    return redirect("/member/list")


@memberBP.route('leader', methods=['GET', "POST"])
def evaluateLeader():
    if session.get("id") is None:
        return redirect("/user/login")
    name = session.get("name")

    if request.method=="GET":
        return render_template('student_templates/evaluateleader.html',name=name)

    else:
        con=request.form.get("con")

        if con is  None or con =="":
            return render_template('student_templates/evaluateleader.html', name=name,message="请填写评分")


        member=Member.query.filter(Member.studentId == session.get("id")).first()
        if member.leaderEvate is  not None:
            return render_template('student_templates/evaluateleader.html', name=name,message="已经填写过评分，不可以重复填写")

        member.leaderEvate=con
        db.session.commit()
        # 查询所有的成员
        memberlst = Member.query.filter(Member.teamId == member.teamId)
        memberCount=0
        count=0
        num=0
        for i in memberlst:
            count+=1
            if i.leaderEvate is not None:
                memberCount+=1
                num+=float(i.leaderEvate)
        if count==memberCount+1:

            teamLeader=Team.query.filter(Team.TeamNumber==member.teamId).first().leader
            memberLeader=Member.query.filter(Member.studentId == teamLeader).update({"contribution":num/memberCount})
            db.session.commit()




    return redirect("/student/display")



