
from flask import Blueprint,render_template, request,session,redirect
from app.models.base import db
from app.models.student import Student
from app.models.member import Member
from app.models.team import Team
from app.models.CourseAndStudent import CourseAndStudent
from app.models.course import Course
from app.models.invite import Invite

studentBP = Blueprint('student',__name__)

@studentBP.route('', methods=['GET'])
def get_student():
    # with db.auto_commit():
    #     student = Student('Mario', 4.0, 'aaaa@qq.com','123456')
    #     # 数据库的insert操作
    #     db.session.add(student)

    if session.get("id") is None:
        return redirect("/user/login")
    name = session.get("name")


    member=Member.query.filter(Member.studentId==session.get("id")).first()
    if member is None:
        isNotVote = True
        nothaveLeader = True
        isLeader = False
        haveTeam = False




    else:

        if member.isVote ==0:
            isNotVote=True
        else:
            isNotVote=False

        team=Team.query.filter(Team.TeamNumber==member.teamId).first()
        if team.leader is None:
            nothaveLeader=True
        else:
            nothaveLeader=False
        if team.leader==session.get("id"):
            isLeader=True
        else:
            isLeader=False

        member=Member.query.filter_by(studentId=session.get("id")).first()
        team=Team.query.filter_by(TeamNumber=member.teamId).first()
        if team.isFinish==1:
            haveTeam=True

        else:
            haveTeam=False

    return render_template('student_templates/student.html',name=name,isNotVote=isNotVote,nothaveLeader=nothaveLeader,isLeader=isLeader,haveTeam=haveTeam)

@studentBP.route("/password", methods=['GET',"POST"])
def update_student_password():


    if session.get("id") is None:
        return redirect("/user/login")
    name = session.get("name")

    if request.method=="GET":
        return render_template('student_templates/changepsw.html',name=name)
    else:
        oldpwd=request.form.get("oldpwd")
        newpwd=request.form.get("newpwd")
        newpwd2=request.form.get("newpwd2")
        id = session.get("id")
        if newpwd!=newpwd2:
            return render_template('student_templates/changepsw.html', name=name,message="两次密码不一直")


        student=Student.query.filter_by(id=id).first()
        if student.password!=oldpwd:
            return render_template('student_templates/changepsw.html', name=name,message="老密码错误")

        student.password=newpwd2
        db.session.commit()
        return render_template('student_templates/changepsw.html', name=name, message="修改成功")

@studentBP.route("/display", methods=['GET',"POST"])
def displayfirend():
    if session.get("id") is None:
        return redirect("/user/login")
    name = session.get("name")

    member=Member.query.filter(Member.studentId==session.get("id")).first()
    if member is None:
        canInvite=False



        #显示创建按钮，先查询出来当前课程学生的总数，然后查出每组的学生最大量，然后查询当前组的个数
        courseId=CourseAndStudent.query.filter_by(studentId=session.get("id")).first().CourseId
        totalNum=Course.query.filter_by(CourseId=courseId).first().numofmember
        teamNum=Team.query.filter_by(courseId=courseId).count()
        studentCount=CourseAndStudent.query.filter_by(CourseId=courseId).count()


        if totalNum*teamNum>=studentCount:
            canCreateTeam=False
        else:
            canCreateTeam=True
    else:
        canCreateTeam=False
        canInvite=True



    return render_template('student_templates/studentdisplay.html', name=name,canCreateTeam=canCreateTeam,canInvite=canInvite)


@studentBP.route("/invite", methods=['GET',"POST"])
def invitefirend():
    if session.get("id") is None:
        return redirect("/user/login")
    name2 = session.get("name")

    if request.method=="GET":

        return render_template('student_templates/choosefriend.html', name=name2,)
    else:
        name=request.form.get("name")

        student = Student.query.filter_by(name=name).first()
        if student is None:
            return render_template('student_templates/voteleader.html', message="该学生不存在", name=name2)


        member = Member.query.filter(Member.studentId == student.id).first()
        if member is not None:
            return render_template('student_templates/voteleader.html', message="该学生已经加入小组，不能邀请", name=name2)
        member = Member.query.filter(Member.studentId == session.get("id")).first()



        with db.auto_commit():
            invite=Invite()
            invite.inviteeId=session.get("id")
            invite.inviteId=student.id
            invite.teamId=member.teamId
            db.session.add(invite)
        return render_template('student_templates/voteleader.html', message="已经发送邀请", name=name2)


@studentBP.route("/invitation", methods=['GET',"POST"])
def invitation():
    if session.get("id") is None:
        return redirect("/user/login")
    id=session.get("id")
    name = session.get("name")
    invitelst=Invite.query.filter_by(inviteId=session.get("id")).all()
    result=[]
    for i in invitelst:
        dict1={}
        studentname=Student.query.filter(Student.id==i.inviteeId).first().name
        dict1['info']=studentname
        dict1['teamId']=i.teamId
        result.append(dict1)



    return render_template('student_templates/viewinvitation.html', name=name,result=result)


@studentBP.route("/join", methods=['GET', "POST"])
def join():
    if session.get("id") is None:
        return redirect("/user/login")
    name = session.get("name")
    teamId=request.args.get("id")
    team=Team.query.filter_by(TeamNumber=teamId).first()
    #查询该成员是否满员，如果满员禁止加入

    if team.isFinish==1:
        return render_template('student_templates/viewinvitation.html', name=name, message="该小组满员了")

    courseId=CourseAndStudent.query.filter_by(studentId=session.get("id")).first().CourseId
    totalNum=Course.query.filter_by(CourseId=courseId).first().numofmember
    with db.auto_commit():
        memberr=Member()
        memberr.teamId=teamId
        memberr.studentId=session.get("id")
        memberr.votenum=0
        db.session.add(memberr)

    countMember=Member.query.filter_by(teamId=teamId).count()
    if totalNum==countMember:

            team.isFinish=1
            db.session.commit()

    invitelst=Invite.query.filter_by(inviteId=session.get("id")).delete()

    #检查该小组是否满员，满员则设置为isFInish=1
    #如果成功加入小组，则清除邀请信息
    invitelst = Invite.query.filter(Invite.inviteId == session.get("id"))

    result = []
    for i in invitelst:
        dict1 = {}
        studentname = Student.query.filter(Student.id == i.inviteeId).first().name
        dict1['info'] = studentname
        dict1['teamId'] = i.teamId
        result.append(dict1)

    return render_template('student_templates/viewinvitation.html', name=name, result=result)




