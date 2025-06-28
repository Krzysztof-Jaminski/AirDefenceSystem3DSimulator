import random

class Marker:
    def __init__(self, tracker):
        self.tracker = tracker

    def detect_targets(self):
        for t in self.tracker.get_alive_targets():
            if not t.is_marked and random.random() < t.detectability:
                t.is_marked = True

    def mark_targets(self, n=5):
        detected = [t for t in self.tracker.get_alive_targets() if t.is_marked]
        marked = random.sample(detected, min(n, len(detected)))
        return marked 