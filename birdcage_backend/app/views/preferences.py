from flask import Blueprint, request, jsonify
from config import DATABASE_FILE
from app.models.preferences import UserPreferences, check_password
from functools import wraps
import bcrypt
from flask_jwt_extended import create_access_token
from app.decorators import admin_required

preferences_blueprint = Blueprint('preferences', __name__)


@preferences_blueprint.route('/api/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

        # Validate the admin user and password (replace with your own validation logic)
    if username != 'admin' or not check_password(password):
        return jsonify({"msg": "Invalid username or password"}), 401

        # Create a JWT token
    # Add print statements to debug the username variable
    print(f"Type of username: {type(username)}")
    print(f"Value of username: {username}")
    access_token = create_access_token(identity=username)

    return jsonify(access_token=access_token), 200


@preferences_blueprint.route('/api/preferences/<int:user_id>', methods=['GET'])
def get_preferences(user_id):
    preferences = UserPreferences.select().where(UserPreferences.user_id == user_id)
    if not preferences:
        return jsonify({'error': 'Preferences not found'}), 404
    return {preference.preference_key: preference.preference_value for preference in preferences}


def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    return True, None


# Add a validation function to check preference constraints
def validate_preference(preference_key, preference_value):
    if preference_key == 'password':
        return validate_password(preference_value)

    # Add a condition to check for 'locale' preference key
    if preference_key == 'locale':
        allowed_locales = ['af', 'ar', 'cs', 'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja', 'ko', 'nl', 'no', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'sv', 'th', 'tr', 'uk', 'zh']
        if preference_value in allowed_locales:
            return True, None
        else:
            return False, "Invalid locale value."

    if (preference_key == 'mqttbroker') or (preference_key == 'mqttuser') or (preference_key == 'mqttpassword'):
        # we'll try whatever the user put in
        return True, None

    if preference_key == 'mqttrecordings':
        if (preference_value == 'true') or (preference_value == 'false'):
            return True, None
        else:
            return False, "Value must be true or false"

    if preference_key == 'mqttport':
        try:
            int_value = int(preference_value)
        except ValueError:
            return False, "Value must be an integer"

    try:
        numeric_value = float(preference_value)
    except ValueError:
        return False, "Value must be numeric."

    constraints = {
        "recordinglength": (3, 120),
        "confidence": (0, 1),
        "extractionlength": (3, 120),
        "latitude": (-90, 90),
        "longitude": (-180, 180),
        "overlap": (0, 2.9),
        "sensitivity": (0.5, 1.5),
        "sf_thresh": (0.01, 0.99),
        "recordingretention": (0, 36500),
        "mqttport": (1, 65535)
    }

    if preference_key not in constraints:
        return False, "Invalid preference key."

    min_value, max_value = constraints[preference_key]

    if not (min_value <= numeric_value <= max_value):
        return False, f"Value must be between {min_value} and {max_value}."

    return True, None


@preferences_blueprint.route('/api/preferences', methods=['POST'])
@admin_required
def set_preference():
    data = request.get_json()

    user_id = data['user_id']
    preference_key = data['preference_key']
    preference_value = data['preference_value']

    # Validate the preference before inserting into the database
    is_valid, error_message = validate_preference(preference_key, preference_value)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    # Hash the password if the preference_key is 'password'
    if preference_key == 'password':
        preference_value = bcrypt.hashpw(preference_value.encode(), bcrypt.gensalt()).decode()

    pref, created = UserPreferences.get_or_create(user_id=user_id, preference_key=preference_key, defaults={'preference_value': preference_value})
    if not created:
        pref.preference_value = preference_value
        pref.save()

    

    if preference_key == 'password':
        return jsonify({"message": "Password set successfully."})
    else:
        return jsonify({"message": "Preference set successfully."})


@preferences_blueprint.route('/api/preferences/<int:user_id>/<string:preference_key>', methods=['DELETE'])
@admin_required
def delete_preference(user_id, preference_key):
    UserPreferences.delete().where((UserPreferences.user_id == user_id) & (UserPreferences.preference_key == preference_key)).execute()

    return jsonify({"message": "Preference deleted successfully."})
