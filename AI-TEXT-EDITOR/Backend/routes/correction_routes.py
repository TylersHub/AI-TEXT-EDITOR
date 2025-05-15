from flask import Blueprint, request, jsonify
from Backend.config import supabase
from Backend.utils import get_user_tokens, update_user_tokens, require_role, log_action

correction_bp = Blueprint('correction', __name__)

# Self correction route
@correction_bp.route('/corrections/self', methods=['POST'])
@require_role(['paid'])
def self_correction():
    data = request.get_json()
    orig = data['original_text'].split()
    corr = data['corrected_text'].split()

    # Count differences
    diffs = sum(1 for i in range(min(len(orig), len(corr))) if orig[i] != corr[i])
    diffs += abs(len(orig) - len(corr))
    cost = (diffs + 1) // 2

    if get_user_tokens(data['user_id']) < cost:
        return jsonify({'error': 'Insufficient tokens'}), 400

    update_user_tokens(data['user_id'], -cost)

    supabase.table('corrections').insert({
        'document_id': data['document_id'],
        'user_id': data['user_id'],
        'type': 'manual',
        'original_text': data['original_text'],
        'corrected_text': data['corrected_text'],
        'tokens_used': cost
    }).execute()

    supabase.table('documents').update({
        'content': data['corrected_text'],
        'updated_at': 'now()'
    }).eq('id', data['document_id']).execute()

    return jsonify({'corrected_text': data['corrected_text'], 'tokens_used': cost})


# Apply LLM corrections
@correction_bp.route('/corrections/llm/apply', methods=['POST'])
@require_role(['paid'])
def apply_llm_corrections():
    data = request.get_json()
    cost = len(data['accepted_corrections'])

    if get_user_tokens(data['user_id']) < cost:
        return jsonify({'error': 'Insufficient tokens'}), 400

    update_user_tokens(data['user_id'], -cost)

    supabase.table('corrections').insert({
        'document_id': data['document_id'],
        'user_id': data['user_id'],
        'type': 'llm',
        'original_text': data['original_text'],
        'corrected_text': data['final_text'],
        'tokens_used': cost
    }).execute()

    supabase.table('documents').update({
        'content': data['final_text'],
        'updated_at': 'now()'
    }).eq('id', data['document_id']).execute()

    bonus = 0
    if len(data['original_text'].split()) > 10 and cost == 0:
        bonus = 3
        update_user_tokens(data['user_id'], bonus)
        log_action(data['user_id'], 'correction_bonus', f"Bonus {bonus} tokens")

    return jsonify({'final_text': data['final_text'], 'tokens_used': cost, 'bonus_tokens': bonus})


# Submit LLM rejection
@correction_bp.route('/corrections/llm/reject', methods=['POST'])
def reject_llm_corrections():
    data = request.get_json()

    rejection = supabase.table('llm_rejections').insert({
        'user_id': data['user_id'],
        'document_id': data['document_id'],
        'reason': data['reason'],
        'status': 'pending'
    }).execute().data[0]

    update_user_tokens(data['user_id'], -1)

    return jsonify({'message': 'Rejection submitted', 'tokens_used': 1, 'rejection_id': rejection['id']})


# Review LLM rejection by super user
@correction_bp.route('/corrections/llm/review-rejection', methods=['POST'])
def review_llm_rejection():
    data = request.get_json()

    rejection = supabase.table('llm_rejections').select('*').eq('id', data['rejection_id']).execute().data[0]

    supabase.table('llm_rejections').update({
        'status': data['decision']
    }).eq('id', data['rejection_id']).execute()

    if data['decision'] == 'rejected':
        update_user_tokens(rejection['user_id'], -5)
        return jsonify({'message': 'Penalty applied', 'penalty': 5})

    return jsonify({'message': 'Rejection accepted'})

# view all LLM rejection reports | This will be used for moderation/review purposes by super users
@correction_bp.route('/corrections/llm/rejections', methods=['GET'])
@require_role(['super'])
def get_llm_rejections():
    res = supabase.table('llm_rejections').select(
        'id, user_id, document_id, reason, status, created_at'
    ).eq('status', 'pending').execute()

    return jsonify(res.data)
