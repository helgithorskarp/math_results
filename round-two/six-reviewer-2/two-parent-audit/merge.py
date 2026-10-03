"""No arithmetic generation: verify disjoint domains, concatenate whole products."""
from pathlib import Path
import hashlib,json,shutil
ALLOC=((2,5,2),(3,4,2),(4,3,2),(2,4,3),(3,3,3),(2,3,4))
def need(ok,why):
 if not ok:raise ValueError(why)
def wire(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def copy_equal(source,destination):
 if destination.exists():need(destination.read_bytes()==source.read_bytes(),'whole duplicate primitive product')
 else:shutil.copyfile(source,destination)
def capacity(root,destination):
 destination.mkdir(exist_ok=False);base=None;types=[];locals={};globalrows={};total=0;survivors=[];domain=set()
 for r in(1,4):
  for ns in ALLOC:
   child=root/('direct-'+str(r)+'-'+''.join(map(str,ns)));x=json.loads((child/'record.json').read_bytes())
   shared={k:v for k,v in x.items()if k not in('types','local_rows','global_rows','total_global_H_allocations','survivors')}
   if base is None:base=shared
   else:need(base==shared,'all complete common primitive records')
   need(len(x['types'])==1 and x['types'][0][:2]==[r,list(ns)],'exact one declared parent/count case')
   key=str(r)+'-'+''.join(map(str,ns));need(list(x['global_rows'])==[key]and key not in domain,'disjoint global case');domain.add(key)
   types+=x['types'];globalrows.update(x['global_rows']);total+=x['total_global_H_allocations'];survivors+=x['survivors']
   for row in x['local_rows']:
    k=(row[0],tuple(row[1]),row[2])
    if k in locals:need(locals[k]==row,'every shared full local record')
    else:locals[k]=row
   for p in child.glob('*.bin'):copy_equal(p,destination/p.name)
 need(len(domain)==12 and len(types)==12,'entire twelve-case domain')
 x=dict(base,types=types,local_rows=sorted(locals.values()),global_rows=globalrows,total_global_H_allocations=total,survivors=survivors)
 x['parent_populations']={int(r):{int(d):v for d,v in cols.items()}for r,cols in x['parent_populations'].items()}
 (destination/'record.json').write_bytes(wire(x)+b'\n');return x
def physical(root,destination,label):
 destination.mkdir(exist_ok=False);base=None;rows=[];phases=0;row_keys=set();digest=hashlib.sha256();counter=0
 for lo in(0,100,200,300):
  hi=lo+100;child=root/(label+'-'+str(lo));x=json.loads((child/'record.json').read_bytes())
  shared={k:v for k,v in x.items()if k not in('all_BASE_rows','BASE_raw_phases','whole_BASE_sha256','minimum_BASE_capacity','maximum_BASE_capacity','minimum_outside_need','minimum_deficit')}
  if base is None:base=shared
  else:need(base==shared,'all complete literal-phase/common-domain records')
  shapes=sorted({tuple(v[1])for v in x['completions']});need(len(shapes)==400 and x['distinct_shapes']==400,'whole shape domain400')
  need(len(x['all_BASE_rows'])==100,'exact100-shape interval')
  localhash=hashlib.sha256()
  for sid,row in enumerate(x['all_BASE_rows'],start=lo):
   need(tuple(row[0])==shapes[sid]and sid not in row_keys,'complete disjoint ordered shape');row_keys.add(sid)
   need([p[0]for p in row[3]]==x['BASE_labels'],'every original BASE family present')
   for m in x['BASE_labels']:
    p=child/('base-'+str(sid)+'-'+str(m)+'.bin');raw=p.read_bytes();need(len(raw)==4*m,'entire protected/outside phase packet')
    digest.update(raw);localhash.update(raw);copy_equal(p,destination/p.name);counter+=m
  need(localhash.hexdigest()==x['whole_BASE_sha256'],'whole interval phase correspondence')
  for p in child.glob('phases-*.bin'):copy_equal(p,destination/p.name)
  rows+=x['all_BASE_rows'];phases+=x['BASE_raw_phases']
 need(row_keys==set(range(400))and phases==counter,'exact all400 shape/all phase domains')
 x=dict(base,all_BASE_rows=rows,BASE_raw_phases=phases,whole_BASE_sha256=digest.hexdigest(),minimum_BASE_capacity=min(v[2]for v in rows),maximum_BASE_capacity=max(v[2]for v in rows),minimum_outside_need=min(v[1]for v in rows),minimum_deficit=min(v[1]-v[2]for v in rows))
 (destination/'record.json').write_bytes(wire(x)+b'\n');return x
