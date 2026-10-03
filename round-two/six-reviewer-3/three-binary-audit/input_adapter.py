"""Post-seal declared instance decoding. No native executable imported.
Native tail slot order is not a written mathematical premise: all three own
balanced functions are matched bijectively to the three declared witnesses.
"""
from engine import *

def decode(w):
    kind={'DIRECT_COST':'cost','TIGHT_MARKED_PORT_LOCK':'marked','TIGHT_FREE_CUT':'cut','SEMANTIC_WEIGHTED_MASS':'mass'}[w['kind']]
    d={'kind':kind}
    if kind=='mass':
        d['records']=w['distinct_tag_witness_records'];l,h=w['original_counts'];k=N-l-h
        require(w['imported_size']==FLOOR[k] and w['ceiling']==1<<(44-FLOOR[k]),'native mass floor/ceiling')
        require(all((r[0].bit_count(),r[1].bit_count())==(l,h) for r in d['records']),'native family')
        require(sum(1<<(r[4]+r[5]) for r in d['records'])==w['mass'],'native advertised mass')
    else:
        d['record']=w['record'];k=N-(w['record'][0]|w['record'][1]).bit_count();require(w['imported_size']==FLOOR[k],'native floor')
        if kind in ('marked','cut'):
            d.update(port=w['physical_port'],input=w['full_Boolean_witness'])
            require(w['actual_bit'] in (0,1) and w['sorted_bit'] in (0,1) and w['actual_bit']!=w['sorted_bit'],'native wrong-rank bits')
    return d

def confirm_rank_fields(word,native):
    if native['kind'] in ('TIGHT_MARKED_PORT_LOCK','TIGHT_FREE_CUT'):
        q=native['physical_port'];inp=native['full_Boolean_witness'];out=binary_output(word,inp);expected=((1<<inp.bit_count())-1)<<(N-inp.bit_count())
        require((out>>q&1)==native['actual_bit'] and (expected>>q&1)==native['sorted_bit'],'native wrong-rank bit values')

def check(word,native):
    d=decode(native);result=assess(word,d);confirm_rank_fields(word,native);return result
