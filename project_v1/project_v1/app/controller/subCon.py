from flask import Blueprint,render_template, request
from app.models.base import db
from app.models.subCon import SubCon

subConBP = Blueprint('subCon',__name__)

@subConBP.route('', methods=['GET'])
def get_subCon():
    with db.auto_commit():
        subCon = SubCon()
        subCon.contribution = '0'
        db.session.add(subCon)
    return 'sc'