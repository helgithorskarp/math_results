"""Reject genuine false geometries, signs, motions and a too-large gate."""
import json
from audit import run

DAMAGES=['wrong_source','face_height','missing_hull_edge','reversed_hull',
         'wrong_normal','wrong_determinant','unsupported_radius',
         'wrong_boundary_pose','improper_symmetry','translation_nonzero','bad_scale']

if __name__=='__main__':
    out={}
    for name in DAMAGES:
        try:run(name)
        except ValueError as exc:out[name]=str(exc)
        else:raise ValueError('FALSE FIXTURE ACCEPTED: '+name)
    print(json.dumps(out,sort_keys=True,indent=2))
