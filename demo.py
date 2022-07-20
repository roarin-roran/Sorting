import numpy as np
import cProfile

a = np.random.rand(100000000)

print(a)


cProfile.run('b = np.sort(a)')

print(b)
