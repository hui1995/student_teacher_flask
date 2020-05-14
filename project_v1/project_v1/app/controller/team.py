from flask import Blueprint,render_template, request,session,redirect
from app.models.base import db
from app.models.student import Student
from app.models.member import Member
from app.models.team import Team
from app.models.CourseAndStudent import CourseAndStudent
from sqlalchemy import desc



teamBP = Blueprint('team',__name__)

@teamBP.route('', methods=['GET'])
def get_team():
    with db.auto_commit():
        team = Team()
        team.TeamName = 'g1'
        team.TeamNumber = 0
        # 数据库的insert操作
        db.session.add(team)
    
    return 'hello team'


@teamBP.route('vote', methods=['GET',"POST"])
def vote_team():
    if session.get("id") is None:
        return redirect("/user/login")
    name2 = session.get("name")

    if request.method=="GET":


        return render_template('student_templates/voteleader.html',name=name2)
    else:
        name=request.form.get("name")

        student=Student.query.filter_by(name=name).first()
        if student is None:
            return render_template('student_templates/voteleader.html',message="该成员不存在",name=name2)
        currentId=session.get("id")

        curentmember=Member.query.filter(Member.studentId==currentId).first()


        member=Member.query.filter(Member.studentId==student.id).filter(Member.teamId==curentmember.teamId).first()
        if member is None:
            return render_template('student_templates/voteleader.html', message="不是该组成员",name=name2)

        member.votenum=member.votenum+1
        curentmember.isVote=1
        db.session.commit()

        memberlst=Member.query.filter(Member.teamId==curentmember.teamId).order_by(desc(Member.votenum))
        count=0

        voteNum=0

        for i in memberlst:
            count+=1
            voteNum=voteNum+i.votenum
        if count==voteNum:
            leader=memberlst.first()
            team=Team.query.filter(Team.TeamNumber==curentmember.teamId).update({"leader":leader.studentId})
            db.session.commit()
        return redirect("/student")

@teamBP.route('create', methods=['GET',"POST"])

def createTeam():
    if session.get("id") is None:
        return redirect("/user/login")
    name = session.get("name")
    if request.method=="GET":
        return render_template('student_templates/createTeam.html',name=name)
    else:
        name=request.form.get("name")
        userId=session.get("id")
        course=CourseAndStudent.query.filter(CourseAndStudent.studentId==userId).first()
        with db.auto_commit():
            team =Team()
            team.courseId=course.CourseId
            team.TeamName=name
            team.isFinish=0
            db.session.add(team)
            team=Team.query.filter(Team.courseId==course.CourseId).order_by(Team.TeamNumber.desc()).first()

            member=Member()
            member.studentId=userId
            member.teamId=team.TeamNumber
            member.votenum=0

            db.session.add(member)

        return redirect('/student/display')







