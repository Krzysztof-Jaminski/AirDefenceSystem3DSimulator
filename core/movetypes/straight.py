import random
from config import Y_RANGE, Z_RANGE

def move_straight(self):
    """Ruch prostoliniowy w prawo z lekkim dryfem"""
    self.x += self.speed
    self.y += random.uniform(-0.2, 0.2)  # mały dryf
    self.z += random.uniform(-0.2, 0.2)
    # Ograniczenie do zakresu
    self.y = max(Y_RANGE[0], min(Y_RANGE[1], self.y))
    self.z = max(Z_RANGE[0], min(Z_RANGE[1], self.z))
    self._move_step += 1 