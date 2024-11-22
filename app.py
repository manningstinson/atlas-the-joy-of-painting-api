import sys
sys.path.append('/workspaces/atlas-the-joy-of-painting-api/api')

from flask import Flask, jsonify, request
from sqlalchemy import text
from models import Episode, FilterParams
from routes import get_episodes, get_colors, get_subjects

app = Flask(__name__)

app.route('/episodes', methods=['GET'])(get_episodes)
app.route('/colors', methods=['GET'])(get_colors)
app.route('/subjects', methods=['GET'])(get_subjects)

@app.route('/episodes', methods=['GET'])
def get_episodes():
    filter_params = FilterParams(
        months=request.args.getlist('months', type=int),
        subjects=request.args.getlist('subjects'),
        colors=request.args.getlist('colors'),
        filter_type=request.args.get('filter_type', 'all')
    )
    episodes = get_episodes(filter_params)
    return jsonify([e.dict() for e in episodes])

@app.route('/colors', methods=['GET'])
def get_colors():
    result = db.execute(text("SELECT id, name, code FROM colors ORDER BY name"))
    return jsonify([{'id': row[0], 'name': row[1], 'code': row[2]} for row in result])

@app.route('/subjects', methods=['GET'])
def get_subjects():
    result = db.execute(text("SELECT id, name FROM subjects ORDER BY name"))
    return jsonify([{'id': row[0], 'name': row[1]} for row in result])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000))