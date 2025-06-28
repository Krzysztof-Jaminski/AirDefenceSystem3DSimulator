import random
import numpy as np
from core.targets.target_creator import create_target_types, create_single_target

def generate_targets(config):
    """
    Generuje listę celów na podstawie parametrów z configu.
    Metaprogramowanie: dynamiczne typy celów (różne trajektorie) są tworzone przez create_target_type.
    """
    target_types = create_target_types(config)
    
    grid_size = int(np.ceil(np.sqrt(config.NUM_TARGETS)))
    y_vals = np.linspace(config.Y_RANGE[0], config.Y_RANGE[1], grid_size)
    z_vals = np.linspace(config.Z_RANGE[0], config.Z_RANGE[1], grid_size)
    points = [(y, z) for y in y_vals for z in z_vals]
    random.shuffle(points)
    
    targets = []
    for i in range(config.NUM_TARGETS):
        target_class = random.choice(target_types)
        y, z = points[i % len(points)]
        x = random.randint(0, 250)
        
        target = create_single_target(i, target_class, x, y, z, config)
        targets.append(target)
    
    return targets 