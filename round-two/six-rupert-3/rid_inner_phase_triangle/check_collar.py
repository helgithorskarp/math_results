"""Recompute each complete closed receiving-layer collar in exact Q(phi)."""
from pins import verify_pins
verify_pins()
from pathlib import Path
from itertools import product
from math import comb
from time import monotonic
import argparse,json,os,platform,resource
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[name]='1'
from kernel import source_geometry,RING,F,Q,Z,O,phi,dot,cross,sub,encode,need,digest
HERE=Path(__file__).resolve().parent
BITS=list(product(range(2),repeat=2))
BOUNDS=[('1/8','1/4'),('1/4','1/2'),('1/2','1')]

def tensor(n,value):
    result={(u,v):Z for u,v in product(range(n+1),repeat=2)}
    for indices in product(range(4),repeat=n):
        u=sum(BITS[i][0] for i in indices);v=sum(BITS[i][1] for i in indices)
        result[u,v]+=value(*indices)/F(comb(n,u)*comb(n,v))
    return result

def evaluate(layer):
    start=monotonic();data,roots,volume=source_geometry();V=data['V'];s=2-phi
    pairs=list(zip(RING,RING[1:]+RING[:1]))
    def raw(si,x,t):
        i,j=pairs[si];E=sub(V[j],V[i])
        if si in (7,16):
            need(E[:2]==(Z,Z),'pole edge is not z parallel')
            return (-E[2]*t,E[2],Z)
        return cross(E,(x,x*t,O))
    physical=[];norm_controls=[]
    for si,(i,j) in enumerate(pairs):
        ms=[raw(si,F(u)*s,F(v)*s) for u,v in BITS]
        hs=[dot(m,V[i]) for m in ms]
        gaps=[[dot(m,sub(V[i],v)) for v in V] for m in ms]
        need(all(h>Z for h in hs) and all(a>=Z for g in gaps for a in g),'entire phase support failed')
        need(all(dot(m,(F(u)*s,F(u)*F(v)*s*s,O))==Z for m,(u,v) in zip(ms,BITS)),'support planarity failed')
        nc=tensor(2,lambda a,b:F(Q(25,16))*hs[a]*hs[b]-(7+8*phi)*dot(ms[a],ms[b]))
        need(all(a>Z for a in nc.values()),'entire phase support norm bound failed')
        norm_controls.extend(nc.values())
        physical.append({'support':si,'endpoints':[i,j],'height_controls':encode(hs),
            'all240_original_gap_controls_nonnegative':True,'zero_contacts_by_corner':[
                [k for k,a in enumerate(g) if a==Z] for g in gaps],
            'norm_controls':[{'index':list(k),'value':a.encode()} for k,a in nc.items()]})
    certificate=json.loads((HERE/'collars.json').read_text())
    need(len(certificate)==6 and {r['name'] for r in certificate}=={'annulus'+str(i)+str(j) for i in range(3) for j in range(2)},'closed collar cover incomplete')
    records=[]
    for half in range(2):
        proposal=next(r for r in certificate if r['name']=='annulus'+str(layer)+str(half))
        bounds=(*BOUNDS[layer],*([('0','1/2'),('1/2','1')][half]))
        need(proposal['bounds']==list(bounds),'closed annular collar bounds differ')
        u0,u1,v0,v1=map(Q,bounds)
        points=[((F(u0)+F(u1-u0)*u)*s,(F(v0)+F(v1-v0)*v)*s) for u,v in BITS]
        ms=[[raw(si,x,t) for x,t in points] for si in range(18)]
        hs=[[dot(m,V[pairs[si][0]]) for m in row] for si,row in enumerate(ms)]
        need(len(proposal['axes'])==6 and {(a['axis'],a['sign']) for a in proposal['axes']}==set(product(range(3),[-1,1])),'missing signed coordinate collar target')
        axes=[]
        for ar in proposal['axes']:
            target=tuple(F(ar['sign']) if j==ar['axis'] else Z for j in range(3))
            contacts=ar['contacts'];sign=ar['orientation'];mass=ar['mass']
            need(len(contacts)==3 and all(type(si) is int and 0<=si<18 and vi in pairs[si] for si,vi in contacts),'not an actual persistent endpoint torque')
            need(sign in [-1,1] and type(mass) is int and 1<=mass<=100,'malformed Cramer orientation or mass')
            cols=[[cross(V[vi],m) for m in ms[si]] for si,vi in contacts]
            det=tensor(3,lambda a,b,c:sign*dot(cols[0][a],cross(cols[1][b],cols[2][c])))
            nums=[]
            for k,(si,vi) in enumerate(contacts):
                j,l=(k+1)%3,(k+2)%3
                nums.append(tensor(3,lambda a,b,c:sign*hs[si][a]*dot(target,cross(cols[j][b],cols[l][c]))))
            need(all(a>Z for a in det.values()),'actual entire determinant control not positive')
            need(all(a>=Z for n in nums for a in n.values()),'actual entire numerator control negative')
            mc={ex:F(mass)*det[ex]-sum((n[ex] for n in nums),Z) for ex in det}
            need(all(a>Z for a in mc.values()),'actual entire dual mass bound failed')
            weights=[]
            for x,t in [*points,(sum((p[0] for p in points),Z)/4,sum((p[1] for p in points),Z)/4)]:
                ns=[tuple(a/dot(raw(si,x,t),V[vi]) for a in raw(si,x,t)) for si,vi in contacts]
                fs=[cross(V[vi],n) for (si,vi),n in zip(contacts,ns)]
                d=dot(fs[0],cross(fs[1],fs[2]));need(d!=Z,'literal normalized basis singular')
                ws=[dot(target,cross(fs[(k+1)%3],fs[(k+2)%3]))/d for k in range(3)]
                need(all(w>=Z for w in ws) and sum(ws,Z)<F(mass),'literal normalized mass/sign failed')
                need(tuple(sum((ws[k]*fs[k][j] for k in range(3)),Z) for j in range(3))==target,'literal Cramer target identity failed')
                weights.append(encode(ws))
            axes.append({'axis':ar['axis'],'sign':ar['sign'],'contacts':contacts,'orientation':sign,'mass':mass,
                'controls':{name:[{'index':list(k),'value':a.encode()} for k,a in g.items()] for name,g in
                    [('determinant',det),('num0',nums[0]),('num1',nums[1]),('num2',nums[2]),('mass',mc)]},
                'five_independent_actual_weight_evaluations':weights})
        records.append({'name':proposal['name'],'bounds':list(bounds),'axes':axes,
                        'coordinate_mass_bounds':[max(a['mass'] for a in axes if a['axis']==j) for j in range(3)]})
    return {'agent':'six-rupert-3','role':'researcher','layer':layer,'closed_rectangles':records,
        'whole_full_phase_supports':physical,'all_original_gap_corner_controls':4320,
        'minimum_norm_control':min(norm_controls).encode(),'full_phase_norm_controls':162,
        'actual_dual_controls':960,'literal_Cramer_vector_identities':60,
        'actual_body_geometry_sha256':digest(data['record']),
        'seconds':round(monotonic()-start,3),'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'optimized':not __debug__,'python':platform.python_version(),'threads':1,'external_guard_seconds':20}

def main():
    p=argparse.ArgumentParser();p.add_argument('--layer',type=int,choices=range(3),required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    need(not a.output.exists(),'fresh unique collar record required')
    r=evaluate(a.layer);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ['layer','actual_dual_controls','seconds','peak_kib','optimized']}),flush=True)

if __name__=='__main__':main()
