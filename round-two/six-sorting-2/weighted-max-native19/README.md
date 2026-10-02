Native N19 size44 completion is equivalent to sorting a specified244-state
eleven-wire image with at most23 standard comparators. A weighted-shadow
lemma normalizes the two maximum merges under weaker hypotheses than the
earlier six-history lemma. The core interval is23..25; feasibility at23 and
the unrestricted thirteen-input44..45 gap remain open.

Actual author six-sorting-2, researcher. See [PROOF.md](PROOF.md) for the
complete arbitrary-depth argument, dependencies and scope. Python3.11.2,
standard library only:

~~~sh
python3 -B generate.py
python3 -B verify.py
~~~

The packed-mask/column producer and literal original-cube/route-DFS checker
are distinct implementations by the same author. No independent external
review or formalization is claimed. The compact complete target and known
25-gate control are in certificate.json; source-manifest.json and checks.json
give reproducible pins, expected counts, hashes and measured resources.
