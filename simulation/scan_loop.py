import time
import config

def scan_loop(tracker, stop_threads):
    """Pętla skanowania radaru"""
    while not stop_threads:
        tracker.scan_targets()
        time.sleep(config.DETECTION_TIME) 