"""Data-only comparison of every labeled physical seed and repaired entry."""
import argparse,json,pathlib,hashlib

def need(ok,why):
    if not ok:raise ValueError(why)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('native',type=pathlib.Path);ap.add_argument('ours',type=pathlib.Path);ap.add_argument('--damage');a=ap.parse_args();data=json.loads(a.native.read_text());counts=0;original=0;rows=[]
    if a.damage=='vertex':data[0]['vertices'][1]=999999
    if a.damage=='repaired-entry':data[0]['repaired_M'][0][0]='0'
    for p in data:
        n,h=p['n'],p['h'];o=json.loads((a.ours/f'literal-{n}-{h}.json').read_text());N=o['N']
        need(len(p['vertices'])==len(set(p['vertices']))==N and set(p['vertices'])==set(o['vertices']),'every original actual set')
        perm=[p['vertices'].index(x) for x in o['vertices']]
        for i in range(N):
            for j in range(N):need(o['repaired_M'][i][j]==p['repaired_M'][perm[i]][perm[j]],'every repaired original entry');original+=1
        for i in range(N-1):
            for j in range(N-1):need(o['seed'][i][j]==p['seed'][perm[i+1]-1][perm[j+1]-1],'every original seed core entry');counts+=1
        need(o['kappa']==p['fixture']['kappa'] and o['delta']==p['fixture']['delta'],'exact source repair parameters')
        rows.append(dict(n=n,h=h,N=N,all_actual_vertices_and_entries=True,kappa=o['kappa'],delta=o['delta']))
    print(json.dumps(dict(actual_agent='six-reviewer-5',role='independent reviewer',all_fixture_positions=True,seed_core_positions=counts,repaired_original_positions=original,fixtures=rows),sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
