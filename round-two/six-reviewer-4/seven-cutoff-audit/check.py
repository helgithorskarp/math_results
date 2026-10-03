"""Independent physical integer energy and determinant-polynomial reader."""
import json,sys,hashlib
from pathlib import Path
from fractions import Fraction as F
from math import lcm
from exact import need,canon,polynomial_psd
from literal import rebuild,table

def bilinear(a,values,den):
 # Integer upper-triangle energy, not producer full double Fraction summation.
 d=len(values);clear=lcm(*(x.denominator for r in a for x in r));num=0
 for i in range(d):
  num+=int(a[i][i]*clear)*values[i]**2
  for j in range(i+1,d):num+=2*int(a[i][j]*clear)*values[i]*values[j]
 return F(num,clear*den**2)
def run(w,record):
 q=record['q'];need(type(q)is int and 7<=q<=27,'complete q');m=rebuild(q);W=m['weights'];kk=m['keys'];d=len(W)
 for k in ('q','N','s','weights'):need(record[k]==m[k],'actual '+k)
 need(record['keys']==list(map(list,kk)),'every actual key');need(record['forms']==[[list(map(str,r))for r in a]for a in m['forms']],'EVERY six physical form entry')
 orientation=[1 if not c else -1 if c==7 else 0 for c,z,t in kk];e=[bilinear(a,orientation,1)for a in m['forms'][:5]];need(e[0]==0 and e[1]>0 and e[2:]==[0,0,0],'independent orientation');need(record.get('orientation',list(map(str,e)))==list(map(str,e)),'whole orientation record')
 if q<27:
  need([x['q']for x in w['negative_cases']]==list(range(7,27)),'all twenty orders');case=next(c for c in w['negative_cases']if c['q']==q);need(len(record['planes'])==len(case['planes'])==len(case['weights']),'all planes retained');coeff=[F(0)]*5;mass=F(0);zeta_norm=sum(W[i]*orientation[i]**2 for i in range(d))
  for plane,weight,got in zip(case['planes'],case['weights'],record['planes'],strict=True):
   need(plane['endpoint']in ('lower','cap'),'physical endpoint');den=plane['denominator'];vals=plane['coordinates'];need(type(den)is int and den>0 and len(vals)==d and all(type(x)is int for x in vals),'whole typed original vector');energies=[bilinear(a,vals,den)for a in m['forms']];row=energies[:5]if plane['endpoint']=='lower'else[energies[-1]]+[-x for x in energies[1:5]];norm=F(sum(W[i]*vals[i]**2 for i in range(d)),den**2);weight=F(weight);need(weight>0,'positive weight');need(got==dict(endpoint=plane['endpoint'],energies=list(map(str,energies)),coefficients=list(map(str,row)),norm_squared=str(norm),weight=str(weight)),'EVERY plane energy/coefficient/norm');coeff=[a+weight*b for a,b in zip(coeff,row,strict=True)];mass+=weight*norm
  need(coeff[0]<0 and coeff[1]<=0 and coeff[2]==0 and coeff[3]==0 and coeff[4]==0,'separate independent trade/BC cancellation');need(record['dual_sum']==list(map(str,coeff)),'whole summed energy');dist=-coeff[0]/(mass-coeff[1]*zeta_norm/e[1]);dyadic=F(record['dyadic_spectral_separation']);need(0<dyadic<=dist<2*dyadic,'entire rigorous separation');need(record['spectral_separation']==str(dist)and record['orientation_norm_squared']==str(zeta_norm)and record['weighted_vector_norm_squared']==str(mass),'all quantitative separation data')
  return dict(q=q,ordered_pairs=m['pairs'],physical_form_entries=6*d*d,dual_planes=len(case['planes']),dyadic_spectral_separation=str(dyadic),original_delta_row_norm=str(m['delta_absolute_row_norm']))
 need(q==w['positive']['q']==27,'literal positive endpoint');case=w['positive'];parameters=list(map(F,[case[x]for x in ('kappa','tb','tc','sigma')]));C=[[m['forms'][0][i][j]+sum(parameters[k]*m['forms'][k+1][i][j]for k in range(4))for j in range(d)]for i in range(d)];U=[[F(m['N']*W[i]if i==j else 0)-W[i]*W[j]-C[i][j]for j in range(d)]for i in range(d)];star=[int(bool(c&1))for c,z,t in kk];s=m['s'];h=m['N']-s;lo=F(case['lower_floor']);hi=F(case['upper_floor']);P=[[F(W[i]if i==j else 0)-F(W[i]*star[i]*W[j]*star[j],s)for j in range(d)]for i in range(d)];A=[[C[i][j]-lo*P[i][j]for j in range(d)]for i in range(d)];B=[[U[i][j]-(hi*W[i]if i==j else 0)for j in range(d)]for i in range(d)];matrices=[C,U,A,B];need(record['positive_forms']==[[list(map(str,r))for r in a]for a in matrices],'EVERY complete positive/floor form');certs=[polynomial_psd(a)for a in matrices];need([r for r,p in certs]==[d-1,d,d-1,d],'independent complete spectral ranks');need([x['rank']for x in record['congruence_certificates']]==[r for r,p in certs],'all original producer ranks');need(all(sum(C[i][j]*star[j]for j in range(d))==0 for i in range(d)),'full fixed star')
 # Construct every actual empty and nonempty position independently at integer scale.
 D=m['denominator'];pd=lcm(*(x.denominator for x in parameters));scale=D*pd;members=m['members'];n=len(members);repair={}
 for a,b,t,v in [(1,2,1,1),(2,5,1,-1),(1,4,2,1),(4,3,2,-1),(2,4,3,1)]:repair[a,b]=repair[b,a]=int(parameters[t]*scale)*v
 rows=[m['row0'][i]*pd+int(parameters[0]*pd)*m['row1'][i]+sum(repair.get((a,b),0)for b in members)for i,a in enumerate(members)];empty=[scale-r for r in rows];loop=scale+sum(rows)-s*scale;M=[[loop]+empty]+[[empty[i]]+[0]*n for i in range(n)];cache={}
 for i,a in enumerate(members):
  x=((a&7).bit_count(),(a&~7).bit_count())
  for j,b in enumerate(members):
   v=0
   if not a&b:
    y=((b&7).bit_count(),(b&~7).bit_count());key=tuple(sorted((x,y)))
    if key not in cache:p0,p1=table(q,*key);t=(p0+parameters[0]*p1)*scale;need(t.denominator==1,'whole original integer lift');cache[key]=int(t)
    v=cache[key]
   M[i+1][j+1]=v+repair.get((a,b),0)
 full=[0]+members;need(all(sum(row)==h*scale for row in M),'EVERY actual M row sum');need(all(M[i][j]==M[j][i]and(not(full[i]&full[j])or M[i][j]==0)for i in range(n+1)for j in range(n+1)),'EVERY original position symmetry/intersection zero');empty_loop=F(loop,h*scale);need(str(empty_loop)==record['original_empty_M_loop'],'actual loop');key=lambda a:(a&7,(a&(((1<<7)-1)<<3)).bit_count(),(a&~((((1<<7)-1)<<3)|7)).bit_count());empty_by_key={key(a):F(empty[i],scale)for i,a in enumerate(members)};need(len(empty_by_key)==d and [str(empty_by_key[k])for k in kk]==record['original_empty_lower_rows'],'EVERY original empty orbit row');need(record['h']==h and record['whole_lower_rank']==m['N']-1 and record['whole_cap_rank']==m['N']-1 and record['unit_gap']==str(hi/h),'actual original ranks/gap');need(lo<=parameters[0]/2 and hi<=m['N']-2*s,'dependency whole-complement floors dominate')
 radius=(lo/2)/(m['delta_absolute_row_norm']+3);need(radius<parameters[0]and radius>0,'closed real box positive kappa');need(hi-lo/2>=hi/2,'box upper floor');need(all(sum(a[i][j]*star[j]for j in range(d))==0 for a in m['forms'][1:5]for i in range(d)),'every parameter change kills forced star')
 return dict(q=q,ordered_pairs=m['pairs'],physical_form_entries=6*d*d,original_M_positions=(n+1)**2,original_M_integer_scale=h*scale,whole_M_integer_bytes=len(canon(M)),whole_M_integer_sha256=hashlib.sha256(canon(M)).hexdigest(),empty_M_loop=str(empty_loop),whole_lower_rank=n,whole_cap_rank=n,unit_gap=str(hi/h),original_delta_row_norm=str(m['delta_absolute_row_norm']),closed_real_parameter_radius=str(radius),box_lower_floor=str(lo/2),box_cap_floor=str(hi/2),box_unit_gap=str(hi/(2*h)),full_determinant_polynomials=[dict(rank=r,certificate=p)for r,p in certs])
if __name__=='__main__':
 w=json.loads(Path(__file__).with_name('INPUT.json').read_text());v=run(w,json.loads(Path(sys.argv[1]).read_text()));Path(sys.argv[2]).write_bytes(canon(v));print(json.dumps(dict(complete=True,q=v['q'],pairs=v['ordered_pairs'],box=v.get('closed_real_parameter_radius'),separation=v.get('dyadic_spectral_separation'))))
