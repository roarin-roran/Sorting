import cProfile
import Experiments as exp

# exp.run_bottom_up(10000,1,2)

# cProfile.run("exp.run_bottom_up(1000000,1,2)",sort=1)

cProfile.run("exp.run_adaptive(1000000,1,2)",sort=1)
