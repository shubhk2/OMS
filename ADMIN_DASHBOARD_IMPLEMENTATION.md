# Admin Dashboard Implementation

## Overview
This document describes the implementation of conditional dashboard rendering for admin users (role ID = 14) in the Office Management System.

## User Story
For employees with role ID 14 (Admin), the dashboard displays different content than regular employees:
- **Admin View**: Shows latest checked-in employees and ongoing projects
- **Regular View**: Shows check-in/out timer and primary team

## Features Implemented

### 1. Personalized Welcome Message
- Displays "Welcome, [FirstName]" for all users
- Extracts first name from the full name field

### 2. Admin-Specific Cards

#### Latest Checked-in Employees Card
- Replaces the check-in/out timer
- Shows the 5 most recent employee check-ins for today
- Includes a link to view all attendance records (ui-forms.html)
- Real-time data fetched from `/api/latest-checkins` endpoint

#### Explore Projects Card
- Replaces the "Primary Team" card
- Lists 4 ongoing projects in a table format
- Shows project name, deadline, and status
- Includes a link to view all projects (ui-alerts.html)
- Real-time data fetched from `/api/ongoing-projects` endpoint

### 3. Preserved Functionality for Regular Employees
- Check-in/out timer continues to work as before
- Primary team card displays as usual
- No changes to existing functionality

## Technical Implementation

### Backend API Endpoints

#### GET /api/latest-checkins
- **Authentication**: JWT required
- **Purpose**: Fetch recent check-ins for admin dashboard
- **Query**: Joins Attendance and Employee tables, filters by today's date
- **Response**: Array of check-in objects with employee details

```python
{
    "id": 1,
    "name": "Employee Name",
    "check_in_time": "09:30:00",
    "date": "2024-11-11"
}
```

#### GET /api/ongoing-projects
- **Authentication**: JWT required
- **Purpose**: Fetch ongoing projects for admin dashboard
- **Query**: Selects projects with status = 1 (ongoing), ordered by deadline
- **Response**: Array of project objects

```python
{
    "id": 1,
    "name": "Project Alpha",
    "status": 1,
    "deadline": "2024-12-31"
}
```

### Frontend Components

#### profile.js
- Main conditional rendering logic
- Fetches user profile on page load
- Determines user role and renders appropriate dashboard
- Handles API errors gracefully with fallback to login page

#### dashboard.js (Modified)
- Added conditional check for timer element existence
- Prevents JavaScript errors when elements are replaced for admin users
- Maintains backward compatibility

#### index.html (Modified)
- Loads profile.js before dashboard.js
- Simplified authentication check (moved to profile.js)

## File Changes

### New Files
- `Frontend/src/assets/js/profile.js` (165 lines)
- `.gitignore` (33 lines)
- `ADMIN_DASHBOARD_IMPLEMENTATION.md` (this file)

### Modified Files
- `backend/app.py` (+55 lines)
- `Frontend/src/assets/js/dashboard.js` (refactored timer init)
- `Frontend/src/html/index.html` (-7 lines, +1 script tag)

## Database Schema

### Tables Used
1. **Employee**: id, name, role (role 14 = Admin)
2. **Attendance**: employee_id, check_in_time, date
3. **Project**: id, name, status, deadline (status 1 = ongoing)

## Security
- All new endpoints protected with JWT authentication
- Parameterized SQL queries prevent SQL injection
- Error handling doesn't expose sensitive information
- CodeQL security scan passed with 0 alerts

## Testing

### Test Users
- **Admin**: User ID 2, "Shubh", Role 14
- **Regular**: User ID 1, "Shlok", Role 1

### Manual Test Steps
1. Login as admin user
2. Verify "Latest Checked-in Employees" card appears
3. Verify "Explore Projects" card appears
4. Verify timer is hidden
5. Login as regular user
6. Verify timer appears
7. Verify "Primary Team" card appears

## Browser Support
- Requires modern browser with ES6+ support
- Fetch API support required
- Tested with Chrome, Firefox, Safari, Edge

## Future Improvements
1. Add pagination for large lists
2. Create dedicated admin attendance and project management pages
3. Add real-time updates using WebSockets
4. Make API URL configurable
5. Add loading skeletons for better UX
6. Add date/time formatting library

## Maintenance Notes
- Backend URL is currently hard-coded to `http://127.0.0.1:5000`
- Admin role ID is hard-coded as `14`
- Check-in data is limited to today's date
- Projects limited to status = 1 (ongoing)
