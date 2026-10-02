"""One of six small, independently bounded replay phases."""
from pathlib import Path
import json, sys
import inputs
from literal import require
from exact import digest


def run(name):
    require(name in ('lower', 'upper', 'duals', 'radical', 'whole', 'controls'),
            'fixed phase list')
    if name in ('lower', 'upper'):
        from schur import phase
        rec = phase(name)
        fixture = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
        require(rec['even_odd_blocks'] == fixture[name+'_schur_blocks'],
                'original solve differs from frozen compact Schur blocks')
    elif name == 'duals':
        from generator import generate
        rec = generate()
    elif name == 'radical':
        from radical import check
        rec = check()
    elif name == 'whole':
        from whole import controls
        rec = controls()
    else:
        from controls import controls
        rec = controls()
    return rec


if __name__ == '__main__':
    print(json.dumps(run(sys.argv[1]), sort_keys=True, separators=(',', ':')))
