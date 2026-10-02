"""Late credited theorem-composition arithmetic; no local stability verifier imported."""
from fractions import Fraction as F
import json

def require(condition,label):
    if not condition:raise ValueError(label)

def build():
    e=F(1,65536)
    margins={'direct_energy_to_local':F(1,512)-60*e,
             'direct_energy_to_collar':F(1,625)-60*e,
             'same_window_within_9707':F(1,16384)-e,
             'C_upper_below_3':3-(F(8,3)+F(2,9)),
             'global_slope_89_over_32':F(826,291)-F(14,256)-F(89,32),
             'improved_rational_slope':F(89,32)-F(111,40),
             'marked_rotation_positive':1-e}
    for k,x in margins.items():require(x>0,k)
    require(margins['global_slope_89_over_32']==F(95,37248),'whole exact rational slope')
    require(F(45,8)<25<60<64,'credit stronger later energy honestly')
    return {'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','late_addendum':True,
            'credited_local_result':'REVIEW9756/0 bafkreigzow5ccipbbahscwzhmtncltl2tdq3jwbqywhk46fpfa3d2btlqu',
            'local_source_commit':'345e13e266c576620644bbbc47812b3707623dda','same_eta_endpoint':str(e),
            'strict_full_window_margins':{k:str(v) for k,v in margins.items()},
            'both_near_slope_upper_cuts_retained':True,'arbitrary_epsilon_nonnegative':True,
            'new_stability_verdict_claimed':False,'own_core_seal_changed':False,
            'proof_status':'ordinary theorem composition using reviewed9756; not a second reproduction/formalization of that local theorem'}

if __name__=='__main__':print(json.dumps(build(),sort_keys=True,indent=2))
