import concurrent.futures,json,time
from pathlib import Path
from contact_search import source_run,workdir
W=workdir()

def one(i):
 if (W/'STOP').exists():return {'source_index':i,'status':'skipped_after_candidate'}
 out=source_run(i)
 if out['tally'].get('UNSAT'):(W/'STOP').write_text(str(i)+'\n')
 return {'source_index':i,'tally':out['tally'],'seconds':out['seconds'],'groups':out['total_quadratics'],'vertices':out['vertices'],'unresolved':out['unresolved']}
if __name__=='__main__':
 st=time.time();sources=json.loads((W/'sources.json').read_text());ids=[i for i in range(len(sources))if not(W/f'result_{i}.json').exists()];results=[]
 with concurrent.futures.ProcessPoolExecutor(max_workers=2)as ex:
  for r in ex.map(one,ids):
   results.append(r);(W/'batch_status.json').write_text(json.dumps({'completed_new':results,'seconds':time.time()-st},indent=2)+'\n')
 print('BATCH_FINISHED',len(results),'seconds',time.time()-st,flush=True)
