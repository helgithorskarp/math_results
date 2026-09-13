from geometry51 import *

def run(tag):
 st=time.time();x=json.loads((W/f'placements_{tag}.json').read_text());b=json.loads((W/f'boundary_{tag}.json').read_text());nn=b['neighbours'];keep=[];stats=Counter()
 for i,p in enumerate(x['placements']):
  boundary=set(p['old'])
  for j in p['new']:boundary.update(nn[j])
  if len(boundary)<4:stats['boundary_under4']+=1;continue
  if all(len(nn[j])>=4 for j in p['new']):stats['old_shell']+=1;continue
  keep.append(i)
 ids=sorted({j for i in keep for j in x['placements'][i]['new']});raw=x['seed_points']+[x['new_points'][j]for j in ids];P=[(tuple(map(F,p[:4])),tuple(map(F,p[4:])))for p in raw];s=tuple(map(F,x['radicand']));print('ADMITTED',tag,'placements',len(keep),'newpoints',len(ids),'filters',dict(stats),'seconds',time.time()-st,flush=True)
 G=Geometry51(W/'sparse_geometry.so');es=G.graph(P,s,audit=True);print('PHYSICAL_HOST',tag,'vertices',len(P),'edges',len(es),'seconds',time.time()-st,flush=True)
 (W/f'host_edges_{tag}.json').write_text(json.dumps({'edges':es,'new_point_ids':ids,'placements':keep},separators=(',',':'))+'\n')
 status,colour,solverstats=solve(es,len(P),1000000);out={'tag':tag,'admitted_placements':keep,'new_point_ids':ids,'filters':dict(stats),'vertices':len(P),'edges':len(es),'edge_list':es,'status':status,'colouring':colour,'solver_stats':solverstats,'seconds':time.time()-st};(W/f'screen_{tag}.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print('HOST_COLOUR',tag,status,solverstats,'seconds',time.time()-st,flush=True)
if __name__=='__main__':run(sys.argv[1])
