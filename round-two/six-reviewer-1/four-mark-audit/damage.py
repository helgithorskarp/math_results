"""Designated semantic defects; each must fail at its stated mathematical gate."""
import json,signal,sys
from pathlib import Path
from certificate import verify
from geometry import construct
from blocks import verify_symbolic
signal.alarm(45)
GATES={
 'denominator-zero':'polynomial denominator',
 'duplicate-exponent':'all coefficient exponents',
 'domain-wrong':'whole four-mark data domain and attribution',
 'ordered-coverage':'entire ordered Schur coverage',
 'pivot-link':'whole pivot working links',
 'old-row-drop':'complete coefficient identity failed',
 'Schur-sign':'complete coefficient identity failed',
 'empty-row':'actual empty negative-row-sum Gram',
 'light-mean-omitted':'all original physical five-block metric entries',
 'light-dual':'every original dual score and actual empty',
 'star-census':'all original star sizes',
 'deleted-inverse-row':'every original inverse equation including deleted rows',
 'outside-empty-lift':'complete original centered outside-line witness',
 'prototype-count':'whole generic prototype coefficient identity'}
fixture=sys.argv[1]
if fixture not in GATES:raise ValueError('unknown designated fixture')
try:
    if fixture in ['denominator-zero','duplicate-exponent','domain-wrong','ordered-coverage','pivot-link']:
        data=json.loads(Path(__file__).with_name('CERTIFICATE_INPUT.json').read_text())
        if fixture=='denominator-zero':data['polynomials'][0]['denominator']=0
        elif fixture=='duplicate-exponent':data['polynomials'][0]['terms'].append(data['polynomials'][0]['terms'][0])
        elif fixture=='domain-wrong':data['domain']='u,v,w>=0; q=9+w'
        elif fixture=='ordered-coverage':data['updates'][0],data['updates'][1]=data['updates'][1],data['updates'][0]
        elif fixture=='pivot-link':data['rows'][0]['pivot']=1
        verify(data=data)
    elif fixture in ['old-row-drop','Schur-sign']:verify(defect=fixture)
    elif fixture=='prototype-count':verify_symbolic(defect=fixture)
    else:construct(4,3,2,defect=fixture)
except ValueError as e:
    if str(e)!=GATES[fixture]:raise ValueError('rejection occurred at an unexpected gate: '+str(e))from e
    print(json.dumps({'fixture':fixture,'rejected':True,'gate':str(e)},sort_keys=True))
    raise SystemExit(0)
raise ValueError('designated mathematical corruption survived')
