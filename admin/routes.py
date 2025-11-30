from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from functools import wraps

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route("/")
@admin_required
def dashboard():
    return render_template("admin_dashboard.html")

@admin_bp.route("/users")
@admin_required
def manage_users():
    # ví dụ: liệt kê tất cả user
    from models import User
    users = User.query.all()
    return render_template("admin_users.html", users=users)