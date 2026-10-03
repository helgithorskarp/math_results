"""Credited original exact Bareiss function, defining AST unchanged."""
from bivariate import P
from exact import require

def leading_polynomial_minors(matrix):
 a=[row[:] for row in matrix];last=P(1);out=[]
 for k in range(len(a)):
  pivot=a[k][k];require(bool(pivot),'nonzero original-field leading pivot');out.append(pivot)
  for i in range(k+1,len(a)):
   for j in range(k+1,len(a)):
    num=pivot*a[i][j]-a[i][k]*a[k][j];quot=num.exact_div(last)
    require(quot is not None,'EVERY fraction-free Bareiss division exact');a[i][j]=quot
  last=pivot
 return out
