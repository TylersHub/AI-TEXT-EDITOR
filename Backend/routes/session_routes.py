from flask import Blueprint, request, jsonify
from config import supabase
import uuid
from datetime import datetime, timedelta, timezone

session_bp = Blueprint('session', __name__)

# Create a session token for a user
def create_session(user_id):
    token = str(uuid.uuid4())
    expires = datetime.now(timezone.utc) + timedelta(hours=24)

    supabase.table('sessions').insert({
        'session_token': token,
        'user_id': user_id,
        'expires_at': expires.isoformat()
    }).execute()

    return token


# Validate token route (used in next step)
@session_bp.route('/auth/session/validate', methods=['POST'])
def validate_session():
    data = request.get_json()
    token = data.get('session_token')
    if not token:
        return jsonify({'valid': False, 'error': 'No token provided'}), 400

    # Look up session token that hasn't expired
    res = supabase.table('sessions').select('*') \
        .eq('session_token', token).gt('expires_at', 'now()').execute()

    if not res.data:
        return jsonify({'valid': False}), 200

    return jsonify({'valid': True, 'user_id': res.data[0]['user_id']})

# remove the session token from the sessions table

@session_bp.route('/auth/logout', methods=['POST'])
def logout():
    data = request.get_json()
    token = data.get('session_token')

    if not token:
        return jsonify({'success': False, 'error': 'Missing session_token'}), 400

    supabase.table('sessions').delete().eq('session_token', token).execute()
    return jsonify({'success': True, 'message': 'Signed out successfully'})
