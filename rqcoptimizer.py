from utils.cfgraph import CFGraph

# Code Optimizer class
class RQCOptimizer:
    def __init__(self):
        pass

    def midlevel_optimize(self, mid_code):
        cfg = CFGraph(mid_code)
        return mid_code
    
    def lowlevel_optimize(self, low_code):
        return low_code