import threading
import time
from core.targets.air_target import AirTarget

class Tracker:
    """
    Klasa do śledzenia celów.
    Programowanie współbieżne: użycie threading.Lock do bezpiecznego dostępu do listy celów.
    """
    def __init__(self, targets):
        self.targets = targets
        self.lock = threading.Lock()

    def update_positions(self):
        with self.lock:
            for target in self.targets:
                if target.alive:
                    target.move()

    def scan_targets(self):
        """Symuluje skanowanie radaru: aktualizuje last_scanned_positions każdego celu (deque)."""
        now = time.time()
        with self.lock:
            for target in self.targets:
                if target.alive:
                    target.last_scanned_positions.append((target.x, target.y, target.z, now))
                    target.last_scanned_position = target.last_scanned_positions[-1]

    def get_alive_targets(self):
        with self.lock:
            return [t for t in self.targets if t.alive] 