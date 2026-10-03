"""Eight semantic certificate damage checks. Timeout/guard is not rejection."""
from pathlib import Path
import copy,json,sys,signal,time,resource
from check import verify,require

def alter_interior(c):
    p=c['fields']['comparison']['numerator'];a={tuple(e):int(v) for e,v in p['terms']};d=p['denominator']
    for e,v in (((1,1),1),((1,0),-4),((0,1),-2),((0,0),8)):a[e]=a.get(e,0)+v*d
    p['terms']=[[list(e),str(v)] for e,v in sorted(a.items()) if v]
def main():
    def alarm(a,b):raise TimeoutError('unchanged60s semantic certificate controls')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    c=json.loads(Path('CERTIFICATE.json').read_text());mutations=[]
    x=copy.deepcopy(c);x['domain']='h>=2 only';mutations.append(('omitted_q_domain',x))
    x=copy.deepcopy(c);del x['fields']['comparison'];mutations.append(('omitted_active_comparison',x))
    x=copy.deepcopy(c);p=x['fields']['comparison']['numerator'];p['terms'][0][1]=str(-int(p['terms'][0][1]));mutations.append(('changed_complete_comparison',x))
    x=copy.deepcopy(c);alter_interior(x);mutations.append(('interior_only_perturbation_agrees_on_both_boundaries',x))
    x=copy.deepcopy(c);p=x['fields']['c0']['numerator'];p['terms'][0][1]=str(int(p['terms'][0][1])+p['denominator']);mutations.append(('changed_mean_bound',x))
    x=copy.deepcopy(c);x['fields']['comparison']['denominator_factors'][0]['factor']={'denominator':1,'terms':[[[0,0],'-2'],[[1,0],'1']]};mutations.append(('zero_boundary_pole',x))
    x=copy.deepcopy(c);x['fields']['comparison']['denominator_factors'][0]['power']+=1;mutations.append(('wrong_pole_power',x))
    x=copy.deepcopy(c);x['fields']['comparison']['numerator']['terms'].pop();mutations.append(('omitted_last_comparison_coefficient',x))
    out=[]
    for name,x in mutations:
        try:verify(x)
        except ValueError as exc:
            message=str(exc);require('guard' not in message and 'bound' not in message,'operational stop is not semantic damage rejection')
            out.append({'damage':name,'rejected':True,'reason':message})
        else:raise ValueError('semantic damage was accepted: '+name)
    signal.alarm(0);work=Path(__file__).resolve().parent/'work';work.mkdir(exist_ok=True)
    (work/f'damages-O{sys.flags.optimize}.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'COMPLETE eight semantic damages rejected','rejections':len(out),'seconds':time.monotonic()-start,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'optimized':sys.flags.optimize}),flush=True)
if __name__=='__main__':main()
