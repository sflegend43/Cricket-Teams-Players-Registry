// logic.js
document.addEventListener('DOMContentLoaded', () => {
    loadUser();
    loadDashboardStats();
});

function loadUser() {
    const userStr = localStorage.getItem('cricketUser');
    if (!userStr) {
        window.location.href = 'login.html';
        return;
    }
    const user = JSON.parse(userStr);
    document.getElementById('user-name-display').textContent = user.fullname || 'User';
    document.getElementById('user-role-display').textContent = user.role || 'Fan';
    document.getElementById('user-avatar').textContent = (user.fullname || 'U')[0].toUpperCase();
}

async function loadDashboardStats() {
    const userStr = localStorage.getItem('cricketUser');
    if(!userStr) return;
    const token = JSON.parse(userStr).token;
    
    try {
        const res = await fetch('/api/stats/overview', {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        if (res.ok) {
            const data = await res.json();
            document.getElementById('stat-teams').textContent = data.teams;
            document.getElementById('stat-players').textContent = data.players;
            document.getElementById('stat-fans').textContent = data.fans;
        }
    } catch (e) {
        console.error("Failed to load stats", e);
    }
}

function logout() {
    localStorage.removeItem('cricketUser');
    window.location.href = 'login.html';
}
