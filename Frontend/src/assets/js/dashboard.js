$(function () {


  // =====================================
  // Profit
  // =====================================
  // Timer and Buttons Logic
  // Removed duplicate timer/listener logic so `attendance.js` is the single source of truth
  // Keep helpers for formatting and set initial UI state only
  let clockInterval = null; // reserved but not started here
  let isCheckedIn = false; // UI-only placeholder
  let isOnBreak = false; // UI-only placeholder
  let elapsedTime = 0; // placeholder
  const clockElement = document.getElementById("digitalClock");
  const checkInOutBtn = document.getElementById("checkInOutBtn");
  const breakBtn = document.getElementById("breakBtn");

  function formatTime(seconds) {
    const hrs = String(Math.floor(seconds / 3600)).padStart(2, '0');
    const mins = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
    const secs = String(seconds % 60).padStart(2, '0');
    return `${hrs}:${mins}:${secs}`;
  }

  // Initialize clock display and button states (attendance.js will attach handlers)
  clockElement.textContent = "--:--:--";
  if (breakBtn) breakBtn.disabled = true;






  // =====================================
  // Updates
  // =====================================
  document.querySelectorAll('.update-btn').forEach((button) => {
  button.addEventListener('click', (event) => {
    const type = button.getAttribute('data-type');
    switch (type) {
      case 'task_due':
        alert('Project alpha details: It is due today. Prioritize completion!');
        break;
      case 'new_task':
        alert('Details about the new task in project beta.');
        break;
      case 'task_approved':
        alert('Your task rest request has been approved. No further action needed.');
        break;
      case 'task_reminder':
        alert('Project gamma details: It is due tomorrow. Start preparations.');
        break;
      default:
        alert('No additional information available.');
    }
  });
});


});
