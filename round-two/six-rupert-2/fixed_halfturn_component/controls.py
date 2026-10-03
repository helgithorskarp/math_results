"""Eight semantic false-certificate author controls; no independent review."""
from pathlib import Path
import argparse, copy, json, time
import geometry as g
import ray, width

def record():
    certificate = json.loads((g.HERE/'certificate.json').read_text())
    out = []
    def reject(name, layer, mutate):
        altered = copy.deepcopy(certificate)
        mutate(altered)
        try:
            layer.record(altered)
        except ValueError as error:
            out.append({'name': name, 'rejected': True, 'reason': str(error)})
            return
        raise ValueError('false mathematical certificate accepted: '+name)
    reject('one original corner-source ray omitted', ray, lambda d: d['ray_hits'].pop())
    reject('noncommon source label changed to actual common0', ray,
           lambda d: d['ray_hits'][0].update(source=0))
    reject('zero instead of positive ray intersection parameter', ray,
           lambda d: d['ray_hits'][0].update(t=['0', '0']))
    reject('all barycentric masses zero', ray,
           lambda d: d['ray_hits'][0].update(barycentric=[['0', '0']]*3))
    reject('false negative facet for the first necessary side', ray,
           lambda d: d['side_witnesses'][0].__setitem__(2, 31))
    reject('second closed receiving child missing', width,
           lambda d: d['width_cover']['nodes'][0]['children'].pop())
    reject('same receiving child used twice', width,
           lambda d: d['width_cover']['nodes'][0]['children'].__setitem__(
               1, d['width_cover']['nodes'][0]['children'][0]))
    reject('positive receiving contact without an actual negative source preimage', width,
           lambda d: d['width_cover']['leaves'][0]['original_edges'].__setitem__(0, [16, 17]))
    return {'agent': 'six-rupert-2', 'role': 'researcher',
            'scope': 'author semantic certificate rejection controls only, no independent review',
            'controls': out, 'rejected': len(out)}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    started = time.monotonic()
    result = record()
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'rejected': result['rejected'], 'mathematical_sha256': g.digest(result),
                      'wall_seconds': time.monotonic()-started}, indent=2))
