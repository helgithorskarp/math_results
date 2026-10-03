"""Independent physical witness acceptance and actual semantic damages."""
import json
from itertools import product
import shell as s
import coordinate as c

def verify(spec,a,b,color,pages,violation=False):
    s.need(spec[s.pair(a,b)]==color,'actual RED/BLUE spine must match certificate')
    r,bl=s.rows(spec);actual=sorted((r if color else bl)[a]&(r if color else bl)[b])
    s.need(actual==c.pages(spec,a,b,color),'independent complete physical page sets')
    s.need(sorted(pages)==actual and len(pages)==len(set(pages)),'whole distinct witness pages')
    s.need(a not in pages and b not in pages,'pages are not spine endpoints')
    if violation:s.need(len(pages)>(3 if color else 6),'actual book violation')
    return actual

def check():
    base=s.specification();r,b=s.rows(base);guards=[]
    for a,z,color in [('SX0','SX1',0),('u','T1',0),('u','T2',0),*[(s.X[i],s.X[j],1) for i,j in s.MIXED],*[(sx,t,1) for sx,t in product(['SX0','SX1'],['T1','T2'])]]:
        pages=sorted((r if color else b)[a]&(r if color else b)[z]);verify(base,a,z,color,pages);guards.append([a,z,color,pages])
    witnesses=[]
    spec=s.assign(s.assign(base,'T1',s.X,3),'T2',s.X,3)
    witnesses.append((spec,'T1','T2',0))
    spec=s.assign(s.assign(base,'SX0',s.Q,62),'SX1',s.Q,0)
    witnesses.append((spec,'SX0','SX1',0))
    for mask,ti in product([13,50,60],[1,2]):
        spec=s.assign(s.assign(s.assign(base,f'T{ti}',s.X,mask),f'T{ti}',s.Q,7),'SX0',s.Q,63)
        witnesses.append((spec,'SX0',f'T{ti}',1))
    accepted=[];rejected=[]
    for index,(spec,a,b,color) in enumerate(witnesses):
        rr,bb=s.rows(spec);pages=sorted((rr if color else bb)[a]&(rr if color else bb)[b])
        verify(spec,a,b,color,pages,True);verify(spec,a,b,color,list(reversed(pages)),True)
        accepted.append([index,a,b,color,pages])
        mutations=[('opposite alleged spine color',spec,a,b,1-color,pages),
          ('omitted physical page',spec,a,b,color,pages[1:]),
          ('duplicated physical page',spec,a,b,color,pages+[pages[0]]),
          ('spine endpoint used as page',spec,a,b,color,pages+[a]),
          ('altered actual spine color',{**spec,s.pair(a,b):1-color},a,b,color,pages)]
        p=pages[0];changed={**spec,s.pair(a,p):1-color}
        mutations.append(('altered actual incidence to a page',changed,a,b,color,pages))
        for name,ms,ma,mb,mc,mp in mutations:
            try:verify(ms,ma,mb,mc,mp,True)
            except ValueError as e:rejected.append([index,name,str(e)])
            else:raise ValueError('damaged physical witness accepted')
    s.need(len(accepted)==8 and len(rejected)==48,'complete actual control domain')
    # Invalid use of the union budget outside its premise is concretely rejected.
    a,b,f=62,0,1
    s.need(a|b!=63 and (a&f).bit_count()+(b&f).bit_count()<f.bit_count(),'necessary full-union premise control')
    return {'all11_actual_spine_color_guards':guards,'all8_physical_book_witnesses':accepted,
      'all48_physical_witness_damages_rejected':rejected,'page_order_neutral_controls':8,
      'union_without_full_cover_is_invalid':[a,b,f],'native_target_files_accessed':False}

if __name__=='__main__':print(json.dumps(check(),sort_keys=True,separators=(',',':')))
