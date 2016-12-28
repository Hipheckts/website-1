from app import app, utils, login_signup, models, login_manager, post, faculty, page
from app.utils import render_with_navbar
from app.models import User, Post, Page, Faculty, Message
from flask_login import login_required
from flask import request, redirect

@app.route('/')
@app.route('/index/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_with_navbar("index.html", posts=posts)

@app.route('/page/<string:page_name>/')
def render_page(page_name):
    page = Page.query.filter_by(name=page_name).first()
    if page:
        return render_with_navbar("page.html", page=page)
    return page_not_found(404)

@app.route('/newpage/', methods=["GET", "POST"])
@login_required
def new_page():
    return page.new_page()

@app.route('/page/<string:page_name>/delete')
@login_required
def delete_page(page_name):
    return page.delete_page(page_name)

@app.route('/page/<string:page_name>/edit', methods=["GET", "POST"])
@login_required
def edit_page(page_name):
    return page.edit_page(page_name)

@app.route('/news/')
def news():
    if request.args.get("postid"):
        post = Post.query.filter_by(id=request.args.get("postid")).first()
        if post:
            return render_with_navbar("news/newsitem.html", post=post, heading="LASA News")
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_with_navbar("news/news.html", posts=posts, heading="LASA News")

@app.route('/messages/')
def messages():
    if request.args.get("postid"):
        post = Message.query.filter_by(id=request.args.get("postid")).first()
        if post:
            return render_with_navbar("news/newsitem.html", post=post, heading="Principal's Messages")
    posts = Message.query.order_by(Message.timestamp.desc())
    return render_with_navbar("news/news.html", posts=posts, heading="Principal's Messages")

@app.route('/message/')
def message():
    post = Message.query.order_by(Message.timestamp.desc()).first()
    if not post:
        return redirect("/newmessage")
    return render_with_navbar("news/newsitem.html", post=post, heading="Principal's Message")

@app.route('/faculty/')
def all_faculty():
    faculty = Faculty.query.order_by(Faculty.lastname.asc())
    return render_with_navbar("faculty/faculty.html", faculty=faculty, title="Faculty")

@app.route('/administration/')
def administration():
    administrators = Faculty.query.filter_by(category="admin").order_by(Faculty.lastname.asc())
    return render_with_navbar("faculty/faculty.html", faculty=administrators, title="Administration")

@app.route('/guidance/')
def guidance():
    counselors = Faculty.query.filter_by(category="guidance").order_by(Faculty.lastname.asc())
    return render_with_navbar("faculty/faculty.html", faculty=counselors, title="Guidance and Counseling")

@app.route('/teachers/')
def teachers():
    teachers = Faculty.query.filter_by(category="teaching").order_by(Faculty.lastname.asc())
    return render_with_navbar("faculty/faculty.html", faculty=teachers, title="Teachers")

@app.route('/support/')
def support():
    support = Faculty.query.filter_by(category="support").order_by(Faculty.lastname.asc())
    return render_with_navbar("faculty/faculty.html", faculty=support, title="Support Staff")

@app.route("/login/", methods=["GET", "POST"])
def login():
    return login_signup.login()

@app.route("/logout/", methods=["GET", "POST"])
def logout():
    return login_signup.logout()

@app.route("/newpost/", methods=["GET", "POST"])
@login_required
def new_post():
    return post.new_post()

@app.route("/editpost/", methods=["GET", "POST"])
@login_required
def edit_post():
    return post.edit_post()

@app.route("/delpost/")
@login_required
def delete_post():
    return post.delete_post()

@app.route("/newmessage/", methods=["GET", "POST"])
@login_required
def new_message():
    return post.new_message()

@app.route("/editmessage/", methods=["GET", "POST"])
@login_required
def edit_message():
    return post.edit_message()

@app.route("/delmessage/")
@login_required
def delete_message():
    return post.delete_message()

@app.route("/newfaculty/", methods=["GET", "POST"])
@login_required
def new_faculty():
    return faculty.new_faculty()

@app.route("/editfaculty/", methods=["GET", "POST"])
@login_required
def edit_faculty():
    return faculty.edit_faculty()

@app.route("/delfaculty/")
@login_required
def delete_faculty():
    return faculty.delete_faculty()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.errorhandler(404)
def page_not_found(e):
    return render_with_navbar('404.html'), 404
