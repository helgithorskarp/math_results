"""Reviewer-owned arithmetic, support and interval rejection controls."""
from fractions import Fraction as F
from itertools import product
from exact import require,determinant,inverse,leading,polynomial,value
from audit import literal,blocks,full_matrix,maximal_interval

def run():
    rejected=[]
    def reject(name,call):
        try:call()
        except ValueError:rejected.append(name)
        else:raise ValueError('Control accepted '+name)
    reject('nonsquare determinant',lambda:determinant([[1,2]]))
    reject('oversized determinant',lambda:determinant([[int(i==j) for j in range(7)] for i in range(7)]))
    reject('float arithmetic',lambda:determinant([[1.0]]))
    reject('singular adjugate',lambda:inverse([[1,1],[1,1]]))
    reject('empty inverse',lambda:inverse([]))
    reject('empty strict matrix',lambda:leading([]))
    reject('asymmetric matrix',lambda:leading([[2,1],[0,2]]))
    reject('zero diagonal indefinite',lambda:leading([[0,1],[1,0]]))
    reject('semidefinite is not strict',lambda:leading([[1,0],[0,0]]))
    reject('changing Schur remainder',lambda:polynomial([[2,0],[0,2]],[[0,0],[0,1]]))
    permutations=0
    for entries in product((-1,0,1),repeat=4):
        a,b,c,d=entries;require(determinant([[a,b],[c,d]])==a*d-b*c,'two-dimensional determinant definition');permutations+=1
    for a in ([[3,1,0],[1,4,1],[0,1,2]],[[2,-1],[-1,3]],[[F(3,2),F(1,3)],[F(1,3),F(2,5)]]):
        leading(a);inverse(a)
    sets,base,slope=literal();small,_,_=blocks(sets,base,slope)
    wrong=[[502*int(i==j)-small['C2'][0][i][j]-F(69,200)*small['C2'][1][i][j] for j in range(4)] for i in range(4)]
    reject('forgotten coupled Gram norms',lambda:leading(wrong))
    reject('zero coupling is indefinite',lambda:leading(small['Q0'][0]))
    high=[[small['Q0'][0][i][j]+F(349,1000)*small['Q0'][1][i][j] for j in range(6)] for i in range(6)]
    reject('outside exact interval',lambda:leading(high))
    core=[[base[i][j]+69*slope[i][j]//200 for j in range(492)] for i in range(492)]
    core[0][1]+=200;core[1][0]+=200
    reject('changed intersecting middle entry',lambda:full_matrix(sets,core))
    reject('malformed full core',lambda:full_matrix(sets,[]))
    return dict(status='COMPLETE',rejections=rejected,literal_2x2_determinants=permutations,
                positive_adjugate_controls=3,checks_use_assert=False)

if __name__=='__main__':
    import json
    print(json.dumps(run(),indent=2))
