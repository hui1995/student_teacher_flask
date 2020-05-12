from flask import Blueprint,render_template, request
from app.models.base import db
from app.models.subItem import SubItem

subItemBP = Blueprint('subItem',__name__)

@subItemBP.route('', methods=['GET'])
def get_subItem():
    with db.auto_commit():
        subItem = SubItem('A',0)
        db.session.add(subItem)
    return 'si'