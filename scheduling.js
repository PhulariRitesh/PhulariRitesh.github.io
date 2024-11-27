let processes = [];
let processCounter = 1;
let totalEnergy = 0; // Variable to keep track of cumulative energy

function addProcess() {
    const burstTime = document.getElementById('burst-time').value;
    const arrivalTime = document.getElementById('arrival-time').value;

    if (burstTime === '' || arrivalTime === '') {
        alert('Please enter both burst time and arrival time!');
        return;
    }

    const process = {
        id: processCounter++,
        burstTime: parseInt(burstTime),
        arrivalTime: parseInt(arrivalTime),
        state: 'ready', // Initial state
        frequency: 0,
        voltage: 0
    };

    processes.push(process);
    displayProcesses();
}

function deleteProcess() {
    const processId = prompt('Enter the Process ID to delete:');
    const index = processes.findIndex(p => p.id === parseInt(processId));

    if (index !== -1) {
        processes.splice(index, 1);
        displayProcesses();
    } else {
        alert('Process not found!');
    }
}

function displayProcesses() {
    const readyQueueElement = document.getElementById('ready-queue');
    readyQueueElement.innerHTML = ''; // Clear the current ready queue

    processes.forEach(process => {
        const processElement = document.createElement('div');
        processElement.className = `process-box ready`;
        processElement.id = `process-${process.id}`;
        processElement.innerHTML = `
            <h3>Process ${process.id}</h3>
            <p>Burst Time: ${process.burstTime}</p>
            <p>Arrival Time: ${process.arrivalTime}</p>
        `;
        readyQueueElement.appendChild(processElement);
    });
}

function simulateScheduling() {
    if (processes.length === 0) {
        alert('No processes to simulate!');
        return;
    }

    // Start the simulation by sorting by arrival time
    processes.sort((a, b) => a.arrivalTime - b.arrivalTime);

    // Display the processes starting from the ready queue
    processes.forEach((process, index) => {
        // Animate the state transitions for each process
        setTimeout(() => {
            const processElement = document.getElementById(`process-${process.id}`);
            processElement.classList.remove('ready');
            processElement.classList.add('executing');
            document.getElementById('executing-queue').appendChild(processElement);
            processElement.classList.add('executing-animation');
            processElement.innerHTML += '<p>Executing...</p>';

            // Simulate DVFS adjustments
            process.frequency = calculateFrequency(process.burstTime);
            process.voltage = calculateVoltage(process.frequency);
        }, index * 1000); // Adjust timing for each process

        setTimeout(() => {
            const processElement = document.getElementById(`process-${process.id}`);
            processElement.classList.remove('executing');
            processElement.classList.add('completed');
            document.getElementById('completed-queue').appendChild(processElement);
            processElement.classList.add('completed-animation');
            processElement.innerHTML += '<p>Completed!</p>';

            // Add the process results to the results table
            addToResultTable(process);
        }, (index + 1) * 3000); // Adjust timing for each process's completion
    });

    // Show the results table after all processes have been simulated
    setTimeout(() => {
        document.getElementById('simulation-result').classList.remove('hidden');
    }, (processes.length + 1) * 3000);
}

function calculateFrequency(burstTime) {
    // Example DVFS frequency calculation based on burst time
    return 1000 / burstTime; // Simplified example
}

function calculateVoltage(frequency) {
    // Example DVFS voltage calculation based on frequency
    return 1.0 + (frequency / 1000); // Simplified example
}

function calculateEnergy(frequency, voltage, burstTime) {
    // Example energy calculation based on frequency, voltage, and burst time
    return 0.5 * frequency * (voltage ** 2) * burstTime; // Simplified example
}

function addToResultTable(process) {
    const resultTable = document.getElementById('result-table');
    const row = document.createElement('tr');
    const energy = calculateEnergy(process.frequency, process.voltage, process.burstTime);
    totalEnergy += energy; // Update cumulative energy
    row.innerHTML = `
        <td class="border px-4 py-2">${process.id}</td>
        <td class="border px-4 py-2">${process.burstTime}</td>
        <td class="border px-4 py-2">${process.arrivalTime}</td>
        <td class="border px-4 py-2">${(process.frequency * 10).toFixed(2)} MHz</td>
        <td class="border px-4 py-2">${process.voltage.toFixed(2)} V</td>
        <td class="border px-4 py-2">${energy.toFixed(2)} J</td>
        <td class="border px-4 py-2">${totalEnergy.toFixed(2)} J</td>
    `;
    resultTable.appendChild(row);
}

// Update the table header to include the new column
document.addEventListener('DOMContentLoaded', () => {
    const resultTableHeader = document.getElementById('result-table-header');
    resultTableHeader.innerHTML = `
        <th class="border px-4 py-2">Process ID</th>
        <th class="border px-4 py-2">Burst Time</th>
        <th class="border px-4 py-2">Arrival Time</th>
        <th class="border px-4 py-2">Frequency</th>
        <th class="border px-4 py-2">Voltage</th>
        <th class="border px-4 py-2">Individual Energy</th>
        <th class="border px-4 py-2">Total Energy</th>
    `;
});
