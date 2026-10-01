"""Finite QR31 XOR C20 construction search; emit one literal AP per failure."""
import argparse
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def crt(r, s):
    return s+20*((r-s)*14 % 31)


def run(directory):
    directory.mkdir(parents=True,exist_ok=True);records=[]
    residues={x*x % 31 for x in range(1,31)}
    for zero in [0,1]:
        field=[zero]+[int(r not in residues) for r in range(1,31)]
        patterns={}
        for d in range(31):
            for a in range(31):
                code=sum(field[(a+j*d) % 31]<<j for j in range(7))
                patterns.setdefault((code,d!=0),(a,d))
        for mask in range(1024):
            row=[(mask>>s)&1 for s in range(10)];row += [1-bit for bit in row]
            witness=None
            for ds in range(20):
                for b in range(20):
                    code=sum(row[(b+j*ds) % 20]<<j for j in range(7))
                    for target in [code,code^127]:
                        for nonzero in [True,False]:
                            if ds==0 and not nonzero:
                                continue
                            if (target,nonzero) not in patterns:
                                continue
                            a,dr=patterns[target,nonzero];start=crt(a,b);step=crt(dr,ds)
                            require(step!=0,'nonconstant CRT AP')
                            if step>310:
                                start=(start+6*step)%620;step=620-step
                            colors=[field[(start+j*step)%31]^row[(start+j*step)%20] for j in range(7)]
                            require(start+6*step<2296 and len(set(colors))==1,'literal product AP')
                            witness=[zero,mask,start,step,colors[0]];break
                        if witness is not None:break
                    if witness is not None:break
                if witness is not None:break
            if witness is None:
                word=[field[x%31]^row[x%20] for x in range(620)]
                (directory/'candidate-period620.bits').write_text(''.join(map(str,word))+'\n')
                (directory/'candidate-3704.bits').write_text(''.join(str(word[x%620]) for x in range(3704))+'\n')
                result={'status':'PRODUCT_CANDIDATE_REQUIRES_INDEPENDENT_CHECK','zero':zero,'mask':mask}
                (directory/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));return
            records.append(witness)
    result={'author':'six-vdw-1','role':'researcher','status':'COMPLETE_QR31_X_C20_AP_COVER',
            'period':620,'target_N':2296,'research_target_N':3704,'parameter_words':2097152,'zero_choices':2,
            'forced_antipodal_row_words':1024,'covered_antipodal_cases':len(records),
            'record_format':['zero_color','low_ten_bit_mask','start_zero_based','positive_step','monochromatic_color'],
            'records':records,
            'proof_limit':'Only QR31 XOR arbitrary C20 templates. Non-antipodal rows have a step310 AP; all antipodal rows have the listed literal AP. No unrestricted exclusion.'}
    (directory/'cover.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=Path)
    run(parser.parse_args().directory)
