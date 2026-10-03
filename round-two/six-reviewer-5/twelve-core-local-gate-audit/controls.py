"""Isolated mathematical damages; successful exits never count as rejection."""
import json,pathlib,tempfile,subprocess,sys,copy
P=pathlib.Path(__file__).resolve().parent
CODE=('enclosure.py','algebra.py','normals.py','jets.py','chart.py','cover.py','primitives.py')

def main():
    data=json.loads((P/'REFERENCE.json').read_text());records=[]
    def case(name,program,edit_data=None,source=None,args=(),valid=False):
        with tempfile.TemporaryDirectory(prefix='damage-',dir=P) as tmp:
            root=pathlib.Path(tmp);d=copy.deepcopy(data)
            if edit_data:edit_data(d)
            for file in CODE:(root/file).write_bytes((P/file).read_bytes())
            if source:
                file,old,new=source;s=(root/file).read_text()
                if s.count(old)!=1:raise ValueError('damage location not unique')
                (root/file).write_text(s.replace(old,new))
            (root/'REFERENCE.json').write_text(json.dumps(d))
            r=subprocess.run([sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(root/program),*args],capture_output=True,timeout=8)
            if (r.returncode==0)!=valid:raise ValueError('wrong semantic damage verdict:'+name+':'+r.stderr.decode())
            records.append(dict(name=name,accepted=r.returncode==0,expected_accepted=valid,rejection=(r.stderr.decode().strip().splitlines()[-1] if r.stderr else '')))
    case('wrong root','normals.py',lambda d:d.update(root_bracket=['3/5','61/100']))
    case('nonunit reference','normals.py',lambda d:d['vectors'][3][0].__setitem__(0,str(__import__('fractions').Fraction(d['vectors'][3][0][0])+1)))
    case('nonunit alternate','normals.py',lambda d:d['alternate_last'][0].__setitem__(0,str(__import__('fractions').Fraction(d['alternate_last'][0][0])+1)))
    case('zero cap normal','cover.py',lambda d:d.update(cap_center=[['0']*5 for _ in range(3)]),args=('K',))
    case('missing original core label','cover.py',lambda d:d['core_labels'].pop(),args=('K',))
    case('wrong completion Gram map','cover.py',lambda d:d['candidate_gram_permutations'][2]['heuristic_matches'][0]['permutation'].__setitem__(slice(0,2),[0,1]),args=('maps',))
    case('wrong cyclic relabeling','cover.py',lambda d:d['known_cyclic_permutation'].__setitem__(slice(0,2),[0,1]),args=('maps',))
    case('wrong q intersection','normals.py',source=('normals.py','for i in (8,9,11)','for i in (8,9,10)'))
    case('wrong p3 normal support','normals.py',source=('normals.py',"(1,4,7)","(1,4,6)"))
    case('reversed chart branch','chart.py',source=('chart.py','rad=-Dt*determinant','rad=Dt*determinant'))
    case('wrong inverse chart polynomial','chart.py',source=('chart.py','F(-115,16)','F(-114,16)'))
    case('wrong frame scalar k','chart.py',source=('jets.py','9*t.square()-2*t-3','9*t.square()+2*t-3'))
    case('wrong multiplication derivative','primitives.py',source=('jets.py','self.d[0]*y.v+self.v*y.d[0]','self.d[0]*y.v-self.v*y.d[0]'))
    case('wrong division derivative','primitives.py',source=('jets.py','self.d[1]*y.v-self.v*y.d[1]','self.d[1]*y.v+self.v*y.d[1]'))
    case('incorrect entire derivative constant','chart.py',source=('chart.py','not norms[0]<15','not norms[0]<1'))
    case('unsupported tripled physical gate','normals.py',source=('normals.py','10*1122*F(2,10**10)','10*1122*F(3,10**10)'))
    case('harmless exact rational representation','normals.py',lambda d:d['vectors'][0][0].__setitem__(0,'2/2'),valid=True)
    case('ignored scout fields','cover.py',lambda d:[c.update(packing_max=-9999) for c in d['candidate_gram_permutations']],args=('maps',),valid=True)
    print(json.dumps(dict(semantic_rejections=sum(not r['accepted'] for r in records),valid_controls=sum(r['accepted'] for r in records),records=records),sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
