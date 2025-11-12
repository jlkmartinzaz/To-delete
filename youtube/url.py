from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.config import Config
from models.video_model import Video
from models.user_model import User
from models import db
import requests, re, json

youtube_bp = Blueprint("youtube", __name__)

def extract_video_id(url: str):
    pattern = r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})"
    m = re.search(pattern, url)
    return m.group(1) if m else None

def get_current_user():
    identity = get_jwt_identity()
    if not identity:
        return None
    try:
        data = json.loads(identity)  # parseamos el string JSON
        user_id = data.get("id")
        if not user_id:
            return None
        return User.query.get(user_id)
    except Exception:
        return None

# -------------------------------
# Agregar video: user y admin
# -------------------------------
@youtube_bp.route("/", methods=["POST"])
@jwt_required()
def add_youtube_video():
    user = get_current_user()
    if not user or user.role not in ["user", "admin"]:
        return jsonify({"error": "No tienes permisos"}), 403

    data = request.get_json() or {}
    url = data.get("url")
    if not url:
        return jsonify({"error": "Falta la URL"}), 400

    vid = extract_video_id(url)
    if not vid:
        return jsonify({"error": "URL inválida"}), 400

    if Video.query.filter_by(youtube_id=vid).first():
        return jsonify({"error": "Video ya registrado"}), 409

    api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={vid}&key={Config.YOUTUBE_API_KEY}"
    res = requests.get(api_url)
    if res.status_code != 200:
        return jsonify({"error": "Error al contactar la API de YouTube"}), 500

    data = res.json()
    if not data.get("items"):
        return jsonify({"error": "Video no encontrado"}), 404

    item = data["items"][0]
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})

    video = Video(
        youtube_id=vid,
        title=snippet.get("title", ""),
        description=snippet.get("description", ""),
        likes=int(stats.get("likeCount", 0)) if stats.get("likeCount") else 0
    )

    db.session.add(video)
    db.session.commit()
    return jsonify(video.to_dict()), 201

# -------------------------------
# Listar videos: todos los roles
# -------------------------------
@youtube_bp.route("/", methods=["GET"])
@jwt_required()
def list_videos():
    vids = Video.query.all()
    return jsonify([v.to_dict() for v in vids]), 200

# -------------------------------
# Actualizar video: solo admin
# -------------------------------
@youtube_bp.route("/<int:video_id>", methods=["PUT"])
@jwt_required()
def update_video(video_id):
    user = get_current_user()
    if not user or user.role != "admin":
        return jsonify({"error": "No tienes permisos"}), 403

    video = Video.query.get(video_id)
    if not video:
        return jsonify({"error": "Video no encontrado"}), 404

    data = request.get_json() or {}
    url = data.get("url")
    if url:
        vid = extract_video_id(url)
        if not vid:
            return jsonify({"error": "URL inválida"}), 400

        api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={vid}&key={Config.YOUTUBE_API_KEY}"
        res = requests.get(api_url)
        if res.status_code != 200:
            return jsonify({"error": "Error al contactar la API de YouTube"}), 500

        yt_data = res.json()
        if not yt_data.get("items"):
            return jsonify({"error": "Video no encontrado"}), 404

        item = yt_data["items"][0]
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})

        video.youtube_id = vid
        video.title = snippet.get("title", "")
        video.description = snippet.get("description", "")
        video.likes = int(stats.get("likeCount", 0)) if stats.get("likeCount") else 0

        db.session.commit()
    return jsonify(video.to_dict()), 200

# -------------------------------
# Eliminar video: solo admin
# -------------------------------
@youtube_bp.route("/<int:video_id>", methods=["DELETE"])
@jwt_required()
def delete_video(video_id):
    user = get_current_user()
    if not user or user.role != "admin":
        return jsonify({"error": "No tienes permisos"}), 403

    video = Video.query.get(video_id)
    if not video:
        return jsonify({"error": "Video no encontrado"}), 404

    db.session.delete(video)
    db.session.commit()
    return jsonify({"message": "Video eliminado"}), 200
