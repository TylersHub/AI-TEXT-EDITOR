# token_routes.py
from flask import Blueprint, request, jsonify
from config import supabase
from utils import update_user_tokens, get_user_tokens, require_role

token_bp = Blueprint('token', __name__)

@token_bp.route('/tokens/add', methods=['POST'])
@require_role(['paid', 'super'])  # free users shouldn't add manually
def add_tokens():
    data = request.get_json()
    amount = data.get('amount')
    user_id = data.get('user_id')

    if not amount or not user_id:
        return jsonify({'error': 'Missing amount or user_id'}), 400

    # Upgrade user to paid if they are still marked as free
    user = supabase.table('users').select('user_type').eq('id', user_id).execute().data[0]
    if user['user_type'] == 'free':
        supabase.table('users').update({'user_type': 'paid'}).eq('id', user_id).execute()

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

# any user can deduct tokens from themselves

@token_bp.route('/tokens/charge', methods=['POST'])
def charge_token():
    data = request.get_json()
    user_id = data.get('user_id')
    amount = data.get('amount', 1)  # defaults to 1 token

    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400

    current = get_user_tokens(user_id)
    if current < amount:
        return jsonify({'error': 'Insufficient tokens'}), 400

    new_balance = update_user_tokens(user_id, -amount)
    return jsonify({
        'message': f'{amount} token(s) charged',
        'new_balance': new_balance
    })
