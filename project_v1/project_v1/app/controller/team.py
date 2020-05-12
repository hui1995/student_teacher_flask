from flask import Blueprint,render_template, request
from app.models.base import db
from app.models.team import Team

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