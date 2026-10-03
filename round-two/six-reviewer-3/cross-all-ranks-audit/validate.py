"""Serial normal/optimized source-only reproduction and semantic damage checks."""
import copy,hashlib,json,os,pathlib,resource,subprocess,sys,tempfile,time
HERE=pathlib.Path(__file__).resolve().parent
ENV=dict(os.environ)
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):ENV[k]='1'
def run(args,positive=True):
 start=time.monotonic();p=subprocess.run([sys.executable,'-B',*args],env=ENV,capture_output=True,text=True,timeout=45)
 if (p.returncode==0)!=positive:raise ValueError('unexpected child status: '+p.stdout+p.stderr)
 return {'args':[str(x) for x in args],'seconds':time.monotonic()-start,'exit':p.returncode,'stdout':p.stdout.strip(),'positive':positive}
def damage(x,kind):
 y=copy.deepcopy(x);r=y['terminal']['labeled_cases'][0]
 if kind=='missing_case':y['terminal']['labeled_cases'].pop()
 elif kind=='fixed_color':r['known_red_rows']['sy1'].append('t2')
 elif kind=='degree':r['degrees']['t2']+=1
 elif kind=='lost_column':r['domains'][0].pop()
 elif kind=='inserted_column':r['domains'][0].append({'h':0,'word':[0]*8,'degree':0})
 elif kind=='wrong_h':r['domains'][0][0]['h']+=1
 elif kind=='lost_cut':r['cuts'][0].pop()
 else:raise ValueError('unknown damage')
 return y

def main():
 checks=[];summary={};expected=json.loads((HERE/'SUMMARY.json').read_text())
 with tempfile.TemporaryDirectory(prefix='cross-independent-') as td:
  work=pathlib.Path(td)
  # Four source-only computations, and an independent checker, in both modes.
  for opt in ([],['-O']):
   tag='O' if opt else 'normal'
   for script,key in [('audit.py','terminal'),('reductions.py','reductions'),('gap.py','gap')]:
    path=work/(tag+'-'+key+'.json');checks.append(run(opt+[str(HERE/script),'--output',str(path)]));raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=expected['full_records'][key]['sha256'] or len(raw)!=expected['full_records'][key]['bytes']:raise ValueError('entire regenerated record mismatch')
    if key=='terminal':checks.append(run(opt+[str(HERE/'check.py'),str(path)]))
    if key=='gap':
     g=json.loads(raw);rows={a:set(v) for a,v in g['rows'].items()};allv=set(rows)
     if len(rows)!=22 or len(g['all231_spines'])!=231:raise ValueError('gap full size')
     for a,ns in rows.items():
      if a in ns or any(a not in rows[b] for b in ns) or len(ns)!=g['degrees'][a]:raise ValueError('gap graph semantics')
     for spine in g['all231_spines']:
      a,b=spine['pair'];red=b in rows[a];pages=sorted(rows[a]&rows[b] if red else allv-{a,b}-rows[a]-rows[b]);color='red' if red else 'blue'
      if pages!=spine['pages'] or color!=spine['color'] or spine['cap']!=(3 if red else 6):raise ValueError('gap direct physical pages')
     if len(rows['a'])!=9 or any(len(rows[a])!=10 for a in rows['u'] if a!='a') or rows['u']!=set(('v','a','X0','X1','X2','X3','X4','X5','SX0','SX1')):raise ValueError('gap marked degrees')
   base=json.loads((work/(tag+'-terminal.json')).read_text())
   for kind in ('missing_case','fixed_color','degree','lost_column','inserted_column','wrong_h','lost_cut'):
    path=work/'damage.json';path.write_text(json.dumps(damage(base,kind)));result=run(opt+[str(HERE/'check.py'),str(path)],False);result['damage']=kind;checks.append(result)
 summary={'Python':sys.version,'native_threads':1,'serial_math_children':True,'guard_seconds_per_child':45,'checks':checks,'peak_children_rss_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'all_complete_positive_records_match':True,'damages_rejected_per_mode':7}
 out=pathlib.Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps({'children':len(checks),'maximum_child_seconds':max(c['seconds'] for c in checks),'peak_children_rss_KiB':summary['peak_children_rss_KiB'],'damages_per_mode':7}))
if __name__=='__main__':main()
