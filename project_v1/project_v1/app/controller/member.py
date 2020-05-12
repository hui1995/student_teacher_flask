from flask import Blueprint,render_template, request
from app.models.student import Student
from app.models.member import Member

memberBP = Blueprint('member',__name__)

@memberBP.route('', methods=['GET'])
def get_member():
    with Student.auto_commit():
        member = Member("Mario", 3.0,'aaa@mail.uic.edu.hk','A','123456')
        # 数据库的insert操作
        Student.session.add(member)
    
    return 'hello member'


@memberBP.route('edit', methods=['GET'])
def edit_member():
    return render_template('teacher_templates/enternumofgroup.html')