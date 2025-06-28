import time
import config

def shoot_loop(tracker, shooter, stop_threads):
    """Pętla zestrzeliwania celów"""
    while not stop_threads:
        detected = [t for t in tracker.get_alive_targets() if t.is_marked and not t.left_field]
        # Użyj nowego systemu zestrzeliwania
        shooter.shoot_targets(detected)
        time.sleep(config.SHOOT_TIME) 