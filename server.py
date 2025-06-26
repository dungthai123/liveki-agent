import os
from livekit import api
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from livekit.api import LiveKitAPI, ListRoomsRequest
import uuid
import json

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load Chinese conversation topics
with open('TrumChinese.conversation_topics.json', 'r', encoding='utf-8') as f:
    CHINESE_TOPICS = json.load(f)

async def generate_room_name(category_id="general", topic_id="general"):
    base_name = f"room-chinese-{category_id}-{topic_id}-{str(uuid.uuid4())[:8]}"
    rooms = await get_rooms()
    while base_name in rooms:
        base_name = f"room-chinese-{category_id}-{topic_id}-{str(uuid.uuid4())[:8]}"
    return base_name

async def get_rooms():
    api = LiveKitAPI()
    rooms = await api.room.list_rooms(ListRoomsRequest())
    await api.aclose()
    return [room.name for room in rooms.rooms]

@app.route("/getToken")
async def get_token():
    name = request.args.get("name", "student")
    room = request.args.get("room", None)
    category_id = request.args.get("category_id", type=int)
    topic_id = request.args.get("topic_id", type=int)
    
    if not room:
        room = await generate_room_name(category_id or "general", topic_id or "general")
    
    # Create metadata with category_id and topic_id
    metadata = json.dumps({
        "category_id": category_id,
        "topic_id": topic_id
    })
        
    token = api.AccessToken(os.getenv("LIVEKIT_API_KEY"), os.getenv("LIVEKIT_API_SECRET")) \
        .with_identity(name)\
        .with_name(name)\
        .with_metadata(metadata)\
        .with_grants(api.VideoGrants(
            room_join=True,
            room=room
        ))
    print("🎟️ Generated token:", token.to_jwt())
    return token.to_jwt()

@app.route("/chinese-categories")
def get_chinese_categories():
    """Get all Chinese conversation categories"""
    categories = []
    for category in CHINESE_TOPICS:
        categories.append({
            "id": category["id"],
            "name": category["regions"]["en"]["name"],
            "display_order": category["display_order"],
            "topic_count": len(category["topic_details"])
        })
    
    # Sort by display_order
    categories.sort(key=lambda x: x["display_order"])
    
    return jsonify({
        "success": True,
        "categories": categories
    })

@app.route("/chinese-topics/<int:category_id>")
def get_chinese_topics_by_category(category_id):
    """Get all topics for a specific category"""
    for category in CHINESE_TOPICS:
        if category["id"] == category_id:
            topics = []
            for topic_detail in category["topic_details"]:
                topics.append({
                    "topic_id": topic_detail["topic_id"],
                    "title": topic_detail["regions"]["en"]["title"],
                    "description": topic_detail["regions"]["en"]["description"],
                    "tasks": topic_detail["regions"]["en"]["tasks"],
                    "image_url": topic_detail["image_url"]
                })
            
            return jsonify({
                "success": True,
                "category": {
                    "id": category["id"],
                    "name": category["regions"]["en"]["name"]
                },
                "topics": topics
            })
    
    return jsonify({"success": False, "error": "Category not found"}), 404

@app.route("/chinese-topic/<int:category_id>/<int:topic_id>")
def get_chinese_topic_detail(category_id, topic_id):
    """Get detailed information for a specific topic"""
    for category in CHINESE_TOPICS:
        if category["id"] == category_id:
            for topic_detail in category["topic_details"]:
                if topic_detail["topic_id"] == topic_id:
                    return jsonify({
                        "success": True,
                        "category": {
                            "id": category["id"],
                            "name": category["regions"]["en"]["name"]
                        },
                        "topic": {
                            "topic_id": topic_detail["topic_id"],
                            "title": topic_detail["regions"]["en"]["title"],
                            "description": topic_detail["regions"]["en"]["description"],
                            "tasks": topic_detail["regions"]["en"]["tasks"],
                            "image_url": topic_detail["image_url"],
                            "first_message": topic_detail["first_message"]
                        }
                    })
    
    return jsonify({"success": False, "error": "Topic not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)