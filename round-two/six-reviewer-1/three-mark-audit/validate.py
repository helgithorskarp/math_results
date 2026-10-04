"""Meaningful failures at coefficient and original-set trust boundaries."""
from pathlib import Path
import json,copy,hashlib,signal,sys
HERE=Path(__file__).resolve().parent
for n,h in json.loads((HERE/'PRIMARY_SEAL.json').read_text())['files'].items():
    if hashlib.sha256((HERE/n).read_bytes()).hexdigest()!=h:raise ValueError('preimport primary source binding')
sys.path.insert(0,str(HERE))
from certificate import verify
from geometry import construct

def rejects(name,work):
    try:work()
    except ValueError as e:return {'fixture':name,'rejected':True,'message':str(e)}
    raise ValueError('invalid fixture accepted: '+name)

if __name__=='__main__':
    signal.alarm(45);raw=json.loads((HERE/'CERTIFICATE_INPUT.json').read_text());out=[]
    for defect in ['denominator-zero','duplicate-exponent','negative-final-pivot','ordered-update','old-row-drop','Schur-sign']:
        data=copy.deepcopy(raw)
        if defect=='denominator-zero':data['polynomials'][0]['denominator']=0
        elif defect=='duplicate-exponent':data['polynomials'][0]['terms'].append(copy.deepcopy(data['polynomials'][0]['terms'][0]))
        elif defect=='negative-final-pivot':
            index=data['fields'][data['rows'][4]['pivot']]['numerator']
            for e in data['polynomials'][index]['terms']:
                if e[0]==[0,0,0]:e[1]=str(-int(e[1]));break
        elif defect=='ordered-update':data['updates'][-1]['i']=3
        out.append(rejects(defect,lambda:verify(data,defect)))
    for defect in ['empty-row','light-dual','light-mean-omitted','star-census']:
        out.append(rejects(defect,lambda:construct(3,3,2,defect)))
    Path(sys.argv[1]).write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print('all10 distinct invalid mathematical fixtures rejected')
