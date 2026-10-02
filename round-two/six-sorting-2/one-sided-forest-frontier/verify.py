"""Standalone numeric original-cube/forest/free-cut checker.

Imports only the separately credited numeric primitives. No producer, profile,
old exclusion certificate or solver is imported. Universal bridges are written
in PROOF.md; finite projection checks do not enumerate preparation functions.
"""
from collections import Counter,deque
from copy import deepcopy
import hashlib,json,resource,time
from itertools import combinations,product
from pathlib import Path
import numeric_primitives as v

ROOT=Path(__file__).resolve().parent
N19=[[0,11],[1,7],[2,4],[3,5],[8,9],[10,12],[0,2],[3,6],[4,12],[5,7],[8,10],[0,8],[1,3],[2,5],[4,9],[6,11],[7,12],[0,1],[2,10]]
INITIAL_LOW=((1,7),(2,7),(3,5),(4,6),(6,5),(8,6))
INITIAL_HIGH=((3,5),(5,6),(6,5),(7,6),(9,6),(10,6),(11,7))
POST_LOW=((1,7),(2,7),(3,6),(4,6),(8,6))
POST_HIGH=((5,6),(6,6),(7,6),(9,6),(10,6),(11,7))
RETAINED=[('LOW',0),('LOW',1),('LOW',2),('HIGH',3),('HIGH',4),('HIGH',6),('HIGH',12),('HIGH',21),('HIGH',22),('HIGH',24),('HIGH',26),('HIGH',30),('HIGH',31),('HIGH',33),('HIGH',36),('HIGH',37),('HIGH',38)]

def fixture_check(f):
    v.need(f['n']==13 and f['size_budget']==44,'wrong native size budget')
    v.need(f['imported_S11_lower_bound']==35,'wrong imported lower bound')
    v.need(f['prefix19']==N19 and f['maximum_word']==[[9,11],[11,12]] and f['joint_gate']==[3,6],'wrong literal H21 or J')
    for name,pin in f['primitive_sha256'].items():
        v.need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==pin,'primitive source provenance differs')
    for gate in f['control11']:
        v.need(len(gate)==2 and 0<=gate[0]<gate[1]<11,'invalid positive control gate')
    v.need(len(f['control11'])==35,'wrong positive control size')

def first_one_sided_control(initial):
    """Complete ZERO-profile closure and all first one-sided binary edges."""
    start=(*initial,False);seen={start};queue=deque([start]);first=set();pending=[set(),set()]
    gates=list(combinations(range(1,12),2));zero_edges=0;first_edges=0
    while queue:
        lo,hi,jdone=state=queue.popleft();profiles=(lo,hi)
        v.need(tuple(map(v.mass,profiles))==(448,448),'zero closure changes mass')
        for gate in gates:
            new=(v.passage(lo,gate,False),v.passage(hi,gate,True));weights=tuple(map(v.mass,new))
            hits=[len(set(gate)&{p for p,_ in a}) for a in profiles]
            v.count('zero_closure_next_gates')
            v.need(min(weights)>=448,'ordinary mass decreased')
            if max(weights)>512:continue
            joint=not jdone and gate==(3,6)
            if weights==(448,448):
                if not jdone and not joint:v.need(not set(gate)&{3,6},'pre-first zero gate enters future J')
                child=(*new,jdone or joint)
                if child!=state:
                    zero_edges+=1
                    if child not in seen:seen.add(child);queue.append(child)
                continue
            strict=[k for k in range(2) if weights[k]>448]
            if len(strict)!=1 or hits[strict[0]]!=2:continue
            k=strict[0];first_edges+=1;first.add(weights)
            v.need(weights[k]==512,'one-sided first binary event does not saturate')
            if not jdone:
                v.need(not set(gate)&{3,6},'one-sided first binary gate enters shared J support')
                pending[k].add(new[k])
    v.need(first=={(448,512),(512,448)},'first one-sided binary mass pairs differ')
    pending_count=0;pending_gates=0
    for high,seeds in enumerate(pending):
        seen_pending=set(seeds);todo=list(seeds)
        while todo:
            a=todo.pop();v.need(v.mass(a)==512 and dict(a)[3]==dict(a)[6]==5,'pending J profile differs')
            for gate in gates:
                b=v.passage(a,gate,bool(high));pending_gates+=1
                if v.mass(b)>512:continue
                if set(gate)&{3,6}:
                    v.need(gate==(3,6),'saturated selected side permits non-J shared touch')
                    continue
                if b not in seen_pending:seen_pending.add(b);todo.append(b)
        pending_count+=len(seen_pending)
    return {'zero_profiles':len(seen),'nonidentity_zero_edges':zero_edges,'one_sided_first_binary_edges':first_edges,
            'first_one_sided_mass_pairs':[list(p) for p in sorted(first)],
            'saturated_pending_J_profiles':pending_count,'pending_J_next_gate_controls':pending_gates}

def chosen_family_control(profile,high):
    """Necessary selected-family projection; other-family operations unrestricted."""
    seen={profile};todo=[profile];terminals=set();edges=0;gates=tuple(combinations(range(1,12),2))
    while todo:
        state=todo.pop();old=v.mass(state);support={p for p,_ in state}
        v.need(old in (448,512),'selected mass outside its two states')
        if len(state)==1:terminals.add(state)
        for gate in gates:
            child=v.passage(state,gate,high);weight=v.mass(child);hit=len(set(gate)&support)
            v.count('selected_family_next_gates')
            if weight>512 or (old==448 and weight>448 and hit!=2):continue
            v.need(hit in (0,2),'admissible selected event is a singleton')
            v.need({p for p,_ in child}<=support,'selected support resurrects a port')
            if child==state:v.need(hit==0,'selected identity touches future support');continue
            edges+=1
            if child not in seen:seen.add(child);todo.append(child)
    v.need(terminals=={((11 if high else 1,9),)},'selected terminal differs')
    return {'states':len(seen),'nonidentity_edges':edges,'terminals':len(terminals)}

def words_check(data,lo,hi):
    words=data['family_words'];v.need(set(words)=={'LOW','HIGH'},'missing selected family')
    for side,profile,high,total,gates in [('LOW',lo,False,9,4),('HIGH',hi,True,45,5)]:
        family=words[side]
        v.need(len(family)==total and len({v.digest(w) for w in family})==total,'missing or duplicate genealogy')
        support=sorted(p for p,_ in profile)
        functions=set()
        for word in family:
            state=profile
            v.need(len(word)==gates,'wrong genealogy gate count')
            for gate in word:
                v.need(len(gate)==2 and 0<=gate[0]<gate[1]<13,'invalid standard genealogy gate')
                v.need(set(gate)<={p for p,_ in state},'genealogy event is not binary')
                state=v.passage(state,gate,high)
                v.need(v.mass(state)<=512,'genealogy exceeds ordinary ceiling')
            v.need(state==((11 if high else 1,9),),'genealogy terminal differs')
            functions.add(v.full_family_function(word,support))
        v.need(functions==v.forest_cover(profile,high),'declared genealogy functions do not cover bottom-up forests')

def initial_image(prefix):
    image=set()
    for x in range(8192):
        row=v.simulate([x>>q&1 for q in range(13)],prefix)
        image.add(tuple(row));v.count('H21_original_Boolean_assignments')
    v.need(len(image)==246,'complete H21 Boolean image differs')
    return sorted(image)

def roots_check(data,f,image):
    roots=data['roots'];v.need(len(roots)==54,'missing literal root')
    cases=[(s,i,w) for s in ['LOW','HIGH'] for i,w in enumerate(data['family_words'][s])]
    results={}
    for root,(side,index,word) in zip(roots,cases):
        v.need(root['id']==len(results) and root['side']==side and root['genealogy']==index and root['word']==word,'literal root binding differs')
        prefix=f['prefix19']+f['maximum_word']+[f['joint_gate']]+word
        length=26 if side=='LOW' else 27
        v.need(root['prefix_length']==length and len(prefix)==length,'wrong prefix length')
        v.need(root['remaining_budget']==44-length,'wrong remaining gate budget')
        v.need(root['prefix_sha256']==v.digest(prefix),'prefix fingerprint differs')
        held=[0,1,12] if side=='LOW' else [0,11,12]
        core=list(range(2,12)) if side=='LOW' else list(range(1,11))
        v.need(root['held_physical_ports']==held and root['physical_core_ports']==core,'physical core route differs')
        projected=set()
        for row in image:
            out=v.simulate(row,[f['joint_gate']]+word);ordered=sorted(row)
            v.need(all(out[q]==ordered[q] for q in held),'held original rank differs')
            projected.add(sum(out[q]<<j for j,q in enumerate(core)))
            v.count('one_sided_complete_image_assignments')
            v.count('one_sided_complete_image_gate_evaluations',1+len(word))
        projected=sorted(projected)
        v.need(root['image_size']==len(projected) and root['image_sha256']==v.digest(projected),'whole ten-core image differs')
        results[root['id']]=(prefix,projected)
    return results

def obstruction_check(e,prefix):
    lo,hi=e['original_masks'];family=e['original_family']
    v.need((lo|hi).bit_count()==2 and not lo&hi,'invalid two-marked original domain')
    v.need((family,lo.bit_count(),hi.bit_count()) in [('LOW',2,0),('HIGH',0,2),('MIXED',1,1)],'original family differs')
    record=v.family(13,prefix,lo,hi,'selected_original')
    v.need(record==e['record'],'whole original deletion record differs')
    pruned=v.pruning(13,prefix,record)
    v.need(pruned==e['pruning'],'whole carrier function differs')
    c=record[4]+record[5]
    if e['kind']=='DELETION_COST_GE10':
        v.need(c>=10 and e['total_lower_bound']==35+c,'direct deletion threshold differs')
        return
    v.need(e['kind']=='TIGHT_FREE_CUT' and c==9,'tight original deletion cost differs')
    q=e['physical_free_port'];free_ports=pruned['output_free_wires']
    v.need(q in free_ports,'cut port is marked')
    template,free=v.template(13,lo,hi)
    for x in range(2048):
        row=list(template)
        for j,p in enumerate(free):row[p]=x>>j&1
        out=v.simulate(row,prefix)
        v.need(all(out[p]<=out[q] if p<q else out[q]<=out[p] for p in free_ports if p!=q),'whole original free-cut inequality fails')
        v.count('selected_cut_original_assignments');v.count('selected_cut_gate_evaluations',len(prefix))
    witness=e['global_Boolean_witness'];v.need(isinstance(witness,int) and 0<=witness<8192,'invalid Boolean witness')
    row=[witness>>p&1 for p in range(13)];actual=v.simulate(row,prefix);ordered=sorted(row)
    v.need(actual[q]==e['actual_bit'] and ordered[q]==e['sorted_bit'] and actual[q]!=ordered[q],'global rank witness differs')

def exclusions_check(data,targets,results):
    ex=data['exclusions'];v.need(len(ex)==37 and len({e['root_id'] for e in ex})==37,'missing or duplicate selected exclusion')
    for e in ex:
        v.need(e['root_id'] in results,'unbound exclusion root')
        obstruction_check(e,results[e['root_id']][0])
    excluded={e['root_id'] for e in ex};retained=[r for r in data['roots'] if r['id'] not in excluded]
    v.need(data['retained_root_ids']==[r['id'] for r in retained],'retained complement differs')
    v.need([(r['side'],r['genealogy']) for r in retained]==RETAINED,'necessary residual frontier differs')
    v.need(len(targets['targets'])==17,'missing exact residual target')
    for root,target in zip(retained,targets['targets']):
        v.need({k:target[k] for k in root}==root and target['core_states']==results[root['id']][1],'whole residual target differs')
    return Counter(e['kind'] for e in ex)

def cut_controls():
    rows=gates=0
    for row in product(range(3),repeat=5):
        if not all(row[p]<=row[2] if p<2 else row[2]<=row[p] for p in [0,1,3,4]):continue
        rows+=1
        for gate in combinations(range(5),2):
            out=v.simulate(row,[gate]);gates+=1
            if 2 in gate:v.need(out==list(row),'incident cut control is not identity')
            else:v.need(out[2]==row[2] and all(out[p]<=out[2] if p<2 else out[2]<=out[p] for p in [0,1,3,4]),'avoid-cut control breaks invariant')
    return {'abstract_ternary_cut_rows':rows,'abstract_ternary_cut_gates':gates}

def positives(f,data,results):
    for x in range(2048):
        row=[x>>p&1 for p in range(11)]
        v.need(v.simulate(row,f['control11'])==sorted(row),'positive S11 sorter fails')
        v.count('positive_sorter_assignments')
    for rid in [0,9]:
        root=data['roots'][rid];core=root['physical_core_ports'];tail=[]
        for j in range(1,len(core)):
            for k in range(j,0,-1):tail.append([core[k-1],core[k]])
        prefix=results[rid][0]
        for x in range(8192):
            row=[x>>p&1 for p in range(13)]
            v.need(v.simulate(row,prefix+tail)==sorted(row),'larger native positive sorter fails')
            v.count('positive_sorter_assignments')

def rejects(test,message,label):
    try:test()
    except ValueError as error:
        v.need(message in str(error),'damaged control rejected for unintended reason: '+label+' -> '+str(error))
        return label
    raise ValueError('damaged control accepted: '+label)

def damages(f,data,targets,results,image,lo,hi):
    out=[]
    a=deepcopy(f);a['size_budget']=45;out.append(rejects(lambda:fixture_check(a),'wrong native size budget','wrong total budget'))
    a=deepcopy(f);a['imported_S11_lower_bound']=34;out.append(rejects(lambda:fixture_check(a),'wrong imported lower bound','wrong imported size'))
    a=deepcopy(f);a['joint_gate']=[3,5];out.append(rejects(lambda:fixture_check(a),'wrong literal H21 or J','wrong J'))
    a=deepcopy(data);a['family_words']['LOW'][1]=a['family_words']['LOW'][0];out.append(rejects(lambda:words_check(a,lo,hi),'duplicate genealogy','duplicate family word'))
    for field,value,message,label in [('prefix_length',25,'wrong prefix length','wrong front length'),('remaining_budget',19,'wrong remaining gate budget','wrong remainder'),('image_sha256','0'*64,'whole ten-core image differs','wrong full image')]:
        a=deepcopy(data);a['roots'][0][field]=value
        out.append(rejects(lambda:roots_check(a,f,image),message,label))
    a=deepcopy(data);a['roots'].pop();out.append(rejects(lambda:roots_check(a,f,image),'missing literal root','missing root'))
    a=deepcopy(data);a['exclusions'].pop();out.append(rejects(lambda:exclusions_check(a,targets,results),'missing or duplicate selected exclusion','missing selected exclusion'))
    e=next(e for e in data['exclusions'] if e['kind']=='TIGHT_FREE_CUT');prefix=results[e['root_id']][0]
    a=deepcopy(e);a['record'][4]+=1;out.append(rejects(lambda:obstruction_check(a,prefix),'whole original deletion record differs','wrong D'))
    a=deepcopy(e);a['record'][6]^=1;out.append(rejects(lambda:obstruction_check(a,prefix),'whole original deletion record differs','wrong identity mask'))
    a=deepcopy(e);a['physical_free_port']=(a['record'][2]|a['record'][3]).bit_length()-1;out.append(rejects(lambda:obstruction_check(a,prefix),'cut port is marked','marked cut port'))
    a=deepcopy(e);a['global_Boolean_witness']=0;out.append(rejects(lambda:obstruction_check(a,prefix),'global rank witness differs','wrong Boolean witness'))
    a=deepcopy(e);a['pruning']['input_to_output_wire'][0]=a['pruning']['input_to_output_wire'][1];out.append(rejects(lambda:obstruction_check(a,prefix),'whole carrier function differs','wrong carrier permutation'))
    # Valid original LOW5 has the SAME final tags/D9/R0 as LOW40, but not its min.
    e=next(e for e in data['exclusions'] if data['roots'][e['root_id']]['side']=='LOW' and data['roots'][e['root_id']]['genealogy']==3)
    prefix=results[e['root_id']][0];a=deepcopy(e);a['original_masks']=[5,0]
    a['record']=v.family(13,prefix,5,0,'semantic_damage_original');a['pruning']=v.pruning(13,prefix,a['record'])
    v.need(a['record'][2:6]==e['record'][2:6],'semantic damage does not preserve tag/cost premise')
    out.append(rejects(lambda:obstruction_check(a,prefix),'whole original free-cut inequality fails','same-tag different original function'))
    a=deepcopy(targets);a['targets'][0]['core_states'][0]^=1
    root=data['roots'][a['targets'][0]['id']]
    out.append(rejects(lambda:v.need(a['targets'][0]['core_states']==results[root['id']][1],'whole residual target differs'),'whole residual target differs','wrong literal residual target'))
    return out

def main():
    start=time.monotonic();f=json.loads((ROOT/'fixture.json').read_text());data=json.loads((ROOT/'certificate.json').read_text());targets=json.loads((ROOT/'targets.json').read_text())
    fixture_check(f)
    v.need(data['n']==13 and data['size_budget']==44,'certificate size budget differs')
    v.need(data['fixture_sha256']==hashlib.sha256((ROOT/'fixture.json').read_bytes()).hexdigest(),'fixture binding differs')
    h21=f['prefix19']+f['maximum_word'];lo=v.ordinary_initial(h21,False);hi=v.ordinary_initial(h21,True)
    v.need((lo,hi)==(INITIAL_LOW,INITIAL_HIGH),'whole original ordinary inventories differ')
    first=first_one_sided_control((lo,hi));lo=v.passage(lo,(3,6),False);hi=v.passage(hi,(3,6),True)
    v.need((lo,hi)==(POST_LOW,POST_HIGH),'post-J inventories differ')
    selected={'LOW':chosen_family_control(lo,False),'HIGH':chosen_family_control(hi,True)}
    words_check(data,lo,hi);image=initial_image(h21);results=roots_check(data,f,image)
    kinds=exclusions_check(data,targets,results);abstract=cut_controls();positives(f,data,results)
    metrics=deepcopy(v.METRICS);damage_list=damages(f,data,targets,results,image,lo,hi)
    print(json.dumps({'agent':'six-sorting-2','role':'researcher','status':'COMPLETE_ONE_SIDED54_TO17_FRONTIER_AND37_ORIGINAL_CUTS_VERIFIED',
      'fronts':54,'excluded':37,'retained':17,'obstruction_kinds':dict(kinds),
      'retained_genealogies':[list(x) for x in RETAINED],'first_event_controls':first,'selected_family_controls':selected,
      'abstract_free_cut_controls':abstract,'metrics_before_damages':metrics,'damaged_controls_rejected':damage_list,
      'certificate_sha256':hashlib.sha256((ROOT/'certificate.json').read_bytes()).hexdigest(),
      'targets_sha256':hashlib.sha256((ROOT/'targets.json').read_bytes()).hexdigest(),
      'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      'boundary':'Same-author distinct algorithms, no external review/formalization. Universal one-sided commutation/free-cut bridges and S11>=35 are imported or written ordinary mathematics.'},sort_keys=True))

if __name__=='__main__':main()
