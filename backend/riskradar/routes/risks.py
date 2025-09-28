import uuid
from flask import Blueprint, jsonify, request, abort

bp = Blueprint("risks", __name__)

# in-memory store
RISKS = {}

@bp.get("/")
def list_risks():
    return jsonify(list(RISKS.values()))

@bp.post("/")
def create_risk():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    likelihood = data.get("likelihood")
    impact = data.get("impact")

    if not title or likelihood is None or impact is None:
        abort(400, description="title, likelihood, impact are required")

    rid = uuid.uuid4().hex[:8]
    score = int(likelihood) * int(impact)
    item = {
        "id": rid,
        "title": title,
        "likelihood": int(likelihood),
        "impact": int(impact),
        "score": score,
        "notes": data.get("notes", "")
    }
    RISKS[rid] = item
    return jsonify(item), 201

@bp.get("/<rid>")
def get_risk(rid: str):
    item = RISKS.get(rid)
    if not item:
        abort(404)
    return jsonify(item)

@bp.put("/<rid>")
def update_risk(rid: str):
    item = RISKS.get(rid)
    if not item:
        abort(404)
    data = request.get_json(silent=True) or {}
    for k in ("title","likelihood","impact","notes"):
        if k in data:
            item[k] = int(data[k]) if k in ("likelihood","impact") else data[k]
    item["score"] = int(item["likelihood"]) * int(item["impact"])
    RISKS[rid] = item
    return jsonify(item)

@bp.delete("/<rid>")
def delete_risk(rid: str):
    if rid not in RISKS:
        abort(404)
    del RISKS[rid]
    return "", 204
