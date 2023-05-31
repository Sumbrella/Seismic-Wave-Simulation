import numpy as np
import matplotlib.pyplot as plt
from utils.boundary import Boundary

bound = Boundary.get_boundary("atten")

field = np.ones((100, 100))

plt.figure(dpi=120)
plt.imshow(field, vmin=0.1, vmax=1.0)
plt.show()

plt.figure(dpi=120)
bound.set_parameter(100, 100, 15, 15, 0.01)
bound.apply(field)

plt.imshow(field, vmin=0.1, vmax=1.0)
plt.colorbar()
plt.show()
