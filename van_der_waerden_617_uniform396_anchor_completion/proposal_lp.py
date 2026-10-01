"""Numerical proposals only; exact checking imports none of this module."""
import heapq
import math
import time
import highspy


def cover_lp(petals,rhs,n):
    columns=[[] for _ in range(n)]
    for i,row in enumerate(petals):
        for x in row:columns[x].append(i)
    starts=[0];indices=[]
    for col in columns:indices.extend(col);starts.append(len(indices))
    lp=highspy.HighsLp();lp.num_col_=n;lp.num_row_=len(petals)
    lp.col_cost_=[1.0]*n;lp.col_lower_=[0.0]*n;lp.col_upper_=[highspy.kHighsInf]*n
    lp.row_lower_=[float(b) for b in rhs];lp.row_upper_=[highspy.kHighsInf]*len(petals)
    matrix=highspy.HighsSparseMatrix();matrix.format_=highspy.MatrixFormat.kColwise
    matrix.num_col_=n;matrix.num_row_=len(petals);matrix.start_=starts;matrix.index_=indices;matrix.value_=[1.0]*len(indices)
    lp.a_matrix_=matrix;h=highspy.Highs()
    for key,value in {'threads':1,'parallel':'off','output_flag':False,'solver':'ipm','run_crossover':'on','time_limit':15.0}.items():
        if h.setOptionValue(key,value)!=highspy.HighsStatus.kOk:raise RuntimeError('Native solver option rejected')
    if h.passModel(lp)!=highspy.HighsStatus.kOk:raise RuntimeError('Native model rejected')
    start=time.monotonic();h.run();elapsed=time.monotonic()-start
    sol=h.getSolution();status=h.getModelStatus();obj=h.getObjectiveValue()
    data={'status':str(status),'objective':obj if math.isfinite(obj) else None,'seconds':elapsed,
          'value_valid':bool(sol.value_valid),'dual_valid':bool(sol.dual_valid)}
    good=status==highspy.HighsModelStatus.kOptimal and sol.value_valid and sol.dual_valid
    if not good:return None,None,data
    values=list(sol.col_value);weights=list(sol.row_dual)
    if len(values)!=n or len(weights)!=len(petals) or not all(math.isfinite(v) for v in values+weights):raise RuntimeError('Incomplete or nonfinite guide')
    return values,weights,data


def select_triples(petals,values,max_triples=20000,seconds=8,candidate_limit=2000000):
    start=time.monotonic();epsilon=1e-7
    # A violated triple cannot include a vertex with value>=1: some one of
    # its three APs misses that vertex, and that AP already has weight>=1.
    active=[i for i,p in enumerate(petals) if all(values[x]<1-epsilon for x in p) and sum(values[x] for x in p)<2-epsilon]
    incidence={}
    for i in active:
        for x in petals[i]:
            if values[x]>epsilon:incidence.setdefault(x,[]).append(i)
    adjacency={i:set() for i in active}
    for rows in incidence.values():
        group=set(rows)
        for i in rows:adjacency[i].update(group-{i})
    masks=[sum(1<<x for x in p) for p in petals];heap=[];tested=valid=violated=0;limited=False
    for i in active:
        if limited:break
        for j in sorted(x for x in adjacency[i] if x>i):
            if limited:break
            for k in sorted(x for x in adjacency[i]&adjacency[j] if x>j):
                if tested>=candidate_limit or time.monotonic()-start>=seconds:limited=True;break
                tested+=1
                if masks[i]&masks[j]&masks[k]:continue
                valid+=1;union=masks[i]|masks[j]|masks[k];bits=union;cost=0.0
                while bits:
                    bit=bits&-bits;bits-=bit;cost+=values[bit.bit_length()-1]
                if cost>=2-epsilon:continue
                violated+=1;item=(-cost,-union.bit_count(),-i,-j,-k)
                if len(heap)<max_triples:heapq.heappush(heap,item)
                elif item>heap[0]:heapq.heapreplace(heap,item)
    chosen=sorted([[-i,-j,-k] for _,_,i,j,k in heap])
    return chosen,{'active_APs':len(active),'positive_fractional_vertices':len(incidence),'triangle_candidates_tested':tested,
                   'valid_empty_intersection_triangles':valid,'violated_triangles':violated,'kept_triples':len(chosen),
                   'selection_limited':limited,'candidate_limit':candidate_limit,'seconds':time.monotonic()-start,
                   'no_mathematical_completeness_or_nonexistence_claim':True}
