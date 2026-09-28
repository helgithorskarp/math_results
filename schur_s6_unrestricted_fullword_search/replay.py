"""Replay the 10-million-step full-colour local-search checkpoint."""
import argparse
import re
import subprocess
from pathlib import Path

from check import defects

HERE=Path(__file__).resolve().parent


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--binary',type=Path,required=True)
    a=p.parse_args()
    command=[str(a.binary),str(HERE/'completed11.txt'),'20260930',
             '100','100000','20','3','15','7']
    result=subprocess.run(command,capture_output=True,text=True,check=True)
    final=re.search(r'^FINAL steps=(\d+) defects=(\d+) direct=(\d+)$',
                    result.stdout,re.M)
    word=re.search(r'^BEST_COLOR ([1-6]{537})$',result.stdout,re.M)
    assert final and tuple(map(int,final.groups()))==(10000000,4,4)
    assert word and word.group(1)==(HERE/'best4.txt').read_text(encoding='ascii').strip()
    assert defects(word.group(1))==[(1,1,2),(1,2,3),(4,4,8),(4,5,9)]
    print('PASS replay_steps=10000000 defects=4 direct=4 exact_word_match=yes')


if __name__=='__main__':main()
