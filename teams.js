// teams.js
function getUser() { return JSON.parse(localStorage.getItem('cricketUser') || 'null'); }
function logout() { localStorage.removeItem('cricketUser'); window.location.href = 'login.html'; }

document.addEventListener('DOMContentLoaded', () => {
    const user = getUser();
    if (!user || user.role !== 'Admin') {
        document.querySelectorAll('.admin-only').forEach(e => e.style.display = 'none');
    }
    loadTeams();

    const form = document.getElementById('add-team-form');
    if(form) form.addEventListener('submit', addTeam);
});

async function loadTeams() {
    const user = getUser();
    const res = await fetch('/api/teams', { headers: { 'Authorization': 'Bearer ' + user.token } });
    if(res.ok) {
        const teams = await res.json();
        const tb = document.getElementById('teams-tbody');
        tb.innerHTML = teams.map(t => `
            <tr>
                <td>${t.teamName}</td>
                <td>${t.country}</td>
                <td>${t.headCoach}</td>
                <td class="admin-only" style="display: ${user.role === 'Admin' ? 'table-cell' : 'none'}">
                    <button onclick="deleteTeam('${t.teamName}')" class="btn btn-danger" style="background: red; padding: 5px; border-radius: 5px; color: white; cursor: pointer;">Delete</button>
                </td>
            </tr>
        `).join('');
    }
}

async function addTeam(e) {
    e.preventDefault();
    const user = getUser();
    const payload = {
        teamName: document.getElementById('t-name').value,
        country: document.getElementById('t-country').value,
        headCoach: document.getElementById('t-coach').value
    };
    const res = await fetch('/api/teams', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + user.token },
        body: JSON.stringify(payload)
    });
    if(res.ok) {
        alert('Team added');
        loadTeams();
    } else alert('Failed to add team');
}

async function deleteTeam(name) {
    if(!confirm('Are you sure?')) return;
    const user = getUser();
    const res = await fetch('/api/teams/' + encodeURIComponent(name), {
        method: 'DELETE',
        headers: { 'Authorization': 'Bearer ' + user.token }
    });
    if(res.ok) loadTeams();
    else alert('Failed to delete');
}
