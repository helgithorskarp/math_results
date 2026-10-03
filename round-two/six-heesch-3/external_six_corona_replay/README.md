# Exact polygon replay of two public six-corona witnesses

Actual author **six-heesch-3**, role **researcher**. This is a reproduction
of existing public positive certificates, author checked and independently
unreviewed. It makes no new-construction, priority or finite-upper claim.

After exact common scaling, the published `h7` source is the owned T7
prototype; its189-copy patch has six complete disc coronas. The published
`h8l` source is T8 with the left triangle((-2,2),(0,0),(2,2)) added; its
258-copy patch also has six. Coordinates mean(x,sqrt(3)y)/4. Every prefix
is a simple disc, strictly surrounds the preceding prefix, and passes
whole-copy packing, grounding and exclusion of skipped-layer contacts.

The original witnesses are credited to
[XyraSinclair's primary package](https://gist.github.com/XyraSinclair/667c99c02479133bfc297121f5f42e92),
pinned revisionf8fc3b50bb776a4b5ce574e0c55f8363296ac6df. The author's
solver-trusted upper is not reproduced or adopted. No foreign program,
solver or large search is run. The capped source has no finite upper here.

Python>=3.10, standard library only; checked with CPython3.12.14. Run serially:

```bash
python3 check.py
python3 -O check.py
python3 controls.py
python3 -O controls.py
```

`check.py` reconstructs the complete source geometry, every affine pose and
every prefix. `expected.json` seals full geometry and placement records,
including whole boundary cycles and contacts, rather than only counts.
`controls.py` exercises six semantic corruptions and ignores a false
producer upper header. See PROOF.md for the unformalized geometric bridges.
