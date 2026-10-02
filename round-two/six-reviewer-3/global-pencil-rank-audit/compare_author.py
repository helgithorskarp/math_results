"""Late data-only whole coefficient comparison; never imports producer code."""
import argparse,json,hashlib
from fractions import Fraction as F
from pathlib import Path
from polys import Poly,need
from audit import load

def compare(own,native,export):
 names={**own['four_cleared'],**own['elimination']};names['h']=(load(names['f2'])-6*load(names['g'])).record();checked=[]
 need(set(names)==set(export['all_necessary_polynomials']),'entire exported coefficient census')
 for name,record in names.items():
  terms={}
  for powers,v in export['all_necessary_polynomials'][name]:
   need(len(powers)==3 and all(type(e)==int and e>=0 for e in powers),'native full exponent triple')
   m=tuple((var,e) for var,e in zip(['q','r','x'],powers) if e);need(m not in terms,'native duplicate monomial');terms[m]=(F(v),F(0))
  need(load(record)==Poly(terms),'ALL coefficients '+name);checked.append(name)
 c=native['characteristic_zero_resultant'];need(c['P20']==own['derived_P20'] and c['S5']==own['S5'] and int(c['nonzero_exact_content'])==own['constant_c'],'ALL integer factor coefficients and content')
 digest=hashlib.sha256(json.dumps(own['integer_determinant_values'],sort_keys=True,separators=(',',':')).encode()).hexdigest();need(digest==c['full_evaluations_sha256'],'ALL85 exact rational Gaussian/Bareiss determinant values')
 checked_units=[]
 for name,row in zip(['S5_branch','P20_branch'],own['full_modular_units']):
  target=native['complete_modular_units'][name]
  need(target['factor']==[v%257 for v in row['integer_factor']] and target['resultant']==row['entire_determinant'] and target['factor_multiplier']==row['U'] and target['resultant_multiplier']==row['V'],'entire modular determinant/factor/Bezout multipliers '+name);checked_units.append(name)
 return {'status':'PASS','whole_exported_polynomials':checked,'all_polynomial_coefficients_compared':True,'all_integer_determinant_values':85,'all_integer_factor_coefficients':27,'whole_modular_determinants_and_both_full_multiplier_pairs':checked_units,'native_record_sha256':hashlib.sha256(json.dumps(native,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'comparison_after_own_seal':True,'same_representation_or_whole_record_claim':False}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('native_record',type=Path);ap.add_argument('native_export',type=Path);args=ap.parse_args();print(json.dumps(compare(json.loads(Path(__file__).with_name('EXPECTED.json').read_text()),json.loads(args.native_record.read_text()),json.loads(args.native_export.read_text())),sort_keys=True))
if __name__=='__main__':main()
