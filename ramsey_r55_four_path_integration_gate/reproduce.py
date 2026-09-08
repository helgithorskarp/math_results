"""Manifest-checked, no-download replay in normal and assertion-disabled Python."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def require(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    root = Path(__file__).resolve().parent
    names = set()
    for line in (root/'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        require(Path(name).name == name and name not in names, 'manifest path')
        require(hashlib.sha256((root/name).read_bytes()).hexdigest() == digest, 'manifest '+name)
        names.add(name)
    require(names == {p.name for p in root.iterdir() if p.is_file()}-{'SHA256SUMS'}, 'source file set')
    certificate = json.loads((root/'CERTIFICATE.json').read_text())
    deps = json.loads((root/'DEPENDENCIES.json').read_text())
    require(certificate['P'] == deps['baseline_P'], 'pinned upstream P')
    for mode in ([], ['-O']):
        for script, expected, args in (
                ('produce.py', 'CERTIFICATE.json', []),
                ('check.py', 'EXPECTED_CHECK.json', [str(root/'CERTIFICATE.json')]),
                ('controls.py', 'EXPECTED_CONTROLS.json', [])):
            run = subprocess.run([sys.executable, '-B']+mode+[str(root/script)]+args,
                                 capture_output=True, check=True)
            require(not run.stderr, 'unexpected stderr '+script)
            require(run.stdout == (root/expected).read_bytes(), 'replay mismatch '+script+str(mode))
    print(json.dumps({'status': 'REPRODUCED_DIRECT_INTEGRATION_GATE_FAILURE',
                      'manifest_files': len(names), 'replay_modes': ['normal', 'assertions_disabled'],
                      'strict_comparison': '12*Gamma*P < R < 13*Gamma*P',
                      'physical_pair_matrices_per_checker_run': 131072,
                      'corruption_rejections_per_mode': 14,
                      'target_solver_calls': 0, 'physical_target_tasks_decided': 0}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
