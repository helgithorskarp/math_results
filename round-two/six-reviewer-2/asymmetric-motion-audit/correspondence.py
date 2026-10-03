"""LATE native correspondence. No native module imported. Independent seals precede this file."""
from pathlib import Path
import json,sys,hashlib
from fractions import Fraction as F
from second import H,R,W,J,c,d,sf,hf,require,const,plus,times,mulnum

def native_field(v):
    require(type(v)is list and len(v)==2 and all(type(a)is list and len(a)==6 for a in v),'native complete paired basis')
    require(all(type(q)is str and str(F(q))==q for a in v for q in a),'native canonical rationals')
    return H([F(q)for a in v for q in a])
def native_series(v):
    require(type(v)is list,'native series');ans=const(0);orders=[]
    for n,rows in v:
        require(type(n)is int and 0<=n<=4 and n not in orders,'native unique whole series order');orders.append(n);coefs={}
        for ex,field in rows:
            require(ex in [[0,0],[1,0],[0,1]]and tuple(ex)not in coefs,'native affine parameter term');coefs[tuple(ex)]=native_field(field)
        ans[n]=R(coefs)
    return ans

def compare(primary,native):
    counts={'whole_series':0,'affine_field_vectors':0,'rational_coordinates':0,'scalar_field_vectors':0};rows=[]
    def same(name,a,b):
        require(a==b,'LATE full native correspondence '+name);rows.append({'name':name,'whole_jet':[[x.enc()for x in a]]})
        counts['whole_series']+=1;counts['affine_field_vectors']+=15;counts['rational_coordinates']+=180
    for key,pkey,n in [('whole_polynomial','full_primitive_coefficients',10),('all_nine_roots','all_nine_parameter_root_jets',9),('all_nine_half_normals','all_nine_parameter_half_normals',9)]:
        require(len(primary[key])==len(native[pkey])==n,'all native physical labels')
        for j in range(n):same(key+'/'+str(j),sf(primary[key][j]),native_series(native[pkey][j]))
    same('full objective',sf(primary['whole_first_objective']),native_series(native['complete_first_power_objective']))
    ms,bs=map(hf,primary['closing_parameters'])
    def fixed(z):return[R(a.at(ms,bs))for a in sf(z)]
    for key,pkey in [('all_nine_roots','all_nine_fixed_root_jets'),('all_nine_half_normals','all_nine_fixed_half_normals')]:
        require(len(native[pkey])==9,'every fixed native original')
        for j in range(9):same('fixed '+key+'/'+str(j),fixed(primary[key][j]),native_series(native[pkey][j]))
    same('fixed entire objective',fixed(primary['whole_first_objective']),native_series(native['fixed_first_power_objective']))
    mean=sf(primary['critical_mean']);nuL=plus(sf(primary['critical_large']),mulnum(mean,-1));nuS=plus(sf(primary['critical_small']),mulnum(mean,-1))
    for n,key in [(2,'T'),(3,'U3')]:
        def pw(z):
            acc=const(1)
            for _ in range(n):acc=times(acc,z)
            return acc
        same('complete centered moment '+key,plus(pw(nuL),mulnum(pw(nuS),7)),native_series(native['centered_moments'][key]))
    iv=(8*c*c-8*c+2)/3;lam=12*(1+c);k=-7*(1+2*c)/18;y=iv/3;x=F(2,3)-y
    r3=sf(primary['all_nine_half_normals'][3])[4].v.get((0,0),H());r4=sf(primary['all_nine_half_normals'][4])[4].v.get((0,0),H())
    constants={'c':c,'d':d,'y':y,'x':x,'lambda':lam,'k':k,'g':48*k,'C':F(8,3)+y,'det':12*(c+d),'R3':r3,'R4':r4,'M':ms,'b':bs,'K_eta':hf(primary['closing_second_coefficient'])}
    require(set(native['constants'])==set(constants),'all native scalar constants')
    for name,value in constants.items():
        require(value==native_field(native['constants'][name]),'LATE full native constant '+name);rows.append({'constant':name,'entire_field_vector':value.enc()});counts['scalar_field_vectors']+=1;counts['rational_coordinates']+=12
    raw=json.dumps(rows,sort_keys=True,separators=(',',':')).encode()
    return {'status':'COMPLETE_LATE_NATIVE_CORRESPONDENCE','timing':'after independent seven-file seal/native exposure; primary files untouched','counts':counts,'entire_compared_record_bytes':len(raw),'entire_compared_record_sha256':hashlib.sha256(raw).hexdigest(),'native_imported':False,'fixture_hash_is_mathematical_premise':False}
if __name__=='__main__':
    require(len(sys.argv)==3,'usage: correspondence.py PRIMARY NATIVE_EXPECTED')
    print(json.dumps(compare(json.loads(Path(sys.argv[1]).read_text()),json.loads(Path(sys.argv[2]).read_text())),sort_keys=True,separators=(',',':')))
