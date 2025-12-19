// JS for Leaves / OT / WFH page (ui-card.html)

(function () {
  const token = localStorage.getItem('accessToken');
  if (!token) {
    if (window.omsAuth && typeof window.omsAuth.makeLoginPath === 'function') {
      window.location.href = window.omsAuth.makeLoginPath();
    } else {
      // fallback (works when served with /html/... as root)
      window.location.href = '../../authentication-login.html';
    }
  }
})();

function toggleFormFields() {
  const type = document.getElementById('amenityType').value;
  const leaveFields = document.getElementById('leaveFields');
  const otFields = document.getElementById('otFields');
  const toDateGroup = document.getElementById('toDateGroup');

  if (!leaveFields || !otFields || !toDateGroup) return;

  // Reset visibility
  leaveFields.classList.add('d-none');
  otFields.classList.add('d-none');
  toDateGroup.classList.remove('d-none'); // Default show

  if (type === 'leave') {
    leaveFields.classList.remove('d-none');
  } else if (type === 'ot') {
    otFields.classList.remove('d-none');
    toDateGroup.classList.add('d-none'); // OT is usually single day
  } else if (type === 'wfh') {
    // Standard fields only
  }
}

async function submitRequest() {
  const type = document.getElementById('amenityType').value;
  if (!type) {
    alert('Please select a type');
    return;
  }

  const formData = {
    reason: document.getElementById('reason').value,
    from_date: document.getElementById('fromDate').value,
  };

  let endpoint = '';

  if (type === 'leave') {
    endpoint = 'http://127.0.0.1:5000/requests/leave';
    formData.leave_type_id = parseInt(document.getElementById('leaveTypeId').value, 10);
    formData.to_date = document.getElementById('toDate').value;
  } else if (type === 'ot') {
    endpoint = 'http://127.0.0.1:5000/requests/ot';
    formData.for_date = formData.from_date; // Map from_date to for_date
    delete formData.from_date;
    formData.extra_task_description = formData.reason || '';
    delete formData.reason;
    formData.requested_minutes = parseInt(
      document.getElementById('requestedMinutes').value,
      10
    );
  } else if (type === 'wfh') {
    endpoint = 'http://127.0.0.1:5000/requests/wfh';
    formData.to_date = document.getElementById('toDate').value;
  }

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + localStorage.getItem('accessToken'),
      },
      body: JSON.stringify(formData),
    });

    if (response.ok) {
      alert('Request submitted successfully!');
      await loadCalendars();
      const modalEl = document.getElementById('requestModal');
      if (window.bootstrap && modalEl) {
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
      }
    } else {
      const err = await response.json().catch(() => ({}));
      alert('Error: ' + (err.message || JSON.stringify(err)));
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Network error occurred.');
  }
}

// Calendar + month selector logic
const monthNames = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
];

let currentDate = new Date();

function getDaysInMonth(month, year) {
  return new Date(year, month + 1, 0).getDate();
}

async function fetchRequests(type, month, year) {
  try {
    const response = await fetch(
      `http://127.0.0.1:5000/requests/${type}/list`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + localStorage.getItem('accessToken'),
        },
        body: JSON.stringify({ month: month + 1, year }),
      }
    );
    if (response.ok) {
      return await response.json();
    } else {
      const errText = await response.text();
      console.error('Fetch error', type, errText);
    }
  } catch (e) {
    console.error(e);
  }
  return [];
}

function renderCalendar(elementId, year, month, requests, type) {
  const container = document.getElementById(elementId);
  if (!container) return;

  container.innerHTML = '';

  const daysInMonth = getDaysInMonth(month, year);
  const statusMap = {};

  requests.forEach((req) => {
    let statusClass = 'cal-pending';
    if (req.status === 1) statusClass = 'cal-approved';
    if (req.status === 2) statusClass = 'cal-declined';

    let start, end;
    if (type === 'ot') {
      start = new Date(req.for_date);
      end = new Date(req.for_date);
    } else {
      start = new Date(req.from_date);
      end = new Date(req.to_date || req.from_date);
    }

    for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) {
      if (d.getMonth() === month && d.getFullYear() === year) {
        statusMap[d.getDate()] = statusClass;
      }
    }
  });

  for (let i = 1; i <= daysInMonth; i++) {
    const dayDiv = document.createElement('div');
    dayDiv.className = 'cal-day';
    dayDiv.innerText = i;

    if (statusMap[i]) {
      dayDiv.classList.add(statusMap[i]);
      dayDiv.title = statusMap[i].replace('cal-', '').toUpperCase();
    }

    container.appendChild(dayDiv);
  }
}

async function loadCalendars() {
  const month = currentDate.getMonth();
  const year = currentDate.getFullYear();

  const leaves = await fetchRequests('leave', month, year);
  renderCalendar('leave-calendar', year, month, leaves, 'leave');
  const leaveCount = document.getElementById('leave-count');
  if (leaveCount) leaveCount.innerText = leaves.length;

  const ots = await fetchRequests('ot', month, year);
  renderCalendar('ot-calendar', year, month, ots, 'ot');
  const otCount = document.getElementById('ot-count');
  if (otCount) otCount.innerText = ots.length;

  const wfhs = await fetchRequests('wfh', month, year);
  renderCalendar('wfh-calendar', year, month, wfhs, 'wfh');
  const wfhCount = document.getElementById('wfh-count');
  if (wfhCount) wfhCount.innerText = wfhs.length;

  updateMonthSelectorUI();
}

function changeMonth(delta) {
  currentDate.setMonth(currentDate.getMonth() + delta);
  loadCalendars();
}

function updateMonthSelectorUI() {
  const label = document.getElementById('month-label');
  if (label) {
    label.textContent = `${monthNames[currentDate.getMonth()]} ${currentDate.getFullYear()}`;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // Hook up month selector buttons if present
  const prevBtn = document.getElementById('month-prev');
  const nextBtn = document.getElementById('month-next');
  if (prevBtn) prevBtn.addEventListener('click', () => changeMonth(-1));
  if (nextBtn) nextBtn.addEventListener('click', () => changeMonth(1));

  loadCalendars();
});
