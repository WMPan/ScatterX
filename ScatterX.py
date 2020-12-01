import numpy as np

def getPick(p):
    if p.ndim != 1:
        raise Exception("ndim does not equal 1！");
    lp = p.shape[0]
    
    def pick(i):
        if lp == 0:
            return np.array([], dtype='int16')
        mx = p.max();
        mn = p.min();
        if i.ndim != 1:
            raise Exception("ndim does not equal 1！");  
        
        if mx >= i.shape[0]:
            raise Exception("Argument Invalid！");
        j = np.zeros(lp, dtype = 'int16');
        for k in range(lp):
            j[k]= i[p[k]];
        return j
    return pick

def traversal(traversalShape,action):      
    ilen = len(traversalShape)
    if ilen == 0:
        raise Exception("traversalShape's length == 0！");
    elif traversalShape[0] == 0:
        raise Exception("traversalShape's length == 0！");
    traversalInd = np.array(traversalShape);
    def traversalForInner(i):   
        n = traversalShape[i];
        
        if i < ilen-1:
            for j in range(n):
                traversalInd[i] = j;
                traversalForInner(i+1);
        elif i == ilen-1:
            for j in range(n):
                traversalInd[i] = j;
                action(traversalInd);
        else:
            raise Exception("Exception raised！");
    traversalForInner(0)

def getProvisionXTransformer(shape0, shape1, T0, p0, p1, p):    
    if p0.dtype != 'int16' or p0.dtype != 'int16' or p.dtype != 'int16':
        raise Exception("Data type error！");
    elif p0.ndim != 1 or p0.ndim != 1 or p.ndim != 1:
        raise Exception("ndim to form pick does not equal 1！");
    E = np.zeros(shape0 + (len(shape1),), dtype = 'int16');
    I = np.zeros(len(shape0), dtype = 'int16');
    J = np.zeros(len(shape1), dtype = 'int16');
    pick0 = getPick(p0);
    pick1 = getPick(p1);
    pick = getPick(p);
    def combine(IC):
        J0 = pick0(IC);
       
        Jp = T0[tuple(J0)] 
        J1 = pick1(IC)
        Jl = list(tuple(Jp) + tuple(J1))
        Ja = np.array(Jl, dtype = 'int16')
        J = pick(Ja)
        E[tuple(IC)] = J;
    traversal(shape0,combine)
   
    return E

def scatter(src, X, XTransformer):
    shape = XTransformer.shape[:-1];    
    I = np.zeros(len(shape), dtype = 'int16');
    def action(Ia):
        src[tuple(XTransformer[tuple(Ia)])] = X[tuple(Ia)]
    traversal(shape,action)
    return src

def scatterX(src, X, shape1, T0, p0, p1, p):
    shape0 = X.shape;
    
    XTransformer = getProvisionXTransformer(shape0, shape1, T0, p0, p1, p);
    
    scatter(src, X, XTransformer)
    return src
def tensorflowScatter(tensor, indices, updates):
    l = list(range(len(indices.shape) - 1))
   
    tl = indices.shape[-1]
    ln = list(range(len(tensor.shape)))
    
    t1 = ln[tl:]   
    
    p0 = np.array(l, dtype='int16')
    p1 = np.array(t1, dtype='int16')
    p = np.array(ln, dtype='int16')
    scatterX(tensor, updates, tensor.shape, indices, p0, p1, p)
    