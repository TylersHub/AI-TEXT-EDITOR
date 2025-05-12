# token_routes.py
from flask import Blueprint, request, jsonify
from config import supabase
from utils import update_user_tokens, get_user_tokens, require_role

token_bp = Blueprint('token', __name__)

@token_bp.route('/tokens/add', methods=['POST'])
@require_role(['paid', 'super'])  # free users can't add manually
def add_tokens():
    data = request.get_json()
    amount = data.get('amount')
    user_id = data.get('user_id')

    if not amount or not user_id:
        return jsonify({'error': 'Missing amount or user_id'}), 400

    new_balance = update_user_tokens(user_id, amount)
    return jsonify({'message': 'Tokens added', 'new_balance': new_balance})


@token_bp.route('/tokens/deduct', methods=['POST'])
@require_role(['super'])  # Only super can deduct
def deduct_tokens():
    data = request.get_json()
    amount = data.get('amount')
    user_id = data.get('user_id')

    if not amount or not user_id:
        return jsonify({'error': 'Missing amount or user_id'}), 400

    new_balance = update_user_tokens(user_id, -amount)
    return jsonify({'message': 'Tokens deducted', 'new_balance': new_balance})
