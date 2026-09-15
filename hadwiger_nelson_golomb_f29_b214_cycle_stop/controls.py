#!/usr/bin/env python3
import copy,json
import verify as v

def main():
 c=json.loads((v.HERE/'certificate.json').read_text());r=v.run(c);rejected=[]
 def reject(name,d):
  try:v.run(d)
  except ValueError:rejected.append(name)
  else:raise ValueError('corruption accepted: '+name)
 d=copy.deepcopy(c);d['proper4']='0'*250;reject('improper whole colouring',d)
 d=copy.deepcopy(c);d['golomb_equal_template']=d['golomb_different_template'];reject('wrong endpoint relation on equal template',d)
 d=copy.deepcopy(c);d['f29_equal_template']='0'*29;reject('improper F29 extension template',d)
 d=copy.deepcopy(c);d['connected_input_equal_tips_word']='0'*38;reject('false input compatibility witness',d)
 rows,edges,maps,own,_=v.geometry();gw,fw=v.extend(c,'1','0');values=dict(zip(maps[0],gw));values.update(zip(maps[1],fw));G=set(maps[0])-set(maps[1]);F=set(maps[1])-set(maps[0]);extra=next((a,b) for a in sorted(G) for b in sorted(F) if values[a]==values[b] and (a,b) not in edges and (b,a) not in edges)
 try:v.proper(gw+fw,39,[(maps[0].index(extra[0]),10+maps[1].index(extra[1]))])
 except ValueError:rejected.append('hypothetical private contact invalidates extension')
 else:raise ValueError('extra contact not detected')
 print(json.dumps({'status':'CONTROLS_PASSED','valid_result':r['status'],'semantic_corruptions_rejected':rejected,'hypothetical_extra_edge':extra},indent=2,sort_keys=True))
if __name__=='__main__':main()
