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

    subItemList=SubItem.query.filter(SubItem.courseId==courseId)

    return render_template('teacher_templates/edititems.html',result=subItemList,name=name,courseId=courseId)

@subItemBP.route('delete', methods=['GET'])

def delete_subItem():
    if request.method == "GET":
        id=request.args.get("courseId",None)
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


        if title is not  None and title!="":
            subItem=SubItem.query.filter(SubItem.title==title).filter(SubItem.courseId==courseId).first()
        else:
            subItem=None

        return render_template('teacher_templates/editoneitem.html', result=subItem,courseId=courseId)
    else:
        title = request.args.get("title", None)
        percentage=request.form.get("percentage",None)
        title2=request.form.get("title",None)
        if title is not None and title != "":
            sublist = SubItem.query.filter(SubItem.courseId == courseId)
            total = 0
            for i in sublist:
                if i.title!=title:
                    total += float(i.percentage)
            if total+float(percentage)>100:
                subItem = SubItem.query.filter(SubItem.title == title).filter(SubItem.courseId == courseId).first()

                return render_template("teacher_templates/editoneitem.html", message="综合不能超过一百哦",result=subItem,courseId=courseId)


            SubItem.query.filter(SubItem.title==title).filter(SubItem.courseId==courseId).update({"percentage":percentage})

            db.session.commit()
        else:


            #添加操作
            subItem=SubItem.query.filter(SubItem.title==title2).filter(SubItem.courseId==courseId).first()
            if subItem:
                return render_template("teacher_templates/editoneitem.html",message="title已经存在",courseId=courseId)


            sublist=SubItem.query.filter(SubItem.courseId==courseId)
            total=0
            for i in sublist:
                total+=float(i.percentage)
            if total+float(percentage)>100:
                return render_template("teacher_templates/editoneitem.html", message="综合不能超过一百哦",courseId=courseId)


            with db.auto_commit():
                subItem = SubItem(title2,percentage)
                subItem.courseId=courseId
                # 数据库的insert操作
                db.session.add(subItem)
        return redirect("/subItem?id="+courseId)



