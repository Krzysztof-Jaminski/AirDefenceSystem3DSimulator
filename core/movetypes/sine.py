import math
from config import Y_RANGE, Z_RANGE

def move_sine(self):
    """Ruch po sinusoidzie"""
    self.x += self.speed
    self.y += 2 * math.sin(self._move_step / 10)
    self.z += 2 * math.sin(self._move_step / 15)
    # Ograniczenie do zakresu
    self.y = max(Y_RANGE[0], min(Y_RANGE[1], self.y))
    self.z = max(Z_RANGE[0], min(Z_RANGE[1], self.z))
    self._move_step += 1 