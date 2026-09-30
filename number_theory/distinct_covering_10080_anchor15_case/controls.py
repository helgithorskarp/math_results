"""Reject malformed proof input and verify that transports must fix anchors."""
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
import json
from pathlib import Path
import check


def main():
    original=json.loads(Path(__file__).with_name('certificate.json').read_text())
    rejected=[]
    def bad(name,mutate):
        fixture=deepcopy(original);mutate(fixture)
        try:
            with redirect_stdout(StringIO()):check.verify(fixture)
        except (ValueError,KeyError,TypeError):
            rejected.append(name);return
        raise ValueError('Accepted malformed fixture: '+name)
    bad('wrong_period',lambda x:x.update(period=20160))
    bad('missing_case',lambda x:x['trees'].pop())
    bad('pending_leaf',lambda x:x['trees'][0]['nodes'][-1].update(status='pending'))
    bad('missing_advertised_child',lambda x:x['trees'][0]['nodes'].pop())
    bad('duplicate_node',lambda x:x['trees'][0]['nodes'].append(deepcopy(x['trees'][0]['nodes'][0])))
    def weighted_change(document,kind):
        n=next(n for n in document['trees'][0]['nodes'] if n['status']=='weighted')
        if kind=='false_total':n['payload']['demand']+=1
        if kind=='negative_weight':n['payload']['boxes'][0][-1]=-1
        if kind=='used_resource_pair':n['payload']['pairs']=[[8,24]]
    for kind in ('false_total','negative_weight','used_resource_pair'):
        bad(kind,lambda x,kind=kind:weighted_change(x,kind))
    try:check.coordinate_transport(2,32,4,1,3,((4,1),))
    except ValueError:rejected.append('transport_moves_fixed_anchor')
    else:raise ValueError('Accepted a transport moving a fixed anchor')
    print(json.dumps({'malformed_rejections':len(rejected),'controls':rejected},sort_keys=True))


if __name__=='__main__':main()
