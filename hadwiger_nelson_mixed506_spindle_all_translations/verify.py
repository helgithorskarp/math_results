"""Regenerate and check the finite certificate; see PROOF.md for all translations."""
from pathlib import Path
import argparse,json,subprocess
import geometry as G
import coverage as C

def native_screen(tables,work,binary):
    inp=work/'modular_input.txt';out=work/'modular_survivors.txt'
    with inp.open('w') as f:
        f.write(f'{len(tables[0][1])} {len(tables[0][2])} {len(tables)}\n')
        for p,xx,yy,acc in tables:
            f.write(str(p)+'\n'+' '.join(str(int(a)) for a in acc)+'\n')
            for x,y in xx+yy:f.write(f'{x} {y}\n')
    result=subprocess.run([str(binary.resolve()),str(inp),str(out),'0',str(len(tables[0][1]))],capture_output=True,text=True,check=True)
    record=json.loads(result.stdout);pairs=[tuple(map(int,s.split())) for s in out.read_text().splitlines()]
    G.require(record['begin']==0 and record['end']==len(tables[0][1]) and record['survivors']==len(pairs),'incomplete native screen')
    G.require(pairs==sorted(set(pairs)),'native survivor stream is not canonical')
    return record['stages'],pairs

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--work',type=Path,required=True);parser.add_argument('--native',type=Path)
    args=parser.parse_args();args.work.mkdir(parents=True,exist_ok=False)
    B,V,EB,EV,X,Y,I,J=G.data();tables=G.prepare(X,Y)
    stages,survivors=native_screen(tables,args.work,args.native) if args.native else G.screen(tables)
    (args.work/'screen.json').write_text(json.dumps({'stages':stages,'survivors':survivors})+'\n')
    positive,negative,zero=G.classify(X,Y,survivors)
    proposals=G.positive_json(positive)
    (args.work/'positive.json').write_text(json.dumps(proposals)+'\n')
    (args.work/'negative.json').write_text(json.dumps(negative)+'\n')
    del tables
    rows,projection=G.project(B,V,I,J,X,Y,positive)
    cover=C.cover(rows,C.libraries(B,V,EB,EV),args.work/'translations.jsonl')
    result={'rotation':'(7+i sqrt(15))/8','source_sizes':[292,214],'source_edges':[len(EB),len(EV)],
            'difference_counts_including_zero':[len(X),len(Y)],'nonzero_pair_domain':len(X)*len(Y)-1,
            'modular_stages':stages,'modular_survivors':len(survivors),'modular_survivor_sha256':G.digest(survivors),
            'positive_difference_pairs':len(positive),'relative_circle_centres':sum(len(hs) for _,_,hs in positive),
            'positive_centres_sha256':G.digest(proposals),'negative_pairs':len(negative),'negative_pair_sha256':G.digest(negative),
            'zero_pair':zero[0],**projection,**cover,'all_translations_requires_PROOF_md_and_audit':True}
    (args.work/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
