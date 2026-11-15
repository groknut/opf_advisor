from flask import Blueprint, jsonify, request
from src.models import BusinessScale, ActivityType
from src.services.recommender import Answers, recommend

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.post("/recommend")
def api_recommend():
    data = request.get_json()
    answers = Answers(
        activity=ActivityType(data["activity"]),
        scale=BusinessScale(data["scale"]),
        founders_count=data["founders_count"],
        need_investments=data["need_investments"],
        unlimited_liability_ok=data["unlimited_liability_ok"],
    )
    opf, reason = recommend(answers)
    return jsonify({"opf": opf.value, "reason": reason})
