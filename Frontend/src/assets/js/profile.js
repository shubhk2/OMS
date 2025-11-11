// Profile and conditional rendering logic
(async function() {
    const token = localStorage.getItem('accessToken');
    if (!token) {
        window.location.href = './authentication-login.html';
        return;
    }

    try {
        // Fetch user profile
        const response = await fetch('http://127.0.0.1:5000/profile', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const user = await response.json();
            
            // Update welcome message with first name
            const firstName = user.name.split(' ')[0];
            const welcomeText = document.getElementById('welcomeText');
            if (welcomeText) {
                welcomeText.textContent = `Welcome, ${firstName}`;
            }

            // Check if user is admin (role 14)
            if (user.role === 14) {
                // Admin view
                renderAdminDashboard();
            } else {
                // Regular employee view - keep existing functionality
                renderEmployeeDashboard();
            }
        } else {
            // Token might be invalid, redirect to login
            localStorage.removeItem('accessToken');
            window.location.href = './authentication-login.html';
        }
    } catch (error) {
        console.error('Error fetching profile:', error);
        localStorage.removeItem('accessToken');
        window.location.href = './authentication-login.html';
    }
})();

function renderAdminDashboard() {
    const token = localStorage.getItem('accessToken');
    
    // Replace the timer section with latest check-ins
    const profitDiv = document.getElementById('profit');
    if (profitDiv) {
        profitDiv.innerHTML = `
            <div class="w-100">
                <h5 class="card-title mb-3 fw-semibold">Latest Checked-in Employees</h5>
                <div id="latest-checkins-list" class="text-start">
                    <p class="text-muted">Loading...</p>
                </div>
                <a href="./ui-forms.html" class="btn btn-primary btn-sm mt-3">
                    View All Attendance <i class="ti ti-arrow-right"></i>
                </a>
            </div>
        `;
        
        // Fetch and display latest check-ins
        fetch('http://127.0.0.1:5000/api/latest-checkins', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(checkins => {
            const listDiv = document.getElementById('latest-checkins-list');
            if (checkins && checkins.length > 0) {
                listDiv.innerHTML = checkins.map(checkin => `
                    <div class="d-flex align-items-center justify-content-between mb-2 p-2 bg-light rounded">
                        <div>
                            <strong>${checkin.name}</strong>
                            <div class="text-muted small">Checked in at ${checkin.check_in_time}</div>
                        </div>
                    </div>
                `).join('');
            } else {
                listDiv.innerHTML = '<p class="text-muted">No check-ins yet today</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching check-ins:', error);
            document.getElementById('latest-checkins-list').innerHTML = 
                '<p class="text-danger">Failed to load check-ins</p>';
        });
    }

    // Replace Primary Team section with Explore Projects
    const primaryTeamSection = document.querySelector('.col-lg-8.d-flex.align-items-stretch .card');
    if (primaryTeamSection) {
        primaryTeamSection.innerHTML = `
            <div class="card-body p-4">
                <div class="d-flex mb-4 justify-content-between align-items-center">
                    <h5 class="mb-0 fw-bold">Explore Projects</h5>
                </div>
                <div id="ongoing-projects-list">
                    <p class="text-muted">Loading...</p>
                </div>
                <a href="./ui-alerts.html" class="btn btn-primary btn-sm mt-3">
                    View All Projects <i class="ti ti-arrow-right"></i>
                </a>
            </div>
        `;
        
        // Fetch and display ongoing projects
        fetch('http://127.0.0.1:5000/api/ongoing-projects', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(projects => {
            const listDiv = document.getElementById('ongoing-projects-list');
            if (projects && projects.length > 0) {
                listDiv.innerHTML = `
                    <div class="table-responsive">
                        <table class="table table-hover align-middle">
                            <thead>
                                <tr>
                                    <th>Project Name</th>
                                    <th>Deadline</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${projects.map(project => `
                                    <tr>
                                        <td><strong>${project.name}</strong></td>
                                        <td>${project.deadline || 'N/A'}</td>
                                        <td><span class="badge bg-success">Ongoing</span></td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
            } else {
                listDiv.innerHTML = '<p class="text-muted">No ongoing projects</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching projects:', error);
            document.getElementById('ongoing-projects-list').innerHTML = 
                '<p class="text-danger">Failed to load projects</p>';
        });
    }
}

function renderEmployeeDashboard() {
    // For regular employees, the existing timer and primary team functionality remains
    // This function is here for clarity but doesn't need to do anything
    // as the HTML already has the correct structure
}
