from flask import Blueprint,render_template, request,redirect
from app.models.base import db
from app.models.course import Course

courseBP = Blueprint('course',__name__)

@courseBP.route('', methods=['GET','POST'])
def get_course():

    if request.method=="GET":
        return render_template('teacher_templates/importcourse.html')

    else:
        name=request.form.get("name")
        if name=="" or name is None:
            return render_template('teacher_templates/importcourse.html', message="title不能为空")

        course =Course.query.filter_by(courseName=name).first()
        if course:
            return render_template('teacher_templates/importcourse.html', message="该课程已经存在")

        with db.auto_commit():
            course = Course()
            course.courseName = name
            db.session.add(course)
        return redirect("/teacher/display")
