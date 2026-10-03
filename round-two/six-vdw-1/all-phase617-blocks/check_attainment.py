"""Source-only Gauss/literal3703 attainment checker, with construction membership."""
import hashlib
import json


def need(ok,message):
    if not ok:
        raise ValueError(message)


def check():
    q=617;N=3703
    signs={r:sum((j*r)%q>308 for j in range(1,309))%2 for r in range(1,q)}
    results=[]
    for flip in (0,1):
        word=[(signs[n%q] if n%q else int(n==3702))^flip for n in range(N)]
        regular=roots=0
        for n in range(N):
            r=n%q
            if r in (0,1,4,16):
                roots+=1
            else:
                key=sum(w*signs[(r-t)%q] for w,t in zip((8,4,2,1),(0,1,4,16)))
                need(word[n]==((key//8)%2)^flip,'explicit first-character row membership')
                regular+=1
        aps=points=vertical=0
        for step in range(1,(N-1)//6+1):
            for start in range(N-6*step):
                image=[word[start+j*step] for j in range(7)]
                need(len(set(image))>1,'actual monochromatic AP:'+str([start,step]))
                aps+=1;points+=len(image);vertical+=step%617==0
        need(aps==1140833 and points==7985831 and roots==25 and regular==3678 and vertical==1,
             'all literal interval APs and exact family membership')
        results.append({'flip':flip,'N':N,'all_actual_APs':aps,'literal_AP_points':points,
                        'actual_free_roots':roots,'regular_positions':regular,
                        'raw_binary_bytes_sha256':hashlib.sha256(bytes(word)).hexdigest(),
                        'ascii_binary_word_sha256':hashlib.sha256(''.join(map(str,word)).encode()).hexdigest()})
    need(results[0]['raw_binary_bytes_sha256']=='6293a318f5517dd993264ddac3cd6cdd027f6a2119c2b8f743fcb19639030244',
         'known original3703 word retained exactly')
    return {'author':'six-vdw-1','role':'researcher','status':'KNOWN3703_FAMILY_ATTAINMENT_EXACTLY_CHECKED',
            'words':results,'family_membership_proved':True,'historical_word_is_new_bound':False}


if __name__=='__main__':
    print(json.dumps(check(),sort_keys=True))
