import time
import random
import config

def detect_loop(tracker, stop_threads):
    while not stop_threads:
        with tracker.lock:
            for t in tracker.targets:
                if t.alive and not t.left_field and not t.is_marked:
                    if random.random() < t.detectability:
                        t.is_marked = True
        time.sleep(config.DETECTION_TIME) 