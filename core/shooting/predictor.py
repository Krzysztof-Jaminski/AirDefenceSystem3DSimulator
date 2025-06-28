import math
import time
import random
import config

def calculate_velocity(positions, timestamps):
    """Oblicza prędkość na podstawie ostatnich pozycji"""
    if len(positions) < 2:
        return None
    
    # Oblicz prędkość na podstawie ostatnich 2 pozycji
    x1, y1, z1 = positions[-2]
    x2, y2, z2 = positions[-1]
    t1, t2 = timestamps[-2], timestamps[-1]
    
    dt = t2 - t1
    if dt == 0:
        return None
    
    vx = (x2 - x1) / dt
    vy = (y2 - y1) / dt
    vz = (z2 - z1) / dt
    
    return (vx, vy, vz)

def predict_position(positions, timestamps, prediction_time):
    """Przewiduje pozycję celu w przyszłości"""
    velocity = calculate_velocity(positions, timestamps)
    if velocity is None:
        return None
    
    vx, vy, vz = velocity
    last_x, last_y, last_z = positions[-1]
    last_time = timestamps[-1]
    
    # Przewidywana pozycja
    dt = prediction_time - last_time
    predicted_x = last_x + vx * dt
    predicted_y = last_y + vy * dt
    predicted_z = last_z + vz * dt
    
    return (predicted_x, predicted_y, predicted_z)

def is_hit(real_position, predicted_position, tolerance=None):
    """Sprawdza czy przewidywana pozycja zgadza się z rzeczywistą"""
    if predicted_position is None:
        return False
    
    # Użyj tolerancji z config lub domyślnej
    if tolerance is None:
        tolerance = config.PREDICTION_TOLERANCE
    
    rx, ry, rz = real_position
    px, py, pz = predicted_position
    
    # Oblicz odległość między pozycjami
    distance = math.sqrt((rx - px)**2 + (ry - py)**2 + (rz - pz)**2)
    
    # Dodaj losowość - nawet jeśli pozycja jest bliska, nie zawsze trafiamy
    if distance <= tolerance:
        # Szansa trafienia maleje z odległością
        hit_chance = max(0.1, 1.0 - (distance / tolerance))
        return random.random() < hit_chance
    
    return False 