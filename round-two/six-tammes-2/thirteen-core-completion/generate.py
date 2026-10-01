"""Rebuild the reference construction and cap with exact rational arithmetic."""
import argparse,json
from pathlib import Path
import check as c
import field as f

def generate():
    H=tuple(tuple(f.ONE if i==j else f.T for j in range(3)) for i in range(3))
    a=tuple(map(f.Q,('-27/2','-3','35','-24','117/2')))
    b=tuple(map(f.Q,('-31/4','-19/2','34','-53/2','195/4')))
    d=tuple(map(f.Q,('81/4','21/2','-69','101/2','-429/4')))
    M=((a,b,d),(d,a,b),(b,d,a))
    u=f.inverse(f.sub(f.ONE,f.T))
    v=f.mul(f.T,f.inverse(f.mul(f.sub(f.ONE,f.T),f.add(f.ONE,f.scale(f.T,2)))))
    anchors=[[f.sub(f.mul(u,M[i][j]),f.mul(v,f.sum_field(M[k][j] for k in range(3))))
              for j in range(3)] for i in range(3)]
    V={i:tuple(f.ONE if j==k else f.ZERO for j in range(3)) for k,i in enumerate((0,5,11))}
    for j,i in enumerate((1,2,4)):V[i]=tuple(anchors[k][j] for k in range(3))
    r=f.mul(f.scale(f.T,2),f.inverse(f.add(f.ONE,f.T)))
    for n,i,j,o in c.STEPS+((3,1,4,2),(14,0,6,11)):
        V[n]=tuple(f.sub(f.mul(r,f.add(x,y)),z) for x,y,z in zip(V[i],V[j],V[o]))
    V=[V[i] for i in range(15)];N=[f.matvec(H,p) for p in V];longs=[]
    for labels in ((0,4,6),(0,4,7)):
        A=[N[i] for i in labels];D=f.det(A);di=f.inverse(D)
        U=tuple(f.det([[f.T if j==k else A[i][j] for j in range(3)] for i in range(3)]) for k in range(3))
        longs.append(tuple(f.mul(x,di) for x in U))
    C=tuple(f.add(f.add(x,y),f.scale(z,f.Q(4,5))) for x,y,z in zip(longs[0],longs[1],V[3]))
    enc=lambda point:[list(map(str,p)) for p in point]
    result={'format':1,'core_labels':list(c.CORE),'core_edges':[list(e) for e in c.graph()[0]],
            'incumbent_vectors':[enc(p) for p in V],
            'exterior_vertices':[{'active_labels':list(labels),'vector':enc(p)} for labels,p in zip(((0,4,6),(0,4,7)),longs)],
            'center':enc(C),'center_blend':'4/5','cap_bound':'667/250',
            'short_squared_norm_upper':'99/100','cap_code_parameter_upper':'593/1000',
            'cap_capacity_gap_lower':'9/1000','relaxation_max':'1/1000',
            'relaxed_isolated_distance_constant':802,'near_contact_max':'1/10000000000000',
            'whole_configuration_constant':1700000000000,'exclusion_max':'1/10000000000000000000'}
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();data=generate();result=c.verify(data)
    args.output.write_text(json.dumps(data,separators=(',',':'))+'\n')
    print(json.dumps(result,sort_keys=True))
