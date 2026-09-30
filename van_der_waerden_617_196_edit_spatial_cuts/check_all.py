"""Verify the four explicit spatial certificates without numerical software."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import verify

PHASES = [184,201,205,269]
BUDGETS = [196,197,198,200]


def check_directory(directory):
    paths = sorted(directory.glob('phase-*.json'))
    verify.need([p.name for p in paths] == [f'phase-{s:03d}.json' for s in PHASES],
                'Coverage must be exactly the four stated phases')
    cases = []
    digest = hashlib.sha256()
    for s,p in zip(PHASES,paths):
        raw = p.read_bytes()
        out,loads = verify.check(json.loads(raw),BUDGETS,return_loads=True)
        verify.need(out['phase'] == s,'Phase filename mismatch')
        verify.need(out['inner'] == [1287,2417],'Stated bridge')
        out['certificate_sha256'] = hashlib.sha256(raw).hexdigest()
        d,u,total = out['denominator'],out['mu_numerator'],out['sum_numerator']
        out['budget196_cut_numerator'] = total-196*u
        out['budget196_cut_value'] = str(Fraction(total-196*u,d))
        # Exactly count reference class sizes and poles on the actual interval.
        count = [0,0]
        far = [0,0]
        poles = []
        eligible = [[],[]]
        eligible_inner = [0,0]
        limit = out['conditional_far_edits_per_color']['196']
        slack = 196*u+limit*d-total
        verify.need(0<=slack<d,'Nontrivial rounded spatial slack')
        for x in range(verify.N):
            r = (x-verify.C+(s if x<verify.C else (1-s)%verify.P))%verify.P
            if r == 0:
                poles.append(x)
                continue
            c = verify.q[r]^int(x>=verify.C)
            count[c] += 1
            far[c] += int(not 1287 <= x < 2417)
            defect = u+(0 if 1287<=x<2417 else d)-loads[x]
            verify.need(defect>=0,'Nonnegative capacity defect')
            if defect<=slack:
                eligible[c].append(x)
                eligible_inner[c]+=int(1287<=x<2417)
        verify.need(count == [1849,1849] and far == [1285,1285],'Class/band size')
        out['reference_class_sizes'] = count
        out['far_reference_class_sizes'] = far
        out['poles'] = poles
        verify.need(eligible[1] == sorted(3703-x for x in eligible[0]),'Reflected eligible sets')
        out['conditional_reduction'] = {
            'hypotheses':{'class_edit_budget':196,'far_edit_budget':limit},
            'maximum_aggregate_capacity_defect':str(Fraction(slack,d)),
            'slack_numerator':slack,
            'eligible_positions_each_color':len(eligible[0]),
            'forbidden_edit_positions_each_color':1849-len(eligible[0]),
            'eligible_inner_each_color':eligible_inner[0],
            'eligible_far_each_color':len(eligible[0])-eligible_inner[0],
            'color0_eligible_set_sha256':hashlib.sha256(
                (json.dumps(eligible[0],separators=(',',':'))+'\n').encode()).hexdigest(),
            'color1_is_reflection_of_color0':True,
            'candidate_existence_established':False}
        cases.append(out)
        digest.update(f"{s}:{out['certificate_sha256']}\n".encode())
    minima = [v['conditional_far_edits_per_color']['196'] for v in cases]
    verify.need(all(a>=b for a,b in zip(minima,[55,57,56,60])),'Published conditional bounds')
    return {'agent':'six-vdw-3','role':'researcher',
            'status':'VERIFIED_FOUR_PHASE_SPATIAL_CERTIFICATES',
            'phases':PHASES,'inner':[1287,2417],'phase_count':len(cases),
            'checked_APs':sum(c['checked_APs'] for c in cases),
            'checked_incidences':sum(c['checked_incidences'] for c in cases),
            'conditional_budget_per_reference_color':196,
            'far_bounds_per_reference_color':minima,
            'uniform_far_bound_if_each_class_budget196':2*min(minima),
            'canonical_certificate_manifest_sha256':digest.hexdigest(),
            'all617_phase_exclusion_imported':False,
            'solver_trusted':False,'edit_optimality_claim':False,'cases':cases}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--directory',type=Path,default=Path(__file__).resolve().parent/'certificates')
    p.add_argument('--output',type=Path)
    args = p.parse_args()
    out = check_directory(args.directory)
    raw = json.dumps(out,sort_keys=True)+'\n'
    if args.output:args.output.write_text(raw)
    print(json.dumps({k:v for k,v in out.items() if k!='cases'}))


if __name__ == '__main__':
    main()
