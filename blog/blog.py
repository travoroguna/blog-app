from flask import Blueprint, g, render_template, request, url_for, redirect, session, flash
from . import db
from .auth import login_required
import markdown
from markupsafe import escape


def escape(string):
    return string

marker = markdown.Markdown(extensions=['extra', 'codehilite', 'toc'])

blog = Blueprint('blog', __name__)
posts_per_page = 10


@blog.route('/')
def index():
    if g.get("page") is None:
        g.page = 1

    posts = [
        {
            "author": post.author,
            "created": post.created,
            "title": post.title,
            "body": marker.convert(escape(post.body)),
            "id": post.id,
            "author_id": post.author_id
        }
        for post in db.get_posts(posts_per_page * g.page)
    ]
    return render_template("blog/index.html", posts=posts)


@blog.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == "POST":
        post_name = request.form["postname"]
        markdown = request.form["markdown"]

        if not markdown:
            flash("Can not submit empty post")
            return render_template("blog/create.html", post_name=post_name, body="", is_new=True)
        else:

            db.new_post(post_name, escape(markdown))
            return redirect(url_for('blog.index'))
    return render_template("blog/create.html", post_name="", body="", is_new=True)


@blog.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id: int):
    post = db.get_post_by_id(id)

    if request.method == "POST":
        post_name = request.form["postname"]
        if markdown := request.form["markdown"]:
            db.edit_post(id, post_name, markdown)
            return redirect(url_for('blog.index'))

        else:
            flash("Can not submit empty post")
            return render_template("blog/create.html", post_name=post_name, body="", post_id=id)

    return render_template("blog/create.html", post_id=id, post_name=post.title, body=escape(post.body))


@blog.route('/<int:id>/delete', methods=('POST', ))
@login_required
def delete(id: int):
    db.delete_post(id)
    return redirect(url_for('blog.index'))


@blog.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id: int):
    post = db.get_post_by_id(id)
    return render_template("blog/view.html", post=marker.convert(escape(post.body)), post_obj=post)