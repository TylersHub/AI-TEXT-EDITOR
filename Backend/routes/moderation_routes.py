# moderation_routes.py
from flask import Blueprint, request, jsonify
from config import supabase
from utils import update_user_tokens

moderation_bp = Blueprint('moderation', __name__)

# Submit blacklist word for review
@moderation_bp.route('/blacklist', methods=['POST'])
def submit_blacklist_word():
    data = request.get_json()
    existing = supabase.table('blacklist').select('*').eq('word', data['word']).execute()
    if existing.data:
        return jsonify({'error': 'Already blacklisted'}), 400

    submission = supabase.table('blacklist_submissions').insert({
        'user_id': data['user_id'],
        'word': data['word'],
        'status': 'pending'
    }).execute().data[0]

    return jsonify({'message': 'Submitted for review', 'submission_id': submission['id']})


# Review blacklist submission
@moderation_bp.route('/blacklist/review', methods=['POST'])
def review_blacklist():
    data = request.get_json()
    submission = supabase.table('blacklist_submissions').select('*') \
        .eq('id', data['submission_id']).execute().data[0]

    if data['decision'] == 'approve':
        supabase.table('blacklist').insert({'word': submission['word']}).execute()

    supabase.table('blacklist_submissions').update({'status': data['decision']}) \
        .eq('id', data['submission_id']).execute()

    return jsonify({'message': f"Word {data['decision']}."})


# Submit a user complaint
@moderation_bp.route('/complaints', methods=['POST'])
def submit_complaint():
    data = request.get_json()
    comp = supabase.table('complaints').insert({
        'complainant_id': data['complainant_id'],
        'accused_id': data['accused_id'],
        'document_id': data['document_id'],
        'reason': data['reason'],
        'status': 'pending'
    }).execute().data[0]
    return jsonify(comp)


# View all complaints (super user panel)
@moderation_bp.route('/complaints', methods=['GET'])
def get_complaints():
    res = supabase.table('complaints').select('*').execute()
    return jsonify(res.data)


# Resolve a complaint and apply penalties
@moderation_bp.route('/complaints/<comp_id>/resolve', methods=['POST'])
def resolve_complaint(comp_id):
    data = request.get_json()
    comp = supabase.table('complaints').select('*').eq('id', comp_id).execute().data[0]
    target = comp['accused_id'] if data['decision'] == 'valid' else comp['complainant_id']
    update_user_tokens(target, -data.get('penalty', 1))

    supabase.table('complaints').update({
        'status': f"resolved_{data['decision']}"
    }).eq('id', comp_id).execute()

    return jsonify({'message': f"{data['decision']} and penalty applied"})
