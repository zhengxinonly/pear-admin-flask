from flask import Blueprint, render_template

views_bp = Blueprint("views", __name__, url_prefix="/views")


@views_bp.get("/rights")
def rights_view():
    return render_template("views/rights/index.html")
