"""Controls for the new edge-addition reduction, membership relation and cut."""
import argparse
import copy
import itertools
import json
from pathlib import Path

import analyze
import verify


def require(ok, message):
    if not ok:
        raise ValueError(message)


def rejected(function, *args):
    try:
        function(*args)
    except ValueError:
        return
    raise ValueError('negative control accepted')


def contains(mask, cliques):
    return any(mask & q == q for q in cliques)


def valid_pair(s0,s1,triangles,fours):
    return not contains(s0,fours) and not contains(s1,fours) and not contains(s0&s1,triangles)


def exhaustive_controls():
    graphs = additions = subset_bounds = pair_assignments = cut_assignments = 0
    for n in range(6):
        pairs=list(itertools.combinations(range(n),2))
        for code in range(1<<len(pairs)):
            edges={p for i,p in enumerate(pairs) if code>>i&1}
            adj=[sum(1<<v for v in range(n) if tuple(sorted((u,v))) in edges) for u in range(n)]
            triangles=verify.clique_masks(n,edges,3)
            fours=verify.clique_masks(n,edges,4)
            # Literal maximum over all contained triangle-free subsets.
            tau={m:max(t.bit_count() for t in range(1<<n) if t&m==t and not contains(t,triangles))
                 for m in range(1<<n)}
            for u,v in pairs:
                if (u,v) in edges:
                    continue
                child=edges|{(u,v)}
                ct=verify.clique_masks(n,child,3)
                cq=verify.clique_masks(n,child,4)
                new3,new4=analyze.addition_obstructions(adj,u,v)
                require(set(new3)==set(ct)-set(triangles) and set(new4)==set(cq)-set(fours), 'new clique identities')
                for m in range(1<<n):
                    tc=max(t.bit_count() for t in range(1<<n) if t&m==t and not contains(t,ct))
                    vs=[w for w in range(n) if m>>w&1]
                    eb=sum(p in edges for p in itertools.combinations(vs,2))
                    ec=sum(p in child for p in itertools.combinations(vs,2))
                    require(tc<=tau[m] and ec-eb==int((m>>u&1) and (m>>v&1)), 'monotone capacity and exact edge increment')
                    require(ec+4*tc<=eb+4*tau[m]+1, 'one-addition density bound')
                    subset_bounds+=1
                if n<=4:
                    for s0 in range(1<<n):
                        for s1 in range(1<<n):
                            incremental=(valid_pair(s0,s1,triangles,fours)
                                         and not contains(s0,new4) and not contains(s1,new4)
                                         and not contains(s0&s1,new3))
                            require(incremental==valid_pair(s0,s1,ct,cq), 'exact marked relation under edge addition')
                            pair_assignments+=1
                additions+=1
            if n<=4:
                text=analyze.cut_text(n,edges)
                rows=text.splitlines()
                require(rows[0]==f'p cnf {len(pairs)} 1' and len(rows)==2, 'cut header')
                lits=list(map(int,rows[1].split()))
                require(lits[-1]==0, 'cut terminator')
                for other_code in range(1<<len(pairs)):
                    other={p for i,p in enumerate(pairs) if other_code>>i&1}
                    truth=any(not (other_code>>(abs(lit)-1)&1) for lit in lits[:-1])
                    require(truth==(not edges<=other), 'cut literal semantics')
                    if len(other)==len(edges)+1:
                        deleted=len(edges-other)
                        distance=len(edges^other)
                        require(distance==2*deleted+1, 'signed edit identity')
                        if truth:
                            require(distance>=3, 'conditional edit bound')
                    cut_assignments+=1
            graphs+=1
    return {'base_graphs_orders0_to5':graphs,'single_edge_additions':additions,
            'subset_capacity_and_density_checks':subset_bounds,'marked_pair_truth_assignments':pair_assignments,
            'cut_truth_assignments':cut_assignments}


def negative_controls(expected):
    g,c,cnf,_=expected
    bad=[]
    for field,value in [('base_uniform_density_ceiling',91),('required_density_at_b',91),
                        ('whole_degree_profile_excluded',True),('target_graph_found',1),
                        ('newly_closed_labeled_markings',1684),('conditional_cut_width',124),
                        ('edge_toggle_lower_bound_from_base_at_124_red_edges',5)]:
        x=copy.deepcopy(c);x[field]=value;bad.append(x)
    for field,value in [('valid_base_case_bits_hex','0'*35),('density_ceiling',92),('added_red_edge',[0,20])]:
        x=copy.deepcopy(c);x['family'][0][field]=value;bad.append(x)
    x=copy.deepcopy(c);x['base_cases'].pop();bad.append(x)
    x=copy.deepcopy(c);x['S1_entries'][0]['base_cover_markings']=1;bad.append(x)
    x=copy.deepcopy(c);x['S1_entries'][0]['all_triangle_free_maximizers'].pop();bad.append(x)
    x=copy.deepcopy(c);x['family'].pop();bad.append(x)
    for doc in bad:
        rejected(verify.check_data,g,doc,cnf,expected)
    cuts=[cnf.replace('231','230',1),cnf.replace(' 1\n',' 2\n',1),
          cnf.replace('-','',1),cnf+'0\n',cnf.replace(' 0\n','\n'), 'p cnf 231 1\n0\n']
    for cut in cuts:
        rejected(verify.check_data,g,c,cut,expected)
    malformed=[{'n':True,'red_edges':[]},{'n':2,'red_edges':[[0,True]]},
               {'n':2,'red_edges':[[0,1],[0,1]]},{'n':2,'red_edges':[[1,0]]},
               {'n':2,'red_edges':[[0,2]]},{'n':3,'red_edges':[[1,2],[0,1]]}]
    for doc in malformed:
        rejected(verify.parse_graph,doc)
    for u,v in [(-1,1),(0,2),(0,0),(True,1)]:
        rejected(analyze.addition_obstructions,[0,0],u,v)
    rejected(analyze.addition_obstructions,[2,1],0,1)
    return {'corrupt_certificates_rejected':len(bad),'corrupt_cuts_rejected':len(cuts),
            'malformed_graphs_rejected':len(malformed),'invalid_edge_additions_rejected':5}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args()
    expected=verify.reconstruct()
    verify.check_data(json.loads((args.work/'BASE_GRAPH.json').read_text()),
                      json.loads((args.work/'certificate.json').read_text()),
                      (args.work/'conditional_cut.cnf').read_text(),expected)
    report={'accepted':True,'exhaustive_controls':exhaustive_controls(),
            'negative_controls':negative_controls(expected)}
    with args.report.open('x') as out:
        out.write(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)


if __name__=='__main__':
    main()
