from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        handle_or_email = request.form.get("handle")
        pwd = request.form.get("password")

        if not handle_or_email or not pwd:
            flash("⚠️ Vui lòng nhập đầy đủ thông tin.")
            return render_template("auth_login.html")

        user = User.query.filter((User.handle == handle_or_email) | (User.email == handle_or_email)).first()

        if user and user.check_password(pwd):
            login_user(user)
            flash("🎉 Đăng nhập thành công!")
            return redirect(url_for("problems.list_problems"))
        else:
            flash("❌ Sai tài khoản hoặc mật khẩu.")

    return render_template("auth_login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        handle = request.form.get("handle")
        email = request.form.get("email")
        pwd = request.form.get("password")

        if not handle or not email or not pwd:
            flash("⚠️ Điền đầy đủ thông tin.")
            return render_template("auth_register.html")

        existing = User.query.filter((User.handle == handle) | (User.email == email)).first()
        if existing:
            flash("⚠️ Handle hoặc email đã tồn tại.")
            return render_template("auth_register.html")

        user = User(handle=handle, email=email)
        user.set_password(pwd)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("🎉 Đăng ký thành công, chào mừng bạn!")
        return redirect(url_for("problems.list_problems"))

    return render_template("auth_register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("👋 Bạn đã đăng xuất.")
    return redirect(url_for("auth.login"))
