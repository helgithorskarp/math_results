"""Exact scalar certificate for the new high-angular-value direction margin."""
from fractions import Fraction as F
import json


def main():
    D=F(6,7)/F(47,2)
    X=F(1,8)+D
    S2=1/(4*X)
    ratio=16*X**2
    relative=(1-ratio)/12
    absolute=S2*relative
    got={'D_upper':D,'mu4_upper':X,'K2_upper':X/4,
         'S2_lower':S2,'S2_upper':F(2),'fourK_over_S3_upper':ratio,
         'q_over_S2_lower':relative,'q_real_line_lower':absolute}
    exact={'D_upper':F(12,329),'mu4_upper':F(425,2632),'K2_upper':F(425,10528),
           'S2_lower':F(658,425),'S2_upper':F(2),'fourK_over_S3_upper':F(425,658)**2,
           'q_over_S2_lower':F(84113,1731856),'q_real_line_lower':F(84113,1118600)}
    if got!=exact or not (0<ratio<1 and absolute>0):raise ValueError('exact direction margin')
    print(json.dumps({k:str(v)for k,v in got.items()},sort_keys=True))


if __name__=='__main__':main()
