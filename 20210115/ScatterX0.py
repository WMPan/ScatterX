import numpy as np
def traversal(traversalShape,action):  
    print(traversalShape);
    ilen = len(traversalShape)
    if ilen == 0:
        raise Exception("traversalShape's length == 0！");
    elif traversalShape[0] == 0:
        raise Exception("traversalShape's length == 0！");
    traversalInd = np.array(traversalShape);
    def traversalForInner(i):   
        n = traversalShape[i];
        print("traversalShape[i]-1:::",n);
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

def getPick(E):
    P = np.zeros(E.shape()[1])
    def pick(i):
        pass
    pass


class scatter():
    def __init__(self,x,indices,updates,axis = 0):    
        if x.size == 0:
            raise Exception("Tensor's size == 0！");
        elif indices.size == 0:
            raise Exception("Tensor's size == 0！");
        elif x.size == 0:
            raise Exception("Tensor's size == 0！");
        elif updates.size == 0:
            raise Exception("Tensor's size == 0！");
        #Todo verify length
        self.x = x
        self.xNdim = x.ndim
        self.indices = indices
        self.indicesNdim = indices.ndim
        self.updates = updates
        self.updatesNdim = updates.ndim
        self.ushape = updates.shape
        self.axis = axis
        self.xshape = x.shape
        xlen = len(self.xshape);
        if axis > xlen -1 or axis < -xlen:
            raise Exception("Exception raised！");
        self.xshapeA1 = self.xshape[:axis];
        self.xshapeA2 = self.xshape[(axis+1):];
        self.ishape = indices.shape;
        
        self.ushapeA1 = self.ushape[:axis];
        self.ushapeA2 = self.ushape[(axis+1):];
        
    def withMaps(self,axmap,u1map,u2map):
        (self.axis,self.axdomain) = axmap;
        (self.u1,self.u1domain) = u1map;
        (self.u2,self.u2domain) = u2map;

    def getTargetIndex(self,updatesInd):
        '''
        updatesInd, 1-dim nparray
        '''
        tindofind = tuple(updatesInd[self.axdomain])
        taxis = (self.indices[tindofind],)
        tu1 = tuple(updatesInd[self.u1domain])
        tu2 = tuple(updatesInd[self.u1domain])
        return tu1 + taxis + tu2
        
    def scatterElement(self, updatesInd, op):   
        print("scatterElement",updatesInd)
        tupdatesInd = tuple(updatesInd)
        ttarInd = self.getTargetIndex(updatesInd)
        op(ttarInd,tupdatesInd);        
        print(ttarInd,tupdatesInd);
    def scatterSlice(self, updatesInd, op):   
        print("scatterSlice",updatesInd);
        tupdatesInd = tuple(updatesInd);
        i = self.indices[tupdatesInd];
        def toOpA1(xindA1):
            print("toUpdateA1",xindA1);
            tA1 = tuple(xindA1);
            A = tA1 +(i,);
            B = tupdatesInd + tA1;       
            op(A,B);
        def toOpA2(xindA2):
            print("toUpdateA2",xindA2);
            tA2 = tuple(xindA2);
            A = (i,)+ tA2;
            B = tupdatesInd + tA2;        
            op(A,B);
        def scatterSlice2(xindA1):
            print("scatterSlice2",xindA1);
            tA1 = tuple(xindA1);
            def toOp(xindA2):
                print("toUpdate");
                tA2 = tuple(xindA2);
                A = tA1 +(i,)+ tA2;
                B = tupdatesInd + tA1 + tA2;        
                op(A,B);
            traversal(self.xshapeA2,toOp);
        if len(self.xshapeA1) == 0:
            print("len(xshapeA1) == 0");
            if len(self.xshapeA2) != 0:
                traversal(self.xshapeA2,toOpA2);
            else:
                raise Exception("traversalShape's length == 0！");
        elif len(self.xshapeA2) == 0:
            print("len(xshapeA2) == 0");
            traversal(self.xshapeA1,toOpA1);
        else:
            print("A1S2");
            traversal(self.xshapeA1,scatterSlice2);
        print(tupdatesInd);
  
    def scatterWithOp(self,opName):  
        def getScatterInner(op):
            def scatterInner(theind):
                #def op(a,b):
                #    self.x[a] = self.updates[b];
                if self.indicesNdim == self.updatesNdim:
                    self.scatterElement(theind,op);
                else:
                    self.scatterSlice(theind,op);
            return scatterInner
        def update(a,b): 
            self.x[a] = self.updates[b];
        def getOp(s):
            if s == "update":
                return update;
            else: 
                return 0        
        traversal(self.ishape,getScatterInner(getOp(opName)));
    