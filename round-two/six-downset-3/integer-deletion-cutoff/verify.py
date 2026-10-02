"""Whole standard-library replay and freeze, with explicit optimized-mode checks."""
from pathlib import Path
import sys,json,time,resource
SOURCE=Path(__file__).resolve().parent
import source_pins
if Path(source_pins.__file__).resolve().parent!=SOURCE:raise ValueError('Wrong source-local pin helper')
source_pins.check()
import check_integer_gap as checker
sys.path.insert(0,str(SOURCE))
import cutoffs
for helper in (checker,cutoffs):
 if Path(helper.__file__).resolve().parent!=SOURCE:raise ValueError('Wrong source-local verifier helper: '+helper.__name__)
require=checker.require
def run():
 start=time.perf_counter();frozen=json.loads((SOURCE/'EXPECTED.json').read_text());saved=frozen.pop('record_sha256')
 require(checker.residual.digest(frozen)==saved,'whole expected record digest')
 require(json.loads((SOURCE/'INTEGER-GAP.json').read_text())==frozen['certificate'],'entire frozen coefficient certificate')
 actual=checker.run();require(actual==frozen['check'],'entire replayed check record equals freeze')
 # Arithmetic sanity checks join the written root bridge to the published interface.
 samples=[5,6,24,25,29,60,297,4743,75600,10**6,10**12,10**100]
 boundaries=[]
 for k in samples:
  q=cutoffs.cutoff(k)
  require(q>=max(4,k) and cutoffs.feasible(q,k) and not cutoffs.feasible(q-1,k),'exact cutoff boundary arithmetic')
  require(cutoffs.feasible(q+1,k),'exact next boundary arithmetic')
  boundaries.append({'k':str(k),'cutoff':str(q),'norm':str(cutoffs.norm(q,k))})
 source_pins.check()
 result={'agent':'six-downset-3','role':'researcher','status':'whole standard-library checks pass; ordinary proof unformalized; independent review pending','frozen_record_sha256':saved,'complete_certificate_and_check_equal':True,'mandatory_executable_closure':13,'optional_CAS_executables':2,'whole_JSON_inputs':2,'new_coefficient_counts':actual['coefficient_counts'],'complete_modular_squared_positions':actual['complete_modular_squared_positions'],'credited_finite_parent_cases':20,'semantic_damages_rejected':actual['semantic_damages_rejected'],'hash_only_damages':0,'cutoff_interface_sanity_checks_not_unbounded_proof':boundaries}
 result['record_sha256']=checker.residual.digest(result)
 (SOURCE/'RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'digest':result['record_sha256'],'frozen':saved,'seconds':time.perf_counter()-start,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
 return result
if __name__=='__main__':run()
