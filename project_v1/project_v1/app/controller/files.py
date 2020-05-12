from flask import Blueprint,render_template, request
from app.models.base import db
from app.models.files import File

fileBP = Blueprint('files',__name__)

@fileBP.route('', methods=['GET'])
def get_file():
    if request.method=="GET":
        return render_template('teacher_templates/selectfile.html')