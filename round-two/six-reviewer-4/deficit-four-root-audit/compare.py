#!/usr/bin/env python3
"""Optional full author-output comparison and semantic damage controls.
Actual reviewer six-reviewer-4; no author code is imported.
"""
import argparse,copy,json
from pathlib import Path
from check import need,digest
HERE=Path(__file__).resolve().parent

def compare(records,cases):
 own=json.loads((HERE/'expected.json').read_text())['records']
 need(type(records) is list and len(records)==135,'Complete raw incidence list')
 need([r['rows'] for r in records]==[r['rows'] for r in own],'Every incidence entry')
 for r in records:
  ds=[z.bit_count()-4 for z in r['rows']]
  actual=[ds] if all(own[records.index(r)]['domain_sizes']) else []
  need(r['deficit_assignments']==actual,'Every unique deficit assignment')
 need(type(cases) is list and len(cases)==41,'Complete uniquely tagged case population')
 seen=set()
 for c in cases:
  q=c['incidence_index'];need(type(q) is int and 0<=q<135 and q not in seen,'Case index or duplicate')
  seen.add(q);r=own[q]
  ds=c['deficits'];need(type(ds) is list and len(ds)==11 and all(type(x) is int for x in ds),'Exact integer deficit tags')
  need(r['deficits']==ds,'Every unique tag')
  need(all(r['domain_sizes']) and r['domain_sizes']==c['domain_sizes'],'Every actual domain size')
  domains=c['domain_masks']
  need(type(domains) is list and len(domains)==11 and all(type(s) is list and all(type(z) is int for z in s) for s in domains),'Exact integer domain data')
  need(all(len(s)==len(set(s))==size for s,size in zip(domains,r['domain_sizes'])),'Complete domain cardinality')
  need(r['domain_sha256']==digest([sorted(s) for s in domains]),'Every exact physical star domain')
 need(seen=={q for q,r in enumerate(own) if all(r['domain_sizes'])},'Every independent candidate covered')
 return {'all_135_incidence_entries_match':True,'all_41_unique_tags_match':True,'all_41_exact_domains_match':True}

def controls(records,cases):
 mutations=[]
 def missing(r,c):r.pop()
 mutations.append(('missing_incidence',missing))
 def duplicate(r,c):r[1]=r[0]
 mutations.append(('duplicate_incidence',duplicate))
 def missing_case(r,c):c.pop()
 mutations.append(('missing_case',missing_case))
 def duplicate_case(r,c):c[1]=c[0]
 mutations.append(('duplicate_case',duplicate_case))
 def false_minimum(r,c):c[:]=[s for s in c if max(s['deficits'])<=2]
 mutations.append(('false_minimum_eight',false_minimum))
 def wrong_tag(r,c):
  ds=c[0]['deficits'];b=next(i for i,d in enumerate(ds) if d);a=next(i for i,d in enumerate(ds) if not d);ds[b]-=1;ds[a]+=1
 mutations.append(('wrong_tag_preserving_total',wrong_tag))
 def wrong_star(r,c):c[0]['domain_masks'][0][0]^=1
 mutations.append(('altered_physical_star',wrong_star))
 def boolean_tag(r,c):
  ds=c[0]['deficits'];q=next(i for i,d in enumerate(ds) if d==1);ds[q]=True
 mutations.append(('boolean_deficit_tag',boolean_tag))
 rejected=[]
 for name,mutate in mutations:
  r,c=copy.deepcopy(records),copy.deepcopy(cases);mutate(r,c)
  try:compare(r,c)
  except ValueError:rejected.append(name)
  else:raise ValueError('Damaged comparison accepted: '+name)
 return rejected

def main():
 p=argparse.ArgumentParser();p.add_argument('native_output',type=Path);p.add_argument('--controls',action='store_true');a=p.parse_args()
 records=json.loads((a.native_output/'transfer14_records.json').read_text());cases=json.loads((a.native_output/'coupled14_cases.json').read_text())
 result=compare(records,cases)
 if a.controls:result['damaged_inputs_rejected']=controls(records,cases)
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
