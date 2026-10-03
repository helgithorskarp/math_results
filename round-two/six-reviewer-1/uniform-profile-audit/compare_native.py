"""LATE data-only complete core-map correspondence, after primary sealing.

Converts native Q[omega,i] coefficients to fresh QQ[zeta36], and reorders
all six moment/control variables. No producer executable kernel imported.
This supplements, and does not define, the independent calculations.
"""
from pathlib import Path
import sys,json,hashlib,argparse
sys.path.insert(0,str(Path(__file__).resolve().parent))
from field import E,Q,I,W,need
import jets as J
import poly as P


def no_duplicates(pairs):
    out={}
    for key,value in pairs:
        need(key not in out,'duplicate JSON key');out[key]=value
    return out


def load(path):
    return json.loads(path.read_text(),object_pairs_hook=no_duplicates,
                      parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite JSON')))


def scalar(value):
    need(type(value)is list and len(value)==2,'native complex coefficient shape')
    out=E(0)
    for side,values in enumerate(value):
        need(type(values)is list and len(values)==6,'native ninth coefficient shape')
        for j,v in enumerate(values):
            need(type(v)is str,'native rational coefficient type')
            out=out+Q(v)*W**j*(I if side else 1)
    return out


def polynomial(value):
    out={}
    for exp,coefficient in value:
        need(type(exp)is list and len(exp)==7 and all(type(n)is int and n>=0 for n in exp),
             'native seven-variable exponent')
        need(exp[6]==0,'no unsummed coordinate in compared map')
        e=tuple(exp[j]for j in (0,1,4,5,2,3))
        need(e not in out,'duplicate native monomial')
        c=scalar(coefficient);need(bool(c),'native coefficient canonical nonzero')
        out[e]=c
    return out


def series(value):
    out={}
    for t,p in value:
        need(type(t)is int and 0<=t<=4 and t not in out,'native retained series order')
        a=polynomial(p);need(bool(a),'native series canonical nonzero');out[t]=a
    return out


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('native_record',type=Path)
    parser.add_argument('primary_record',type=Path)
    parser.add_argument('--record',type=Path)
    args=parser.parse_args();here=Path(__file__).resolve().parent
    seal=load(here/'PRIMARY_SEAL.json')
    for name,digest in seal['files'].items():
        need(hashlib.sha256((here/name).read_bytes()).hexdigest()==digest,'sealed independent source '+name)
    native=load(args.native_record);primary=load(args.primary_record)
    source=load(here/'expected.json')['modes']['primary']
    primary_bytes=json.dumps(primary,sort_keys=True,separators=(',',':')).encode()
    need(hashlib.sha256(primary_bytes).hexdigest()==source['record_sha256'],'entire primary input binding')
    names=[];maps=[]
    def compare(a,b,name):
        need(a==b,'late entire map correspondence '+name);names.append(name)
        # Store full normalized maps to compare whole-byte records in normal/O.
        maps.append([name,P.record(a)])
    def parsed(p):return {tuple(e):E(c)for e,c in p}
    # Complete polynomial all ten z degrees and every retained t coefficient.
    expected=[{}for _ in range(10)]
    for t,values in enumerate(primary['whole_primitive_maps']):
        for z,p in values:expected[z][t]=parsed(p)
    need(len(native['entire_moment_primitive'])==10,'all primitive z degrees')
    for z,rows in enumerate(native['entire_moment_primitive']):
        actual=series(rows)
        for t in range(5):compare(actual.get(t,{}),expected[z].get(t,{}),f'primitive/{z}/{t}')
    need(len(native['all_nine_control_root_jets'])==9,'all native original branches')
    need(len(native['all_nine_control_half_normals'])==9,'all native individual normals')
    for j in range(9):
        actual=series(native['all_nine_control_root_jets'][j])
        desired={0:P.const(W**j),2:parsed(primary['whole_root_jets'][j][0]),
                 3:parsed(primary['whole_root_jets'][j][1]),4:parsed(primary['whole_root_jets'][j][2])}
        for t in range(5):compare(actual.get(t,{}),desired.get(t,{}),f'root/{j}/{t}')
        actual=series(native['all_nine_control_half_normals'][j])
        for t in range(5):
            desired=parsed(primary['whole_individual_normals'][j][t-2])if t>=2 else {}
            compare(actual.get(t,{}),desired,f'normal/{j}/{t}')
    for name,col in [('closing_M0',4),('closing_b0',5)]:
        compare(polynomial(native[name]),parsed(primary['base_controls'][str(col)]),name)
    objective=series(native['entire_first_power_objective'])
    for t in range(5):compare(objective.get(t,{}),parsed(primary['whole_objective'][t]),f'objective/{t}')
    compare(polynomial(native['whole_profile_cost']),parsed(primary['profile_cost']),'profile_cost')
    compare(polynomial(native['whole_Pearson_defect']),parsed(primary['dispersion']),'dispersion')
    compare(polynomial(native['whole_maximum_cost_defect']),parsed(primary['maximum_defect']),'maximum_defect')
    odd=native['odd_Jacobian'];need(len(odd)==2 and all(len(v)==2 for v in odd),'odd Jacobian shape')
    for col in range(2):
        for row in range(2):
            compare(P.const(scalar(odd[col][row])),parsed(primary['jacobian'][row][col]),
                    f'odd_Jacobian/{row}/{col}')
    constants={'c':J.C,'d':2*J.C*J.C-1,'e':2*(2*J.C*J.C-1)**2-1,
               'y':J.y,'x':J.x,'H':J.H,'U0':J.U,'C':E(Q(8,3))+J.y,
               'k':J.k,'rho':J.rho,'ell':J.ell,'alpha':J.alpha,'tau':J.tau,
               'K1':J.K1,'Bstar':J.Bstar,'sharp_K_maximum':J.Kmax,
               'detE':3*J.H*(J.C+2*J.C*J.C-1)/14,
               'coarse_K_upper':J.K1+(J.alpha+J.tau)*J.H*J.H}
    constants['w4']=1/(J.C+2*J.C*J.C-1)
    constants['w3']=Q(2,3)*(7-(1-(2*J.C*J.C-1))*constants['w4'])
    need(set(native['constants'])==set(constants),'entire native scalar census')
    for name,value in constants.items():compare(P.const(scalar(native['constants'][name])),P.const(value),'scalar/'+name)
    determinant=J.H*(W**3).imag()*(W**4).imag()*(1-2*J.C)/7
    compare(P.const(scalar(native['odd_determinant'])),P.const(determinant),'odd_determinant')
    need([str(Q(v['squared_skewness']))for v in native['all_seven_stationary_skewness_cases']]
         ==primary['skewness_table'],'all seven skewness ratios')
    # Explicitly excluded: replay-only33-variable baseline, native closed-root
    # maps, coordinate q(V), and differently isolated scalar-margin intervals.
    out={'agent':'six-reviewer-1','role':'independent mathematical reviewer',
         'late_after_primary_seal':True,'native_code_imported':False,
         'whole_map_comparisons':len(names),'names':names,'whole_normalized_maps':maps,
         'all_seven_skewness_cases_match':True}
    data=json.dumps(out,sort_keys=True,separators=(',',':')).encode()
    if args.record:args.record.write_bytes(data+b'\n')
    print(json.dumps({'late_whole_map_comparisons':len(names),'record_bytes':len(data),
                      'record_sha256':hashlib.sha256(data).hexdigest()}))


if __name__=='__main__':main()
