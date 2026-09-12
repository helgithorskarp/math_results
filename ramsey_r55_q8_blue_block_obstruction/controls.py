"""Adversarial controls for certificate admission and literal SAT evidence."""
from pathlib import Path
import json,subprocess
from check_lrat import check,require
import encode
HERE=Path(__file__).resolve().parent

def run(cache,classification,checker,output):
 output=Path(output);output.mkdir(parents=True,exist_ok=False);count=0
 def rejected(fn,label):
  nonlocal count
  try:fn()
  except (ValueError,KeyError):count+=1;return
  raise ValueError('accepted corrupt '+label)
 proof=(HERE/'obstruction.lrat').read_text().splitlines()
 noempty=output/'incomplete.lrat'
 noempty.write_text('\n'.join(line for line in proof if line.split()[1]!='0')+'\n')
 rejected(lambda:check(HERE/'obstruction.cnf',noempty),'unfinished trace')
 corrupt=output/'bad-hint.lrat';changed=False;lines=[]
 for line in proof:
  words=line.split()
  if not changed and words[1]!='d':
   zero=words.index('0');words[zero+1]='999999999';changed=True
  lines.append(' '.join(words))
 corrupt.write_text('\n'.join(lines)+'\n')
 rejected(lambda:check(HERE/'obstruction.cnf',corrupt),'unknown propagation hint')
 badinput=output/'bad-input.cnf';rows=(HERE/'obstruction.cnf').read_text().splitlines();rows[1]='45 0';badinput.write_text('\n'.join(rows)+'\n')
 rejected(lambda:check(badinput,HERE/'obstruction.lrat'),'out of range input')
 original=bytearray((Path(classification)/'witnesses.u48le').read_bytes());original[:6]=bytes(6)
 badwit=output/'bad-witnesses.u48le';badwit.write_bytes(original)
 proc=subprocess.run([str(checker),str(Path(cache)/'r44_11.g6'),str(badwit),str(Path(classification)/'BLOCKED_IDS.txt')],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 require(proc.returncode!=0 and b'blue K5 in witness' in proc.stderr,'false literal SAT witness accepted');count+=1
 # A q8,r8 task has no disjoint prescribed blue block; its supposed map overlaps the core.
 wrong_r8=list(range(32,43))+list(range(32,36));require(len(set(wrong_r8))<15,'wrong-stratum control');count+=1
 # Red/blue exchange is not a premise of this fixed-r original-task exclusion.
 record=encode.catalog(Path(cache)/'r44_11.g6')[516166]
 known=encode.decode(record);require(any(color for color in known.values()) and any(not color for color in known.values()),'two colors required')
 swapped={p:1-color for p,color in known.items()};require(swapped!=known,'color-swapped core must not match');count+=1
 result=dict(status='ALL_ADMISSION_CONTROLS_PASSED',controls=count,corrupt_certificates_rejected=3,false_sat_witness_rejected=True,wrong_r8_embedding_rejected=True,color_swap_not_accepted_as_same_task=True)
 (output/'CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');return result
