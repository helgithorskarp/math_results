"""Actual positive RUP kernels and semantically corrupted proof controls."""
import hashlib
import json
from pathlib import Path
import tempfile

from strict_rup import verify


def need(ok, message):
    if not ok:
        raise ValueError(message)


if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    cnf = 'p cnf 2 4\n1 2 0\n-1 2 0\n1 -2 0\n-1 -2 0\n'
    proof = '5 2 0 1 2 0\n6 -2 0 3 4 0\n7 0 5 6 0\n'
    deletion_proof = '5 2 0 1 2 0\n6 -2 0 3 4 0\n6 d 1 2 0\n7 0 5 6 0\n'
    mutations = [
        ('nonfresh_addition', proof.replace('5 2', '4 2', 1), 'addition ID is not fresh and increasing'),
        ('outside_actual_literal', proof.replace('5 2', '5 3', 1), 'proof literal outside domain'),
        ('missing_terminator', proof.replace('5 2 0 1 2 0', '5 2 1 2 0'), 'addition needs two terminators'),
        ('wrong_actual_unit', proof.replace('5 2 0', '5 1 0', 1), 'addition has no checked propagation contradiction'),
        ('unknown_actual_hint', proof.replace('5 2 0 1 2 0', '5 2 0 999 2 0'), 'unknown or deleted hint clause'),
        ('negative_RAT_hint', proof.replace('5 2 0 1 2 0', '5 2 0 -1 2 0'), 'RAT hints are unsupported'),
        ('nonunit_initial_hint', proof.replace('7 0 5 6 0', '7 0 1 5 6 0'), 'hint is neither unit nor conflicting'),
        ('missing_empty', proof.rsplit('7 0', 1)[0], 'no checked empty clause'),
        ('deleted_actual_hint', proof.replace('7 0', '6 d 5 0\n7 0'), 'unknown or deleted hint clause'),
    ]
    positives = []
    damages = []
    with tempfile.TemporaryDirectory(dir=here) as folder:
        folder = Path(folder)
        cp, pp = folder/'positive.cnf', folder/'proof.lrat'
        cp.write_text(cnf)
        for image in [proof, deletion_proof]:
            pp.write_text(image)
            positives.append(verify(cp, pp))
        for name, image, reason in mutations:
            need(image != proof, 'actual damaged proof image:'+name)
            pp.write_text(image)
            try:
                verify(cp, pp)
            except ValueError as error:
                need(str(error) == reason, 'wrong proof rejection:'+name+':'+str(error))
                damages.append({'name': name, 'rejection': str(error)})
            else:
                raise ValueError('damaged actual RUP proof accepted:'+name)
    print(json.dumps({'author': 'six-vdw-1', 'role': 'researcher',
                      'status': 'RUP_REAL_POSITIVE_AND_SEMANTIC_DAMAGE_CONTROLS_PASS',
                      'positive_proofs': positives, 'damages': damages,
                      'semantic_damage_rejections': len(damages), 'native_solver_used': False,
                      'finite68_exclusion_established': False,
                      'kernel_source_sha256': hashlib.sha256((here/'strict_rup.py').read_bytes()).hexdigest()},
                     sort_keys=True))
