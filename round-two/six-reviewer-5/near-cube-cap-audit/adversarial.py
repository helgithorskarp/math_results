"""Small controls specifically expose omitted hypotheses and normalizations."""
from independent import data,require,coefficient_identity
from fractions import Fraction as Q

def run():
 d=data(11);a=b=3;rho=1-d['f'][a]*d['f'][b]/d['mu']
 # Missing the unordered-pair factor, missing kernel defect, root approximation,
 # and falsely using equality for the clipped fourth-moment bound each reject.
 physical=2*(d['mu']-d['f'][a]*d['f'][b]);wrong_factor=d['mu']-d['f'][a]*d['f'][b]
 require(physical!=wrong_factor,'factor-two control')
 require(data(11,Q(2))['eta']>0>d['eta'],'root2 control')
 d12=data(12);upper=(d12['s']+12)*Q(107,48)
 require(d12['S']<upper,'clipping equality control')
 n=12;defect=2*d12['u'][3]*3+2*d12['u'][3]*3-18
 require(defect!=0,'dropping cardinality kernel is observable on a proper edge')
 # A complement and a proper-union pair have distinct coefficients.
 require(1-d['f'][3]*d['f'][8]/d['mu']!=rho,'complement cannot be treated as proper')
 return {'damage_controls':{'unordered_factor_two':True,'r2_at11_positive':True,'clipped_norm_not_full_norm':True,'cardinality_kernel_defect_nonzero':True,'proper_vs_complement_distinguished':True},'damaged_proper_kernel_defect_n12':str(defect),'scope':'Arithmetic controls; all-n coverage comes from the ordinary proof.'}
if __name__=='__main__':
 import json
 print(json.dumps(run(),indent=2))
