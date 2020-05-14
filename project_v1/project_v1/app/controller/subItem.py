from flask import Blueprint,render_template, request,redirect,session
from app.models.base import db
from app.models.subItem import SubItem

subItemBP = Blueprint('subItem',__name__)

@subItemBP.route('', methods=['GET'])
def get_subItem():
    if session.get("id") is None:
        return redirect("/user/login")
    name = session.get("name")
    courseId=request.args.get("id")

    subItemList=SubItem.query.all()

    return render_template('teacher_templates/edititems.html',result=subItemList,name=name,courseId=courseId)

@subItemBP.route('delete', methods=['GET'])

def delete_subItem():
    if request.method == "GET":
        id=request.args.get("id",None)
        title = request.args.get("title", None)
        if title is not None and title != "":
            SubItem.query.filter(SubItem.title == title).filter(SubItem.courseId==id).delete()
            db.session.commit()


        return redirect("/subItem?id="+id)



@subItemBP.route('/edit', methods=['GET',"POST"])
def edit_subItem():
    courseId = request.args.get("courseId", None)

    if request.method=="GET":
        title=request.args.get("title",None)
        id=request.args.get("id",None)


        if title is not  None and title!="":
            subItem=SubItem.query.filter(SubItem.title==title).filter(SubItem.courseId==courseId).first()
        else:
            subItem=None

        return render_template('teacher_templates/editoneitem.html', result=subItem)
    else:
        title = request.args.get("title", None)
        percentage=request.form.get("percentage",None)
        title2=request.form.get("title",None)
        if title is not None and title != "":
            SubItem.query.filter(SubItem.title==title).filter(SubItem.courseId==courseId).update({"percentage":percentage})

            db.session.commit()
        else:
            subItem=SubItem.query.filter(SubItem.title==title2).filter(SubItem.courseId==courseId).first()
            if subItem:
                return render_template("teacher_templates/editoneitem.html",message="title已经存在")

            with db.auto_commit():
                subItem = SubItem(title2,percentage)
                # 数据库的insert操作
                db.session.add(subItem)
        return redirect("/subItem?id="+courseId)



