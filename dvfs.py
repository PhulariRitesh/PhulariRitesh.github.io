#Programmers : 1. Ritesh Prakashrao Phulari (2203125)
#              2. Shreeraj Kishor Deshmukh (2203130)

# Instructions to run the code:
# 1. Save this script as dvfs.py.
# 2. Run the script using the command:
#    python dvfs.py

import random
import matplotlib.pyplot as plt
import numpy as np

class AdvancedDVFSController:
    class DVFSLevel:
        def __init__(self, frequency, power, mode):
            self.frequency = frequency  # in MHz
            self.power = power          # in Watts
            self.mode = mode            # Performance mode label

    class Process:
        def __init__(self, id, arrival_time, burst_time, assigned_level):
            self.id = id
            self.arrival_time = arrival_time
            self.burst_time = burst_time
            self.remaining_time = burst_time
            self.assigned_level = assigned_level

    class ProcessMetrics:
        def __init__(self, process_id, time, frequency, energy, cumulative_energy, system_load):
            self.process_id = process_id
            self.time = time
            self.frequency = frequency
            self.energy = energy
            self.cumulative_energy = cumulative_energy
            self.system_load = system_load

    def __init__(self):
        # Defining DVFS levels with different frequencies and power consumptions
        self.dvfs_levels = [
            self.DVFSLevel(800, 10.0, "Very Low"),    # 0.8 GHz, 10W
            self.DVFSLevel(1000, 15.0, "Low"),        # 1.0 GHz, 15W
            self.DVFSLevel(1200, 20.0, "Low-Medium"), # 1.2 GHz, 20W
            self.DVFSLevel(1500, 30.0, "Medium"),     # 1.5 GHz, 30W
            self.DVFSLevel(1800, 40.0, "Medium-High"),# 1.8 GHz, 40W
            self.DVFSLevel(2000, 50.0, "High"),       # 2.0 GHz, 50W
            self.DVFSLevel(2200, 60.0, "Very High")   # 2.2 GHz, 60W
        ]
        self.process_metrics_log = []

    def generate_processes(self, num_processes):
        # Generating a list of processes with random arrival and burst times
        processes = []
        for i in range(num_processes):
            arrival_time = random.uniform(0.0, 5.0)
            burst_time = random.uniform(5.0, 20.0)
            process = self.Process(i, arrival_time, burst_time, self.dvfs_levels[0])
            processes.append(process)
        processes.sort(key=lambda p: p.arrival_time)
        return processes

    def calculate_process_energy(self, process, time_slice):
        # Calculating the energy consumed by a process during a time slice
        return process.assigned_level.power * (time_slice / 3600.0)  # Energy in Wh

    def select_optimal_dvfs_level(self, system_load):
        # Function to Select the optimal DVFS level based on the system load
        if system_load > 0.85:
            return self.dvfs_levels[6]  # Very High Performance
        elif system_load > 0.7:
            return self.dvfs_levels[5]  # High Performance
        elif system_load > 0.55:
            return self.dvfs_levels[4]  # Medium-High Performance
        elif system_load > 0.4:
            return self.dvfs_levels[3]  # Medium Performance
        elif system_load > 0.25:
            return self.dvfs_levels[2]  # Low-Medium Performance
        elif system_load > 0.1:
            return self.dvfs_levels[1]  # Low Performance
        else:
            return self.dvfs_levels[0]  # Very Low Performance

    def simulate_process_scheduling(self, num_processes):
        # Function to Simulate the scheduling of processes and log their metrics
        processes = self.generate_processes(num_processes)
        current_time = 0.0
        total_system_energy = 0.0
        cumulative_energy = 0.0
        completed_processes = []

        time_points = []  # List to store actual time points as processes are executed
        system_load_curve = []  # List to store system load values for each time point

        while processes:
            total_remaining_time = sum(p.remaining_time for p in processes)
            system_load = random.uniform(0.1, 1.0)  # Simulating system load, can be replaced by your own logic
            system_load = max(0.0, min(1.0, system_load))

            process = processes[0]
            process.assigned_level = self.select_optimal_dvfs_level(system_load)

            execute_time = min(1.0, process.remaining_time)  # Simulate 1 second execution
            process.remaining_time -= execute_time
            current_time += execute_time

            # Log the time points and system load
            time_points.append(current_time)
            system_load_curve.append(system_load)

            process_energy = self.calculate_process_energy(process, execute_time)
            cumulative_energy += process_energy
            total_system_energy += process_energy

            self.process_metrics_log.append(self.ProcessMetrics(
                process.id,
                current_time,
                process.assigned_level.frequency,
                process_energy,
                cumulative_energy,
                system_load
            ))

            if process.remaining_time <= 0:
                completed_processes.append(process)
                processes.pop(0)

        print(f"Total Energy Consumption: {total_system_energy:.2f} Wh")
        self.generate_plot(time_points, system_load_curve)

    def generate_plot(self, times, system_loads):
        # Generate plots for power consumption, cumulative energy, frequency scaling, and system load
        energies = [m.energy for m in self.process_metrics_log]
        cumulative_energies = [m.cumulative_energy for m in self.process_metrics_log]
        frequencies = [m.frequency for m in self.process_metrics_log]

        # Plotting
        plt.figure(figsize=(12, 10))

        # Energy Consumption Plot
        plt.subplot(4, 1, 1)
        plt.plot(times, energies, label="Power Consumption", color='r')
        plt.title("Power Consumption over Time")
        plt.xlabel("Time (s)")
        plt.ylabel("Power (Wh)")
        plt.grid(True)

        # Cumulative Energy Consumption Plot
        plt.subplot(4, 1, 2)
        plt.plot(times, cumulative_energies, label="Cumulative Energy", color='orange')
        plt.title("Cumulative Energy Consumption over Time")
        plt.xlabel("Time (s)")
        plt.ylabel("Cumulative Energy (Wh)")
        plt.grid(True)

        # Frequency Scaling Plot
        plt.subplot(4, 1, 3)
        plt.plot(times, frequencies, label="Frequency", color='g')
        plt.title("Frequency Scaling over Time")
        plt.xlabel("Time (s)")
        plt.ylabel("Frequency (MHz)")
        plt.grid(True)

        # System Load Plot
        plt.subplot(4, 1, 4)
        plt.plot(times, system_loads, label="System Load", color='b')
        plt.title("System Load (Non-Linear) over Time")
        plt.xlabel("Time (s)")
        plt.ylabel("System Load")
        plt.grid(True)

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    dvfs_controller = AdvancedDVFSController()
    print("Simulation with 100 Processes:")
    dvfs_controller.simulate_process_scheduling(15)
