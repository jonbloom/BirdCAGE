from app import create_app

from flask import Flask, redirect
from flask_swagger_ui import get_swaggerui_blueprint
from config import API_SERVER_PORT

app = create_app(init_celery=False)

# Set up Swagger UI
SWAGGER_URL = '/api/docs'
API_URL = '/static/openapi.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "My API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# Redirect the root URL to Swagger UI
@app.route('/')
def index():
    return redirect('/api/docs')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=API_SERVER_PORT)
