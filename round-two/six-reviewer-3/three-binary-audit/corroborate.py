"""Direct distinct-rank scalar check of full cubes, separately from bit columns."""
import sys,json
from engine import *

def run(primary,cover,kind,start,stop):
    products=[];assignments=0
    if kind=='base':
        items=[]
        for b in cover['base']:
            for rec in b['records']:items.append((Q,rec))
        items=items[start:stop]
        for word,expected in items:
            actual,output=scalar(word,expected[0],expected[1]);require(actual==expected,'baseline physical scalar record');_,bits,free=replay(word,expected[0],expected[1]);require(output==list(rows(bits,len(free))),'baseline entire literal cubes')
            assignments+=len(output);products.append({'record':actual,'whole_rows_sha256':digest(output)})
    else:
        expected={}
        for b in primary['actual_bindings']:
            word=Q+gates(b['word'])+(tuple(sorted((8,b['head']))),)+ (() if b['tail'] is None else gates(b['tail']))
            for rec in b['result'].get('records',[b['result'].get('record')]):
                if rec is not None:expected[(word,rec[0],rec[1])]=rec
        for cube in primary['physical_cubes'][start:stop]:
            word=gates(cube['word']);lo=cube['low'];hi=cube['high'];rec,output=scalar(word,lo,hi)
            require(rec==expected[(word,lo,hi)],'actual binding whole scalar record');require(digest(output)==cube['whole_rows_sha256'],'whole scalar physical cube differs')
            assignments+=len(output);products.append({'word':word,'record':rec,'whole_rows_sha256':digest(output)})
    return {'kind':kind,'slice':[start,start+len(products)],'full_cubes':len(products),'assignments':assignments,'products':products}
if __name__=='__main__':
    p=json.load(open(sys.argv[1]));c=json.load(open(sys.argv[2]));out=run(p,c,sys.argv[3],int(sys.argv[4]),int(sys.argv[5]));open(sys.argv[6],'w').write(json.dumps(out,separators=(',',':'),sort_keys=True)+'\n');print(json.dumps({k:out[k] for k in ('kind','slice','full_cubes','assignments')}));print('whole_record_sha256',digest(out))
