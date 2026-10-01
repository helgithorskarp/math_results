"""Numerical proposals only; exact checking imports none of this module."""
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
