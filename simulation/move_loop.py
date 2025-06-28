import time
import config

def move_loop(tracker, stop_threads):
    """Pętla ruchu celów"""
    while not stop_threads:
        tracker.update_positions()
        # Oznacz left_field dla tych, które opuściły pole
        with tracker.lock:
            for t in tracker.targets:
                if t.alive and not t.left_field and (
                    t.x > config.X_RANGE[1] or t.y < config.Y_RANGE[0] or t.y > config.Y_RANGE[1] or t.z < config.Z_RANGE[0] or t.z > config.Z_RANGE[1]
                ):
                    t.left_field = True
                    t.is_marked = False
        time.sleep(config.ANIMATION_INTERVAL / 1000.0) 