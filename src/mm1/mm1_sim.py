import heapq
import random
from collections import deque
from typing import Deque, List, Optional, Tuple


class MM1Sim:
    """
    Discrete‐event simulation of an M/M/1 queue using a single event‐heap.
    Bootstraps with an arrival at t=0 and stops after max_events departures.

    Returns:
      - avg_N:    time‐averaged number in system
      - E[T_sys]: average time from arrival to departure
      - E[T_q]:   average waiting time in queue
      - util:     fraction of time server is busy
    """

    def __init__(
        self,
        lam: float,
        mu: float,
        max_events: int,
        seed: Optional[int] = None,
    ) -> None:
        self.lam: float = lam
        self.mu: float = mu
        self.max_events: int = max_events
        self.seed: Optional[int] = seed
        if seed is not None:
            random.seed(seed)

    def simulate(self) -> Tuple[float, float, float, float]:
        # Event heap: (time, type) where type is 'arrival' or 'departure'
        pending: List[Tuple[float, str]] = []
        heapq.heappush(pending, (0.0, "arrival"))

        # Server state & queue of arrival times
        server_busy: bool = False
        queue: Deque[float] = deque()

        # Statistics
        t: float = 0.0
        last_t: float = 0.0
        area_N: float = 0.0
        total_wait: float = 0.0
        total_system: float = 0.0
        busy_time: float = 0.0
        completed: int = 0
        t_end: float = 0.0
        arrival_current: float = 0.0
        service_start: float = 0.0

        while completed < self.max_events and pending:
            t_next, event = heapq.heappop(pending)

            # Update time‐averaged N(t)
            area_N += (len(queue) + (1 if server_busy else 0)) * (t_next - last_t)
            last_t = t_next
            t = t_next

            if event == "arrival":
                # Schedule next arrival
                next_arrival: float = t + random.expovariate(self.lam)
                heapq.heappush(pending, (next_arrival, "arrival"))

                if not server_busy:
                    # Begin service immediately
                    server_busy = True
                    arrival_current = t
                    service_start = t
                    departure_time: float = t + random.expovariate(self.mu)
                    heapq.heappush(pending, (departure_time, "departure"))
                else:
                    # Join queue
                    queue.append(t)

            else:  # departure
                # Complete current service
                completed += 1
                total_system += t - arrival_current
                busy_time += t - service_start

                if completed == self.max_events:
                    t_end = t
                    break

                if queue:
                    # Dequeue next customer
                    arrival_current = queue.popleft()
                    total_wait += t - arrival_current
                    service_start = t
                    departure_time = t + random.expovariate(self.mu)
                    heapq.heappush(pending, (departure_time, "departure"))
                    server_busy = True
                else:
                    # No one waiting
                    server_busy = False

        # If we never set t_end inside loop, use last event time
        t_end = t_end or t

        # Compute metrics
        duration: float = t_end if t_end > 0 else 1.0
        avg_N: float = area_N / duration
        utilization: float = busy_time / duration
        E_T_sys: float = total_system / completed if completed > 0 else 0.0
        E_T_q: float = total_wait / completed if completed > 0 else 0.0

        return avg_N, E_T_sys, E_T_q, utilization
