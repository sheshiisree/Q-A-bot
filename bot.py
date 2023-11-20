import logging
import traceback

from flask import Blueprint, request, jsonify
from services import BotService

bot = Blueprint("bot", __name__)
logger = logging.getLogger("bot")

bot_service_obj = BotService()

@bot.route("/preload_data", methods=["GET"])
def create():
    try:
        bot_service_obj.preload_data()
        return jsonify({"status": True, "message": "data updated"})
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@bot.route("/answer_question", methods=["POST"])
def answer_question():
    try:
        data = request.get_json()
        question = data["question"]
        response = bot_service_obj.answer_question(question)
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@bot.route("/load_conversation", methods=["GET"])
def load_conversation():
    try:
        data = request.args.to_dict()
        start_index = data["start_index"]
        stop_index = data["stop_index"]

        response = bot_service_obj.load_conversation(start_index, stop_index)
        
        print("response", response)
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@bot.route("/full_list", methods=["GET"])
def full_list():
    try:
        response = bot_service_obj.full_list()
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@bot.route("/<int:user_id>/list", methods=["GET"])
def list(user_id):
    try:
        response = bot_service_obj.list_bot(user_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@bot.route("/<int:bot_id>/delete", methods=["DELETE"])
def delete(bot_id):
    try:
        response = bot_service_obj.delete_bot(bot_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@bot.route("/<int:bot_id>/deactivate", methods=["POST"])
def deactivate(bot_id):
    try:
        response = bot_service_obj.deactivate(bot_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@bot.route("/<int:bot_id>/activate", methods=["POST"])
def activate(bot_id):
    try:
        response = bot_service_obj.activate(bot_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500