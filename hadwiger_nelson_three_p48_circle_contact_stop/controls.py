"""Reject malformed semantic certificates, not merely checksum changes."""
import copy,json
from pathlib import Path
from verify import reconstruct,check_certificate,times,rad,num,need

def main():
    need(times(rad(33),rad(105))=={385:3},'squarefree product calibration')
    need(times(rad(1155),rad(1155))==num(1155),'radical square calibration')
    g=reconstruct();c=json.loads(Path(__file__).with_name('certificate.json').read_text());check_certificate(c,g)
    bad={}
    b=copy.deepcopy(c);b['four_word']=b['four_word'][:-1];bad['short_four_word']=b
    b=copy.deepcopy(c);b['four_word']='4'+b['four_word'][1:];bad['fifth_colour_in_four_word']=b
    b=copy.deepcopy(c);i,j=g['edges'][0];w=list(b['four_word']);w[j]=w[i];b['four_word']=''.join(w);bad['monochromatic_unit_edge']=b
    b=copy.deepcopy(c);b['five_word']='5'+b['five_word'][1:];bad['sixth_colour_in_five_word']=b
    for key in ['vertices','edges','extra_edges']:
        b=copy.deepcopy(c);b['expected'][key]+=1;bad['wrong_'+key]=b
    b=copy.deepcopy(c);b['expected']['coordinate_sha256']='0'*64;bad['wrong_coordinate_identity']=b
    b=copy.deepcopy(c);b['expected']['moser'][0]=b['expected']['moser'][1];bad['collapsed_moser_role']=b
    rejected=[]
    for name,b in bad.items():
        try:check_certificate(b,g)
        except ValueError:rejected.append(name)
        else:raise RuntimeError('accepted corruption '+name)
    print(json.dumps({'valid_certificate_accepted':True,'rejected_corruptions':rejected},indent=2,sort_keys=True))
if __name__=='__main__':main()
