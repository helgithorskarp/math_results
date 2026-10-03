"""Literal control for the ordinary distinct-cofactor three-pair capacity141."""
from math import lcm
import json

def require(test,message):
    if not test:raise ValueError(message)

P=[(8,0),(9,0),(10,1),(14,1),(12,10)]
pairs=[(1,3),(5,15),(7,21)]
require(len({d for pair in pairs for d in pair})==6 and all(315%d==0 for pair in pairs for d in pair),'Original three-pair cofactor inventory differs')
require(sum(315//lcm(*pair) for pair in pairs)==141,'Ordinary141 arithmetic control differs')
H2=set(range(2,2520,24));H4=set(range(4,2520,120));H6=set(range(86,2520,168))
H=H2|H4|H6
require([len(H2),len(H4),len(H6)]==[105,21,15] and len(H)==141,'Abstract three-parent demand differs')
require(all(all(x%n!=a for n,a in P) for x in H),'Abstract demand intersects P')
classes=[(16,2),(48,26),(80,4),(240,124),(112,86),(336,254)]
require(len({n for n,a in classes})==6,'Repeated original16d label')
lifts={x+2520*j for x in H for j in range(4)}
covered={x for n,a in classes for x in range(a,10080,n)}
require(len(lifts)==564 and lifts<=covered and all(any(x%n==a for x in lifts) for n,a in classes),'Six-original abstract repair incomplete/unproductive')
bad=[(n,2 if n==48 else a) for n,a in classes]
badcover={x for n,a in bad for x in range(a,10080,n)}
require(len(lifts-badcover)==210,'Same-half16 repair damage not detected')
Pcover={x for n,a in P for x in range(a,10080,n)}
left=len(set(range(10080))-Pcover-covered)
require(left>0,'Abstract141 control incorrectly became full cover')
print(json.dumps({'agent':'six-covering-3','role':'researcher','status':'PRIVATE_LITERAL_CONTROL_FOR_ORDINARY_THREE_PAIR_BOUND',
 'original_cofactor_pairs':[list(x) for x in pairs],'ordinary_upper':141,
 'abstract_parent_holes':[105,21,15],'abstract_holes':141,'abstract_lifts':564,
 'abstract_six_original_classes':[list(x) for x in classes],'same_half16_damage_uncovered_lifts':210,
 'P_plus_six_uncovered_physical_points':left,'completed_BASE_H_witness_claimed':False,
 'exhaustive_matching_table_computed':False,'general_bound_requires_written_case_proof':True,
 'generic_priority_claimed':False,'external_review':False},indent=2))
