from flask import Flask
from flask_cors import CORS
from Backend.config import supabase
from Backend.routes.auth_routes import auth_bp
from Backend.routes.submission_routes import submission_bp
from Backend.routes.invite_routes import invite_bp
from Backend.routes.stats_routes import stats_bp
from Backend.routes.correction_routes import correction_bp
from Backend.routes.moderation_routes import moderation_bp
from Backend.routes.session_routes import session_bp
from Backend.routes.token_routes import token_bp




app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(session_bp)
app.register_blueprint(submission_bp)
app.register_blueprint(invite_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(correction_bp)
app.register_blueprint(moderation_bp)
app.register_blueprint(token_bp)


if __name__ == '__main__':
    app.run(debug=True)