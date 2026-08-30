# B.Tech Survival Hub 🚀

Hey! I'm Arjun, and this is my Task 10 project for amFOSS.

I decided to build something that I would actually find useful instead of making another random demo just for the sake of completing a task.

As a B.Tech student, there are always a bunch of things going on at the same time — assignments, coding, studying, projects, deadlines... and somehow I still end up wondering what I was supposed to do five minutes ago. 😭

So I made the **B.Tech Survival Hub**.

It's basically a small personal dashboard where I can keep track of my tasks, focus sessions and progress, while also having a few useful tools when I need them.

---

## What can it do?

### ✅ Keep track of tasks

I can add things that I need to get done, mark them as completed and delete them when I don't need them anymore.

The tasks are stored in the browser using `localStorage`, so they don't disappear every time I refresh the page.

### 🔥 Track my progress

The dashboard shows:

- My current streak
- Number of completed tasks
- Focus time
- Overall task progress

So I can get a quick idea of how productive (or unproductive 💀) I've been.

### ⏱️ Focus Timer

There's a simple 25-minute Pomodoro timer for those times when I actually decide to focus.

It supports:

- Start
- Pause
- Reset

Completed focus sessions are also counted in the dashboard.

### 🧮 Quick Percentage Calculator

A tiny tool for quickly calculating marks percentage.

Because sometimes opening a calculator feels like too much work. 😂

### 💡 Random Project Ideas

Sometimes I want to build something but have absolutely no idea what.

So I added a button that randomly gives me a project idea.

Maybe one of them will actually become a real project someday.

### 💬 Random Quotes

There's also a small quote generator because apparently every productivity dashboard needs one.

I won't pretend it will magically make me productive, but it looks nice. 😭

---

## Why did I make this?

The main reason was simple:

**I wanted Task 10 to actually represent me.**

Instead of building something completely unrelated, I thought about the things I deal with as a computer science student and tried to turn some of them into a small application.

This project started as a simple idea and slowly turned into a proper little dashboard.

I also wanted to use this task as an opportunity to experiment with things rather than just following a tutorial line by line.

---

## Things I used

I kept the project simple:

- HTML
- CSS
- JavaScript
- `localStorage`

No frameworks, no backend and no database.

Just the basics and a lot of tweaking until I liked how it looked.

---

## Things I learned

While making this, I got more comfortable with:

- Manipulating HTML elements using JavaScript
- Handling button clicks and keyboard events
- Creating and controlling timers
- Using arrays and objects to manage data
- Saving data with `localStorage`
- Updating parts of a webpage dynamically
- Using CSS Grid and Flexbox
- Making a website responsive
- Thinking about how a user would actually interact with something I build

One thing I especially liked was seeing how a small piece of JavaScript could immediately change something on the webpage.

It made the project feel less like a collection of files and more like an actual application.

---

## How to run it

If you have Python installed, go into the `task_10` folder and run:

```bash
python3 -m http.server 8000
