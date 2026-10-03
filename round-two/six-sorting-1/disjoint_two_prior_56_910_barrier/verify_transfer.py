"""Whole ordered function controls; deletion histories are not transferred."""
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time

from controls import operations_allow
from run_preparations import need

ROOT = Path(__file__).resolve().parent


def canonical(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def main():
    operations_allow()
    started = time.monotonic()
    prefix = json.loads((ROOT/'nested-fixture.json').read_text())['literal_prefix']
    need(len(prefix)==32 and all(0<=a<b<13 for a,b in prefix), 'Wrong actual standard P32')
    alternatives = [prefix, prefix[:26]+[prefix[27],prefix[26]]+prefix[28:], prefix+[[0,11]]]
    cols = [sum((x>>j&1)<<x for x in range(8192)) for j in range(13)]
    packed = []
    for word in alternatives:
        actual = list(cols)
        for a,b in word:
            actual[a],actual[b] = actual[a]&actual[b],actual[a]|actual[b]
        packed.append(actual)
    need(packed[0]==packed[1]==packed[2], 'Actual whole Boolean function control differs')
    s=importlib.util.spec_from_file_location('transfer_scalar',ROOT/'prior/numeric.py')
    scalar=importlib.util.module_from_spec(s);s.loader.exec_module(scalar)
    ordered=[]
    for x in range(8192):
        if x%512==0:
            operations_allow()
            need(time.monotonic()-started < 45, 'Incomplete full function transfer control; no exclusion')
        inputs=[x>>p&1 for p in range(13)]
        outputs=[scalar.simulate(inputs,word) for word in alternatives]
        need(outputs[0]==outputs[1]==outputs[2] and
             outputs[0]==[c>>x&1 for c in packed[0]], 'Actual scalar/packed ordered function differs')
        ordered.append(sum(v<<p for p,v in enumerate(outputs[0])))
    records=[scalar.family(13,word,265,1030,'transfer') for word in alternatives]
    need(records[0][2:4]==records[1][2:4]==records[2][2:4] and
         records[0][4:6]==records[1][4:6]==[26,0] and records[2][4:6]==[27,0],
         'Function equality control must have genuinely different actual internal marked costs')
    finite={'schema':'whole-ordered-P32-function-transfer-controls-v1',
            'prefix_length':32,'full_original_Boolean_inputs':8192,
            'whole_ordered_output_function_sha256':canonical(ordered),
            'column_function_sha256':canonical(packed[0]),
            'actual_comparison_lengths':[32,32,33],
            'reordered_disjoint_priors_entire_function_equal':True,
            'appended_identity_entire_function_equal':True,
            'actual_original_LOW_HIGH':[265,1030],
            'entire_actual_marked_history_control_records':records,
            'internal_D_R_history_transferred':False,
            'ordinary_corollary_hypothesis':'Any standard prefix R of length at least32 with this complete ordered Boolean function',
            'ordinary_corollary_conclusion':'No sorting extension of total size at most44, by threshold equality and replacement by the proved literal P32',
            'global_size44_exclusion_claimed':False}
    result={'agent':'six-sorting-1','role':'researcher','status':'FULL_ORDERED_FUNCTION_AND_DIFFERENT_ACTUAL_HISTORY_CONTROLS_VERIFIED',
            'finite':finite,'finite_sha256':canonical(finite),'seconds':time.monotonic()-started,
            'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    default=ROOT/'work'/('transfer-checked'+('-O' if not __debug__ else '')+'.json')
    path=Path(sys.argv[1]) if len(sys.argv)>1 else default
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':
    main()
