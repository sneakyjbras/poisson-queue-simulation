# mm1_sim.py
import random
from typing import Optional

class MM1Sim:
    """
    Simulates a single-server M/M/1 queue using discrete event simulation.
    
    Each packet’s arrival, service start, and departure are tracked to compute:
    - Average time in system (E[T_system])
    - Average time in queue (E[T_queue])
    - Server utilization (fraction of time server is busy)
    """
    lam: float
    mu: float
    sim_time: float
    E_T_system: float
    E_T_queue: float
    utilization: float

    def __init__(self, lam: float, mu: float, sim_time: float, seed: Optional[int] = None) -> None:
        """
        Initialize the M/M/1 simulator with given parameters.
        
        :param lam: Arrival rate (λ) for the Poisson process of packet arrivals.
        :param mu: Service rate (μ) for the exponential service times.
        :param sim_time: Total simulation time horizon.
        :param seed: Optional random seed for reproducibility.
        """
        self.lam = lam
        self.mu = mu
        self.sim_time = sim_time
        if seed is not None:
            # Set the random seed for reproducibility (affects random.expovariate)
            random.seed(seed)
        # Initialize result metrics
        self.E_T_system = 0.0
        self.E_T_queue = 0.0
        self.utilization = 0.0

    def simulate(self) -> tuple[float, float, float]:
        """
        Run the discrete event simulation for the M/M/1 queue.
        
        :return: A tuple (E[T_system], E[T_queue], utilization) with the computed metrics.
        """
        # Simulation clock
        current_time: float = 0.0
        # Time of next arrival and next departure events
        next_arrival: float = random.expovariate(self.lam)
        next_departure: float = float('inf')  # no departure scheduled initially
        # Server state and queue
        server_busy: bool = False
        queue: list[float] = []              # FIFO queue to store arrival times of waiting customers
        # Track the customer currently in service (arrival time and service start time)
        current_customer_arrival: Optional[float] = None
        current_service_start: Optional[float] = None
        # Accumulators for metrics
        total_wait_time: float = 0.0
        total_system_time: float = 0.0
        busy_time: float = 0.0
        completed_jobs: int = 0

        # Main event loop
        while True:
            if next_arrival <= next_departure and next_arrival <= self.sim_time:
                # Process the next arrival event
                current_time = next_arrival
                # Schedule the subsequent arrival
                next_arrival = current_time + random.expovariate(self.lam)
                if not server_busy:
                    # Server is idle, this arrival starts service immediately
                    server_busy = True
                    current_customer_arrival = current_time
                    current_service_start = current_time
                    # No waiting time (service starts upon arrival)
                    service_time = random.expovariate(self.mu)
                    next_departure = current_time + service_time
                else:
                    # Server is busy, put this customer in queue
                    queue.append(current_time)
            elif next_departure <= next_arrival and next_departure <= self.sim_time:
                # Process the next departure (service completion) event
                current_time = next_departure
                completed_jobs += 1
                # Compute system time for the departing customer (departure - arrival)
                if current_customer_arrival is not None:
                    total_system_time += (current_time - current_customer_arrival)
                # Add the service duration to busy time
                if current_service_start is not None:
                    busy_time += (current_time - current_service_start)
                # Server becomes free; check if someone is waiting in queue
                if queue:
                    # Start service for the next customer in queue immediately
                    server_busy = True
                    current_customer_arrival = queue.pop(0)
                    current_service_start = current_time
                    # Compute waiting time for this customer (start service - arrival)
                    total_wait_time += (current_time - current_customer_arrival)
                    # Schedule departure for this customer
                    service_time = random.expovariate(self.mu)
                    next_departure = current_time + service_time
                else:
                    # No one in queue, server goes idle
                    server_busy = False
                    current_customer_arrival = None
                    current_service_start = None
                    next_departure = float('inf')
            else:
                # No more events within the simulation time horizon
                # Account for partial busy time if a service is ongoing at sim_time
                if server_busy and current_service_start is not None:
                    busy_time += (self.sim_time - current_service_start)
                break

        # Calculate average metrics
        if completed_jobs > 0:
            self.E_T_system = total_system_time / completed_jobs
            self.E_T_queue = total_wait_time / completed_jobs
        else:
            # If no jobs completed, averages remain zero
            self.E_T_system = 0.0
            self.E_T_queue = 0.0
        # Utilization: fraction of time the server was busy during the simulation
        self.utilization = busy_time / self.sim_time

        return (self.E_T_system, self.E_T_queue, self.utilization)

