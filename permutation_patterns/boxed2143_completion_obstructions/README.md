# Boxed2143 completion obstructions

These are two exact partial research scopes, authored by Theo
(literature-researcher-4) and separately checked by Lyra
(literature-researcher-2). The full bounded-exponential growth decision remains
UNSOLVED. These are internal team checks, with no novelty or external peer
review claim. No completion of the full target is asserted.

`simple_root/` records the simple input3164275 for which all56 allowed
132-avoiding adjacent-root scaffolds fail, together with a valid nonadjacent
completion and complete shorter-simple-input controls. Its conditional
factorial bridge concerns ALL simple permutations, distinct from simple
boxed avoiders. It refutes that root restriction, leaving unrestricted
completion open. The original author and review bytes retain their scope.

`signed_rectangle/` proves uniformly that a selected quadruple is boxed2143
iff its empty-rectangle graph is a K4 with exactly two negative edges. The
rectangle graphs and strong-Bruhat cover criterion are prior literature.
The exact32541/34521 degree tie rejects strict ascent; it leaves avoiding
maximizer existence and plateau-aware repair open. Neither edge counts nor
the geometric correspondence supplies a growth bound.

Primary target: Kitaev--Qiu--Xu, arXiv2609.13764v1, Section7:
https://arxiv.org/html/2609.13764v1 . Source Conjecture7.4 permits arbitrary
scaffolds; the narrower failed methods here do not refute it.
The all-simple asymptotic is Albert--Atkinson--Klazar, JIS6(2003), Article
03.4.4, Theorem5/Observation8:
https://cs.otago.ac.nz/research/publications/oucs-2003-05.pdf .
Rectangle/strong-Bruhat context:
https://www.mat.univie.ac.at/~slc/s/s53adinroi.pdf and
https://people.maths.ox.ac.uk/keevash/papers/permutation-graphs-journal.pdf .
The two proofs and full written reviews give their precise mathematical use.

Reproduce using CPython3.11+ and its standard library, one process/thread:

```
cd simple_root
python3 -B simple_completion_probe_v1.py --output /tmp/simple-root-author.json
python3 -B check_theo_simple_root.py > /tmp/simple-root-reviewer.json
cd ../signed_rectangle
python3 -B bruhat_completion_probe_v1.py --output /tmp/signed-rectangle-author.json
python3 -B check_theo_bruhat.py > /tmp/signed-rectangle-reviewer.json
```

Every author proof, code, certificate, MANIFEST and full written review is
byte-identical to its separately accepted version. Historical review manifests
refer to the original working-directory layout. ORIGINAL_REVIEWER.py retains
the original checker; the runnable checker changes only its packet-directory
default to the containing directory. The simple-root reviewer's sole helper
function is extracted byte-for-byte from its original dependency, omitting
unused controls. PORTABILITY_EDITS.json pins each change. PORTABLE_REPLAY.json
records complete deterministic replay agreement, excluding runtime/RSS and
the intentionally changed checker hash. SOURCE_MANIFEST.json pins public
source bytes; it does not serve as a correctness certificate.
