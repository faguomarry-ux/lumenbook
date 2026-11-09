# 中文注释：能量的离散近似
import numpy as np

def energy(u, dx):
    return 0.5 * dx * np.sum(u**2)
