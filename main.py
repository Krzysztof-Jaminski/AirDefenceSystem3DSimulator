"""
Główny plik uruchamiający
"""
import threading
import time
import config
from core.targets.generator import generate_targets
from core.tracker import Tracker
from core.shooting.shooter import Shooter
from visualization.visualizer import Visualizer
from simulation.move_loop import move_loop
from simulation.scan_loop import scan_loop
from simulation.detect_loop import detect_loop
from simulation.shoot_loop import shoot_loop

stop_threads = False

def main():
    global stop_threads
    targets = generate_targets(config)
    tracker = Tracker(targets)
    shooter = Shooter(tracker)
    
    # Dodaj referencję do shooter w tracker, aby visualizer mógł uzyskać dostęp do statystyk
    tracker.shooter = shooter
    
    visualizer = Visualizer(tracker)

    move_thread = threading.Thread(target=move_loop, args=(tracker, stop_threads), daemon=True)
    scan_thread = threading.Thread(target=scan_loop, args=(tracker, stop_threads), daemon=True)
    detect_thread = threading.Thread(target=detect_loop, args=(tracker, stop_threads), daemon=True)
    shoot_thread = threading.Thread(target=shoot_loop, args=(tracker, shooter, stop_threads), daemon=True)
    
    move_thread.start()
    scan_thread.start()
    detect_thread.start()
    shoot_thread.start()

    try:
        visualizer.animate()
    finally:
        stop_threads = True
        move_thread.join(timeout=1)
        scan_thread.join(timeout=1)
        detect_thread.join(timeout=1)
        shoot_thread.join(timeout=1)

if __name__ == '__main__':
    main()

