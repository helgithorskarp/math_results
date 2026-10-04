"""Exact exceptional-domain, scalar bound constants and no-pole gate."""
import argparse,hashlib,json,pathlib
from fractions import Fraction as R
from five_check import read,need
def main():
    a=argparse.ArgumentParser();a.add_argument('--input',required=True);a.add_argument('--out',required=True);args=a.parse_args()
    raw=pathlib.Path(args.input).read_bytes();rec=json.loads(raw);rats=[]
    for row in rec['entries']:rats+=row
    rats+=rec['pivots']
    for st in rec['stages']:rats+=st['column']+st['row']+[x['value'] for x in st['updates']]
    need(len(rats)==80,'entire rational-field no-pole coverage')
    count=0
    for v in rats:
        d=read(v).d;need(d.get((0,0,0),0)>0 and all(c>=0 for c in d.values()),'every intermediate denominator positive');count+=len(d)
    need(2-R(54,169)>1 and R(2,3)-R(15,169)>R(1,2),'positive alpha and beta ranges')
    coeff=R(1,3)-R(1,18)-R(9,512)
    need(coeff==R(1199,4608) and (coeff-R(1,5))*16-R(5,8)==R(487,1440),'all h>=4 scalar lower margin')
    need((R(13,48)-R(9,338)-R(1,5))*13-R(7,16)==R(1391,10140),'exceptional integer h3/l2 scalar margin')
    rows=[R(1009,676),R(1135,676),R(19,13),R(1907,988)]
    need(all(x<2 for x in rows) and R(991,676)<2,'entire normalized frame bounds')
    need((R(5,3)+R(13,2))/13==R(49,78),'full spread dual uniform scalar bound')
    need(31**2>15*8**2 and 3+R(31,8)==R(55,8),'exact irrational perturbation norm upper bound')
    need(1-R(55,8)/7==R(1,56) and 1-R(55,8)/32==R(201,256),'strengthened original cap floors')
    need(R(1,7)<6/R(49,78),'strengthened interval within strict lower interior')
    out=dict(complete=True,all_encoded_denominators=80,all_positive_denominator_coefficients=count,
             field_certificate_bytes=len(raw),field_certificate_sha256=hashlib.sha256(raw).hexdigest(),
             alpha_lower='s',beta_lower='s/2',mu_lower='s/5',exceptional_integer_case='h=3,l=2',
             standard_row_bounds=list(map(str,rows)),odd_trace_row_bound='991/676',
             perturbation_norm_upper='55/8',uniform_delta_interval='0<delta<=1/7',uniform_cap_floor='1/56',main_delta_cap_floor='201/256',
             trust='No-pole and exact scalar arithmetic checks; universal inequality arguments in PROOF.md, not finite samples.')
    data=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();pathlib.Path(args.out).write_bytes(data);print(data.decode().strip())
if __name__=='__main__':main()
