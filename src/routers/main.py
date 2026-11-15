from flask import Blueprint, render_template, request
from src.models import BusinessScale, ActivityType
from src.services.recommender import Answers, recommend

bp = Blueprint("main", __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            answers = Answers(
                activity=ActivityType(request.form["activity"]),
                scale=BusinessScale(request.form["scale"]),
                founders_count=int(request.form["founders_count"]),
                need_investments=request.form.get("need_investments") == "yes",
                unlimited_liability_ok=request.form.get("unlimited_liability") == "yes",
            )
        except (ValueError, KeyError):
            return render_template("index.html", error="Заполните все поля корректно.")

        opf, reason = recommend(answers)
        return render_template("result.html", opf=opf, reason=reason, answers=answers)

    return render_template("index.html")
