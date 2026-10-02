"""Independent domain/PSD/completeness and moment-floor semantic controls."""
from fractions import Fraction as F
from linear import need,psd,canonical,digest
from affine import family,parameters
from sparse import poly,add,scale,power,eq,y
from variance import scalar,boundary
from physical import singleton,closed_gram,key

def sharp_floor_certificate(a,g,c2,d):
 need(g>0 and c2>=0 and 0<d<=min(a,g),'moment-floor domain')
 need((a-d)*(g-d)>=c2,'exact sharp comparison-floor criterion')
 return (a-d)*(g-d)-c2

def run():
 refused=[]
 def reject(name,fn):
  try:fn()
  except(ValueError,ZeroDivisionError):refused.append(name);return
  raise ValueError('damaged hypothesis accepted: '+name)
 for name,args in [('qbelow4',(3,1)),('kzero',(4,0)),('koutside',(4,5)),('qnoninteger',(F(9,2),2))]:reject(name,lambda args=args:scalar(*args))
 reject('no new general builder',lambda:singleton(25,6));reject('no inherited allocation guard enlargement',lambda:family(24,6))
 bad=scalar(24,6);need(bad['m']<0 and 'mu'not in bad,'failed sufficient test retained')
 reject('failed variance cannot issue floor',lambda:need(bad['m']>0,'failed sufficient margin'))
 # Negative moment test can coexist with actual strict PSD; not an exclusion.
 comparison=[[F(1),F(2)],[F(2),F(1)]];actual=[[F(1),F(2)],[F(2),F(5)]]
 reject('indefinite sharp comparison',lambda:psd(comparison));positive=psd(actual);need(positive['rank']==2,'actual strict PSD despite negative sufficient test')
 need(sharp_floor_certificate(F(2),F(3),F(1),F(11,8))==F(1,64),'positive rational sharp floor')
 reject('floor above exact small eigenvalue',lambda:sharp_floor_certificate(F(2),F(3),F(1),F(7,5)))
 reject('nonpositive complement',lambda:sharp_floor_certificate(F(2),F(0),F(1),F(1)))
 oldfloor=F(15,11);need(F(11,8)>oldfloor,'specific moment-floor strict enlargement')
 samples=[];checked=0
 for k in range(5,19):
  for q in range(boundary(k)-4,6*k):
   r=scalar(q,k)
   if r['m']<=0:continue
   a=r['e']/(r['N']-1);g=F(r['g']);c2=r['h0']/(r['N']-1)
   sharp_floor_certificate(a,g,c2,r['mu']);checked+=1
   if(q,k)in[(19,5),(30,7),(92,18)]:
    low=r['mu'];high=min(a,g)
    for unused in range(24):
     mid=(low+high)/2
     if(a-mid)*(g-mid)>=c2:low=mid
     else:high=mid
    need(high-low==(min(a,g)-r['mu'])/(2**24),'complete exact bisection width')
    residual=sharp_floor_certificate(a,g,c2,low)
    samples.append({'q':q,'k':k,'a':a,'g':g,'c2':c2,'old_mu':r['mu'],'certified_rational_floor':low,'comparison_residual':residual,'upper_bracket':high,'bisection_steps':24})
 need(checked==191,'all positive closure floors agree with exact sharp moment comparison')
 r=scalar(19,5);kap=r['kappa'];threshold=F(5,2*11)*kap
 reject('open lower energy threshold cannot be closed by this proof',lambda:need((4+F(2,5))*threshold/kap<1,'strict residual'))
 reject('sharp six-deletion negative endpoint mis-signed',lambda:need(parameters(23,6)['Q0']>0,'actual all-real Q0'))
 reject('Pell root floor off by one',lambda:need(boundary(49)==270,'strict root floor'))
 reject('wrong positive cubic coefficient',lambda:eq(add(poly(4159209),scale(y,1019686),scale(power(y,2),72545),scale(power(y,3),1600)),add(poly(4159209),scale(y,1019685),scale(power(y,2),72545),scale(power(y,3),1600)),'full cubic'))
 S,Z,stars=singleton(24,6);keys=sorted(set(key(A,Z)for A in S[1:]));weights=[sum(key(A,Z)==v for A in S[1:])for v in keys]
 G=closed_gram(keys,weights,24,6,F(1,4096),F(5));a=[int(bool(m&1))for m,z,w in keys]
 need(all(sum(v*b for v,b in zip(row,a))==0 for row in G),'original closed star kernel')
 damaged=[row[:]for row in G];i=keys.index((1,0,0));damaged[i][i]+=1
 reject('changed physical diagonal breaks star kernel',lambda:need(all(sum(v*b for v,b in zip(row,a))==0 for row in damaged),'kernel'))
 reject('missing orbit norm loses full dimension',lambda:need(sum(weights[:-1])==445,'complete orthogonal space'))
 reversedG=closed_gram(keys,weights,24,6,F(1,4096),F(-5))
 reject('reversed four-edge repair no positive certificate',lambda:psd(reversedG))
 need(len(refused)>=16,'meaningful semantic damage count')
 return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','status':'PASS','semantic_rejections':refused,'positive_actual_despite_negative_moment_test':positive,'sharp_floor_toy':{'a':2,'g':3,'c2':1,'old_completed_square':oldfloor,'new_rational':F(11,8)},'all191_original_mu_pass_sharp_comparison':True,'rational_sharp_floor_samples':samples,'scope':'sharpness given only moment/complement data,not actual spectrum;24exact bisections,nofloat'}
if __name__=='__main__':
 import signal,json
 def alarm(*args):raise TimeoutError('fixed60s controls')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(60)
 print(json.dumps(canonical(run()),sort_keys=True,separators=(',',':')))
