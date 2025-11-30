# problems/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from models import db, Problem

problems_bp = Blueprint('problems', __name__)

@problems_bp.route("/")
def list_problems():
    q = request.args.get("q","")
    items = Problem.query.filter(Problem.title.ilike(f"%{q}%")).order_by(Problem.created_at.desc()).all()
    return render_template("problems_list.html", items=items, q=q)

@problems_bp.route("/new", methods=["GET","POST"])
@login_required
def new_problem():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        tags = request.form.get("tags","")
        p = Problem(title=title, description=description, tags=tags, author_id=current_user.id)
        db.session.add(p); db.session.commit()
        return redirect(url_for("problems.detail", problem_id=p.id))
    return render_template("problem_detail.html", edit=True, item=None)

@problems_bp.route("/<int:problem_id>")
def detail(problem_id):
    p = Problem.query.get_or_404(problem_id)
    return render_template("problem_detail.html", item=p, edit=False)

@problems_bp.route("/<int:problem_id>/edit", methods=["GET","POST"])
@login_required
def edit(problem_id):
    p = Problem.query.get_or_404(problem_id)
    if p.author_id != current_user.id: abort(403)
    if request.method == "POST":
        p.title = request.form["title"]; p.description = request.form["description"]; p.tags = request.form.get("tags","")
        db.session.commit()
        return redirect(url_for("problems.detail", problem_id=p.id))
    return render_template("problem_detail.html", item=p, edit=True)

@problems_bp.route("/<int:problem_id>/delete", methods=["POST"])
@login_required
def delete(problem_id):
    p = Problem.query.get_or_404(problem_id)
    if p.author_id != current_user.id: abort(403)
    db.session.delete(p); db.session.commit()
    return redirect(url_for("problems.list_problems"))