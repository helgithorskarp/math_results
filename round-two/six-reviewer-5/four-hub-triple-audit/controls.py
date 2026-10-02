"""Post-seal certificate controls. No producer, census or author import.
Checks arithmetic soundness; count-DAG completeness remains a separate bridge.
"""
import collections,copy,itertools as it,json,pathlib
P=pathlib.Path(__file__).resolve().parent
def need(ok,message):
    if not ok:raise ValueError(message)
def validate(a):
    types=a['types'];need(len(types)==60,'all semantic types')
    for t in types:
        h=t['histogram'];d=sum(h);weighted=sum((j+1)*c for j,c in enumerate(h))
        need(t['h']==5-t['e'] and d==t['h']-t['k'] and t['sigma']==weighted-d and t['g1']==h[0] and t['w']==5-weighted,'every histogram/weight identity')
        psi=h[0] if t['e']==0 and t['eligible'] else -h[0] if t['e'] and not t['eligible'] else 0
        need(t['psi']==psi and t['margin']==psi-3*(t['k']-t['e']-t['q'])>=0,'exact m4 charge')
    keys={(Q,T,X,tau) for T in (3,4) for Q in range(13) for X in range(7) for tau in range(4) if Q+2*T+2*X+4*tau<=12}
    need(len(a['cases'])==30 and {tuple(c['case'][k] for k in ('Q','T','X','tau')) for c in a['cases']}==keys,'complete distinct case rectangle')
    total=0;stages=collections.Counter();final=[]
    for c in a['cases']:
        t=c['case'];Q,T,X,tau=(t[k] for k in ('Q','T','X','tau'));E=18-Q-T-2*tau
        need((t['E'],t['K'],t['budget'])==(E,24-E+2*X,3*(12-Q-2*T-2*X-4*tau)),'every exact target')
        seen=set()
        for r in c['records']:
            v=r['counts'];need(len(v)==60 and all(type(x)==int and x>=0 for x in v) and tuple(v) not in seen,'full unique nonnegative vector');seen.add(tuple(v))
            need(sum(v)==14 and all(sum(n*s[f] for n,s in zip(v,types))==t[k] for f,k in (('e','E'),('k','K'),('q','Q'))),'fourteen rows and exact E/K/Q')
            need(sum(n*s['sigma'] for n,s in zip(v,types))==2*X and sum(n*s['margin'] for n,s in zip(v,types))<=t['budget'],'weighted excess and margin')
            V=[s for n,s in zip(v,types) for _ in range(n)];pot={}
            for i,j in it.combinations(range(14),2):
                x,y=V[i],V[j]
                if (x['e']==0 and y['eligible']) or (y['e']==0 and x['eligible']):continue
                col={z for z,(a,b) in enumerate(zip(x['histogram'],y['histogram'])) if a and b}
                if col:pot[i,j]=col
            bad=[]
            if any(sum(s['histogram'][j] for s in V)%2 for j in range(5)):bad.append('color_parity')
            if any(sum(i in pair and j in col for pair,col in pot.items())<s['histogram'][j] for i,s in enumerate(V) for j in range(5)):bad.append('distinct_partners')
            if any(sum(sorted((sum(V[j]['histogram']) for j in range(14) if j!=i and tuple(sorted((i,j))) in pot),reverse=True)[:sum(s['histogram'])])<13 for i,s in enumerate(V) if s['k']==0):bad.append('relaxed_radius13')
            cut=r['cut'];stage=cut['stage'];stages[stage]+=1;total+=1
            if bad:need(stage=='prior' and cut['failures']==bad,'all actual prior failures');continue
            final.append(dict(case=t,counts=v,cut=cut))
            U=[s for s in V if s['e']==0];A=[s for s in U if not s['eligible']]
            C=[s for s in V if s['e'] and not s['eligible']]
            if stage=='unit_capacity':
                demand=sum(sum(s['histogram']) for s in U);internal=sum(min(sum(s['histogram']),len(A)-1) for s in A);cross=sum(s['g1'] for s in C)
                need(cut==dict(stage=stage,demand=demand,internal_upper=internal,cross_upper=cross) and demand>internal+cross,'strict unit incidence inequality')
            elif stage=='closed_unit_parity':
                ds=[sum(s['histogram']) for s in U]
                need(U and not C and sum(ds)%2==1 and cut['degrees']==ds,'closed actual odd degree list')
            elif stage=='new_disjoint_radius':
                Delta=max(sum(s['histogram']) for s in V)
                need(all(s['k']<=1 for s in V) and Delta<=3 and cut==dict(stage=stage,n=14,hubs=4,max_degree=Delta,column_minimum=14-Delta**2,required=4*(14-Delta**2)) and cut['required']>14,'disjoint radius-support formula under credited positive-column bridge')
            elif stage=='support':need(cut['population'] in ({'A':2,'C':12},{'A':2,'C':11,'J':1}),'two residual support populations')
            else:raise ValueError('unjustified final reason')
    need(total==283 and dict(stages)==a['stages'] and final==a['final_populations'],'complete certificate totals and full final stream')
    return True

def run():
    a=json.loads((P/'EVIDENCE.json').read_text());validate(a);damaged=[]
    def reject(name,change):
        b=copy.deepcopy(a);change(b)
        try:validate(b)
        except (ValueError,KeyError,IndexError):damaged.append(name);return
        raise ValueError('semantic damage accepted: '+name)
    reject('missing branch',lambda b:b['cases'].pop())
    reject('incorrect K',lambda b:b['cases'][0]['case'].__setitem__('K',b['cases'][0]['case']['K']+1))
    reject('altered histogram',lambda b:b['types'][0]['histogram'].__setitem__(0,4))
    c=next(i for i,c in enumerate(a['cases']) if c['records'])
    reject('missing vector',lambda b:b['cases'][c]['records'].pop())
    reject('incorrect vector charge',lambda b:b['cases'][c]['records'][0]['counts'].__setitem__(0,b['cases'][c]['records'][0]['counts'][0]+1))
    def change_cut(b,stage,key,value):
        r=next(r for c in b['cases'] for r in c['records'] if r['cut']['stage']==stage);r['cut'][key]=value
    reject('dropped return contribution in radius support',lambda b:change_cut(b,'new_disjoint_radius','column_minimum',4))
    reject('false unit capacity',lambda b:change_cut(b,'unit_capacity','cross_upper',16))
    reject('forged closed degree list',lambda b:change_cut(b,'closed_unit_parity','degrees',[4,4,4,4,4]))
    result=dict(actual_author='six-reviewer-5',role='independent mathematical reviewer',original_passes=True,rejected=damaged,controls_added_after_primary_seal=True,completeness_proof='separately stated count DAG and full late comparison, not inferred from this semantic checker')
    (P/'CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':run()
