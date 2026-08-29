package main

import "fmt"

type Process struct {
	ID         string
	Arrival    int
	Burst      int
	Waiting    int
	Turnaround int
	Completion int
	Remaining  int
}

func printResults(processes []Process, totalWaiting, totalTurnaround int) {
	fmt.Println()

	fmt.Printf("%-10s %-10s %-10s %-12s %-12s\n",
		"Process", "Arrival", "Burst", "Waiting", "Turnaround")

	for _, p := range processes {
		fmt.Printf("%-10s %-10d %-10d %-12d %-12d\n",
			p.ID, p.Arrival, p.Burst, p.Waiting, p.Turnaround)
	}

	fmt.Printf("\nAverage Waiting Time: %.2f\n",
		float64(totalWaiting)/float64(len(processes)))

	fmt.Printf("Average Turnaround Time: %.2f\n",
		float64(totalTurnaround)/float64(len(processes)))
}

func fcfs(processes []Process) {
	for i := 0; i < len(processes)-1; i++ {
		for j := i + 1; j < len(processes); j++ {
			if processes[j].Arrival < processes[i].Arrival {
				processes[i], processes[j] = processes[j], processes[i]
			}
		}
	}

	currentTime := 0
	totalWaiting := 0
	totalTurnaround := 0

	fmt.Println("\n--- FCFS Scheduling ---")
	fmt.Println("Gantt Chart:")

	for i := range processes {
		if currentTime < processes[i].Arrival {
			currentTime = processes[i].Arrival
		}

		processes[i].Waiting = currentTime - processes[i].Arrival
		processes[i].Completion = currentTime + processes[i].Burst
		processes[i].Turnaround =
			processes[i].Completion - processes[i].Arrival

		fmt.Printf("| %s ", processes[i].ID)

		currentTime = processes[i].Completion

		totalWaiting += processes[i].Waiting
		totalTurnaround += processes[i].Turnaround
	}

	fmt.Println("|")
	printResults(processes, totalWaiting, totalTurnaround)
}

func sjf(processes []Process) {
	n := len(processes)
	completed := make([]bool, n)

	currentTime := 0
	completedCount := 0
	totalWaiting := 0
	totalTurnaround := 0

	fmt.Println("\n--- SJF (Non-Preemptive) Scheduling ---")
	fmt.Println("Gantt Chart:")

	for completedCount < n {
		selected := -1

		for i := 0; i < n; i++ {
			if completed[i] || processes[i].Arrival > currentTime {
				continue
			}

			if selected == -1 ||
				processes[i].Burst < processes[selected].Burst ||
				(processes[i].Burst == processes[selected].Burst &&
					processes[i].Arrival < processes[selected].Arrival) {
				selected = i
			}
		}

		if selected == -1 {
			nextArrival := -1

			for i := 0; i < n; i++ {
				if !completed[i] &&
					(nextArrival == -1 || processes[i].Arrival < nextArrival) {
					nextArrival = processes[i].Arrival
				}
			}

			currentTime = nextArrival
			continue
		}

		processes[selected].Waiting =
			currentTime - processes[selected].Arrival

		processes[selected].Completion =
			currentTime + processes[selected].Burst

		processes[selected].Turnaround =
			processes[selected].Completion - processes[selected].Arrival

		fmt.Printf("| %s ", processes[selected].ID)

		currentTime = processes[selected].Completion
		completed[selected] = true
		completedCount++

		totalWaiting += processes[selected].Waiting
		totalTurnaround += processes[selected].Turnaround
	}

	fmt.Println("|")
	printResults(processes, totalWaiting, totalTurnaround)
}

func roundRobin(processes []Process, quantum int) {
	n := len(processes)

	for i := range processes {
		processes[i].Remaining = processes[i].Burst
	}

	// Sort by arrival time.
	for i := 0; i < n-1; i++ {
		for j := i + 1; j < n; j++ {
			if processes[j].Arrival < processes[i].Arrival {
				processes[i], processes[j] = processes[j], processes[i]
			}
		}
	}

	queue := make([]int, 0)
	visited := make([]bool, n)

	currentTime := 0
	completed := 0

	fmt.Println("\n--- Round Robin Scheduling ---")
	fmt.Println("Gantt Chart:")

	addArrived := func() {
		for i := 0; i < n; i++ {
			if !visited[i] && processes[i].Arrival <= currentTime {
				queue = append(queue, i)
				visited[i] = true
			}
		}
	}

	for completed < n {
		addArrived()

		if len(queue) == 0 {
			currentTime = processes[completed].Arrival
			addArrived()
		}

		index := queue[0]
		queue = queue[1:]

		runTime := quantum
		if processes[index].Remaining < quantum {
			runTime = processes[index].Remaining
		}

		startTime := currentTime

		fmt.Printf("| %s ", processes[index].ID)

		currentTime += runTime

		fmt.Printf("%d", currentTime)
		_ = startTime

		processes[index].Remaining -= runTime

		addArrived()

		if processes[index].Remaining > 0 {
			queue = append(queue, index)
		} else {
			processes[index].Completion = currentTime
			processes[index].Turnaround =
				processes[index].Completion - processes[index].Arrival
			processes[index].Waiting =
				processes[index].Turnaround - processes[index].Burst

			completed++
		}
	}

	fmt.Println("|")

	totalWaiting := 0
	totalTurnaround := 0

	for _, p := range processes {
		totalWaiting += p.Waiting
		totalTurnaround += p.Turnaround
	}

	printResults(processes, totalWaiting, totalTurnaround)
}

func main() {
	fmt.Println("================================")
	fmt.Println("   PIRATE KING'S SCHEDULER")
	fmt.Println("================================")

	var n int

	fmt.Print("\nEnter number of processes: ")
	fmt.Scan(&n)

	processes := make([]Process, n)

	for i := 0; i < n; i++ {
		fmt.Printf("\nProcess %d\n", i+1)

		fmt.Print("Process ID: ")
		fmt.Scan(&processes[i].ID)

		fmt.Print("Arrival Time: ")
		fmt.Scan(&processes[i].Arrival)

		fmt.Print("Burst Time: ")
		fmt.Scan(&processes[i].Burst)
	}

	fmt.Println("\nScheduling Algorithms:")
	fmt.Println("1. FCFS")
	fmt.Println("2. SJF (Non-Preemptive)")
	fmt.Println("3. Round Robin")

	var choice int
	fmt.Print("\nChoose algorithm: ")
	fmt.Scan(&choice)

	switch choice {
	case 1:
		fcfs(processes)

	case 2:
		sjf(processes)

	case 3:
		var quantum int
		fmt.Print("Enter Time Quantum: ")
		fmt.Scan(&quantum)

		if quantum <= 0 {
			fmt.Println("Time Quantum must be greater than 0.")
			return
		}

		roundRobin(processes, quantum)

	default:
		fmt.Println("\nInvalid choice.")
	}
}
