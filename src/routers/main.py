from flask import Blueprint, render_template, request, send_file, session, redirect, url_for
from io import BytesIO

from src.models import BusinessScale, ActivityType
from src.services.recommender import Answers, recommend
from src.utils.pdf_generator import generate_recommendation_pdf

bp = Blueprint("main", __name__)


def _parse_answers_from_form() -> Answers:
    return Answers(
        activity=ActivityType(request.form["activity"]),
        scale=BusinessScale(request.form["scale"]),
        founders_count=int(request.form["founders_count"]),
        need_investments=request.form.get("need_investments") == "yes",
        unlimited_liability_ok=request.form.get("unlimited_liability") == "yes",
    )


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            answers = _parse_answers_from_form()
        except (ValueError, KeyError):
            return render_template("index.html", error="Заполните все поля корректно.")

        recommendation = recommend(answers)

        session["last_answers"] = {
            "activity": answers.activity.value,
            "scale": answers.scale.value,
            "founders_count": answers.founders_count,
            "need_investments": answers.need_investments,
            "unlimited_liability_ok": answers.unlimited_liability_ok,
        }

        return render_template(
            "result.html",
            recommendation=recommendation,
            answers=answers,
        )

    return render_template("index.html")


@bp.route("/pdf")
def download_pdf():
    """Скачать PDF-отчёт по последней рекомендации."""
    data = session.get("last_answers")
    if not data:
        return redirect(url_for("main.index"))

    answers = Answers(
        activity=ActivityType(data["activity"]),
        scale=BusinessScale(data["scale"]),
        founders_count=data["founders_count"],
        need_investments=data["need_investments"],
        unlimited_liability_ok=data["unlimited_liability_ok"],
    )
    recommendation = recommend(answers)
    pdf_bytes = generate_recommendation_pdf(answers, recommendation)

    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"recomendaciya_opf_{recommendation.opf.value}.pdf",
    )