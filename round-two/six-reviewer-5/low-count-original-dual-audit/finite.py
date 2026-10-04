"""Read untrusted compact proof vectors; independently count every energy."""
import json,sys,pathlib,hashlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from energy import F,KEYS,need,forms,plane,beta,constant_vectors
p=pathlib.Path(sys.argv[1]);data=json.loads(p.read_text())
need(type(data) is dict and set(data)=={'actual_agent','role','coordinate_order','dyadic_denominator','points','untrusted_certificate_must_be_read_by_checker'},'whole input schema')
need(data['coordinate_order']==[list(x) for x in KEYS],'all23 physical coordinate keys')
need(type(data['dyadic_denominator']) is int and data['dyadic_denominator']==256,'dyadic denominator')
need(type(data['points']) is list and len(data['points'])==33,'all33 proof points')
want=[(k,q) for k in range(8,17) for q in range(k,3*k) if 3*q*q-12*k*q+4*k*k+F(69,2)*q-14*k+F(121,4)>=0]
need(len(want)==33,'fresh complete finite coverage')
need([(x['k'],x['q']) for x in data['points']]==want,'whole coverage no omission/duplicate/order')
out=[]
for item in data['points']:
 need(set(item)=={'k','q','cap','lower','positive_weights','whole_original_affine_sum'},'whole point schema')
 k,q=item['k'],item['q'];need(type(k) is type(q) is int,'integer order/count')
 N,m,A=forms(F(q),F(k));low,cap=(list(map(F,item[x])) for x in ('lower','cap'));w=list(map(F,item['positive_weights']))
 need(len(low)==len(cap)==23 and w==[1,1],'whole original vectors/positive weights')
 need(all(x.denominator>0 and 256%x.denominator==0 for x in low+cap),'dyadic vectors')
 pl,pc=plane(A,low),plane(A,cap,True);total=[a+b for a,b in zip(pl,pc)]
 need(total==list(map(F,item['whole_original_affine_sum'])),'all untrusted supplied affine coefficients match')
 need(total[0]<0 and total[1]<0 and total[2:]==[0,0,0],'negative constant/slope, independent trade/BC cancellation')
 z=constant_vectors()[2];pz=plane(A,z);alpha=F(q*(q+1),2)+F(3*(q+1),3*q+5)
 need(pz==[0,alpha,0,0,0],'actual orientation each point')
 norms=[beta(N,m,x) for x in (low,cap,z)];need(all(b>0 for b in norms),'positive original lifted norms')
 separation=-total[0]/(norms[0]+norms[1]-total[1]*norms[2]/alpha)
 need(separation>0,'proved unrestricted-parameter spectral margin')
 out.append({'k':k,'q':q,'N':int(N),'lower_plane':list(map(str,pl)),'cap_plane':list(map(str,pc)),'sum_plane':list(map(str,total)),'lifted_norms':list(map(str,norms)),'orientation_plane':list(map(str,pz)),'endpoint_separation':str(separation),'M_separation':str(separation/(N-(3*q+4)))})
need(min(-F(x['sum_plane'][0]) for x in out)==F(2306279189,16580608),'whole constant margin census')
need(min(-F(x['sum_plane'][1]) for x in out)==F(74897067859,197197824),'whole slope margin census')
print(json.dumps({'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'coordinate_order':[list(x) for x in KEYS],'points':out},sort_keys=True,separators=(',',':')))
