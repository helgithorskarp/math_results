"""Full original coordinates, uncancelled contact circuits and cap norms."""
import json
from digit import T,Z,prove_zero
from geometry import model,dot,LABELS,CONTACTS
from census import classify,CAPS

def check():
    m=model();Y=m['Y'];a=m['a'];b=m['b'];c=m['c'];t=T;z=Z
    rows={}
    def radical(name,v):
        rows[name+'_constant']=prove_zero(v.p)
        rows[name+'_linear']=prove_zero(v.q)
    for i in LABELS:radical('unit_'+str(i),dot(Y[i],Y[i])-m['Omega']**2)
    for i,j in CONTACTS:radical('contact_'+str(i)+'_'+str(j),dot(Y[i],Y[j])-t*m['Omega']**2)
    circuits=[(0,9,5,11),(5,6,0,11),(11,7,0,5),(1,8,2,4),(4,10,1,2),(2,12,1,10)]
    for i,j,k,l in circuits:
        for q in range(3):radical('circuit_'+str(i)+'_'+str(j)+'_'+str(q),(Y[i][q]+Y[j][q])*a-(Y[k][q]+Y[l][q])*(2*t))
    for q in range(3):
        radical('long_B_'+str(q),(Y[8][q]+Y[12][q])*a*a-(Y[1][q]+Y[2][q])*(4*t*t+2*t*a-a*a))
        radical('low_A_'+str(q),Y[0][q]*m['h']-(Y[6][q]*(2*t)+Y[7][q]*(2*t)+Y[9][q]*b)*a)
    D,C,S,E,O=(m[k] for k in ['D','C','S','E','Omega'])
    Q=a*D*z*z-2*D*z+2*t*t-t+1
    scalar={'CminusS':C-S-b*c*(b*z+1)**2,'CplusS':C+S-Q,
            'positiveQ_square':a*Q-D*(a*z-1)**2-4*t*t,
            'Omega_factor':O-m['h']*m['J']*b*b*c*c*a**8*C*(b*z+1)**2*Q}
    for k,p in scalar.items():rows[k]=prove_zero(p)
    for k,(normal,threshold) in CAPS.items():
        raw=dot(normal,normal)
        rows['capnorm_'+str(k)]=prove_zero(raw-({98:233-232*t,99:621-620*t}[k]))
    return {'complete_identity_rows':rows,'whole364_case_rows':classify(),
            'input_status':'original written9912 defining formulas; new10109 factor/certificate data not needed'}

if __name__=='__main__':print(json.dumps(check(),sort_keys=True,separators=(',',':')))
