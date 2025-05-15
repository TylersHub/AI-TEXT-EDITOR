from flask import Blueprint, request, jsonify, g
from Backend.config import supabase
from Backend.utils import log_action, require_role
from Backend.utils import get_user_tokens, update_user_tokens, log_action, check_blacklisted_words

import time

submission_bp = Blueprint('submission', __name__)

# Submit text and apply role-based restrictions
@submission_bp.route('/submit/text', methods=['POST'])
def submit_text():
    data = request.get_json()
    user_id, text = data['user_id'], data['text']
    user = supabase.table('users').select('*').eq('id', user_id).execute().data[0]
    role, tokens = user['user_type'], user['tokens']
    word_count = len(text.split())

    if role == 'free' and word_count > 20:
        supabase.table('lockouts').insert({
            'user_id': user_id,
            'reason': 'exceeded_word_limit',
            'expires_at': time.time() + 180
        }).execute()
        return jsonify({'error': 'Free users can only submit 20 words', 'lockout': True}), 403

    if role == 'paid' and tokens < word_count:
        penalty = tokens // 2
        update_user_tokens(user_id, -penalty)
        log_action(user_id, 'token_penalty', f"Penalty of {penalty} tokens")
        return jsonify({'error': 'Insufficient tokens', 'penalty': penalty}), 400

    censored, bl_count, bl_chars = check_blacklisted_words(text)
    total_cost = word_count + bl_chars if role == 'paid' else 0

    if role == 'paid' and tokens < total_cost:
        return jsonify({'error': 'Not enough tokens to cover blacklist cost'}), 400

    if total_cost > 0:
        update_user_tokens(user_id, -total_cost)
        log_action(user_id, 'submission_cost', f'Used {total_cost} tokens')

    doc = supabase.table('documents').insert({
        'owner_id': user_id,
        'title': data.get('title', 'Untitled Document'),
        'content': censored
    }).execute()

    return jsonify({'document': doc.data[0], 'tokens_used': total_cost})

@submission_bp.route('/documents/previews/<user_id>', methods=['GET'])
#@require_role(['free', 'paid', 'super'])
def file_previews(user_id):
    docs = supabase.table('documents') \
        .select('id, title, content') \
        .eq('owner_id', user_id).execute().data

    previews = []
    for doc in docs:
        preview_text = ' '.join(doc['content'].split()[:10])
        previews.append({
            'title': doc['title'],
            'preview': preview_text,
            'id': doc['id']
        })

    return jsonify(previews)

# users can open a full document (for editing or review)

@submission_bp.route('/documents/<doc_id>', methods=['GET'])
#@require_role(['free', 'paid', 'super'])
def open_document(doc_id):
    #user_id = g.user_id
    res = supabase.table('documents') \
        .select('id, title, content, owner_id, updated_at') \
        .eq('id', doc_id).execute()

    if not res.data:
        return jsonify({'error': 'Document not found'}), 404

    doc = res.data[0]
    return jsonify({
        'id': doc['id'],
        'title': doc['title'],
        'content': doc['content'],
        'owner_id': doc['owner_id'],
        'updated_at': doc['updated_at']
    })
