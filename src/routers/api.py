from flask import Blueprint, jsonify, request

from src.models import BusinessScale, ActivityType
from src.services.recommender import Answers, recommend

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.post("/recommend")
def api_recommend():
    data = request.get_json(force=True, silent=True) or {}
    try:
        answers = Answers(
            activity=ActivityType(data["activity"]),
            scale=BusinessScale(data["scale"]),
            founders_count=int(data["founders_count"]),
            need_investments=bool(data["need_investments"]),
            unlimited_liability_ok=bool(data["unlimited_liability_ok"]),
        )
    except (KeyError, ValueError, TypeError) as e:
        return jsonify({"error": "Некорректные входные данные", "detail": str(e)}), 400

    rec = recommend(answers)
    return jsonify({
        "opf": rec.opf.value,
        "opf_full_name": rec.opf.full_name,
        "reason": rec.reason,
        "tax_regime": rec.tax_regime.value,
        "tax_comment": rec.tax_comment,
        "pros": rec.pros,
        "cons": rec.cons,
        "next_steps": rec.next_steps,
        "risk_level": rec.risk_level,
        "alternatives": rec.alternatives,
    })