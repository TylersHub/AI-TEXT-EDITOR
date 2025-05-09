from flask import Blueprint, request, jsonify
from config import supabase
from utils import log_action, require_role

auth_bp = Blueprint('auth', __name__)

# Register a new user
@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    res = supabase.table('users').insert({
        'email': data['email'],
        'password': data['password'],
        'user_type': data.get('user_type', 'free')
    }).execute()
    return jsonify(res.data[0]), 201

# Log in a user and check for lockout
@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    res = supabase.table('users').select('*').eq('email', data['email']).eq('password', data['password']).execute()
    if not res.data:
        return jsonify({'error': 'Invalid credentials'}), 401
    user = res.data[0]
    if user['user_type'] == 'free':
        lock = supabase.table('lockouts').select('*').eq('user_id', user['id']).gt('expires_at', 'now()').execute()
        if lock.data:
            return jsonify({'error': 'Account temporarily locked', 'expires_at': lock.data[0]['expires_at']}), 403
    log_action(user['id'], 'login')
    return jsonify(user)

# Submit a request to upgrade to paid
@auth_bp.route('/auth/upgrade', methods=['POST'])
def request_upgrade():
    data = request.get_json()
    res = supabase.table('upgrade_requests').insert({
        'user_id': data['user_id'],
        'status': 'pending',
        'notes': data.get('notes', '')
    }).execute()
    return jsonify({'message': 'Upgrade request submitted', 'data': res.data[0]})

# Approve upgrade request (super only)
@auth_bp.route('/auth/upgrade/approve', methods=['POST'])
@require_role(['super'])
def approve_upgrade():
    data = request.get_json()
    req = supabase.table('upgrade_requests').select('*').eq('id', data['request_id']).execute().data[0]
    supabase.table('users').update({'user_type': 'paid', 'tokens': 50}).eq('id', req['user_id']).execute()
    supabase.table('upgrade_requests').update({'status': 'approved'}).eq('id', data['request_id']).execute()
    return jsonify({'message': 'User upgraded to paid status'})
