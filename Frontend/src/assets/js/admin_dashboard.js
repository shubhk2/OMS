// Frontend/src/assets/js/admin_dashboard.js
// Admin home page UI wiring.

(function () {
  const API_URL = 'http://127.0.0.1:5000';

  function getToken() {
    return localStorage.getItem('accessToken');
  }

  async function api(path, options = {}) {
    const token = getToken();
    const headers = Object.assign(
      {
        'Content-Type': 'application/json',
        Authorization: token ? `Bearer ${token}` : '',
      },
      options.headers || {}
    );

    const res = await fetch(`${API_URL}${path}`, { ...options, headers });
    const contentType = res.headers.get('content-type') || '';
    const data = contentType.includes('application/json') ? await res.json().catch(() => ({})) : await res.text();

    if (!res.ok) {
      const msg = (data && data.error) || (data && data.message) || JSON.stringify(data);
      throw new Error(msg || `Request failed: ${res.status}`);
    }
    return data;
  }

  function el(id) {
    return document.getElementById(id);
  }

  function setText(id, value) {
    const node = el(id);
    if (node) node.textContent = value;
  }

  function renderLastCheckins(rows) {
    const tbody = el('lastCheckinsBody');
    if (!tbody) return;
    tbody.innerHTML = '';

    if (!rows || rows.length === 0) {
      const tr = document.createElement('tr');
      tr.innerHTML = '<td colspan="4" class="text-muted">No active check-ins yet.</td>';
      tbody.appendChild(tr);
      return;
    }

    rows.forEach((r) => {
      const tr = document.createElement('tr');
      const statusBadge = r.status === 'Break'
        ? '<span class="badge bg-warning">Break</span>'
        : '<span class="badge bg-success">In</span>';
      tr.innerHTML = `
        <td>${r.employee || '-'}</td>
        <td>${r.team || '-'}</td>
        <td>${r.check_in_time || '-'}</td>
        <td>${statusBadge}</td>
      `;
      tbody.appendChild(tr);
    });
  }

  async function loadSnapshot() {
    const data = await api('/admin/home', { method: 'GET' });

    // indicators
    setText('checkedInIndicator', `${data.indicators.checked_in} / ${data.indicators.total}`);
    setText('onLeaveIndicator', String(data.indicators.on_leave_today));
    setText('onWfhIndicator', String(data.indicators.on_wfh_today));

    // quick stats
    setText('statTotalEmployees', String(data.quick_stats.total_employees));
    setText('statActiveTeams', String(data.quick_stats.active_teams));
    setText('statTeamLeaders', String(data.quick_stats.team_leaders));
    setText('statHrMembers', String(data.quick_stats.hr_members));

    // alerts
    setText('alertPendingOT', String(data.alerts.pending_ot_approvals));
    setText('alertPendingLeaves', String(data.alerts.pending_leave_requests));
    setText('alertMissedCheckout', String(data.alerts.missed_check_out));
    setText('alertTeamsNoLeader', String(data.alerts.teams_without_leader));

    renderLastCheckins(data.last_checked_in);
  }

  async function loadDropdowns() {
    const [emps, teams] = await Promise.all([
      api('/admin/employees', { method: 'GET' }),
      api('/admin/teams', { method: 'GET' }),
    ]);

    const employeeSelect = el('assignEmployeeSelect');
    const leaderSelect = el('newTeamLeaderSelect');
    const teamSelect = el('assignTeamSelect');

    function fillSelect(select, items, labelFn, valueFn) {
      if (!select) return;
      select.innerHTML = '';
      const opt0 = document.createElement('option');
      opt0.value = '';
      opt0.textContent = 'Select...';
      select.appendChild(opt0);
      items.forEach((it) => {
        const opt = document.createElement('option');
        opt.value = valueFn(it);
        opt.textContent = labelFn(it);
        select.appendChild(opt);
      });
    }

    fillSelect(
      employeeSelect,
      emps.employees || [],
      (e) => `${e.name} (#${e.id})`,
      (e) => e.id
    );

    fillSelect(
      leaderSelect,
      emps.employees || [],
      (e) => `${e.name} (#${e.id})`,
      (e) => e.id
    );

    fillSelect(
      teamSelect,
      teams.teams || [],
      (t) => `${t.name} (#${t.id})`,
      (t) => t.id
    );
  }

  async function handleCreateEmployee() {
    const name = el('newEmpName')?.value || '';
    const username = el('newEmpUsername')?.value || '';
    const email = el('newEmpEmail')?.value || '';
    const role = parseInt(el('newEmpRole')?.value || '1', 10);
    const primaryTeamIdRaw = el('newEmpTeam')?.value || '';

    const payload = {
      name,
      username,
      email,
      role,
      primary_team_id: primaryTeamIdRaw ? parseInt(primaryTeamIdRaw, 10) : null,
    };

    await api('/admin/employees', { method: 'POST', body: JSON.stringify(payload) });
    await loadDropdowns();
    await loadSnapshot();
  }

  async function handleCreateTeam() {
    const name = el('newTeamName')?.value || '';
    const leaderIdRaw = el('newTeamLeaderSelect')?.value || '';
    if (!leaderIdRaw) throw new Error('Select a Team Leader');

    await api('/admin/teams', {
      method: 'POST',
      body: JSON.stringify({ name, team_leader_id: parseInt(leaderIdRaw, 10) }),
    });
    await loadDropdowns();
    await loadSnapshot();
  }

  async function handleAssign() {
    const employeeIdRaw = el('assignEmployeeSelect')?.value || '';
    const roleRaw = el('assignRoleSelect')?.value || '';
    const teamRaw = el('assignTeamSelect')?.value || '';

    if (!employeeIdRaw) throw new Error('Select an employee');

    const payload = {
      employee_id: parseInt(employeeIdRaw, 10),
    };
    if (roleRaw) payload.role = parseInt(roleRaw, 10);
    if (teamRaw) payload.primary_team_id = parseInt(teamRaw, 10);

    await api('/admin/assign', { method: 'POST', body: JSON.stringify(payload) });
    await loadSnapshot();
  }

  function wireActions() {
    el('btnCreateEmployee')?.addEventListener('click', async () => {
      try {
        await handleCreateEmployee();
        alert('Employee created');
      } catch (e) {
        alert(e.message);
      }
    });

    el('btnCreateTeam')?.addEventListener('click', async () => {
      try {
        await handleCreateTeam();
        alert('Team created');
      } catch (e) {
        alert(e.message);
      }
    });

    el('btnAssignRole')?.addEventListener('click', async () => {
      try {
        await handleAssign();
        alert('Updated');
      } catch (e) {
        alert(e.message);
      }
    });
  }

  function setHeader() {
    const now = new Date();
    setText('adminDate', now.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' }));
  }

  document.addEventListener('DOMContentLoaded', async () => {
    if (!getToken()) return; // auth.js will redirect

    setHeader();
    wireActions();

    try {
      await loadDropdowns();
      await loadSnapshot();
    } catch (e) {
      console.error(e);
      // if forbidden, likely non-admin
      alert(`Admin dashboard error: ${e.message}`);
    }
  });
})();

