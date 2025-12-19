document.addEventListener('DOMContentLoaded', function() {
    const welcomeText = document.getElementById('welcomeText');
    const checkInOutBtn = document.getElementById('checkInOutBtn');
    const breakBtn = document.getElementById('breakBtn');
    const digitalClock = document.getElementById('digitalClock');
    const token = localStorage.getItem('accessToken');
    let timerInterval;

    if (!token) {
        // Prefer shared auth routing (handles PyCharm base path)
        if (window.omsAuth && typeof window.omsAuth.makeLoginPath === 'function') {
            window.location.href = window.omsAuth.makeLoginPath();
        } else {
            // fallback relative to views/employee/*
            window.location.href = '../../authentication-login.html';
        }
        return;
    }

    const API_URL = 'http://127.0.0.1:5000';
    let _localSeconds = 0;

    function fetchProfile() {
        fetch(`${API_URL}/profile`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.name && welcomeText) {
                const firstName = data.name.split(' ')[0];
                welcomeText.textContent = `Welcome, ${firstName}`;
            }
            // Only employee dashboard logic remains here. If admin UI is needed,
            // it will be implemented in views/admin with its own scripts.
            setupEmployeeDashboard();
        })
        .catch(error => console.error('Error fetching profile:', error));
    }

    function setupEmployeeDashboard() {
        fetchAttendanceStatus();
        if (checkInOutBtn) checkInOutBtn.addEventListener('click', handleCheckInOut);
        if (breakBtn) breakBtn.addEventListener('click', handleBreakToggle);
    }

    function fetchAttendanceStatus() {
        fetch(`${API_URL}/attendance/status`, {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        .then(response => response.json())
        .then(data => {
            updateUI(data.is_checked_in);
            if (data.is_checked_in) {
                // check if currently on break
                fetch(`${API_URL}/attendance/is_on_break`, { headers: { 'Authorization': `Bearer ${token}` } })
                .then(r => r.json())
                .then(b => {
                    // fetch elapsed once to set local clock
                    fetch(`${API_URL}/attendance/elapsed`, { headers: { 'Authorization': `Bearer ${token}` } })
                    .then(r2 => r2.json())
                    .then(d => {
                        let parts = (d.elapsed_time || '00:00:00').split(':');
                        _localSeconds = (+parts[0]) * 3600 + (+parts[1]) * 60 + (+parts[2]);
                        if (b.on_break) {
                            // on break, do not start timer (clock remains static at elapsed_time)
                            stopTimer();
                        } else {
                            startTimer();
                        }
                    });
                });
            } else {
                // not checked in - set clock to placeholder
                if (digitalClock) digitalClock.textContent = '--:--:--';
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
                // sync elapsed and start timer
                fetch(`${API_URL}/attendance/elapsed`, { headers: { 'Authorization': `Bearer ${token}` } })
                .then(r => r.json()).then(d => {
                    let parts = (d.elapsed_time || '00:00:00').split(':');
                    _localSeconds = (+parts[0]) * 3600 + (+parts[1]) * 60 + (+parts[2]);
                    startTimer();
                }).catch(err => { _localSeconds = 0; startTimer(); });
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
                _localSeconds = 0;
                digitalClock.textContent = '--:--:--';
            } else {
                console.error('Check-out failed:', data.error);
            }
        })
        .catch(error => console.error('Error during check-out:', error));
    }

    function handleBreakToggle() {
        fetch(`${API_URL}/attendance/break`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                if (data.message.toLowerCase().includes('started')) {
                    // on break, stop local increment (leave elapsed_time as-is)
                    stopTimer();
                } else if (data.message.toLowerCase().includes('ended')) {
                    // on break ended, resume local timer
                    startTimer();
                }
            } else {
                console.error('Break toggle failed:', data.error);
            }
        })
        .catch(err => console.error('Error toggling break:', err));
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
        timerInterval = setInterval(() => {
            _localSeconds = (_localSeconds || 0) + 1;
            const h = Math.floor(_localSeconds / 3600);
            const m = Math.floor((_localSeconds % 3600) / 60);
            const s = _localSeconds % 60;
            digitalClock.textContent = `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
        }, 1000);
    }

    function stopTimer() {
        if (timerInterval) clearInterval(timerInterval);
        timerInterval = null;
    }

    fetchProfile();
});
