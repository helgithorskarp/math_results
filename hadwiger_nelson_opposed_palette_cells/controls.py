"""Cross-check the geometric and constraint reductions; reject damaged evidence."""
from pathlib import Path
from itertools import product,combinations
import copy,json
import model as M
import verify as V

def main():
    cert=json.loads((Path(__file__).resolve().parent/'certificate.json').read_text())
    pp=M.construction();rows=V.coordinates();pair_checks=0
    for i,j in combinations(range(16),2):
        rational=M.norm(M.sub(pp[i],pp[j]))
        integer=V.norm(tuple(x-y for x,y in zip(rows[i],rows[j])))
        V.need(tuple(x*64 for x in rational)==integer,'independent complete norm agreement')
        pair_checks+=1
    # Check the path-elimination relation against unrestricted general search
    # on every one of the 4^4 named input assignments and 12 ordered edge pins.
    ce=M.edges(M.cell());checked=0
    for w in product('0123',repeat=4):
        relation=V.relation(''.join(w))
        for a,b in product('0123',repeat=2):
            if a==b:continue
            pins=[(0,int(a)),(1,int(b))]+[(v,int(c)) for v,c in zip(range(5,9),w)]
            word=M.solve(9,ce,pins)
            V.need((word is not None)==((a,b) in relation),'incorrect cell elimination')
            if word is not None:V.check_word(word,9,ce,pins)
            checked+=1
    corruptions=[]
    d=copy.deepcopy(cert);d['points'][2][0]+=1;corruptions.append(d)
    d=copy.deepcopy(cert);d['points'][2]=d['points'][0];corruptions.append(d)
    d=copy.deepcopy(cert);d['positive'].pop();corruptions.append(d)
    d=copy.deepcopy(cert);d['negative'].pop();corruptions.append(d)
    d=copy.deepcopy(cert);d['positive'][0][1]='0'*16;corruptions.append(d)
    d=copy.deepcopy(cert);d['three_colour_word']='3'+d['three_colour_word'][1:];corruptions.append(d)
    d=copy.deepcopy(cert);d['delete_one_pin_words'].pop();corruptions.append(d)
    d=copy.deepcopy(cert);d['irreducible_example']='01010101';corruptions.append(d)
    d=copy.deepcopy(cert)
    w,word=d['positive'][0]
    # A global permutation remains proper but violates every selected pin.
    d['positive'][0][1]=''.join(str((int(c)+1)%4) for c in word);corruptions.append(d)
    # Preserve the complete terminal domain but interchange the signs of two cases.
    d=copy.deepcopy(cert);yes,word=d['positive'].pop(0);no=d['negative'].pop(0)
    d['negative']=sorted(d['negative']+[yes]);d['positive']=sorted(d['positive']+[[no,word]])
    corruptions.append(d)
    for i,d in enumerate(corruptions):
        try:V.verify(d)
        except ValueError:pass
        else:raise ValueError('accepted damaged certificate '+str(i))
    V.need(V.feasible('00000000'),'monochromatic pairs remain allowed')
    return {'status':'CONTROLS_PASSED','all_pair_norm_comparisons':pair_checks,
            'named_cell_pin_cases':checked,'damaged_certificates_rejected':len(corruptions),
            'monochromatic_input_counterexample':True}
if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
