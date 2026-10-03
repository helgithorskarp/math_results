"""Complete primary fixture comparison, exact types; -O retains all checks."""
import json,sys,hashlib
from pathlib import Path
import core,controls

def strict_equal(actual,expected,path='root'):
    core.need(type(actual) is type(expected),'record type '+path)
    if isinstance(actual,dict):
        core.need(set(actual)==set(expected),'record keys '+path)
        for k in actual:strict_equal(actual[k],expected[k],path+'.'+k)
    elif isinstance(actual,list):
        core.need(len(actual)==len(expected),'record length '+path)
        for i,(a,b) in enumerate(zip(actual,expected)):strict_equal(a,b,path+'.'+str(i))
    else:core.need(actual==expected,'record value '+path)

def build():
    return {'core':core.build(),'controls':controls.build()}

def object_pairs(pairs):
    result={}
    for k,v in pairs:
        core.need(k not in result,'duplicate JSON key')
        result[k]=v
    return result

if __name__=='__main__':
    actual=build()
    expected=json.loads(Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).with_name('EXPECTED.json')).read_text(),object_pairs_hook=object_pairs)
    strict_equal(actual,expected)
    print(json.dumps({'whole_sha256':hashlib.sha256(core.canonical(actual)).hexdigest(),
                      'margins':len(actual['core']['margins']),'maps':len(actual['core']['maps']),
                      'phases':len(actual['core']['all9_phase_maps']),'controls':len(actual['controls'])},sort_keys=True))
