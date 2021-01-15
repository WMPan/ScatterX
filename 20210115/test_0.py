import numpy as np
A = np.array([[[8,9,10],[5,19,6],[11,29,3]],
            [[8,9,10],[5,19,6],[11,29,3]]])
import pytest
import ScatterX

def test_001():
    x1 = np.array([[1,2,3,4],[5,6,7,8]])
    indices1 = np.array([[0],[1]])
    updates1 = np.array([[1,1,1,1],[2,3,4,5]])
    ScatterX.scatter(x1,indices1,updates1,0).scatterWithOp("update")
    x1
    assert True
   
if __name__ == "__main__":
    
    pass