const availableDates = {
  "October": [6, 8, 13, 14, 15, 20, 21],
  // ...
};

const month = "October";
const daysInMonth = 31;

const calendar = document.getElementById("calendar");

for (let i = 1; i <= daysInMonth; i++) {
  const dayBox = document.createElement("div");
  dayBox.className = "calendar-box";
  dayBox.innerHTML = i;

  if (!availableDates[month].includes(i)) {
    dayBox.classList.add("unavailable");
  }

  calendar.appendChild(dayBox);
}
