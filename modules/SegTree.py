class SegTree:
    """
    this is a data structure called segment tree
    this structure makes operations in L-R update and query in O(log(n))
    """

    tree = []
    lazy = []
    length = 0
    def __init__(self,a = None):
        if a == None:
            a = [0] * (10**6 * 2)
        
        self.a = a
        self.length = len(a)
        self.lazy = [0] * 4 * self.length
        self.tree = [0] * 4 * self.length
        for i in range(len(a)):
            self.update(i,i,a[i])
    
    def query(self,l, r):
        return self._query(1,0,self.length - 1, l, r)

    def _query(self,n , l , r , a, b):
        self.propagate(n,l,r)
        if l >= a and r <= b:
            return self.tree[n]
        if r < a or l > b:
            return 0
        m  = (l + r) // 2
        q1 = self._query(n*2,l,m,a,b)
        q2 = self._query(n*2+1,m+1,r,a,b)
        return max(q1,q2)

    def update(self,l , r, x):
        self._update(1,0,self.length-1,l,r,x)

    def _update(self,n, l, r , a , b, x):
        self.propagate(n,l,r)
        if l >= a and r <= b:
            self.lazy[n] += x
            self.propagate(n,l,r)
            return
        
        if r < a or l  > b:
            return 
        
        m = (l + r) // 2
        self._update(n*2,l,m,a,b,x)
        self._update(n*2+1,m+1,r,a,b,x)
        self.tree[n] = max(self.tree[n*2] , self.tree[n * 2 + 1])

    def propagate(self,n , l, r):
        if self.lazy[n] == 0:
            return
        
        self.tree[n] += self.lazy[n]
        
        if l != r:
            self.lazy[n*2] += self.lazy[n]
            self.lazy[n*2+1] += self.lazy[n]
        else:
            self.a[l] += self.lazy[n]
        
        self.lazy[n] = 0