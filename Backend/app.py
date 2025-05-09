from flask import Flask
from flask_cors import CORS
from config import supabase
from routes.auth_routes import auth_bp
from routes.submission_routes import submission_bp
from routes.invite_routes import invite_bp
from routes.stats_routes import stats_bp
from routes.correction_routes import correction_bp
from routes.moderation_routes import moderation_bp


app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(submission_bp)
app.register_blueprint(invite_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(correction_bp)
app.register_blueprint(moderation_bp)

if __name__ == '__main__':
    app.run(debug=True)