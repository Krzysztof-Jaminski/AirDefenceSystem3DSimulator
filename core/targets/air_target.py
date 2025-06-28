import math
import time
from collections import deque


class AirTarget:
    def __init__(self, id, x, y, z, speed, camouflage=0.0):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.speed = speed
        self.alive = True
        self.is_marked = False
        self.camouflage = camouflage  # 0.0 (brak kamuflażu) do 1.0 (pełny kamuflaż)
        self.detectability = 1.0 - camouflage
        self.left_field = False
        self._move_step = 0  # do trajektorii
        # Ostatnie zeskanowane pozycje (deque: [(x, y, z, timestamp), ...])
        self.last_scanned_positions = deque([(x, y, z, time.time())], maxlen=7)

    def move(self):
        from core.movetypes.straight import move_straight
        move_straight(self)

    def __repr__(self):
        return f"<AirTarget id={self.id} x={self.x} y={self.y} z={self.z} speed={self.speed} alive={self.alive} left_field={self.left_field} last_scan={self.last_scanned_positions[-1]}>"


# Metaprogramowanie: dynamiczne tworzenie podklas z różnymi trajektoriami

def create_target_type(name, speed, camouflage=0.0, move_type='straight'):
    base = AirTarget

    def move(self):
        if move_type == 'eight':
            self.move_eight()
        elif move_type == 'sine':
            self.move_sine()
        else:
            self.move_straight()

    return type(name, (base,), {"default_speed": speed, "default_camouflage": camouflage, "move": move})
