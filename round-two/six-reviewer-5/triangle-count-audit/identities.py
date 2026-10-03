"""Whole-parameter support/norm/mean identities; own primary data only."""
import argparse,json,pathlib,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from canonical import K,h,q,QQ
from fractions import Fraction as F

def need(ok,why):
    if not ok:raise ValueError(why)

def decode(p):
    def poly(a):return sum((K(QQ(F(c).numerator,F(c).denominator))*h**i*q**j for (i,j),c in a),K.zero)
    return poly(p['num'])/poly(p['den'])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('primary',type=pathlib.Path);ap.add_argument('--damage');args=ap.parse_args();p=json.loads(args.primary.read_text())
    alH,beH,alL,beL,nu,muL=[decode(z) for z in p['scalars']]
    s=q+3*h;d=3*h;ell=3*h+4;w=s-1;rho=(q-1)/(s-4)
    E2=q/(3*h)+rho*rho*(s-3)/3;K2=ell*q+6*h-16;c0=K2/(ell*ell);B2=s*(h-1)/(3*h)
    FF=(q-8)/(ell*rho*(s-3));AA=FF/(2*h);cL=-4*(q-8)/(ell*s)
    b=3*h*(q-ell-1)/(ell*s*(h-1));a=-b/2;cH=-9*(q-ell-1)/(2*ell*s)+AA*q/(h*s)
    muH=((h-1)*nu+muL/h)/h
    if args.damage=='private-support':cL+=1
    identities={
      'heavy marked norm':q/d+B2+2*s/3-w,
      'light marked norm':q/d+B2+2*s/3-w,
      'same facet marked intersection':q/d+B2-s/3+1,
      'different heavy marked intersection':q/d-s/(3*h)+1,
      'heavy private leaf/marked support':-(q-1)/ell+AA*q/d+a*B2-cH*s/3+1,
      'heavy private full/marked support':-(q-1)/ell+b*B2+1,
      'light private leaf/marked support':-(s-4)/ell-FF*rho*(s-3)/3-cL*s/3+1,
      'light private full/marked support':-(s-4)/ell+FF*rho*(s-3)+1,
      'heavy private leaf norm':c0+AA*AA*E2+a*a*B2+2*s*cH*cH/3+muH+(alH+beH)/4-w,
      'heavy private full norm':c0+b*b*B2+2*s*cH*cH/(3*(h-1))+2*s*cL*cL/(3*h*h)+muH+beH-w,
      'light private leaf norm':c0+FF*FF*E2+2*s*cL*cL/3+muL+(alL+beL)/4-w,
      'light private full norm':c0+9*FF*FF*E2+muL+beL-w,
      'heavy private leaf/full intersection':c0+a*b*B2+muH-beH/2+1,
      'light private leaf/full intersection':c0-3*FF*FF*E2+muL-beL/2+1,
      'heavy mean row sum':muH+(h-1)*(muL/h-muH)/(h-1)-muL/h,
      'light mean row sum':h*(-muL/h)+muL,
      'heavy contrast eigenvalue':muH-(muL/h-muH)/(h-1)-nu,
      'heavy mean squared norm':h*muH+h*(h-1)*(muL/h-muH)/(h-1)-muL,
      'old/marked total K identity':1-3*(h+1)/ell-1/ell,
      'private E balance':2*h*AA+2*FF-3*FF,
      'private B balance':2*a+b,
      'private heavy T balance':-cH+(h-1)*cH/(h-1),
      'private light T balance':h*cL/h-cL,
    }
    for label,z in identities.items():need(z==0,'entire QQ(h,q) identity '+label)
    print(json.dumps(dict(actual_agent='six-reviewer-5',role='independent reviewer',domain='QQ(h,q), poles excluded by proved positive factors',all_complete_identities=list(identities),identity_count=len(identities),mandatory_types_exhaustive_under_written_set_decoding=True),sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
