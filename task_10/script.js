// ======================================================
// B.TECH SURVIVAL HUB
// Interactive Dashboard
// Built by Arjun
// ======================================================


// ======================================================
// DATE
// ======================================================

const today = new Date();

document.getElementById("date").textContent =
    today.toLocaleDateString("en-IN", {
        weekday: "long",
        day: "numeric",
        month: "long"
    });


// ======================================================
// TASK MANAGER
// ======================================================

let tasks =
    JSON.parse(localStorage.getItem("survivalTasks")) || [];


function saveTasks() {

    localStorage.setItem(
        "survivalTasks",
        JSON.stringify(tasks)
    );
}


function renderTasks() {

    const taskList =
        document.getElementById("taskList");

    taskList.innerHTML = "";


    tasks.forEach((task, index) => {

        const li =
            document.createElement("li");


        if (task.completed) {
            li.classList.add("completed");
        }


        li.innerHTML = `

            <span onclick="completeTask(${index})">
                ${escapeHTML(task.text)}
            </span>

            <button
                class="delete-btn"
                onclick="deleteTask(${index})"
                aria-label="Delete task"
            >
                ✕
            </button>

        `;


        taskList.appendChild(li);

    });


    updateStats();
}


// Prevent HTML from being inserted as a task

function escapeHTML(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


// Add a new task

function addTask() {

    const input =
        document.getElementById("taskInput");


    const text =
        input.value.trim();


    if (text === "") {

        alert("Enter a task first!");

        return;
    }


    tasks.push({

        text: text,

        completed: false

    });


    input.value = "";


    saveTasks();

    renderTasks();

}


// Complete / uncomplete a task

function completeTask(index) {

    tasks[index].completed =
        !tasks[index].completed;


    saveTasks();

    renderTasks();


    // Update streak when a task is completed

    if (tasks[index].completed) {

        updateStreak();

    }

}


// Delete a task

function deleteTask(index) {

    tasks.splice(index, 1);


    saveTasks();

    renderTasks();

}


// Press Enter to add task

document
    .getElementById("taskInput")
    .addEventListener(
        "keypress",
        function (event) {

            if (event.key === "Enter") {

                addTask();

            }

        }
    );


// ======================================================
// DASHBOARD STATISTICS
// ======================================================

function updateStats() {

    const completedTasks =
        tasks.filter(
            task => task.completed
        ).length;


    const totalTasks =
        tasks.length;


    // Tasks completed

    document.getElementById("completed")
        .textContent =
        completedTasks;


    // Daily progress

    let progress = 0;


    if (totalTasks > 0) {

        progress =
            Math.round(
                (completedTasks / totalTasks) * 100
            );

    }


    document.getElementById("progress")
        .textContent =
        progress + "%";


    // Focus minutes

    const focusMinutes =
        Number(
            localStorage.getItem("focusMinutes")
        ) || 0;


    document.getElementById("focusTime")
        .textContent =
        focusMinutes;

}


// ======================================================
// STREAK SYSTEM
// ======================================================

let streak =
    Number(
        localStorage.getItem("survivalStreak")
    ) || 0;


function updateStreak() {

    const todayString =
        new Date().toDateString();


    const lastCompletedDate =
        localStorage.getItem(
            "lastCompletedDate"
        );


    // Don't increase streak twice on the same day

    if (
        lastCompletedDate ===
        todayString
    ) {

        document.getElementById("streak")
            .textContent =
            streak;

        return;
    }


    streak++;


    localStorage.setItem(
        "survivalStreak",
        streak
    );


    localStorage.setItem(
        "lastCompletedDate",
        todayString
    );


    document.getElementById("streak")
        .textContent =
        streak;

}


// Display saved streak

document.getElementById("streak")
    .textContent =
    streak;


// ======================================================
// POMODORO TIMER
// ======================================================

let timeLeft =
    25 * 60;


let timerInterval =
    null;


let timerRunning =
    false;


// Update timer display

function updateTimerDisplay() {

    const minutes =
        Math.floor(timeLeft / 60);


    const seconds =
        timeLeft % 60;


    document.getElementById("timer")
        .textContent =
        `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;

}


// Start / Pause timer

function toggleTimer() {

    const button =
        document.getElementById("timerButton");


    if (timerRunning) {

        clearInterval(
            timerInterval
        );


        timerRunning = false;


        button.textContent =
            "Start";


        return;
    }


    timerRunning = true;


    button.textContent =
        "Pause";


    timerInterval =
        setInterval(
            function () {

                if (timeLeft > 0) {

                    timeLeft--;

                    updateTimerDisplay();

                }

                else {

                    completeFocusSession();

                }

            },
            1000
        );

}


// Focus session completed

function completeFocusSession() {

    clearInterval(
        timerInterval
    );


    timerRunning = false;


    document.getElementById(
        "timerButton"
    ).textContent = "Start";


    // Add 25 minutes to focus time

    let focusMinutes =
        Number(
            localStorage.getItem(
                "focusMinutes"
            )
        ) || 0;


    focusMinutes += 25;


    localStorage.setItem(
        "focusMinutes",
        focusMinutes
    );


    updateStats();


    alert(
        "🎉 Focus session complete! +25 minutes"
    );


    timeLeft =
        25 * 60;


    updateTimerDisplay();

}


// Reset timer

function resetTimer() {

    clearInterval(
        timerInterval
    );


    timeLeft =
        25 * 60;


    timerRunning =
        false;


    document.getElementById(
        "timerButton"
    ).textContent =
        "Start";


    updateTimerDisplay();

}


// Start focusing button

function startFocus() {

    document
        .getElementById("tools")
        .scrollIntoView({
            behavior: "smooth"
        });


    if (!timerRunning) {

        toggleTimer();

    }

}


// ======================================================
// PERCENTAGE CALCULATOR
// ======================================================

function calculatePercentage() {

    const marks =
        Number(
            document.getElementById(
                "marks"
            ).value
        );


    const total =
        Number(
            document.getElementById(
                "total"
            ).value
        );


    const result =
        document.getElementById(
            "percentageResult"
        );


    if (
        !Number.isFinite(marks) ||
        !Number.isFinite(total) ||
        marks < 0 ||
        total <= 0 ||
        marks > total
    ) {

        result.textContent =
            "Enter valid marks.";

        return;

    }


    const percentage =
        (marks / total) * 100;


    result.textContent =
        `Percentage: ${percentage.toFixed(2)}%`;

}


// ======================================================
// RANDOM QUOTES
// ======================================================

const quotes = [

    "The secret of getting ahead is getting started.",

    "First solve the problem. Then write the code.",

    "It always seems impossible until it's done.",

    "Small progress is still progress.",

    "Debugging is just detective work with coffee.",

    "Your future self will thank you.",

    "One more commit. One less problem.",

    "Don't watch the clock. Do what it does. Keep going.",

    "Code. Break it. Fix it. Learn from it.",

    "You don't need motivation. You need to start."

];


function newQuote() {

    const randomIndex =
        Math.floor(
            Math.random() *
            quotes.length
        );


    document.getElementById(
        "quote"
    ).textContent =
        quotes[randomIndex];

}


// ======================================================
// RANDOM PROJECT IDEAS
// ======================================================

const ideas = [

    "Build a personal expense tracker.",

    "Create a weather dashboard.",

    "Make a quiz game with a leaderboard.",

    "Build a habit tracking application.",

    "Create a movie recommendation website.",

    "Build a typing speed tester.",

    "Make a simple AI chatbot interface.",

    "Create a student attendance tracker.",

    "Build a digital notes application.",

    "Create your own portfolio website.",

    "Build a campus event finder.",

    "Create a study resource organizer.",

    "Build a simple password generator.",

    "Make a coding challenge tracker.",

    "Create a timetable generator."

];


function generateIdea() {

    const randomIndex =
        Math.floor(
            Math.random() *
            ideas.length
        );


    document.getElementById(
        "idea"
    ).textContent =
        ideas[randomIndex];

}


// ======================================================
// INITIALIZE APPLICATION
// ======================================================

updateTimerDisplay();

renderTasks();

updateStats();