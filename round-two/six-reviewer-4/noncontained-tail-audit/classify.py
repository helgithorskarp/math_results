#!/usr/bin/env python3
"""Literal positive point-isomorphism certificates for normalized forms only."""
from pathlib import Path
from collections import deque,Counter
import argparse,json,hashlib
from core import parent,pts,packing,need,canon
from transport import mul,power,image
def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args();D=parent();forms=json.loads((a.work/'NORMAL_FORMS.json').read_text())['words'];rec=json.loads((a.work/'transport-record.json').read_text());pointmap=rec['canonical_to_literal_points'];inv={v:i for i,v in enumerate(pointmap)}
 cg=[tuple(i^b if i<16 else 16 for i in range(17))for b in (1,2,4,8)]+[tuple(mul(2,i)if i<16 else 16 for i in range(17)),tuple(16 if i==0 else 0 if i==16 else power(i,14)for i in range(17)),tuple(mul(i,i)if i<16 else 16 for i in range(17))]
 gs=[tuple(pointmap[g[inv[i]]]for i in range(17))for g in cg];group={tuple(range(17))};q=deque(group)
 while q:
  h=q.popleft()
  for g in gs:
   n=tuple(g[h[i]]for i in range(17))
   if n not in group:group.add(n);q.append(n)
  need(len(group)<=2_000_000,'INCOMPLETE fixed2M point-group state guard')
 stabilizer=sorted(g+(17,)for g in group if image(15,g)==15)
 for g in stabilizer:need(sorted(g)==list(range(18))and g[17]==17 and {image(B,g)for B in D}==set(D),'every physical stabilizer witness')
 def spectrum(code):return tuple(sorted(sum(bool(w>>v&1)for w in code)for v in range(18)))
 classes={}
 for i,c in enumerate(forms):classes.setdefault(spectrum(c),[]).append(i)
 certificates=[]
 for sp,indices in sorted(classes.items()):
  base=min(indices)
  for i in indices:
   candidates=[g for g in stabilizer if sorted(image(w,g)for w in forms[base])==forms[i]]
   need(candidates,'no actual isomorphism certificate');g=candidates[0]
   need(sorted(image(w,g)for w in forms[base])==forms[i],'full69 word-image equality')
   certificates.append({'from_normal_form':base,'to_normal_form':i,'points':g})
 need(len(classes)==2 and len(certificates)==10,'exact two normalized-spectrum classes')
 raw=canon({'normal_form_isomorphisms':certificates,'classes':[{'replication_degrees':list(k),'normal_forms':v}for k,v in sorted(classes.items())]});(a.work/'ISOMORPHISMS.json').write_bytes(raw)
 # Enumerate every one-step optional contained-tail replacement. Literal
 # packing checks show that restoration preserves size, not isomorphism.
 candidates=accepted=pairchecks=0;digest=hashlib.sha256();variant_spectra=Counter();first={}
 for index,code in enumerate(forms):
  for B in sorted(set(code)&set(D)):
   for omit in pts(B):
    candidates+=1;new=(B^(1<<omit))|(1<<17)
    rest=[w for w in code if w!=B]
    if any((new&w).bit_count()>2 for w in rest):continue
    words=sorted(rest+[new]);packing(words);pairchecks+=2346;accepted+=1
    through=[w&((1<<17)-1)for w in words if w>>17&1]
    noncontained=[t for t in through if not any(t&B==t for B in D)]
    acount=len(through)-1;R=len(set(D)-set(words));need(noncontained==[15]and R==acount+4,'same exact t1 minimum-cost family')
    variant_spectra[spectrum(words)]+=1;digest.update(canon([index,B,new,words]))
    first.setdefault(spectrum(words),words)
 need(accepted>0,'nonvacuous optional restoration controls')
 examples=[]
 for sp,indices in sorted(classes.items()):examples.append({'kind':'normalized','words':forms[min(indices)],'replication_degrees':list(sp)})
 for sp,words in sorted(first.items()):examples.append({'kind':'one_optional_replacement','words':words,'replication_degrees':list(sp)})
 need(len(examples)==4 and len({tuple(e['replication_degrees'])for e in examples})==4,'four pairwise inequivalent literal examples')
 examplesraw=canon({'minimum_cost_t1_69_examples':examples});(a.work/'FOUR_CLASS_EXAMPLES.json').write_bytes(examplesraw)
 # Physical malformed witness and map controls.
 rejected=[]
 try:packing(forms[0][:-1]+[forms[0][0]])
 except RuntimeError:rejected.append('duplicate69_word')
 broken=list(stabilizer[0]);broken[0]=broken[1]
 need(sorted(broken)!=list(range(18)),'nonbijective point map detected');rejected.append('nonbijective_point_map')
 need(len(rejected)==2,'all actual malformed controls')
 print(json.dumps({'complete':True,'normal_forms':len(forms),'normalized_point_isomorphism_classes':2,'class_sizes':sorted(len(v)for v in classes.values()),'actual18_point_maps':len(certificates),'whole69_word_images_checked':690,'iso_certificate_bytes':len(raw),'iso_certificate_sha256':hashlib.sha256(raw).hexdigest(),'optional_contained_tail_candidates':candidates,'valid_one_step_variants':accepted,'literal_optional_variant_pairs':pairchecks,'entire_one_step_variant_stream_sha256':digest.hexdigest(),'one_step_variant_spectra':[{'degrees':list(k),'occurrences':v}for k,v in sorted(variant_spectra.items())],'four_actual_isomorphism_classes_lower_bound':True,'four_example_bytes':len(examplesraw),'four_example_sha256':hashlib.sha256(examplesraw).hexdigest(),'rejected_literal_controls':rejected,'all_original69_packings_classified_up_to_isomorphism':False,'no_global_endpoint_change':True},sort_keys=True))
if __name__=='__main__':main()
