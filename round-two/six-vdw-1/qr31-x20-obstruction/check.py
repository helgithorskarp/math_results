"""Helper-free exact cover check, directly covering all2^21 product parameters."""
import argparse
import hashlib
import json
from pathlib import Path
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def check(path):
    begin=time.monotonic();data=json.loads(path.read_text());records=data['records']
    require(data['status']=='COMPLETE_QR31_X_C20_AP_COVER' and data['period']==620 and data['target_N']==2296 and data['research_target_N']==3704 and
            data['parameter_words']==2097152 and data['zero_choices']==2 and
            data['forced_antipodal_row_words']==1024 and data['covered_antipodal_cases']==2048, 'cover metadata')
    require(len(records)==2048,'complete antipodal table size');covered=antipodal=nonantipodal=0
    for zero in [0,1]:
        field=[zero]+[int(pow(r,15,31)!=1) for r in range(1,31)]
        for row_mask in range(1<<20):
            equal=~(row_mask^(row_mask>>10)) & 1023
            if equal:
                start=(equal & -equal).bit_length()-1;step=310;color=None
                nonantipodal+=1
            else:
                low=row_mask & 1023;record=records[zero*1024+low]
                require(type(record) is list and len(record)==5 and all(type(x) is int for x in record),'record domain')
                q,mask,start,step,color=record
                require(q==zero and mask==low and color in [0,1],'complete indexed antipodal cover')
                antipodal+=1
            require(0<=start<620 and 1<=step<=310 and start+6*step<2296,'actual interval AP bounds')
            # Actual integer positions; no CRT or AP-pattern generator import.
            for j in range(7):
                x=start+j*step;value=field[x%31]^((row_mask>>(x%20))&1)
                if color is None:color=value
                require(value==color,'nonmonochromatic claimed AP')
            covered+=1
    require(covered==2097152 and antipodal==2048 and nonantipodal==2095104,'every product parameter covered exactly once')
    return {'author':'six-vdw-1','role':'researcher','status':'ALL_2097152_QR31_X_C20_PARAMETERS_HAVE_A_LITERAL_7_AP',
            'covered':covered,'checked_prefix_length':2296,'antipodal_cases':antipodal,'nonantipodal_cases':nonantipodal,
            'cover_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'elapsed_seconds':time.monotonic()-begin,
            'proof_limit':'Definition-level finite cover of this exact QR31 XOR C20 family; unrestricted period620 and W(2,7) remain open.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('cover',type=Path);parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=check(args.cover)
    if args.output:args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result))
