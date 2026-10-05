#!/usr/bin/env python3
"""Exact fixed-pair DP with interned integer tree IDs, not nested-tuple states.

This is a representation optimization of the already checked recurrence.
Legal masks use its right-child/right-ancestor rule directly; they do not
depend on the unreviewed ABC summary or a new asymptotic hypothesis.
"""
from hashlib import sha256
import json
from pathlib import Path
import resource
from time import perf_counter

from fixed_pair_join_dp import difficult_pair,rank_insertion_gaps
from kernel import boxed_occurrences,validate_permutation
from reverse_tree_merges import perfect_tree
from tree_dynamics import cartesian_shape
from publish_tree_join_v1 import barrier


class Incomplete(RuntimeError):
    pass


class Trees:
    def __init__(self,node_cap=2000000):
        self.left=[0];self.right=[0];self.size=[0];self.masks=[1]
        self.ids={};self.node_cap=node_cap

    def node(self,left,right):
        pair=(left,right)
        old=self.ids.get(pair)
        if old is not None: return old
        if len(self.left)>=self.node_cap:
            raise Incomplete('interned-node cap reached')
        new=len(self.left);self.ids[pair]=new
        self.left.append(left);self.right.append(right)
        self.size.append(1+self.size[left]+self.size[right]);self.masks.append(None)
        return new

    def legal(self,tree):
        old=self.masks[tree]
        if old is not None: return old
        n=self.size[tree];forbidden=0
        pending=[(tree,0,False,None)]
        while pending:
            t,offset,is_right,upper_right=pending.pop()
            if t==0: continue
            l,r=self.left[t],self.right[t]
            root=offset+self.size[l]
            if is_right and upper_right is not None:
                forbidden|=((1<<(upper_right-root))-1)<<(root+1)
            if l: pending.append((l,offset,False,root))
            if r: pending.append((r,root+1,True,upper_right))
        answer=((1<<(n+1))-1)&~forbidden
        self.masks[tree]=answer
        return answer

    def split(self,tree,gap):
        if tree==0:
            if gap!=0: raise RuntimeError('Invalid empty cut')
            return 0,0
        l,r=self.left[tree],self.right[tree];k=self.size[l]
        if gap<=k:
            a,d=self.split(l,gap)
            return a,self.node(d,r)
        d,b=self.split(r,gap-k-1)
        return self.node(l,d),b

    def insert(self,tree,gap):
        if not 0<=gap<=self.size[tree]: raise RuntimeError('Invalid insertion gap')
        a,b=self.split(tree,gap)
        return self.node(a,b)

    def stream(self,current):
        # No recursive closure/cache cycle retaining every previous level.
        words={0:'.'}
        for _,root in current:
            pending=[(root,False)]
            while pending:
                tree,visited=pending.pop()
                if tree in words: continue
                l,r=self.left[tree],self.right[tree]
                if visited:
                    words[tree]='('+words[l]+words[r]+')'
                else:
                    pending.append((tree,True))
                    if r not in words: pending.append((r,False))
                    if l not in words: pending.append((l,False))
        entries=sorted((i,words[tree],weight) for (i,tree),weight in current.items())
        digest=sha256()
        for i,text,weight in entries:
            digest.update((str(i)+':'+text+':'+str(weight)+'\n').encode())
        return digest.hexdigest()

    def retain(self,current):
        """Reindex only the subtree closure of current weighted states."""
        kept=Trees(node_cap=self.node_cap);mapping={0:0}
        for _,root in current:
            pending=[(root,False)]
            while pending:
                tree,visited=pending.pop()
                if tree in mapping: continue
                l,r=self.left[tree],self.right[tree]
                if visited:
                    mapped=kept.node(mapping[l],mapping[r])
                    mapping[tree]=mapped
                    kept.masks[mapped]=self.masks[tree]
                else:
                    pending.append((tree,True))
                    if r not in mapping: pending.append((r,False))
                    if l not in mapping: pending.append((l,False))
        remapped={(i,mapping[tree]):weight for (i,tree),weight in current.items()}
        if len(remapped)!=len(current):
            raise RuntimeError('Canonical reindexing merged distinct states')
        return kept,remapped


def count_join(alpha,beta,state_cap=200000,node_cap=2000000,seconds_cap=600):
    alpha=validate_permutation(alpha);beta=validate_permutation(beta)
    if len(alpha)!=len(beta): raise ValueError('Equal-length inputs required')
    m=len(alpha);gaps_a=rank_insertion_gaps(alpha);gaps_b=rank_insertion_gaps(beta)
    store=Trees(node_cap=node_cap)
    current={(0,0):1};rows=[];processed=0;maximum=1;collections=[]
    start=perf_counter()
    for total in range(2*m):
        if total%16==0: barrier()
        new={};edges={}
        for (i,tree),weight in current.items():
            j=total-i;mask=store.legal(tree)
            options=[]
            if i<m and (mask>>gaps_a[i])&1:
                options.append((i+1,gaps_a[i]))
            if j<m and (mask>>(i+gaps_b[j]))&1:
                options.append((i,i+gaps_b[j]))
            for ni,gap in options:
                edge=(tree,gap)
                child=edges.get(edge)
                if child is None:
                    child=store.insert(tree,gap);edges[edge]=child
                key=(ni,child)
                new[key]=new.get(key,0)+weight;processed+=1
        if len(new)>state_cap: raise Incomplete('DP per-level state cap reached')
        current=new;maximum=max(maximum,len(current))
        rows.append({'ranks_inserted':total+1,'states':len(current),
                     'state_weight_stream_sha256':store.stream(current)})
        if (total+1)%8==0 and len(store.left)>100000:
            before=len(store.left);gcstart=perf_counter()
            store,current=store.retain(current)
            collections.append({'ranks_inserted':total+1,'nodes_before':before,
                                'nodes_retained':len(store.left),
                                'seconds':perf_counter()-gcstart})
        if perf_counter()-start>seconds_cap: raise Incomplete('time cap reached')
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>1400000:
            raise Incomplete('conservative memory stop below fixed2GiB scope')
        if m==63 and (total+1)%16==0:
            print(json.dumps({'ranks_inserted':total+1,'states':len(current),
                              'interned_nodes':len(store.left),'seconds':perf_counter()-start}),flush=True)
    answer=sum(weight for (i,tree),weight in current.items()
               if i==m and (store.legal(tree)>>m)&1)
    return {'alpha':alpha,'beta':beta,'m':m,'valid_rank_partitions':answer,
            'states_per_level':rows,'peak_level_states':maximum,'legal_transitions':processed,
            'state_cap':state_cap,'interned_node_cap':node_cap,'interned_nodes':len(store.left),
            'seconds':perf_counter()-start,'seconds_cap':seconds_cap,
            'reachability_collections':collections}


def same(got,expected,label):
    for key in ['m','valid_rank_partitions','states_per_level','peak_level_states','legal_transitions']:
        if got[key]!=expected[key]: raise RuntimeError('Control mismatch:'+label+':'+key)


def main():
    barrier()
    root=Path(__file__).resolve().parent
    output=root/'compact_join_dp_v2.json'
    if output.exists(): raise RuntimeError('Preserve completed original; use a new version')
    start=perf_counter();controls=[]
    forward=json.loads((root/'fixed_pair_join_counts_v3.json').read_text())['family']
    transpose=json.loads((root/'reciprocal_join_probe_v1.json').read_text())['family']
    for orientation,expected_rows in [('forward',forward),('transpose',transpose)]:
        for row in expected_rows:
            expected=row if orientation=='forward' else row['transpose_count_certificate']
            got=count_join(expected['alpha'],expected['beta'])
            same(got,expected,orientation+':'+str(expected['m']))
            controls.append({'orientation':orientation,'m':expected['m'],
                             'count':got['valid_rank_partitions'],'all_level_streams_match':True,
                             'interned_nodes':got['interned_nodes'],'seconds':got['seconds']})
    literal=json.loads((root/'balanced_join_reference.json').read_text())
    literal_controls=0
    for row in literal['rows']:
        for e in row['pair_counts']:
            if count_join(e['alpha'],e['beta'])['valid_rank_partitions']!=e['valid_rank_partitions']:
                raise RuntimeError('Literal baseline mismatch')
            literal_controls+=1
    print(json.dumps({'all10_existing_family_streams_match':True,'literal_controls':literal_controls,
                      'control_seconds':perf_counter()-start}),flush=True)
    a,b=difficult_pair(6)
    if len(a)!=63 or boxed_occurrences(a) or boxed_occurrences(b):
        raise RuntimeError('Pair outside avoiding domain')
    if cartesian_shape(a)!=perfect_tree(6) or cartesian_shape(b)!=perfect_tree(6):
        raise RuntimeError('Pair outside perfect-tree domain')
    result={'actor':'literature-researcher-3','full_target_solved':False,
            'hypothesis':'forall h,alpha,beta in F_h: N(alpha,beta)*N(beta,alpha)>=2^(m_h-1)',
            'status':'started after representation controls; no complete R verdict',
            'test_scope':'P6,Q6 and transpose only; no larger census','m':63,'height':6,
            'domain_avoidance_and_shapes_checked':True,'R_bound':1<<62,
            'controls':controls,'literal_definition_controls':literal_controls,'certificates':{},
            'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'plan_sha256':sha256((root/'RECIPROCAL_JOIN_PLAN_V1.md').read_bytes()).hexdigest(),
            'representation':'canonical integer IDs; accepted blocker and split rules unchanged',
            'state_cap':200000,'interned_node_cap':2000000,'per_orientation_seconds_cap':600,
            'processes':1,'native_threads':1}
    output.write_text(json.dumps(result,indent=2)+'\n')
    for name,x,y in [('N_P_Q',a,b),('N_Q_P',b,a)]:
        barrier();print('Compact exact count '+name+' at m63',flush=True)
        try: got=count_join(x,y)
        except Incomplete as e:
            result['status']='incomplete at '+name+':'+str(e)+'; no count certified'
            result['incomplete_orientation']=name;break
        result['certificates'][name]=got;result[name]=got['valid_rank_partitions']
        output.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'orientation':name,'N':result[name],'peak_states':got['peak_level_states'],
                          'interned_nodes':got['interned_nodes'],'seconds':got['seconds']}),flush=True)
    if len(result['certificates'])==2:
        result['product']=result['N_P_Q']*result['N_Q_P'];result['R_passes']=result['product']>=result['R_bound']
        result['status']=('R refuted by exact author test; separate independent check pending'
                          if not result['R_passes'] else 'this pair passes; universal R unproved')
    result['seconds']=perf_counter()-start
    result['peak_rss_kib_linux']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in {'certificates','controls'}},indent=2))


if __name__=='__main__': main()
