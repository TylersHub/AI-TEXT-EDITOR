from flask import request, jsonify
from Backend.config import supabase
import re


# Get the user role from Supabase
def get_user_role(user_id):
    res = supabase.table('users').select('user_type').eq('id', user_id).execute()
    return res.data[0]['user_type'] if res.data else None

# Get token balance for a user
def get_user_tokens(user_id):
    res = supabase.table('users').select('tokens').eq('id', user_id).execute()
    return res.data[0]['tokens'] if res.data else 0

# Update token balance for a user
def update_user_tokens(user_id, delta):
    current = get_user_tokens(user_id)
    new_balance = max(0, current + delta)
    supabase.table('users').update({'tokens': new_balance}).eq('id', user_id).execute()
    return new_balance

# Log an action to the activity_logs table
def log_action(user_id, action_type, details=None):
    supabase.table('activity_logs').insert({
        'user_id': user_id,
        'action_type': action_type,
        'details': details
    }).execute()

# Replace blacklisted words with asterisks
def check_blacklisted_words(text):
    res = supabase.table('blacklist').select('word').execute()
    blacklist = [r['word'] for r in res.data]
    count, chars = 0, 0
    for word in blacklist:
        pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
        matches = pattern.findall(text)
        if matches:
            count += len(matches)
            chars += sum(len(m) for m in matches)
            text = pattern.sub(lambda m: '*' * len(m.group(0)), text)
    return text, count, chars

# Decorator to restrict access to specific roles
def require_role(roles):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user_id = None

            # 1. Check URL path params (e.g., /documents/<user_id>)
            if request.view_args and 'user_id' in request.view_args:
                user_id = request.view_args['user_id']

            # 2. Check query string (e.g., ?user_id=...)
            elif 'user_id' in request.args:
                user_id = request.args['user_id']

            # 3. Check JSON body (e.g., { "user_id": ... })
            elif request.is_json:
                data = request.get_json(silent=True)
                user_id = data.get('user_id') if data else None

            if not user_id:
                return jsonify({'error': 'Missing user_id'}), 400

            role = get_user_role(user_id)
            if role not in roles:
                return jsonify({'error': f'Access denied: requires {roles} role'}), 403

            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

