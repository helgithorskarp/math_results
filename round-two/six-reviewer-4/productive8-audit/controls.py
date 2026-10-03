"""Repaired-data semantic damage against independently rebuilt full references."""
import argparse,copy,json,pathlib
from base_check import actual as base_actual,check as base_check,need
from odd_check import actual as odd_actual,check as odd_check
from binary_check import check as binary_check

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',required=True);args=ap.parse_args();w=pathlib.Path(args.work)
    base=json.load(open(w/'base.json'));odd=json.load(open(w/'odd.json'));binary=json.load(open(w/'binary.json'));B=base_actual();O=odd_actual();base_check(base,B);odd_check(odd,O);binary_check(binary,O);rejected=[]
    def reject(label,fn):
        try:fn()
        except ValueError:rejected.append(label)
        else:raise ValueError('accepted semantic damage: '+label)
    b=copy.deepcopy(base);b['fixed'][3][1]=1;reject('wrong14 phase',lambda:base_check(b,B))
    b=copy.deepcopy(base);b['remaining_original_labels'].remove(21);reject('omitted ORIGINAL21',lambda:base_check(b,B))
    b=copy.deepcopy(base);b['rows'][-1][3][-1]+=1;reject('wrong last physical marginal',lambda:base_check(b,B))
    b=copy.deepcopy(base);b['rows'].pop();reject('missing raw phase pair',lambda:base_check(b,B))
    b=copy.deepcopy(base);b['rows'][-1]=copy.deepcopy(b['rows'][0]);reject('duplicate raw phase pair',lambda:base_check(b,B))
    b=copy.deepcopy(base);b['rows'][-1][-1]-=1;reject('false final union bound',lambda:base_check(b,B))
    o=copy.deepcopy(odd);o['third_parent_phase_counts'][-1][-1][-1]+=1;reject('wrong last complete odd phase',lambda:odd_check(o,O))
    o=copy.deepcopy(odd);o['capacities'][-1][-1]+=1;reject('wrong315 capacity',lambda:odd_check(o,O))
    o=copy.deepcopy(odd);o['minimum_nonempty_phase_intersections']['5,7']=0;reject('omitted unavoidable overlap',lambda:odd_check(o,O))
    o=copy.deepcopy(odd);o['two_parent_four_H_bound']=169;reject('false169 relaxed footprint bound',lambda:odd_check(o,O))
    b=copy.deepcopy(binary);b['whole_local_controls'].pop();reject('omitted physical binary state',lambda:binary_check(b,O))
    b=copy.deepcopy(binary);b['two_parent_allocations'][0][-1]+=1;reject('wrong complete allocation row',lambda:binary_check(b,O))
    b=copy.deepcopy(binary);b['whole_local_controls'][0][-1]=not b['whole_local_controls'][0][-1];reject('false inactive-quarter coverage',lambda:binary_check(b,O))
    b=copy.deepcopy(binary);b['complete_T7_max']=169;reject('false complete chosen allocation maximum',lambda:binary_check(b,O))
    rawcases=0
    for r in (1,3,4,5,7):
        proposal=(w/f'raw-{r}-odd.bin').read_bytes();literal=(w/f'raw-{r}-physical.bin').read_bytes();need(proposal==literal,'ALL original raw phase values')
        for label,bad in (('last raw value',proposal[:-1]+bytes([(proposal[-1]+1)%256])),('omitted raw pair',proposal[:-1]),('duplicated raw pair',proposal+proposal[-1:])):
            reject(str(r)+' '+label,lambda bad=bad,literal=literal:need(bad==literal,'full physical raw pair vector'));rawcases+=1
    # Presence is not essentiality: these real originals cover all four lifts without32.
    actual_classes=[(48,6),(80,46)]
    need(all(any((6+2520*ell)%m==a for m,a in actual_classes)for ell in range(4)),'local all-H redundancy fixture')
    need(16*3!=32*3 and len({48,96})==2,'cross-type equal cofactor is allowed by ORIGINAL distinctness')
    print(json.dumps(dict(whole_positives_passed=True,rejected_count=len(rejected),semantic_damages=rejected,raw_pair_damages=rawcases,actual_presence_not_essentiality_fixture=actual_classes,actual_cross_type_equal_cofactor_allowed=[48,96]),sort_keys=True))
if __name__=='__main__':main()
