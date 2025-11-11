$(function () {


  // =====================================
  // Profit
  // =====================================
  // Timer and Buttons Logic
let clockInterval = null; // To store the clock interval
let isCheckedIn = false; // Track check-in status
let isOnBreak = false; // Track break status
let elapsedTime = 0; // Track elapsed time in seconds (for pausing/resuming)
const clockElement = document.getElementById("digitalClock");
const checkInOutBtn = document.getElementById("checkInOutBtn");
const breakBtn = document.getElementById("breakBtn");

// Only initialize timer if elements exist (for non-admin users)
if (clockElement && checkInOutBtn && breakBtn) {
  // Function to format time into HH:MM:SS
  function formatTime(seconds) {
    const hrs = String(Math.floor(seconds / 3600)).padStart(2, '0');
    const mins = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
    const secs = String(seconds % 60).padStart(2, '0');
    return `${hrs}:${mins}:${secs}`;
  }

  // Function to start the timer
  function startClock() {
    const updateClock = () => {
      elapsedTime += 1; // Increment elapsed time
      clockElement.textContent = formatTime(elapsedTime);
    };
    clockInterval = setInterval(updateClock, 1000); // Update every second
  }

  // Function to stop the timer
  function stopClock() {
    clearInterval(clockInterval);
    clockInterval = null;
  }

  // Function to handle Check In/Out button
  checkInOutBtn.addEventListener("click", () => {
    if (isCheckedIn) {
      // Check Out
      checkInOutBtn.textContent = "Check In";
      checkInOutBtn.classList.remove("btn-outline-danger");
      checkInOutBtn.classList.add("btn-outline-success");
      stopClock();
      clockElement.textContent = "--:--:--"; // Reset clock display
      elapsedTime = 0; // Reset elapsed time
      isOnBreak = false; // Reset break status
      breakBtn.textContent = "Break"; // Reset break button
      breakBtn.disabled = true; // Disable break button
    } else {
      // Check In
      checkInOutBtn.textContent = "Check Out";
      checkInOutBtn.classList.remove("btn-outline-success");
      checkInOutBtn.classList.add("btn-outline-danger");
      startClock();
      breakBtn.disabled = false; // Enable break button
    }
    isCheckedIn = !isCheckedIn; // Toggle check-in status
  });

  // Function to handle Break button
  breakBtn.addEventListener("click", () => {
    if (isOnBreak) {
      // Resume from break
      breakBtn.textContent = "Break";
      startClock(); // Resume the clock
    } else {
      // Pause for break
      breakBtn.textContent = "Resume";
      stopClock(); // Pause the clock
    }
    isOnBreak = !isOnBreak; // Toggle break status
  });

  // Initialize clock display and button states
  clockElement.textContent = "--:--:--";
  breakBtn.disabled = true; // Break button is disabled initially
}






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


