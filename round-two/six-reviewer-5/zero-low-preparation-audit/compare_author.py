"""Postseal exact native certificate comparison; imports no target helper."""
import pathlib,json,hashlib,sys
import independent as I
P=pathlib.Path(__file__).resolve().parent

def compare(source):
 source=pathlib.Path(source);raw=(source/'certificate.json').read_bytes()
 own=json.loads((P/'EVIDENCE.json').read_text());native=json.loads(raw)['result']
 fixture=json.loads((source/'fixture.json').read_text())
 I.need(fixture['literal_prefix']==own['prefix'],'whole native literal prefix')
 parent=I.parent();image=sorted({sum(row[p]<<j for j,p in enumerate(range(1,11))) for row in parent})
 I.need(image==fixture['parent_core_states'],'all136 native parent states')
 states=[tuple(bytes.fromhex(v)) for v in own['functions']]
 index={f:i for i,f in enumerate(states)}
 target_states=[]
 for e in native['states']:
  columns=e['full32_function']
  f=tuple(sum(((columns[j]>>x)&1)<<j for j in range(5)) for x in range(32))
  I.need(len(columns)==5 and all(type(c) is int and 0<=c<2**32 for c in columns),'native complete columns')
  I.need(f in index,'native full function lies in sealed complete cover')
  j=index[f];target_states.append(f)
  w=tuple((I.DEAD.index(a),I.DEAD.index(z)) for a,z in e['shortest_word'])
  I.need(all(a<z for a,z in w),'native physical orientation')
  I.need(tuple(sum(v<<q for q,v in enumerate(I.simulate([(x>>q)&1 for q in range(5)],w))) for x in range(32))==f,'every native whole representative')
  I.need(len(w)==own['shortest'][j],'every native shortest distance')
 I.need(len(target_states)==len(set(target_states))==len(states) and set(target_states)==set(states),'entire374-function equality')
 edges={(index[target_states[a]],index[target_states[z]],I.DEAD.index(g[0]),I.DEAD.index(g[1])) for a,g,z in native['transitions']}
 I.need(len(edges)==len(native['transitions']) and edges=={tuple(e) for e in own['edges']},'all446 native directed transitions')
 profiles={tuple((p,s) for p,s in a[0]):a for a in own['profiles']}
 selected={}
 for entry in native['blocked']:
  j=index[target_states[entry['state_id']]];w=entry['witness'];record=w['record']
  root=tuple((p,'L' if record[0]>>p&1 else 'H') for p in range(13) if (record[0]|record[1])>>p&1)
  I.need(root in profiles,'immutable native original domain')
  pr=profiles[root]
  I.need(record[4:6]==pr[2:4] and record[6]==0 and record[2]==0 and record[3]==sum(1<<p for p in pr[4]),'whole original native marked/deletion record')
  I.need(w['physical_port']==10 and w['imported_size']==35 and w['kind']=='TIGHT_FREE_CUT','native maximum cut hypothesis')
  I.need(all(states[j][p]>>4&1 for p in range(32) if pr[6]>>p&1),'native whole original maximum inequality')
  x=w['full_Boolean_witness'];row=parent[x];pat=I.dead_pattern(row);actual=states[j][pat]>>4&1;correct=int(x.bit_count()>=3)
  I.need(actual!=correct and (actual,correct)==(w['actual_bit'],w['sorted_bit']),'all native full wrong-rank witnesses')
  I.need(str(j) in own['exits'] and own['exits'][str(j)]['root']==[list(r) for r in root],'same full-function exit and original root')
  selected[j]=root
 I.need(set(selected)=={int(v) for v in own['exits']},'entire193 native exits')
 masks=sorted({own['profiles'][i][5] for i in own['tight_profile_indices']})
 I.need(native['activity_image_masks']==masks,'all nine whole-original activity images')
 provenance=json.loads((P/('AUTHOR_SOURCE.json' if (P/'AUTHOR_SOURCE.json').exists() else 'author-source.json')).read_text())
 pin=next(a for a in provenance['files'] if a['name']=='certificate.json')
 I.need(len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256'],'full native certificate bytes match exact source pin')
 return dict(status='ALL_NATIVE_ROWS_EDGES_CUTS_AND_DISTANCES_MATCH_SEALED_INDEPENDENT_EVIDENCE',
  full_function_rows=len(states)*32,directed_edges=len(edges),original_cut_records=len(selected),
  native_representatives=len(states),parent_states=len(image),activity_images=len(masks),
  native_certificate_sha256=hashlib.sha256(raw).hexdigest(),own_evidence_sha256=hashlib.sha256((P/'EVIDENCE.json').read_bytes()).hexdigest())

if __name__=='__main__':print(json.dumps(compare(sys.argv[1] if len(sys.argv)>1 else P/'author'),sort_keys=True))
