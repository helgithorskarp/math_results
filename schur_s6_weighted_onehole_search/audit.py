"""Independent direct audit of the one-hole and complete Schur-six words."""
from itertools import permutations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def defects(word):
    assert len(word)==537 and set(word)<=set('123456?')
    return [(x,z-x,z) for z in range(2,538)
            for x in range(1,z//2+1)
            if word[x-1]!='?' and word[x-1]==word[z-x-1]==word[z-1]]


def distance(a,b):
    assert len(a)==len(b)==537
    return min(sum(a[i]!=p[int(b[i])-1] for i in range(537))
               for p in permutations('123456'))


def main():
    read=lambda name:(HERE/name).read_text(encoding='ascii').strip()
    partial=read('partial35.txt')
    assert [i for i,c in enumerate(partial,1) if c=='?']==[35]
    assert defects(partial)==[]
    completion={c:len(defects(partial.replace('?',c))) for c in '123456'}
    assert completion=={'1':31,'2':47,'3':41,'4':43,'5':51,'6':41}
    assert read('completed31.txt')==partial.replace('?','1')
    three=read('best3.txt');two=read('best2.txt')
    assert defects(three)==[(1,1,2),(1,2,3),(1,55,56)]
    assert defects(two)==[(1,1,2),(1,2,3)]
    previous=read('../schur_s6_distant_two_defect_search/best2.txt')
    assert distance(two,previous)==398
    sources=json.loads(read('../schur_s6_multi_alignment_recombination/sources.json'))
    distances={name:distance(two,row['word']) for name,row in sources.items()}
    assert distances=={'W':422,'190':430,'359':416,'best3':426,'347':432}
    print(json.dumps({'hole':[35], 'partial_defects':0,
                      'direct_completion_defects':completion,
                      'best3_defects':defects(three),'best2_defects':defects(two),
                      'distance_previous_two_defect':398,
                      'distance_prior_words':distances},indent=2,sort_keys=True))


if __name__=='__main__':main()
