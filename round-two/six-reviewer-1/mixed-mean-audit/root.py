"""Fresh entire original-root equation and unaveraged mixed normal check."""
from pathlib import Path
import sys,json,signal,time,resource,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fractions import Fraction as Q
from field import E,W,C,I,need
from series import *
from family import primitive
def run(j,tau=0):
    v,A,B,K,p=primitive(tau);z=W**j
    root=sj(z);inv=1/(9*z**8)
    for n in range(1,11):root[n]=ps(value(p,root,n)[n],-inv)
    need(value(p,root)==[{}]*11,'complete original root equation label'+str(j))
    normal=ss(sa(sm(root,conj(root)),sj(-1)),Q(1,2))
    first=-(E(Q(1,3))+v['x']*z.real()+v['y']*(z*z).real())
    need(normal[2]==pc(first),'all individual leading original normals')
    if j in [3,4,5,6]:
        need(normal[:10]==[{}]*10,'all individual active normals through degree nine')
        if j in [3,6]:
            aa=E(Q(21588995,28449792))+Q(86382659,170698752)*C+Q(44717485,85349376)*C*C
            bb=E(Q(83,8232))+Q(137,4116)*C+Q(109,4116)*C*C
        else:
            aa=E(Q(90414379,146313216))+Q(216408443,256048128)*C+Q(65443465,256048128)*C*C
            bb=E(Q(391,24696))+Q(557,24696)*C+Q(41,12348)*C*C
        q0={e:x for e,x in normal[10].items()if e[1]==0}
        want=pa(q0,ps(pm(pc(aa),pp(T,2)),-1),ps(pm(ps(MU,bb),pp(T,2)),-1))
        need(normal[10]==want,'complete individual mixed tenth polynomial and t4 cancellation')
    L=-z/3-v['x']-v['y']/z
    need(root[1]=={}and root[2]==pc(L)and root[3]=={},'all literal lower root jets')
    Wj=((3+4*C)*z-(1+2*C)*(1+1/z)-1/z**2)/18
    need(root[5]==ps(T,I*Wj),'individual complete shrinking motion jet')
    if j==0:
        anchor=sj(1);anchor[2]=pc(-1);need(root==anchor,'exact original marked branch')
    return {'label':j,'tau':tau,'primitive': [record(S)for S in p],'root':record(root),'normal':record(normal),'all_original_root_equation_positions_paid':True,'all_individual_active_normals_and_mixed_tenth_paid':j in [3,4,5,6]}
if __name__=='__main__':
    signal.alarm(45);start=time.monotonic();rec=run(int(sys.argv[1]),int(sys.argv[2]));raw=(json.dumps(rec,sort_keys=True,separators=(',',':'))+'\n').encode();Path(sys.argv[3]).write_bytes(raw)
    print(json.dumps({'label':rec['label'],'tau':rec['tau'],'whole_bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'seconds':round(time.monotonic()-start,6),'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
