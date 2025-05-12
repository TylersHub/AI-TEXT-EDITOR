from flask import Blueprint, request, jsonify
from config import supabase
from utils import log_action, require_role, update_user_tokens

invite_bp = Blueprint('invite', __name__)

# Send an invitation to collaborate on a document
@invite_bp.route('/invite', methods=['POST'])
@require_role(['paid', 'super'])
def send_invite():
    data = request.get_json()
    inviter_id = data.get('inviter_id')
    invitee_email = data.get('invitee_email')
    document_id = data.get('document_id')

    if not inviter_id or not invitee_email or not document_id:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    # Look up invitee by email
    invitee_res = supabase.table('users').select('id', 'user_type').eq('email', invitee_email).execute()
    if not invitee_res.data:
        return jsonify({'success': False, 'error': 'User not found'}), 404

    invitee = invitee_res.data[0]
    if invitee['user_type'] != 'paid':
        return jsonify({'success': False, 'error': 'Invitee must be a paid user'}), 400

    # Create invitation
    invitation = supabase.table('invitations').insert({
        'document_id': document_id,
        'inviter_id': inviter_id,
        'invitee_id': invitee['id'],
        'status': 'pending'
    }).execute().data[0]

    return jsonify({'success': True, 'invitation': invitation})

# Respond to an invitation (accept or reject)
@invite_bp.route('/invite/respond', methods=['POST'])
@require_role(['paid', 'super'])
def respond_invite():
    data = request.get_json()
    invite_id = data.get('invitation_id')
    response = data.get('response')  # "accepted" or "rejected"

    if not invite_id or response not in ['accepted', 'rejected']:
        return jsonify({'success': False, 'error': 'Invalid input'}), 400

    # Get invitation details
    invitation = supabase.table('invitations').select('*').eq('id', invite_id).execute().data[0]

    supabase.table('invitations').update({'status': response}).eq('id', invite_id).execute()

    if response == 'accepted':
        # Add invitee as collaborator
        supabase.table('collaborators').insert({
            'document_id': invitation['document_id'],
            'user_id': invitation['invitee_id'],
            'can_edit': True
        }).execute()
        return jsonify({'success': True, 'message': 'Access granted'})

    # Penalize inviter if rejected
    from utils import update_user_tokens, log_action
    update_user_tokens(invitation['inviter_id'], -3)
    log_action(invitation['invitee_id'], 'invite_rejected', f"Rejected invite from {invitation['inviter_id']}")

    return jsonify({'success': True, 'message': 'Invitation rejected. Inviter penalized 3 tokens.'})

# user can see all collaboration invites they’ve received
@invite_bp.route('/invite/list/<user_id>', methods=['GET'])
@require_role(['paid', 'super'])
def list_invites(user_id):
    invites = supabase.table('invitations') \
        .select('id, document_id, inviter_id') \
        .eq('invitee_id', user_id) \
        .eq('status', 'pending').execute().data

    results = []
    for invite in invites:
        doc = supabase.table('documents').select('title') \
            .eq('id', invite['document_id']).execute().data[0]
        inviter = supabase.table('users').select('first_name', 'last_name') \
            .eq('id', invite['inviter_id']).execute().data[0]
        results.append({
            'invite_id': invite['id'],
            'document_id': invite['document_id'],
            'file_title': doc['title'],
            'inviter_name': f"{inviter['first_name']} {inviter['last_name']}"
        })

    return jsonify(results)
