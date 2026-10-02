"""Only decodes public JSON labels; all semantic checking is in sealed triple_check."""
import pathlib,json,itertools as it,hashlib
import triple_check as t
P=pathlib.Path(__file__).resolve().parent

def inputs(folder):
 bases=json.loads((P/'BASES.json').read_text());old={r['id']:r['words'] for r in bases['classes']}
 cls=json.loads((folder/'CLASSIFICATION.json').read_text());t.need({r['class_index']:r['representative_words'] for r in cls['classes']}==old,'all eight copied prior base bytes decoded correctly')
 owners=json.loads((folder/'OWNERS_FOUR.json').read_text());colors=json.loads((folder/'COLORS_FIVE.json').read_text())
 ownercases={r['class_index']:r for r in owners['cases']};colorcases={r['class_index']:r for r in colors['cases']};t.need(set(ownercases)==set(colorcases)=={0,4,5,6,7},'exact selected case set')
 return bases,old,ownercases,colorcases

def decode(d,ownerrow,colorrow):
 items=ownerrow['owners'];owner=dict(items);t.need(len(owner)==len(items),'duplicate owner word')
 patches={}
 five=colorrow['five_blocker_word_owners'];t.need(len(dict(five))==len(five),'duplicate new word')
 for w,c in five:
  D=d['blockers'][w];t.need(D.bit_count()==5,'literal five-word carrier');t.need(w not in patches.setdefault(D,{}),'duplicate patch word');patches[D][w]=c
 for row in colorrow['conditional_recolorings']:
  deleted,w,c=row;D=sum(1<<i for i in deleted);t.need(len(set(deleted))==len(deleted)==5,'literal collision deletion labels')
  patches.setdefault(D,{})
  t.need(w not in patches[D],'duplicate patch word');patches[D][w]=c
 return owner,patches

def transport(old,domains,folder):
 maps=json.loads((folder/'POINT_MAPS.json').read_text());t.need(len(maps)==4 and {x['target_class'] for x in maps}=={0,1,2,3},'four actual transports')
 def action(w,pi):return sum(1<<pi[k] for k in range(18) if w&(1<<k))
 rows=[]
 for row in maps:
  pi=row['point_map'];target=row['target_class'];t.need(sorted(pi)==list(range(18)),'actual point bijection');source=domains[0];dest=domains[target]
  image=[action(w,pi) for w in source['base']];t.need(set(image)==set(dest['base']),'whole physical base transport');ind={w:i for i,w in enumerate(dest['base'])};labels=[ind[w] for w in image]
  changed=[]
  for w,block in source['blockers'].items():
   to=action(w,pi);expected=sum(1<<labels[i] for i in range(68) if block&(1<<i));t.need(expected==dest['blockers'][to],'whole physical blocker transport');changed.append([w,to,expected])
  rows.append({'target':target,'physical_word_blocker_transports':len(changed),'whole_transport_sha256':t.digest(changed)})
 return rows

def run(folder):
 bases,old,owners,colors=inputs(folder);domains={i:t.domain(w) for i,w in old.items()};records=[]
 for i in sorted(owners):
  own,patch=decode(domains[i],owners[i],colors[i]);records.append({'id':i,**t.audit(domains[i],own,patch)})
 return {'agent':'six-reviewer-5','role':'independent mathematical reviewer','method':'Owned triples and full-domain physical filtering, no author code imports','first_sealed_record':t.first(bases),'five_type_audits':records,'four_complete_transports':transport(old,domains,folder),'generic_sparse_bridge':'All D with |D|<=4 use field; D5 outside exact critical union use same field; every exact critical D5 has fully verified color carrier. No flat 52-million anchor enumeration.'}
if __name__=='__main__':
 raw=t.encode(run(P/'original'));(P/'independent-full-record.json').write_bytes(raw);d=json.loads(raw);print(json.dumps({'sha256':hashlib.sha256(raw).hexdigest(),'cases':d['five_type_audits'],'transports':d['four_complete_transports']},indent=2))
