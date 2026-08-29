# Task 06 – Pirate King's Scheduler

## Overview

Pirate King's Scheduler is a terminal-based CPU scheduling simulator developed in Go.

The simulator accepts process information and executes the processes using three CPU scheduling algorithms:

- First Come First Serve (FCFS)
- Shortest Job First (SJF - Non-Preemptive)
- Round Robin (RR)

## Input

For each process, the simulator accepts:

- Process ID
- Arrival Time
- Burst Time

For Round Robin scheduling, a Time Quantum is also accepted.

## Scheduling Algorithms

### FCFS

First Come First Serve executes processes according to their arrival time.

### SJF

Shortest Job First (Non-Preemptive) selects the process with the shortest burst time among the processes that have already arrived.

### Round Robin

Round Robin gives each process a fixed CPU time called the Time Quantum. If a process does not finish within its quantum, it is placed back into the ready queue.

## Calculations

For every process, the simulator calculates:

### Completion Time

The time at which a process finishes execution.

### Turnaround Time

Turnaround Time = Completion Time - Arrival Time

### Waiting Time

Waiting Time = Turnaround Time - Burst Time

The program also calculates:

- Average Waiting Time
- Average Turnaround Time

## Gantt Chart

The simulator displays the execution order using a simple terminal-based Gantt chart.

Example:

    | P1 | P2 | P3 | P4 | P1 | P2 |

## Technologies Used

- Go
- Linux Terminal
- Go modules

## Concepts Learned

- CPU scheduling
- FCFS scheduling
- Non-Preemptive SJF
- Round Robin scheduling
- Process arrival and burst times
- Waiting time and turnaround time
- Gantt charts
- Go structs
- Go slices
- Functions
- Loops and conditionals
- Go module management

## Resources Used

- Go Tour: https://go.dev/tour/list
- Go documentation: https://go.dev/doc/
- CPU scheduling concepts and standard operating-system references

## Running the Program

Initialize the Go module:

    go mod init pirate-king-scheduler

Run the simulator:

    go run main.go
