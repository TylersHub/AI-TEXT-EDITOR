from flask import Blueprint, jsonify
from config import supabase
from utils import require_role

stats_bp = Blueprint('stats', __name__)

# View user statistics (only for paid and super users)
@stats_bp.route('/stats/<user_id>', methods=['GET'])
@require_role(['paid', 'super'])
def get_user_stats(user_id):
    user = supabase.table('users').select('tokens').eq('id', user_id).execute().data[0]

    submissions = supabase.table('documents').select('id').eq('owner_id', user_id).execute().data
    total_submissions = len(submissions)

    corrections = supabase.table('corrections').select('tokens_used').eq('user_id', user_id).execute().data
    total_corrections = len(corrections)
    total_tokens_used = sum(c['tokens_used'] for c in corrections)

    stats = {
        'user_id': user_id,
        'available_tokens': user['tokens'],
        'total_submissions': total_submissions,
        'total_corrections': total_corrections,
        'total_tokens_used': total_tokens_used
    }

    return jsonify(stats)
