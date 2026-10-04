"""Two bounded complete original controls, not universal parameter enumeration."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,time,signal,resource
from repair_harmonic import repair
from sector_control_harmonic import control
from completion_harmonic import alarm
from exact import require


def main():
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60)
    start=time.monotonic();folder=Path.cwd();records=[]
    for n,h in ((3,3),(3,4)):
        result,certificate=repair(n,h)
        physical=control(n,h)
        require(result['seed']['matrix_sha256']==physical['seed_matrix_sha256'],
                'WHOLE original seed shared by inverse and physical controls')
        require(result['kappa']==physical['closed_kappa'],
                'whole inverse versus original physical dual at boundary')
        if (n,h)==(3,4):
            require(result['seed']['baseline']['matrix_sha256']==
                    'c52e14420449867003a80014fd03d5fef4f99d09503258074afc84b57add98b4',
                    'entire previously reproduced source95 n3/h4 baseline')
        for name,data in (('REPAIR',certificate),('SECTOR',physical)):
            packed=json.dumps(data,indent=2,default=str)+'\n'
            require(len(packed.encode())<=32*1024*1024,'unchanged32MiB packing guard')
            (folder/f'BOUNDARY-n{n}-h{h}-{name}.json').write_text(packed)
        summary=dict(n=n,h=h,N=result['N'],s=result['s'],
            lower_rank=result['final']['lower_rank'],cap_rank=result['final']['upper_rank'],
            original_M_sha256=result['final']['matrix_sha256'],seed_sha256=result['seed']['matrix_sha256'],
            common_norm=result['seed']['common_norm'],tau=result['seed']['tau'],
            kappa=result['kappa'],delta=result['delta'],scaled_cap_floor=result['scaled_cap_floor'],
            physical_dimension=physical['complete_dimension'],
            physical_metric_sha256=physical['metric_sha256'],physical_frame_sha256=physical['frame_sha256'],
            all_original_entries=result['all_original_entries'],
            all_physical_positions=physical['all_metric_and_frame_positions'],
            whole_dual_scores=True,all_inverse_equations=True)
        records.append(summary)
        (folder/'BOUNDARY-CONTROLS.json').write_text(json.dumps(records,indent=2)+'\n')
        print(json.dumps(summary),flush=True)
    signal.alarm(0)
    print(json.dumps(dict(complete=True,exact_original_controls=2,
        records_sha256=sha256((folder/'BOUNDARY-CONTROLS.json').read_bytes()).hexdigest(),
        seconds=time.monotonic()-start,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        optimized=not __debug__,one_serial_mathematical_child=True)),flush=True)


if __name__=='__main__':main()
