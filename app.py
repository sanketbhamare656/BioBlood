from flask import Flask, render_template
from detection.routes import detection_bp

app = Flask(__name__)
app.secret_key = "fingerprint_secret"

# Register the blueprint
app.register_blueprint(detection_bp, url_prefix='/detection')


# --------------------------------------
# Landing Page
# --------------------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/blood_group')
def blood_group():
    return render_template('blood_group.html')


if __name__ == '__main__':
    app.run()
