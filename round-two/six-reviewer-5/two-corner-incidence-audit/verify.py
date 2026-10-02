"""Whole owned certificate verification, including ten semantic damages."""
import copy,json,pathlib,hashlib
import independent as I

def verify(data):
    wanted=I.build()
    I.need(data==wanted,'whole exact independent evidence differs')
    return wanted

def damages(data):
    tests=[]
    def make(name,edit):
        d=copy.deepcopy(data);edit(d);tests.append((name,d))
    make('omit closure word',lambda d:d['closures'].pop())
    make('alter literal closing coefficient',lambda d:d['closures'][0]['g'].__setitem__(0,'17'))
    make('lose closed endpoint',lambda d:d['closures'][0]['sturm'][1]['endpoint_values'].__setitem__(0,'0'))
    make('invent root-free larger band',lambda d:d['closures'][6]['sturm'][2].__setitem__('distinct_roots',0))
    make('alter final vector',lambda d:d['closures'][0]['final_vector'][0].__setitem__(0,'19'))
    make('omit oriented port',lambda d:d['ports'].pop())
    make('alter reversed seam identification',lambda d:d['ports'][0]['seams'][0][1].__setitem__(1,1))
    make('alter boundary dart successor',lambda d:d['ports'][0]['successor'][0][1].__setitem__(1,2))
    make('invent four-cap',lambda d:next(c for a in d['caps'] for c in a['caps'] if c['length']==4)['valid'].append({'triangles':[]}))
    make('alter middle annulus triangle count',lambda d:d['residuals'][0].__setitem__('middle_triangles',10))
    for name,d in tests:
        try:verify(d)
        except ValueError:continue
        raise ValueError('damage accepted: '+name)
    return [name for name,d in tests]

def main():
    p=pathlib.Path(__file__).with_name('EVIDENCE.json');raw=p.read_bytes();data=json.loads(raw)
    verify(data);bad=damages(data)
    print(json.dumps(dict(verified=True,sha256=hashlib.sha256(raw).hexdigest(),words=len(data['closures']),ports=len(data['ports']),cap_boundaries=54,whole_comparison=True,rejected=bad),sort_keys=True))
if __name__=='__main__':main()
