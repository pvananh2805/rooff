# snippets/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from models import db, Snippet, Problem

snippets_bp = Blueprint("snippets", __name__)

@snippets_bp.route("/")
def list_snippets():
    snippets = Snippet.query.all()
    return render_template("snippets_list.html", snippets=snippets)

@snippets_bp.route("/new/<int:problem_id>", methods=["GET","POST"])
@login_required
def new(problem_id):
    problem = Problem.query.get_or_404(problem_id)
    if request.method == "POST":
        s = Snippet(
            title=request.form["title"],
            language=request.form["language"],
            code=request.form["code"],
            author_id=current_user.id,
            problem_id=problem.id
        )
        db.session.add(s)
        db.session.commit()
        return redirect(url_for("snippets.detail", snippet_id=s.id))
    return render_template("snippets_new.html", problem=problem)

@snippets_bp.route("/<int:snippet_id>")
def detail(snippet_id):
    s = Snippet.query.get_or_404(snippet_id)
    return render_template("snippet_detail.html", item=s)

@snippets_bp.route("/<int:snippet_id>/edit", methods=["GET","POST"])
@login_required
def edit(snippet_id):
    s = Snippet.query.get_or_404(snippet_id)
    if s.author_id != current_user.id:
        abort(403)
    if request.method == "POST":
        s.title = request.form["title"]
        s.language = request.form["language"]
        s.code = request.form["code"]
        db.session.commit()
        return redirect(url_for("snippets.detail", snippet_id=s.id))
    return render_template("snippets_new.html", problem=s.problem, item=s)

@snippets_bp.route("/<int:snippet_id>/delete", methods=["POST"])
@login_required
def delete(snippet_id):
    s = Snippet.query.get_or_404(snippet_id)
    if s.author_id != current_user.id:
        abort(403)
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for("problems.detail", problem_id=s.problem_id))
