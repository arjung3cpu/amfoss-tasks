# Grand Line Guardian

## Overview

Grand Line Guardian is a terminal-based system monitoring application developed to monitor running processes in real time.

The application displays:

- Process ID (PID)
- Process name
- CPU usage
- Memory usage
- Total active process count

The information is refreshed continuously at a short time interval so that the process list remains up to date.

## Approach

The application is implemented in Python using the `psutil` library.

`psutil` provides access to process and system information available through the Linux operating system.

For each running process, the application collects:

- PID using `process.pid`
- Process name using `process.name()`
- CPU usage using `process.cpu_percent()`
- Memory usage using `process.memory_percent()`

The program repeatedly collects this information and prints an updated process table in the terminal.

## Real-Time Monitoring

The monitor refreshes the displayed process information approximately once every second.

This allows changes in running processes and resource usage to be observed in real time.

The application also keeps track of the total number of active processes.

## Process Management

Linux represents processes through the operating system process table and kernel interfaces.

The `psutil` library provides a convenient Python interface for accessing this information without directly parsing every `/proc` entry manually.

I also tested the monitor using a temporary CPU-consuming process:

```bash
yes > /dev/null &
