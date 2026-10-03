"""Meaningful rejection and whole function controls, with no target code import."""
import copy,json,sys
from engine import *
from cover import local,semigroup
from input_adapter import check,decode
from audit import run

def reject(f,why):
    try:f()
    except (ValueError,KeyError,IndexError,TypeError):return why
    raise ValueError('damage accepted: '+why)
def test(primary,cover,certificate):
    out=[]
    sample=primary['scalar_first_witnesses']
    for kind in ('DIRECT_COST','TIGHT_FREE_CUT','TIGHT_MARKED_PORT_LOCK','SEMANTIC_WEIGHTED_MASS'):
        one=next(x for x in sample if x['witness']['kind']==kind);word=gates(one['word']);w=one['witness']
        if kind=='SEMANTIC_WEIGHTED_MASS':
            for field in (0,2,4,5,6):
                z=copy.deepcopy(w);z['distinct_tag_witness_records'][0][field]^=1;out.append(reject(lambda:check(word,z),'mass record field'+str(field)))
            z=copy.deepcopy(w);z['distinct_tag_witness_records'].append(z['distinct_tag_witness_records'][0]);z['mass']=sum(1<<(r[4]+r[5]) for r in z['distinct_tag_witness_records']);out.append(reject(lambda:check(word,z),'duplicate actual mass tag'))
            z=copy.deepcopy(w);z['imported_size']+=1;out.append(reject(lambda:check(word,z),'mass floor'))
        else:
            for field in (0,2,4,5,6):
                z=copy.deepcopy(w);z['record'][field]^=1;out.append(reject(lambda:check(word,z),kind+' record field'+str(field)))
            z=copy.deepcopy(w);z['imported_size']+=1;out.append(reject(lambda:check(word,z),kind+' floor'))
            if kind!='DIRECT_COST':
                z=copy.deepcopy(w);z['full_Boolean_witness']=0;out.append(reject(lambda:check(word,z),kind+' wrong rank'))
    # Whole catalogue validation runs before any sliced witness computation.
    z=copy.deepcopy(certificate);z['function_bindings'].pop();out.append(reject(lambda:run(cover,z,0,0),'missing prefix function'))
    z=copy.deepcopy(certificate);z['function_bindings'].append(z['function_bindings'][0]);out.append(reject(lambda:run(cover,z,0,0),'duplicate prefix function'))
    z=copy.deepcopy(certificate);z['literal_prefix'][-1]=[3,5];out.append(reject(lambda:run(cover,z,0,0),'wrong literal Q'))
    z=copy.deepcopy(certificate);z['function_bindings'][0][1][0]='L';out.append(reject(lambda:run(cover,z,0,1),'freed partner called live'))
    row=next(i for i,x in enumerate(certificate['function_bindings']) if any(type(h)is list for h in x[1]));col=next(j for j,h in enumerate(certificate['function_bindings'][row][1]) if type(h)is list)
    z=copy.deepcopy(certificate);z['function_bindings'][row][1][col].pop();out.append(reject(lambda:run(cover,z,row,row+1),'missing balanced tail'))
    # Every tail has six literal equal-cost orders, not just three image sets.
    tailcontrols=[]
    for q in DEAD:
        fs=[];roots=sorted((1,2,3,min(8,q)))
        for t in tails(q):
            u=tuple((roots.index(a),roots.index(b)) for a,b in t);v=(u[1],u[0],u[2]);require(local(u,4)==local(v,4),'commuting balanced orders');fs.append(local(u,4))
        require(len(set(fs))==3,'distinct ordered balanced functions');tailcontrols.append([q,fs])
    early_cubes=[]
    for e in certificate['early_negative_first_gates']:
        word=Q+(tuple(e['gate']),);rec=e['witness']['record'];actual,outputs=scalar(word,rec[0],rec[1]);_,x,free=replay(word,rec[0],rec[1])
        require(actual==rec and outputs==list(rows(x,len(free))),'early whole scalar witness cube');early_cubes.append({'gate':e['gate'],'record':actual,'rows':len(outputs),'whole_rows_sha256':digest(outputs)})
    # Proved transfer corollary controls: whole function equality, not charges.
    firstswap=(Q[1],Q[0])+Q[2:];identity_extension=Q+((0,11),)
    require(boolean(firstswap)==boolean(Q),'disjoint initial reorder');require(boolean(identity_extension)==boolean(Q),'full original identity extension')
    r0,_,_=replay(Q,0,3);r1,_,_=replay(identity_extension,0,3);require(r0[4]!=r1[4],'transfer control must change D')
    # Entire unclamped literal Q, independent scalar ground outputs.
    _,literal=scalar(Q,0,0);packed=boolean(Q)
    require(all(sum((r[i]<<j) for j,r in enumerate(literal))==packed[i] for i in range(N)),'unclamped Q full scalar embedding')
    # Packed columns independently reconstruct each literal three-port function
    # and all transitions of the complete row-based closure.
    sem,edges=semigroup();c3=tuple(sum(1<<r for r in range(8) if r>>i&1) for i in range(3))
    for w,f in sem:
        x=list(c3)
        for a,b in w:x[a],x[b]=x[a]&x[b],x[a]|x[b]
        require(tuple(sum(((x[i]>>r)&1)<<i for i in range(3)) for r in range(8))==f,'semigroup full column function')
    for f,(a,b),g in edges:
        x=[sum(1<<r for r in range(8) if f[r]>>i&1) for i in range(3)];x[a],x[b]=x[a]&x[b],x[a]|x[b]
        require(tuple(sum(((x[i]>>r)&1)<<i for i in range(3)) for r in range(8))==g,'semigroup whole transition')
    positive=((0,12),(1,10),(2,9),(3,7),(5,11),(6,8),(1,6),(2,3),(4,11),(7,9),(8,10),(0,4),(1,2),(3,6),(7,8),(9,10),(11,12),(4,6),(5,9),(8,11),(10,12),(0,5),(3,8),(4,7),(6,11),(9,10),(0,1),(2,5),(6,9),(7,8),(10,11),(1,3),(2,4),(5,6),(9,10),(1,2),(3,4),(5,7),(6,8),(2,3),(4,5),(6,7),(8,9),(3,4),(5,6))
    require(len(positive)==45,'known positive size')
    pos=boolean(positive)
    require(all(sum(((pos[i]>>r)&1)<<i for i in range(N))==((1<<r.bit_count())-1)<<(N-r.bit_count()) for r in range(1<<N)),'known45 whole sorter')
    return {'rejected_semantic_damages':out,'balanced_full_functions':tailcontrols,'transfer_controls':[{'length':28,'function':digest(boolean(firstswap))},{'length':29,'function':digest(boolean(identity_extension)),'original_HIGH_pair':r1}],'Q_HIGH_pair':r0,'unclamped_Q_rows':8192,'semigroup_whole_function_controls':11,'semigroup_whole_transition_controls':33,'early_full_scalar_cubes':early_cubes,'known45_rows':8192,'known45_source':'https://bertdobbelaere.github.io/sorting_networks.html#N13L45D10'}
if __name__=='__main__':
    p=json.load(open(sys.argv[1]));c=json.load(open(sys.argv[2]));i=json.load(open(sys.argv[3]));out=test(p,c,i);open(sys.argv[4],'w').write(json.dumps(out,separators=(',',':'),sort_keys=True)+'\n');print(json.dumps({'semantic_rejections':len(out['rejected_semantic_damages']),'whole_record_sha256':digest(out)}))
