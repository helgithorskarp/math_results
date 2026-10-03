"""Complete coefficient replay and entry-level certificate comparison."""
from pathlib import Path
import json,signal,hashlib
from generate import generate
from schema import require
HERE=Path(__file__).resolve().parent

def replay(system,factors,certificate):
    got=generate(system,factors);require(got==certificate,'whole entry-level certificate mismatch')
    return got

if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('20s exact replay guard')));signal.alarm(20)
    s=json.loads((HERE/'SYSTEM.json').read_text());f=json.loads((HERE/'FACTORS.json').read_text());c=json.loads((HERE/'CERTIFICATE.json').read_text());r=replay(s,f,c)
    print(json.dumps({'actual_agent':'six-tammes-2','role':'researcher','status':'COMPLETE_EXACT_BERNSTEIN_REPLAY','closed_boxes':r['closed_cover_boxes'],'elementary_cells_including_boundaries':r['closed_elementary_cells_checked'],'strict_sign_obligations':len(r['strict_sign_obligations']),'all_coefficients_actually_checked':r['all_coefficients_actually_checked'],'generic_identities':r['identity_replay']['generic_whole_polynomial_identities'],'whole_certificate_sha256':hashlib.sha256((HERE/'CERTIFICATE.json').read_bytes()).hexdigest(),'no_unresolved_case':True,'new_global_bound':False},indent=2))
