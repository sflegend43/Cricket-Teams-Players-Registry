from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os
import time
import secrets
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, 'cricket_stats.db')
app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'Fan',
                managedTeam TEXT,
                token TEXT,
                created TEXT NOT NULL DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS Team (
                teamName TEXT PRIMARY KEY,
                country TEXT NOT NULL,
                headCoach TEXT
            );
            CREATE TABLE IF NOT EXISTS Players (
                playerID TEXT PRIMARY KEY,
                playerName TEXT NOT NULL,
                playerDOB TEXT NOT NULL,
                playerNationality TEXT NOT NULL,
                playerRole TEXT,
                teamName TEXT,
                matchesPlayed INTEGER DEFAULT 0,
                runsScored INTEGER DEFAULT 0,
                wicketsTaken INTEGER DEFAULT 0,
                FOREIGN KEY (teamName) REFERENCES Team(teamName) ON DELETE SET NULL
            );
        ''')
        admin = conn.execute("SELECT * FROM users WHERE email='admin@cricket.com'").fetchone()
        if not admin:
            pw = generate_password_hash("admin123")
            conn.execute("INSERT INTO users (fullname, email, password, role) VALUES (?, ?, ?, ?)", 
                         ("System Admin", "admin@cricket.com", pw, "Admin"))
            
        manager = conn.execute("SELECT * FROM users WHERE email='manager@pakistan.com'").fetchone()
        if not manager:
            pw = generate_password_hash("manager123")
            conn.execute("INSERT INTO users (fullname, email, password, role, managedTeam) VALUES (?, ?, ?, ?, ?)", 
                         ("Pakistan Manager", "manager@pakistan.com", pw, "TeamManager", "Pakistan"))
        
        conn.execute("INSERT OR IGNORE INTO Team (teamName, country, headCoach) VALUES ('Pakistan', 'Pakistan', 'Jason Gillespie')")
        conn.execute("INSERT OR IGNORE INTO Players (playerID, playerName, playerDOB, playerNationality, playerRole, teamName) VALUES ('P1', 'Babar Azam', '1994-10-15', 'Pakistan', 'Batsman', 'Pakistan')")

def get_bearer_token():
    header = request.headers.get('Authorization', '')
    if header.lower().startswith('bearer '):
        return header[7:].strip()
    return ''

def get_current_user():
    token = get_bearer_token()
    if not token: return None
    with get_db() as conn:
        return conn.execute('SELECT * FROM users WHERE token = ?', (token,)).fetchone()

@app.route('/')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory(BASE_DIR, path)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email, pwd = data.get('email'), data.get('password')
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if user and check_password_hash(user['password'], pwd):
            token = secrets.token_hex(32)
            conn.execute("UPDATE users SET token=? WHERE id=?", (token, user['id']))
            return jsonify({'token': token, 'user': {'fullname': user['fullname'], 'role': user['role'], 'managedTeam': user['managedTeam']}})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    try:
        with get_db() as conn:
            pw = generate_password_hash(data['password'])
            conn.execute("INSERT INTO users (fullname, email, password, role) VALUES (?, ?, ?, 'Fan')",
                         (data['fullname'], data['email'], pw))
            return jsonify({'success': True})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email exists'}), 400

@app.route('/api/auth/me', methods=['GET'])
def auth_me():
    user = get_current_user()
    if user:
        return jsonify({'fullname': user['fullname'], 'role': user['role'], 'managedTeam': user['managedTeam']})
    return jsonify({'error': 'Not logged in'}), 401

@app.route('/api/teams', methods=['GET', 'POST'])
def handle_teams():
    if request.method == 'GET':
        with get_db() as conn:
            teams = [dict(r) for r in conn.execute("SELECT * FROM Team")]
            return jsonify(teams)
    
    user = get_current_user()
    if not user or user['role'] != 'Admin': return jsonify({'error': 'Unauthorized'}), 403
    data = request.json
    with get_db() as conn:
        try:
            conn.execute("INSERT INTO Team (teamName, country, headCoach) VALUES (?, ?, ?)",
                         (data['teamName'], data['country'], data['headCoach']))
            return jsonify({'success': True})
        except:
            return jsonify({'error': 'Failed to add team'}), 400

@app.route('/api/teams/<name>', methods=['DELETE', 'PUT'])
def edit_team(name):
    user = get_current_user()
    if not user or user['role'] != 'Admin': return jsonify({'error': 'Unauthorized'}), 403
    with get_db() as conn:
        if request.method == 'DELETE':
            conn.execute("DELETE FROM Team WHERE teamName=?", (name,))
            return jsonify({'success': True})
        elif request.method == 'PUT':
            data = request.json
            conn.execute("UPDATE Team SET country=?, headCoach=? WHERE teamName=?", (data['country'], data['headCoach'], name))
            return jsonify({'success': True})

@app.route('/api/players', methods=['GET', 'POST'])
def handle_players():
    if request.method == 'GET':
        with get_db() as conn:
            players = [dict(r) for r in conn.execute("SELECT * FROM Players")]
            return jsonify(players)
            
    user = get_current_user()
    if not user or user['role'] != 'Admin': return jsonify({'error': 'Unauthorized'}), 403
    data = request.json
    with get_db() as conn:
        try:
            pid = data.get('playerID', secrets.token_hex(4))
            conn.execute("INSERT INTO Players (playerID, playerName, playerDOB, playerNationality, playerRole, teamName) VALUES (?, ?, ?, ?, ?, ?)",
                         (pid, data['playerName'], data['playerDOB'], data['playerNationality'], data['playerRole'], data['teamName']))
            return jsonify({'success': True})
        except:
            return jsonify({'error': 'Failed to add player'}), 400

@app.route('/api/players/<pid>', methods=['DELETE', 'PUT'])
def edit_player(pid):
    user = get_current_user()
    if not user: return jsonify({'error': 'Unauthorized'}), 403
    with get_db() as conn:
        if request.method == 'DELETE':
            if user['role'] != 'Admin': return jsonify({'error': 'Unauthorized'}), 403
            conn.execute("DELETE FROM Players WHERE playerID=?", (pid,))
            return jsonify({'success': True})
        elif request.method == 'PUT':
            data = request.json
            player = conn.execute("SELECT * FROM Players WHERE playerID=?", (pid,)).fetchone()
            if not player: return jsonify({'error': 'Not found'}), 404
            
            if user['role'] == 'Admin':
                conn.execute("UPDATE Players SET playerName=?, playerDOB=?, playerNationality=?, playerRole=?, teamName=? WHERE playerID=?",
                             (data.get('playerName', player['playerName']), data.get('playerDOB', player['playerDOB']), 
                              data.get('playerNationality', player['playerNationality']), data.get('playerRole', player['playerRole']), 
                              data.get('teamName', player['teamName']), pid))
            elif user['role'] == 'TeamManager':
                if user['managedTeam'] != player['teamName']: return jsonify({'error': 'Unauthorized'}), 403
                conn.execute("UPDATE Players SET matchesPlayed=?, runsScored=?, wicketsTaken=? WHERE playerID=?",
                             (data.get('matchesPlayed', player['matchesPlayed']), data.get('runsScored', player['runsScored']), 
                              data.get('wicketsTaken', player['wicketsTaken']), pid))
            else:
                return jsonify({'error': 'Unauthorized'}), 403
            return jsonify({'success': True})

@app.route('/api/stats/overview', methods=['GET'])
def stats_overview():
    with get_db() as conn:
        teams = conn.execute("SELECT COUNT(*) as c FROM Team").fetchone()['c']
        players = conn.execute("SELECT COUNT(*) as c FROM Players").fetchone()['c']
        fans = conn.execute("SELECT COUNT(*) as c FROM users WHERE role='Fan'").fetchone()['c']
        return jsonify({'teams': teams, 'players': players, 'fans': fans})

if __name__ == '__main__':
    init_db()
    app.run(port=5001, debug=True)
