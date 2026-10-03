"""Regenerate the compact six-sign certificate; stdout only."""
from pathlib import Path
import json,signal
from algebra import derive
from signs import summaries
from schema import validate
HERE=Path(__file__).resolve().parent

def generate(system,document):
    cells=validate(system);f,parts,identities=derive(document);signs=summaries(f,system)
    return {'schema_version':1,'actual_agent':'six-tammes-2','role':'researcher','status':'COMPLETE_CONDITIONAL_OUTER_CHART_CUT','closed_cover_boxes':3,'closed_elementary_cells_checked':cells,'identity_replay':identities,'strict_sign_obligations':signs,'all_coefficients_actually_checked':sum(s['coefficient_count'] for s in signs),'unresolved_cells':0,'radical_guards':{'5-12':'A5>0 and A5^2-B5^2R>0; chart equality uses B5>0.','6-8':'B6>0 and A6^2-B6^2R<0.'},'chart_equality_branch':'b*z=1: M5=1-5*t^2<=-71/125<0','new_global_bound':False,'independent_new_result_review':'pending','formalization':'unformalized'}

if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('20s exact generation guard')));signal.alarm(20)
    s=json.loads((HERE/'SYSTEM.json').read_text());f=json.loads((HERE/'FACTORS.json').read_text());print(json.dumps(generate(s,f),indent=2))
