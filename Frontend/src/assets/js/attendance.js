document.addEventListener('DOMContentLoaded', function() {
    const welcomeText = document.getElementById('welcomeText');
    const checkInOutBtn = document.getElementById('checkInOutBtn');
    const breakBtn = document.getElementById('breakBtn');
    const digitalClock = document.getElementById('digitalClock');
    const token = localStorage.getItem('accessToken');
    let timerInterval;

    if (!token) {
        window.location.href = './authentication-login.html';
        return;
    }

    const API_URL = 'http://127.0.0.1:5000';

    function fetchProfile() {
        fetch(`${API_URL}/profile`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.name) {
                const firstName = data.name.split(' ')[0];
                welcomeText.textContent = `Welcome, ${firstName}`;
            }
            if (data.role === 14) {
                setupAdminDashboard();
            } else {
                setupEmployeeDashboard();
            }
        })
        .catch(error => console.error('Error fetching profile:', error));
    }

    function setupAdminDashboard() {
        const profitElement = document.getElementById('profit');
        profitElement.innerHTML = `
            <div class="d-flex justify-content-between align-items-center w-100 mb-3">
                <h5 class="card-title fw-semibold">Latest Check-ins</h5>
                <a href="/admin/attendance" class="arrow-link"><i class="ti ti-arrow-right"></i></a>
            </div>
            <ul class="list-group w-100">
                <!-- Employee data will be dynamically inserted here -->
            </ul>
        `;

        const primaryTeamCard = document.querySelector('.col-lg-8 .card .card-body');
        if (primaryTeamCard) {
            const primaryTeamTitle = primaryTeamCard.querySelector('h5');
            if (primaryTeamTitle && primaryTeamTitle.textContent.includes('Primary Team')) {
                primaryTeamTitle.textContent = 'Explore Projects';
                const dropdown = primaryTeamCard.querySelector('.dropdown');
                if(dropdown) dropdown.remove();
                const table = primaryTeamCard.querySelector('.table-responsive');
                // Replace table with project list
                if(table) {
                    table.innerHTML = `
                        <div class="list-group">
                            <a href="/admin/projects/1" class="list-group-item list-group-item-action">Project Alpha</a>
                            <a href="/admin/projects/2" class="list-group-item list-group-item-action">Project Beta</a>
                            <a href="/admin/projects/3" class="list-group-item list-group-item-action">Project Gamma</a>
                            <a href="/admin/projects/4" class="list-group-item list-group-item-action">Project Theta</a>
                        </div>
                        <div class="text-end mt-2">
                            <a href="/admin/projects" class="arrow-link"><i class="ti ti-arrow-right"></i></a>
                        </div>
                    `;
                }
            }
        }
    }

    function setupEmployeeDashboard() {
        fetchAttendanceStatus();
        checkInOutBtn.addEventListener('click', handleCheckInOut);
    }

    function fetchAttendanceStatus() {
        fetch(`${API_URL}/attendance/status`, {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        .then(response => response.json())
        .then(data => {
            updateUI(data.is_checked_in);
            if (data.is_checked_in) {
                startTimer();
            }
        })
        .catch(error => console.error('Error fetching attendance status:', error));
    }

    function handleCheckInOut() {
        const isCheckedIn = checkInOutBtn.textContent === 'Check Out';
        if (isCheckedIn) {
            checkOut();
        } else {
            checkIn();
        }
    }

    function checkIn() {
        fetch(`${API_URL}/attendance/checkin`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                updateUI(true);
                startTimer();
            } else {
                console.error('Check-in failed:', data.error);
            }
        })
        .catch(error => console.error('Error during check-in:', error));
    }

    function checkOut() {
        fetch(`${API_URL}/attendance/checkout`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                updateUI(false);
                stopTimer();
                digitalClock.textContent = "00:00:00";
            } else {
                console.error('Check-out failed:', data.error);
            }
        })
        .catch(error => console.error('Error during check-out:', error));
    }

    function updateUI(isCheckedIn) {
        if (isCheckedIn) {
            checkInOutBtn.textContent = 'Check Out';
            checkInOutBtn.classList.remove('btn-outline-success');
            checkInOutBtn.classList.add('btn-outline-danger');
            breakBtn.disabled = false;
        } else {
            checkInOutBtn.textContent = 'Check In';
            checkInOutBtn.classList.remove('btn-outline-danger');
            checkInOutBtn.classList.add('btn-outline-success');
            breakBtn.disabled = true;
        }
    }

    function startTimer() {
        if (timerInterval) clearInterval(timerInterval);
        timerInterval = setInterval(updateClock, 1000);
    }

    function stopTimer() {
        clearInterval(timerInterval);
    }

    function updateClock() {
        fetch(`${API_URL}/attendance/elapsed`, {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        .then(response => response.json())
        .then(data => {
            if (data.elapsed_time) {
                digitalClock.textContent = data.elapsed_time;
            }
        })
        .catch(error => console.error('Error fetching elapsed time:', error));
    }

    fetchProfile();
});

