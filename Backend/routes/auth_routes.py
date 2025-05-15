from flask import Blueprint, request, jsonify
from Backend.config import supabase
from Backend.utils import log_action, require_role
from Backend.routes.session_routes import create_session

auth_bp = Blueprint('auth', __name__)

# Register a new user
@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    required = ['email', 'password', 'first_name', 'last_name']
    missing = [field for field in required if field not in data]
    if missing:
        return jsonify({'success': False, 'error': f"Missing fields: {', '.join(missing)}"}), 400

    # Check if email already exists
    existing = supabase.table('users').select('id').eq('email', data['email']).execute().data
    if existing:
        return jsonify({'success': False, 'error': 'Email already registered'}), 400

    # Insert unapproved free user
    res = supabase.table('users').insert({
        'email': data['email'],
        'password': data['password'],
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'user_type': 'free',
        'approved': False
    }).execute()
    
    return jsonify({'success': True, 'user': res.data[0]}), 201


# Log in a user and check for lockout
@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    res = supabase.table('users').select('*') \
        .eq('email', data['email']).eq('password', data['password']).execute()

    if not res.data:
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

    user = res.data[0]

    # Check if user is approved
    if not user.get('approved', False):
        return jsonify({'success': False, 'error': 'Account pending approval'}), 403

    # Check for lockout (free users)
    if user['user_type'] == 'free':
        lock = supabase.table('lockouts').select('*') \
            .eq('user_id', user['id']).gt('expires_at', 'now()').execute()
        if lock.data:
            return jsonify({
                'success': False,
                'error': 'Account temporarily locked',
                'expires_at': lock.data[0]['expires_at']
            }), 403

    # Create session token
    token = create_session(user['id'])

    # Log login event
    log_action(user['id'], 'login')

    # Return success response with token and role
    return jsonify({
        'success': True,
        'session_token': token,
        'account_type': user['user_type'],
        'user_id': user['id']
    })



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


@auth_bp.route('/auth/upgrade/requests', methods=['GET'])
@require_role(['super'])
def get_upgrade_requests():
    res = supabase.table('upgrade_requests').select(
        'id, user_id, status, notes, created_at'
    ).eq('status', 'pending').execute()

    return jsonify(res.data)

# super users reject upgrade requests.
@auth_bp.route('/auth/upgrade/deny', methods=['POST'])
@require_role(['super'])
def deny_upgrade():
    data = request.get_json()
    request_id = data.get('request_id')

    if not request_id:
        return jsonify({'error': 'Missing request_id'}), 400

    # Mark the upgrade request as denied
    supabase.table('upgrade_requests').update({
        'status': 'denied'
    }).eq('id', request_id).execute()

    return jsonify({'message': 'Upgrade request denied'})


# Approve regular free account (super only)
@auth_bp.route('/auth/approve-account', methods=['POST'])
@require_role(['super'])
def approve_free_account():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400

    supabase.table('users').update({'approved': True}) \
        .eq('id', user_id).execute()

    return jsonify({'message': 'User approved successfully'})
