import time
import random
import config
from core.shooting.predictor import predict_position, is_hit

class Shooter:
    def __init__(self, tracker):
        self.tracker = tracker
        self.last_predictions = {}  # {target_id: (predicted_pos, prediction_time)}
        self.shots_fired = 0
        self.shots_missed = 0

    def shoot_targets(self, targets):
        """Zestrzeliwuje cele na podstawie przewidywania pozycji"""
        current_time = time.time()
        
        # Ogranicz liczbę jednoczesnych strzałów
        targets_to_shoot = targets[:config.MAX_SIMULTANEOUS_SHOTS]
        
        for target in targets_to_shoot:
            if not target.is_marked or not target.alive:
                continue
                
            # Pobierz ostatnie zeskanowane pozycje
            scanned_data = list(target.last_scanned_positions)
            if len(scanned_data) < 3:  # Potrzebujemy minimum 3 pozycje
                continue
                
            # Rozdziel pozycje i timestampy
            positions = [(x, y, z) for x, y, z, t in scanned_data]
            timestamps = [t for x, y, z, t in scanned_data]
            
            # Przewiduj pozycję
            predicted_pos = predict_position(positions, timestamps, current_time)
            if predicted_pos is None:
                continue
                
            # Sprawdź czy przewidywana pozycja zgadza się z rzeczywistą
            real_pos = (target.x, target.y, target.z)
            self.shots_fired += 1
            
            if is_hit(real_pos, predicted_pos):
                # Cel zestrzelony!
                target.alive = False
                target.is_marked = False
            else:
                # Spudłowano
                self.shots_missed += 1
            
            # Zapisz predykcję dla przyszłego porównania
            self.last_predictions[target.id] = (predicted_pos, current_time)
    
    def get_stats(self):
        """Zwraca statystyki strzałów"""
        total_shots = self.shots_fired
        hits = self.shots_fired - self.shots_missed
        accuracy = (hits / total_shots * 100) if total_shots > 0 else 0
        return {
            'shots_fired': total_shots,
            'hits': hits,
            'misses': self.shots_missed,
            'accuracy': accuracy
        } 