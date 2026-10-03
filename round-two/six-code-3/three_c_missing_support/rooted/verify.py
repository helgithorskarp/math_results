"""Independent all-point-map, every20/24-word packing and full2352-bit checker."""
import argparse,copy,hashlib,itertools,json,time
from pathlib import Path
from collections import Counter
START=time.monotonic();STATES=0
def require(ok,message):
    if not ok:raise ValueError(message)
def tick():
    global STATES
    STATES += 1
    if STATES > 500000 or time.monotonic() - START > 20:
        raise RuntimeError('INCOMPLETE: original500000/20 guard')


def check_case(case,math,records,ordinal):
    tick();image=case['point_image'];a,b=case['old_C_pair'];heavy=math['fixture_heavy'];words=math['fixture_star']
    require(len(image)==17 and sorted(image)==[p for p in range(18) if p!=1] and
            image[heavy]==0 and image[a]==2 and image[b]==3,'literal normalized original point map')
    fixed=case['fixed_star'];rebuilt=sorted(sorted([1]+[image[p] for p in q]) for q in words)
    require(fixed==rebuilt and len({tuple(w) for w in fixed})==20 and
            all(len(set(w))==5 and 1 in w for w in fixed),'entire actual20-word star')
    require(all(len(set(x)&set(y))<=2 for x,y in itertools.combinations(fixed,2)),'all fixed-star intersections')
    require(sum(0 in w for w in fixed)==3 and sum(2 in w for w in fixed)==sum(3 in w for w in fixed)==5,
            'actual heavy and C-pair replications')
    require(not any({0,2}<=set(w) or {0,3}<=set(w) for w in fixed),'both actual common-missing triples through root1')
    positives={p['anchor_index']:p for p in case['positive_anchors']}
    require(len(positives)==len(case['positive_anchors']) and case['positive_anchors']==sorted(case['positive_anchors'],key=lambda p:p['anchor_index']),
            'whole positive ordered systems')
    for k,rec in enumerate(records):
        tick();added=rec['anchor'][9:]
        require(all(w in fixed for w in rec['anchor'][:9]),'all original nine anchor words retained')
        valid=all(len(set(x)&set(y))<=2 for x in added for y in fixed)
        require(math['coverage'][56*ordinal+k]==str(int(valid)) and (k in positives)==valid,
                'each full-domain bit and physical word extension')
        if valid:
            p=positives[k];full=sorted(fixed+added)
            require(p['additional_words']==added and p['full24']==full and len({tuple(w) for w in full})==24,
                    'every literal24-word certificate')
            require(all(len(set(x)&set(y))<=2 for x,y in itertools.combinations(full,2)),'all physical24-word intersections')
            tails=[set(w)-{2,3} for w in full if {2,3}<=set(w)]
            require(len(tails)==5 and sorted(p for t in tails for p in t)==[p for p in range(1,18) if p not in [2,3]],
                    'opposite pair lambda5 with only heavy0 missing')

def check_math(math,records):
    require(math['cases']==2352 and len(math['coverage'])==2352 and len(math['pair_cases'])==42,'entire42*56 domain')
    friends=math['fixture_friends'];require(len(friends)==7 and sorted(friends)==friends,'seven actual low friends')
    require([c['old_C_pair'] for c in math['pair_cases']]==[list(p) for p in itertools.permutations(friends,2)],'every ordered original LOW pair')
    for ordinal,case in enumerate(math['pair_cases']):check_case(case,math,records,ordinal)

def main():
    ap=argparse.ArgumentParser()
    for n in ['literal','dual','expected','output']:ap.add_argument('--'+n,type=Path,required=True)
    a=ap.parse_args();root=Path(__file__).parent
    expected=json.loads(a.expected.read_text());inp=json.loads((root/'INPUT.json').read_text());records=inp['records']
    source=json.loads((root/'FIXTURES.json').read_text())['stars']
    left,right=[json.loads(p.read_text()) for p in [a.literal,a.dual]];math=left['mathematics']
    require(math==right['mathematics'],'every whole pair case, map, positive certificate and2352 bits')
    common=hashlib.sha256(json.dumps(math,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    require(common==left['common_math_sha256']==right['common_math_sha256'],'whole common record digest')
    require(math['fixture_star']==source[math['fixture_index']],'actual pinned published positive fixture')
    check_math(math,records)
    rejected=[]
    damaged=copy.deepcopy(math);damaged['pair_cases'].pop()
    try:check_math(damaged,records)
    except ValueError:rejected.append('lost ordered LOW-pair case')
    else:raise ValueError('missing case survived')
    damaged=copy.deepcopy(math);damaged['pair_cases'][0]['fixed_star'].pop()
    try:check_case(damaged['pair_cases'][0],damaged,records,0)
    except ValueError:rejected.append('lost original whole star word')
    else:raise ValueError('missing original star word survived')
    positive=[(i,c) for i,c in enumerate(math['pair_cases']) if c['positive_anchors']]
    if positive:
        ordinal,case=positive[0];damaged=copy.deepcopy(math);damaged['pair_cases'][ordinal]['positive_anchors'].pop()
        try:check_case(damaged['pair_cases'][ordinal],damaged,records,ordinal)
        except ValueError:rejected.append('lost whole24-word certificate')
        else:raise ValueError('lost physical certificate survived')
    summary=[dict(old_C_pair=c['old_C_pair'],accepted_anchor_indices=[p['anchor_index'] for p in c['positive_anchors']]) for c in math['pair_cases']]
    result=dict(agent='six-code-3',role='researcher',status='COMPLETE_AUTHOR_CHECKED_FULL_C_STAR_ANCHOR_GLUE',cases=2352,
                fixture_index=math['fixture_index'],fixture_heavy=math['fixture_heavy'],fixture_friends=math['fixture_friends'],
                positive_pair_cases=len(positive),physical24_word_certificates=sum(len(c['positive_anchors']) for c in math['pair_cases']),
                whole_pair_summaries=summary,common_math_sha256=common,semantic_rejections=rejected,states=STATES,
                guard_states=500000,guard_seconds=20,imported_generic_classification_review=expected['classification_review_ref'],
                generic_classification_reexecuted=False,ordinary_bridge_formalized=False,independent_person_review=False,
                other_two_C_stars_completed=False,unrestricted_endpoint_improvement=False)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='whole_pair_summaries'},sort_keys=True))
if __name__=='__main__':main()
