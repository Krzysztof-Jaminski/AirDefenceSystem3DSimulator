from core.movetypes.straight import move_straight
from core.movetypes.eight import move_eight
from core.movetypes.sine import move_sine

def create_target_type(name, speed, camouflage=0.0, move_type='straight'):
    """
    Metaprogramowanie: dynamiczne tworzenie podklas z różnymi trajektoriami
    """
    from core.targets.air_target import AirTarget
    base = AirTarget
    
    def move(self):
        if move_type == 'eight':
            move_eight(self)
        elif move_type == 'sine':
            move_sine(self)
        else:
            move_straight(self)
    
    return type(name, (base,), {
        "default_speed": speed, 
        "default_camouflage": camouflage, 
        "move": move
    }) 