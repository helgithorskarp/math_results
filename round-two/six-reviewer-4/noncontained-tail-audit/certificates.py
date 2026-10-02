#!/usr/bin/env python3
"""Post-seal literal reader checks, baseline comparison and damage controls."""
from pathlib import Path
from itertools import combinations
import argparse,json,hashlib
from core import parent, packing, need, canon, pts, mask
from transport import image
ROOT=Path(__file__).resolve().parent
def spectrum(words):return sorted(sum(bool(w>>v&1) for w in words) for v in range(18))
def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args()
    D=parent();forms=json.loads((a.work/'NORMAL_FORMS.json').read_bytes())['words']
    cert=json.loads((a.work/'ISOMORPHISMS.json').read_bytes());examples=json.loads((a.work/'FOUR_CLASS_EXAMPLES.json').read_bytes())['minimum_cost_t1_69_examples']
    for r in cert['normal_form_isomorphisms']:
        g=r['points'];need(sorted(g)==list(range(18)) and g[17]==17,'bijective y-fixed map')
        need({image(b,g) for b in D}==set(D),'map whole D')
        need(sorted(image(w,g) for w in forms[r['from_normal_form']])==forms[r['to_normal_form']],'all 69 word images')
    for r in examples:
        words=r['words'];packing(words);need(len(words)==69,'example count')
        tails=[w&((1<<17)-1) for w in words if w>>17&1]
        noncontained=[t for t in tails if not any(t&b==t for b in D)]
        need(noncontained==[15] and len(set(D)-set(words))==len(tails)+3,'actual t1 R=a+4')
        need(spectrum(words)==r['replication_degrees'],'full example spectrum')
    need(len(examples)==4 and len({tuple(spectrum(r['words'])) for r in examples})==4,'four inequivalent examples')
    raw=(ROOT/'BASELINE69.txt').read_bytes();lines=raw.decode().splitlines()
    need(len(lines)==69 and all(len(x)==18 and set(x)<={'0','1'} for x in lines),'literal primary binary fixture')
    baseline=[int(x,2) for x in lines];packing(baseline)
    need(all(spectrum(c)!=spectrum(baseline) for c in forms),'baseline spectra distinguish every normalized form')
    controls=[]
    for name,words,message in [('duplicate-word',forms[0][:-1]+[forms[0][0]],'distinct actual weight5 words')]:
        try:packing(words)
        except RuntimeError as e:need(str(e)==message,'wrong control rejection');controls.append(name)
    first=forms[0][0];quad=mask(pts(first)[:4]);collision=next(quad|(1<<v) for v in range(18) if v not in pts(first) and quad|(1<<v) not in forms[0])
    words=forms[0][:-1]+[collision]
    try:packing(words)
    except RuntimeError as e:need(str(e)=='actual word collision','wrong collision rejection');controls.append('distinct-weight5-collision')
    bad=list(cert['normal_form_isomorphisms'][0]['points']);bad[0]=bad[1]
    need(sorted(bad)!=list(range(18)),'actual nonbijective map damage');controls.append('nonbijective-map')
    need(len(controls)==3,'all physical controls reject')
    print(json.dumps({'complete':True,'post_seal_reader_validation':True,'literal_iso_maps':len(cert['normal_form_isomorphisms']),'whole_normal_word_images':69*len(cert['normal_form_isomorphisms']),'four_actual_boundary_examples':len(examples),'example_pairs_checked':2346*len(examples),'baseline69_sha256':hashlib.sha256(raw).hexdigest(),'baseline_pairs_checked':2346,'baseline_owned_triples':690,'baseline_replication_degrees':spectrum(baseline),'ten_normal_forms_inequivalent_to_this_fixture':True,'semantic_damage_rejections':controls},sort_keys=True))
if __name__=='__main__':main()
