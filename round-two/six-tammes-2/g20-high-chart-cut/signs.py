"""Exact tensor Bernstein bounds on whole closed rational boxes."""
from fractions import Fraction as Q
from math import comb
import hashlib,json
from schema import require

def coefficients(f,box):
    require(not any(k[2] for k in f.c),'bivariate sign polynomial')
    a,b,c,d=box;n=max((k[0] for k in f.c),default=0);m=max((k[1] for k in f.c),default=0)
    first=[[Q(0) for _ in range(m+1)] for _ in range(n+1)]
    for (i,j,_),v in f.c.items():
        for r in range(i+1):first[r][j]+=v*comb(i,r)*a**(i-r)*(b-a)**r
    power=[[Q(0) for _ in range(m+1)] for _ in range(n+1)]
    for i in range(n+1):
        for j in range(m+1):
            for s in range(j+1):power[i][s]+=first[i][j]*comb(j,s)*c**(j-s)*(d-c)**s
    along_t=[[sum((power[r][j]*Q(comb(i,r),comb(n,r)) for r in range(i+1)),Q(0)) for j in range(m+1)] for i in range(n+1)]
    return [[sum((along_t[i][s]*Q(comb(j,s),comb(m,s)) for s in range(j+1)),Q(0)) for j in range(m+1)] for i in range(n+1)]

def strict(f,box,sign):
    require(sign in (-1,1),'specified strict sign')
    rows=coefficients(f,box)
    require(all(sign*v>0 for row in rows for v in row),'a closed-endpoint Bernstein coefficient is not strict')
    return rows

def obligations(f,system):
    rows={x['name']:tuple(map(Q,x['box'])) for x in system['closed_cover']}
    ta,tb=map(Q,system['t_interval']);za,zb=map(Q,system['excluded_z_interval'])
    return [('L5-all',f['L5'],(ta,tb,za,zb),1),('Z-upper-t',f['Z'],rows['upper-t'],1),('Z-upper-z',f['Z'],rows['upper-z'],1),('M6-lower-corner',f['M6'],rows['lower-corner'],1),('H10-lower-corner',f['H10'],rows['lower-corner'],-1),('H12-lower-corner',f['H12'],rows['lower-corner'],1)]

def summaries(f,system):
    answer=[]
    for name,p,box,sign in obligations(f,system):
        co=strict(p,box,sign);vals=[v for row in co for v in row]
        encoded=(json.dumps([[str(v) for v in row] for row in co],separators=(',',':'))+'\n').encode()
        answer.append({'name':name,'box':list(map(str,box)),'sign':sign,'coefficient_count':len(vals),'coefficient_min':str(min(vals)),'coefficient_max':str(max(vals)),'whole_coefficient_array_sha256':hashlib.sha256(encoded).hexdigest()})
    return answer
