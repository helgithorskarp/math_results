# T5: exact disc Heesch two and final-hole Heesch three

Author **six-heesch-2**, **researcher**, 2026-10-01.
The unmarked 23-cell honeycomb polyhex in [proof.md](proof.md) has
**Hc=2, Hh=3 and no plane tiling**, allowing all Euclidean motions and
reflections. This is a complete author-checked, unformalized proof package.
No independent T5 review or record claim is asserted. A finite-five polyhex remains
unresolved in this work.

The compact certificate gives two disc coronas and three coronas with holes
only in the final layer, all necessary contact exclusions, complete first
surround inventories, two necessary topological cuts, and three short RUP
contradictions. The reader rebuilds all geometry and CNFs. Full solver logs,
original CNFs and the obsolete 9.55 MB early proof corpus are not needed.

From the repository root, with Python 3.11+ and g++ supporting C++17:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
mkdir -p /tmp/t5-proof
g++ -std=c++17 -O2 -DNDEBUG round-two/six-heesch-2/shifted-inner/rup_audit.cpp -o /tmp/t5-proof/rup_audit
python3 round-two/six-heesch-2/strip-t5/verify.py
python3 round-two/six-heesch-2/strip-t5/cnf.py 4 --output /tmp/t5-proof/case4.cnf --rup-audit /tmp/t5-proof/rup_audit
python3 round-two/six-heesch-2/strip-t5/cnf.py 5 --output /tmp/t5-proof/case5.cnf --rup-audit /tmp/t5-proof/rup_audit
python3 round-two/six-heesch-2/strip-t5/cnf.py 6 --output /tmp/t5-proof/case6.cnf --rup-audit /tmp/t5-proof/rup_audit
```

All four reader stages must pass for the full theorem. The contact stage
establishes Hh=3, non-tiling and Hc>=2. The three CNF/RUP stages exclude the
remaining possibilities for Hc>=3. Every stage has a 45-second guard; a
guard failure is incomplete verification. Run stages sequentially. Optional
Python `-O` runs produce identical deterministic `evidence` fields and hashes.
No Python packages or SAT solver are required. C++ RUP checking uses the
[generic published source](../shifted-inner/rup_audit.cpp).

Expected contact evidence: domains 664/166/39/22, support bounds 347/56,
3 and 8 complete first stars, 1,504 rejection DAG states, seven malformed
controls. The CNFs have 92099/90198/83458 variables and
536757/523222/477620 clauses. RUP cores have 7/14/57 additions.
[expected.json](expected.json) records the exact evidence hashes, source
manifest and measured normal/-O checks. Trust boundaries and the necessity
of every encoding restriction are explained in [proof.md](proof.md).

Compared with the known four-corona T3 and
[three-corona T4](../strip-t4/proof.md), this settles only the next explicit
strip length. The separation between Hc and Hh is essential to the claim.
