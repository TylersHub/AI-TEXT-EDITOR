# moderation_routes.py
from flask import Blueprint, request, jsonify
from Backend.config import supabase
from Backend.utils import update_user_tokens, require_role

moderation_bp = Blueprint('moderation', __name__)

# ------------------------ BLACKLIST ------------------------

# Submit a word for blacklist review
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

# get blacklisted words
@moderation_bp.route('/blacklist/submissions', methods=['GET'])
@require_role(['super'])
def get_blacklist_submissions():
    res = supabase.table('blacklist_submissions').select('word, id, status, created_at').eq('status', 'pending').execute()
    return jsonify(res.data)


# Approve a blacklist word submission
@moderation_bp.route('/blacklist/approve', methods=['POST'])
@require_role(['super'])
def approve_blacklist_word():
    data = request.get_json()
    submission_id = data.get('submission_id')

    if not submission_id:
        return jsonify({'error': 'Missing submission_id'}), 400

    # Fetch word
    submission = supabase.table('blacklist_submissions').select('*') \
        .eq('id', submission_id).execute().data

    if not submission:
        return jsonify({'error': 'Submission not found'}), 404

    word = submission[0]['word']

    # Insert into blacklist
    supabase.table('blacklist').insert({'word': word}).execute()

    # Mark submission as approved
    supabase.table('blacklist_submissions').update({'status': 'approved'}) \
        .eq('id', submission_id).execute()

    return jsonify({'message': f'Word "{word}" approved and blacklisted'})

# Reject a blacklist word submission
@moderation_bp.route('/blacklist/reject', methods=['POST'])
@require_role(['super'])
def reject_blacklist_word():
    data = request.get_json()
    submission_id = data.get('submission_id')

    if not submission_id:
        return jsonify({'error': 'Missing submission_id'}), 400

    # Check it exists
    exists = supabase.table('blacklist_submissions').select('*') \
        .eq('id', submission_id).execute().data

    if not exists:
        return jsonify({'error': 'Submission not found'}), 404

    # Update status
    supabase.table('blacklist_submissions').update({'status': 'rejected'}) \
        .eq('id', submission_id).execute()

    return jsonify({'message': 'Word submission rejected'})


# ------------------------ COMPLAINTS ------------------------

# Submit a user complaint
@moderation_bp.route('/complaints', methods=['POST'])
@require_role(['paid', 'super'])
def submit_complaint():
    data = request.get_json()

    required = ['complainant_id', 'accused_id', 'document_id', 'reason']
    if any(k not in data for k in required):
        return jsonify({'error': 'Missing complaint data'}), 400

    comp = supabase.table('complaints').insert({
        'complainant_id': data['complainant_id'],
        'accused_id': data['accused_id'],
        'document_id': data['document_id'],
        'reason': data['reason'],
        'status': 'pending'
    }).execute().data[0]

    return jsonify(comp)


# View all complaints (admin panel)
@moderation_bp.route('/complaints', methods=['GET'])
@require_role(['super'])
def get_complaints():
    res = supabase.table('complaints').select('*').execute()
    return jsonify(res.data)


# Respond to complaint (by accused user)
@moderation_bp.route('/complaints/<comp_id>/response', methods=['POST'])
@require_role(['paid', 'super'])
def respond_to_complaint(comp_id):
    data = request.get_json()
    user_id = data.get('user_id')
    response = data.get('response')

    if not user_id or not response:
        return jsonify({'error': 'Missing user_id or response'}), 400

    complaint = supabase.table('complaints').select('accused_id') \
        .eq('id', comp_id).execute().data

    if not complaint:
        return jsonify({'error': 'Complaint not found'}), 404

    if complaint[0]['accused_id'] != user_id:
        return jsonify({'error': 'Only the accused can respond'}), 403

    supabase.table('complaints').update({'response': response}) \
        .eq('id', comp_id).execute()

    return jsonify({'message': 'Response submitted'})


# Resolve a complaint and apply penalties
@moderation_bp.route('/complaints/<comp_id>/resolve', methods=['POST'])
@require_role(['super'])
def resolve_complaint(comp_id):
    data = request.get_json()
    decision = data.get('decision')  # 'valid' or 'invalid'
    penalty = data.get('penalty', 1)

    if decision not in ['valid', 'invalid']:
        return jsonify({'error': 'Decision must be valid or invalid'}), 400

    comp = supabase.table('complaints').select('*') \
        .eq('id', comp_id).execute().data[0]

    target_id = comp['accused_id'] if decision == 'valid' else comp['complainant_id']

    update_user_tokens(target_id, -penalty)

    supabase.table('complaints').update({
        'status': f'resolved_{decision}'
    }).eq('id', comp_id).execute()

    return jsonify({'message': f'Complaint resolved as {decision}, penalty applied to {target_id}'})

# Combines approved + permanent blacklist

@moderation_bp.route('/blacklist/all', methods=['GET'])
def get_all_blacklisted_words():
    # Get words from permanent blacklist
    permanent = supabase.table('blacklist').select('word').execute().data
    perm_words = [entry['word'] for entry in permanent]

    # Get words from approved submissions (not yet added)
    approved = supabase.table('blacklist_submissions') \
        .select('word') \
        .eq('status', 'approved').execute().data
    approved_words = [entry['word'] for entry in approved]

    # Combine and deduplicate
    all_words = list(set(perm_words + approved_words))
    return jsonify({'blacklisted_words': all_words})
