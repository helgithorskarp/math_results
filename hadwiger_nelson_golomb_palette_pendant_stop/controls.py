#!/usr/bin/env python3
import copy,json
import verify as v

def main():
    cert=json.loads((v.BASE/'certificate.json').read_text());expected=json.loads((v.BASE/'EXPECTED.json').read_text())
    v.need(v.verify(cert)==expected,'valid baseline must pass')
    mutants=[]
    x=copy.deepcopy(cert);w=list(x['four_word']);w[12]=w[2];x['four_word']=''.join(w);mutants.append(('private old-new unit edge violated',x))
    x=copy.deepcopy(cert);x['forbidden_terminal_word']=cert['four_word'][:2]+''.join(cert['four_word'][i] for i in v.TERM[2:]);mutants.append(('extendible prescription claimed forbidden',x))
    x=copy.deepcopy(cert);x['proper_five_same_terminals']='01212120230101';mutants.append(('proper word with changed marked terminals',x))
    rejected=[]
    for label,c in mutants:
        try:v.verify(c)
        except ValueError:rejected.append(label)
        else:raise ValueError('corruption accepted: '+label)
    print(json.dumps({'valid_baseline':True,'rejected_semantic_corruptions':rejected},indent=2))
if __name__=='__main__':main()
