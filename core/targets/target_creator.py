import random
from core.targets.target_factory import create_target_type

def create_target_types(config):
    """Tworzy typy celów z różnymi trajektoriami"""
    StraightTarget = create_target_type("StraightTarget", speed=1, camouflage=config.CAMOUFLAGE_RANGE[1], move_type='straight')
    EightTarget = create_target_type("EightTarget", speed=1, camouflage=config.CAMOUFLAGE_RANGE[0], move_type='eight')
    SineTarget = create_target_type("SineTarget", speed=1, camouflage=config.CAMOUFLAGE_RANGE[0], move_type='sine')
    return [StraightTarget, EightTarget, SineTarget]

def create_single_target(i, target_class, x, y, z, config):
    """Tworzy pojedynczy cel z losowymi parametrami"""
    camo = getattr(target_class, 'default_camouflage', random.uniform(*config.CAMOUFLAGE_RANGE))
    speed = random.uniform(*config.SPEEDS)
    
    target = target_class(i, x, y, z, speed, camo)
    target.is_marked = False
    return target 