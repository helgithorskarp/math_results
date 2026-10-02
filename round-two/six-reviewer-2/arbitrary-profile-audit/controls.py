"""Bounded semantic controls on certificate trust boundaries."""
from itertools import product
from linear import F,need,psd,inverse,mv,dot,digest,canonical
from scalars import profile
from literal import audit
import json

def reject(fn):
    try:fn()
    except (ValueError,ZeroDivisionError):return
    raise ValueError('damaged mathematics accepted')
def main():
    names=[]
    for name,fn in [
        ('boolean q',lambda:profile(True,[1,3,2,1])),
        ('boolean load',lambda:profile(8,[True,3,2,1])),
        ('zero load',lambda:profile(8,[0,3,2,1])),
        ('excluded two-type',lambda:profile(8,[1,3,3,1])),
        ('excluded three marks',lambda:profile(8,[1,3,2])),
        ('q equals marks',lambda:profile(8,[1,3,2,1,1,1,1,1])),
        ('duplicate actual mark',lambda:audit(8,[1,3,2,1],[0,1,2,2])),
        ('boolean actual mark',lambda:audit(8,[1,3,2,1],[False,1,2,3])),
        ('zero-diagonal nonzero PSD residual',lambda:psd([[0,1],[1,0]])),
        ('negative Schur diagonal',lambda:psd([[1,2],[2,1]])),
        ('nonsymmetric claimed PSD',lambda:psd([[1,1],[0,1]])),
        ('singular claimed inverse',lambda:inverse([[1,1],[1,1]]))]:
        reject(fn);names.append(name)
    # Previously validated max-diagonal PSD reused; inverse bridge independently
    # checked by direct multiplication, including every ternary symmetric2 form.
    inverted=0
    for a,b,c in product([-1,0,1],repeat=3):
        if a*c-b*b==0:continue
        A=[[F(a),F(b)],[F(b),F(c)]];B=inverse(A)
        need([[dot(row,[B[k][j] for k in range(2)]) for j in range(2)] for row in A]==[[1,0],[0,1]],'schoolbook A Ainv')
        inverted+=1
    need(F(49,180)-F(81,1400)==F(2701,12600)>F(1,5),'exact improved constants')
    out={'semantic_rejections':names,'independent_inverse_products':inverted,'improved_constant':'2701/12600','first_normal_before_author_engine_read':True};out['record_sha256']=digest(out);print(json.dumps(canonical(out),sort_keys=True,indent=2))
if __name__=='__main__':main()
