from flask import Blueprint, request, jsonify
from config import supabase
from utils import log_action, require_role, update_user_tokens

invite_bp = Blueprint('invite', __name__)

# Send an invitation to collaborate on a document
@invite_bp.route('/invite', methods=['POST'])
@require_role(['paid'])
def send_invite():
    data = request.get_json()
    invitee = supabase.table('users').select('user_type').eq('id', data['invitee_id']).execute().data
    if not invitee or invitee[0]['user_type'] != 'paid':
        return jsonify({'error': 'Invitee must be a paid user'}), 400

    invitation = supabase.table('invitations').insert({
        'document_id': data['document_id'],
        'inviter_id': data['inviter_id'],
        'invitee_id': data['invitee_id'],
        'status': 'pending'
    }).execute().data[0]

    log_action(data['inviter_id'], 'invite_sent', f'Invited {data["invitee_id"]} to document {data["document_id"]}')
    return jsonify({'message': 'Invitation sent', 'invitation': invitation})

# Respond to an invitation (accept or reject)
@invite_bp.route('/invite/respond', methods=['POST'])
@require_role(['paid'])
def respond_invite():
    data = request.get_json()
    invitation = supabase.table('invitations').select('*').eq('id', data['invitation_id']).execute().data[0]

    supabase.table('invitations').update({'status': data['response']}).eq('id', data['invitation_id']).execute()

    if data['response'] == 'accepted':
        supabase.table('collaborators').insert({
            'document_id': invitation['document_id'],
            'user_id': invitation['invitee_id'],
            'can_edit': True
        }).execute()
        log_action(invitation['invitee_id'], 'invite_accepted', f"Accepted invite to doc {invitation['document_id']}")
        return jsonify({'message': 'Invitation accepted and access granted'})

    update_user_tokens(invitation['inviter_id'], -3)
    log_action(invitation['invitee_id'], 'invite_rejected', f"Rejected invite from {invitation['inviter_id']}")
    return jsonify({'message': 'Invitation rejected. Inviter penalized 3 tokens.'})
