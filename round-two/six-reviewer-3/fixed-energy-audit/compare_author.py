"""Late complete scalar/literal comparison; imports NO author executable."""
import sys,json,hashlib
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build import build,polynomial_from_criticals,evaluate,pairmul,canonical
def compare(path):
 native=json.loads(Path(path).read_text())
 if hashlib.sha256(canonical(native)).hexdigest()!='b04129905ab1b4992352c925338a6ee29d3540e655563410905f66c7a6442022':raise ValueError('exact native input mismatch')
 own=build();m=own['strict_margins'];e=F(1,65536);amin=1-e
 names={
 'nine counted original circles':'rouche_all_nine','disjoint original circles':'disjoint_circles','positive root motion divisor':'cube_displacement_denominator','cube displacement below V/6':'cube_displacement_one_sixth','cube linear displacement below V/6':'cube_linear_one_sixth','full pair remainder E<=|mean|V/6+V^2':'full_pair_normal_error','full individual remainder E<=|mean|V/6+V^2':'full_individual_normal_error','whole centered critical radius from fixed energy':'centered_radius','initial lower objective >=8/r-3V/5':'initial_reciprocal_loss','low F gives r>6399/6400':'r0_from_objective','positive signed variance coefficient':'positive_Q_multiplier','first bootstrap positive divisor':'initial_positive_variance','first bootstrap gives V<700eta':'initial_variance_contraction','retained mean square below eta/11':'mean_square_eleven','mean modulus below1/800':'mean_800','V<26eta permits max centered radius1/50':'centered_radius_26','second bootstrap positive divisor':'second_positive_variance','second bootstrap gives V<26eta':'second_variance_contraction','V<8eta permits max centered radius1/90':'centered_radius_8','third bootstrap positive divisor':'third_positive_variance','third bootstrap gives V<8eta':'third_variance_contraction','fourth bootstrap positive divisor':'fourth_positive_variance','fourth bootstrap gives V<6eta':'fourth_variance_contraction','final V<6eta permits max centered radius1/96':'centered_radius_6','mean real part strictly negative':'mean_strict_negative','V<6eta yields r<1+eta':'radial_upper_box','whole |r^-3-1|<=4eta':'r_inverse_cubic_derivative','joint constraint 7V+5Q<12eta':'trace_ellipse_budget','cube pair slack below eta/12':'individual_slack_budget','real mean above -4eta/5':'radial_mean','imaginary mean modulus below eta/3':'imaginary_mean','mean modulus13eta/15 routes c8 below8eta':'c8_cap','c7 below4eta':'c7_cap','critical energy H below7eta':'energy7','direct uniform first-power slope exceeds13/5':'firstpower_slope_13_5'}
 for j in range(1,7):names['Maclaurin c'+str(j)+' below8eta']='coefficient_'+str(j)
 extra={'sqrt3/9<1/5':F(1,25)-F(1,27),'marked reciprocal denominators finite from fixed energy':amin**2-F(1,512),'V<6eta yields r>1-eta':1-F(33,40),'2/sqrt3<7/6':F(49,36)-F(4,3),'sqrt6<5/2':F(25,4)-6}
 compared=[]
 for row in native['whole_domain_margins']:
  name=row['name'];v=F(m[names[name]]) if name in names else extra[name]
  if v!=F(row['strict_margin']) or v<=0:raise ValueError('full scalar disagreement:'+name)
  compared.append({'name':name,'strict_margin':str(v)})
 if len(compared)!=46 or len({r['name'] for r in compared})!=46:raise ValueError('incomplete scalar comparison')
 controls=[]
 for row in native['literal_controls']:
  crit=[tuple(F(v) for v in z) for z in row['all_eight_criticals']];a=1-e
  p,der=polynomial_from_criticals(crit,a)
  encoded=[[str(t) for t in z] for z in p]
  if encoded!=row['whole_anchored_original_polynomial']:raise ValueError('whole literal polynomial disagreement')
  mean=tuple(sum(z[k] for z in crit)/8 for k in [0,1]);V=sum(sum((z[k]-mean[k])**2 for k in [0,1]) for z in crit)
  H=sum(sum(t*t for t in z) for z in crit)
  if [str(t) for t in mean]!=row['mean'] or F(row['V'])!=V or F(row['H'])!=H:raise ValueError('literal variance disagreement')
  ds=[]
  for z in crit:
   if evaluate(der,z)!=(0,0):raise ValueError('literal derivative mismatch')
   ds.append(str((a-z[0])**2+z[1]**2))
  if ds!=row['all_marked_distance_squares']:raise ValueError('all literal distances disagree')
  # Translate whole polynomial independently through Horner composition.
  from build import cmul,pairadd
  shifted=[(F(0),F(0))]
  for c in reversed(p):
   shifted=cmul(shifted,[mean,(F(1),F(0))]);shifted[0]=pairadd(shifted[0],c)
  while len(shifted)>1 and shifted[-1]==(0,0):shifted.pop()
  if [[str(t) for t in z] for z in shifted]!=row['whole_translated_polynomial']:raise ValueError('whole native translation disagreement')
  controls.append({'name':row['name'],'whole_original_positions':len(p),'whole_translated_positions':len(shifted),'counted_critical_evaluations':len(crit)})
 return {'entire_scalar_margins':compared,'all_native_literal_rows':controls,'native_whole_canonical_sha256':'b04129905ab1b4992352c925338a6ee29d3540e655563410905f66c7a6442022','scope':'All46 scalar margins and six complete anchored/translated polynomials, means/energies and eight distance squares agree. No claim of common full symbolic coefficient representation for the producer20 identity records.'}
if __name__=='__main__':print(json.dumps(compare(sys.argv[1]),sort_keys=True,indent=2))
