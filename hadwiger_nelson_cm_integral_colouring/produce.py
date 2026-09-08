"""Regenerate compact fixtures and finite functional certificates; no solver."""
import json
from pathlib import Path
from colour import cyclotomic, functional, fixture

HERE=Path(__file__).resolve().parent
CONDUCTORS=sorted(set([1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,20,21,24,
    25,27,28,30,32,33,35,36,40,42,49,60,64,72,84,90,105,120,132,210,
    330,420,660,840,1260,2310]))

def main():
    certificates=[{'n':n,'cyclotomic_polynomial':cyclotomic(n),
                    'functional':functional(n)} for n in CONDUCTORS]
    (HERE/'CERTIFICATES.json').write_text(json.dumps(certificates,separators=(',',':'))+'\n')
    graph=fixture()
    (HERE/'FIXTURE.json').write_text(json.dumps(graph,separators=(',',':'))+'\n')
    print(json.dumps({'functional_certificates':len(certificates),
                      'fixture_vertices':len(graph['points']),
                      'fixture_strict_edges':len(graph['edges'])}))
if __name__=='__main__':main()
