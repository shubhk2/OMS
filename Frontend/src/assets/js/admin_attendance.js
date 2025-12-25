// javascript
// Updated admin attendance UI script - use backend API base URL and require token

(function() {
  const root = document.getElementById('admin-attendance-ui');
  if (!root) return;

  const token = localStorage.getItem('accessToken');
  if (!token) {
    if (window.omsAuth && typeof window.omsAuth.makeLoginPath === 'function') {
      window.location.href = window.omsAuth.makeLoginPath();
    } else {
      window.location.href = '../../authentication-login.html';
    }
    return;
  }

  const API_URL = 'http://127.0.0.1:5000';

  root.innerHTML = `
    <div class="card">
      <div class="card-body">
        <div class="row mb-3">
          <div class="col-md-3"><input id="att_date" class="form-control" type="date" /></div>
          <div class="col-md-2"><select id="att_month" class="form-select"><option value="">Month</option>${[...Array(12).keys()].map(i=>`<option value="${i+1}">${i+1}</option>`).join('')}</select></div>
          <div class="col-md-2"><input id="att_year" class="form-control" placeholder="Year" /></div>
          <div class="col-md-3"><select id="att_team" class="form-select"><option value="">All teams</option></select></div>
          <div class="col-md-2 text-end"><button id="btnLoadAttendance" class="btn btn-primary">Load</button></div>
        </div>
        <div class="row mb-3">
          <div class="col-md-4"><input id="att_employee_name" class="form-control" placeholder="Employee name or username (optional)" /></div>
          <div class="col-md-2"><button id="btnLoadSummary" class="btn btn-outline-secondary">Summary</button></div>
          <div class="col-md-6 text-end"><div id="summaryBox" class="text-end small text-muted"></div></div>
        </div>
        <div class="table-responsive"><table class="table" id="attTable"><thead><tr><th>Date</th><th>Employee</th><th>Team</th><th>Check-in</th><th>Check-out</th><th>Status</th></tr></thead><tbody></tbody></table></div>
      </div>
    </div>
  `;

  function authFetch(path, opts = {}) {
    const url = path.startsWith('http') ? path : API_URL + path;
    const headers = Object.assign({}, opts.headers || {}, {
      'Authorization': `Bearer ${token}`
    });
    // avoid forcing content-type on GET
    if (!headers['Content-Type'] && opts.body) headers['Content-Type'] = 'application/json';
    return fetch(url, Object.assign({}, opts, { headers }));
  }

  // load teams for filter
  async function loadTeams() {
    try {
      const res = await authFetch('/admin/teams');
      if (!res.ok) {
        // 401/403 will often return HTML - handle gracefully
        return;
      }
      const j = await res.json();
      const sel = document.getElementById('att_team');
      if (!j.teams || !sel) return;
      j.teams.forEach(t=>{
        const opt = document.createElement('option'); opt.value = t.id; opt.textContent = t.name; sel.appendChild(opt);
      });
    } catch (e) {
      // swallow - non-critical
    }
  }

  function renderRows(rows) {
    const tbody = document.querySelector('#attTable tbody');
    tbody.innerHTML = '';
    rows.forEach(r=>{
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${r.date||''}</td><td>${r.employee_name||''}</td><td>${r.team_id||''}</td><td>${r.check_in_time||''}</td><td>${r.check_out_time||''}</td><td>${r.status||''}</td>`;
      tbody.appendChild(tr);
    });
  }

  async function loadAttendance() {
    const date = document.getElementById('att_date').value;
    const month = document.getElementById('att_month').value;
    const year = document.getElementById('att_year').value;
    const team_id = document.getElementById('att_team').value;
    const employee_name = document.getElementById('att_employee_name').value;
    const qs = new URLSearchParams();
    if (date) qs.set('date', date);
    if (month) qs.set('month', month);
    if (year) qs.set('year', year);
    if (team_id) qs.set('team_id', team_id);
    if (employee_name) qs.set('employee_name', employee_name);

    try {
      const res = await authFetch('/admin/attendance/list?' + qs.toString());
      if (!res.ok) {
        const txt = await res.text();
        alert('Failed to load attendance: ' + (txt || res.statusText));
        if (res.status === 401 || res.status === 403) {
          // redirect to login if unauthorized
          if (window.omsAuth && typeof window.omsAuth.makeLoginPath === 'function') {
            window.location.href = window.omsAuth.makeLoginPath();
          } else {
            window.location.href = '../../authentication-login.html';
          }
        }
        return;
      }
      const data = await res.json();
      renderRows(data.attendance || []);
    } catch (err) {
      alert('Failed to load attendance: ' + err.message);
    }
  }

  async function loadSummary() {
    const month = document.getElementById('att_month').value;
    const year = document.getElementById('att_year').value;
    const qs = new URLSearchParams();
    if (month) qs.set('month', month);
    if (year) qs.set('year', year);
    try {
      const res = await authFetch('/admin/attendance/summary?' + qs.toString());
      if (!res.ok) {
        document.getElementById('summaryBox').textContent = 'Summary: failed';
        return;
      }
      const j = await res.json();
      document.getElementById('summaryBox').textContent = `Total: ${j.total_records} · Checked now: ${j.checked_in_now} · Missed: ${j.missed_checkout} · Avg check-in: ${j.avg_checkin_time}`;
    } catch (e) {
      document.getElementById('summaryBox').textContent = 'Summary: error';
    }
  }

  document.getElementById('btnLoadAttendance').addEventListener('click', loadAttendance);
  document.getElementById('btnLoadSummary').addEventListener('click', loadSummary);
  loadTeams();
  // initial load
  loadAttendance();
})();
