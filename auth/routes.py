from flask import Blueprint, render_template, abort
from flask_login import login_required
from models import User

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/<handle>")
@login_required
def profile(handle):
    user = User.query.filter_by(handle=handle).first()
    if not user:
        abort(404)
    return render_template("user_profile.html", user=user)
