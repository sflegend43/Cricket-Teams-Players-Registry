// players.js
function getUser() { return JSON.parse(localStorage.getItem('cricketUser') || 'null'); }
function logout() { localStorage.removeItem('cricketUser'); window.location.href = 'login.html'; }

document.addEventListener('DOMContentLoaded', () => {
    const user = getUser();
    if (!user || user.role !== 'Admin') {
        document.querySelectorAll('.admin-only').forEach(e => e.style.display = 'none');
    }
    loadPlayers();

    const form = document.getElementById('add-player-form');
    if(form) form.addEventListener('submit', addPlayer);
    
    document.getElementById('update-stats-form').addEventListener('submit', updateStats);
});

async function loadPlayers() {
    const user = getUser();
    const res = await fetch('/api/players', { headers: { 'Authorization': 'Bearer ' + user.token } });
    if(res.ok) {
        const players = await res.json();
        const tb = document.getElementById('players-tbody');
        tb.innerHTML = players.map(p => {
            let actions = '';
            if (user.role === 'Admin') {
                actions += `<button onclick="deletePlayer('${p.playerID}')" style="background:red; color:white; border:none; padding:5px; border-radius:3px; cursor:pointer;">Delete</button> `;
            }
            if (user.role === 'TeamManager' && user.managedTeam === p.teamName) {
                actions += `<button onclick="openStatsForm('${p.playerID}', '${p.playerName}', ${p.matchesPlayed}, ${p.runsScored}, ${p.wicketsTaken})" style="background:var(--gold); color:black; border:none; padding:5px; border-radius:3px; cursor:pointer;">Update Stats</button>`;
            }
            
            return `
            <tr>
                <td>${p.playerName}</td>
                <td>${p.playerRole}</td>
                <td>${p.teamName}</td>
                <td>${p.matchesPlayed}</td>
                <td>${p.runsScored}</td>
                <td>${p.wicketsTaken}</td>
                <td>${actions}</td>
            </tr>
        `}).join('');
    }
}

async function addPlayer(e) {
    e.preventDefault();
    const user = getUser();
    const payload = {
        playerName: document.getElementById('p-name').value,
        playerDOB: document.getElementById('p-dob').value,
        playerNationality: document.getElementById('p-nat').value,
        playerRole: document.getElementById('p-role').value,
        teamName: document.getElementById('p-team').value
    };
    const res = await fetch('/api/players', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + user.token },
        body: JSON.stringify(payload)
    });
    if(res.ok) {
        alert('Player added');
        loadPlayers();
    } else alert('Failed to add player');
}

async function deletePlayer(id) {
    if(!confirm('Are you sure?')) return;
    const user = getUser();
    const res = await fetch('/api/players/' + encodeURIComponent(id), {
        method: 'DELETE',
        headers: { 'Authorization': 'Bearer ' + user.token }
    });
    if(res.ok) loadPlayers();
    else alert('Failed to delete');
}

function openStatsForm(id, name, m, r, w) {
    document.getElementById('stats-form-container').style.display = 'block';
    document.getElementById('editing-player-name').textContent = name;
    document.getElementById('edit-p-id').value = id;
    document.getElementById('edit-matches').value = m;
    document.getElementById('edit-runs').value = r;
    document.getElementById('edit-wickets').value = w;
}

async function updateStats(e) {
    e.preventDefault();
    const user = getUser();
    const id = document.getElementById('edit-p-id').value;
    const payload = {
        matchesPlayed: parseInt(document.getElementById('edit-matches').value),
        runsScored: parseInt(document.getElementById('edit-runs').value),
        wicketsTaken: parseInt(document.getElementById('edit-wickets').value)
    };
    const res = await fetch('/api/players/' + encodeURIComponent(id), {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + user.token },
        body: JSON.stringify(payload)
    });
    if(res.ok) {
        alert('Stats updated');
        document.getElementById('stats-form-container').style.display = 'none';
        loadPlayers();
    } else {
        alert('Failed to update stats');
    }
}
