# Independent review of the Lean `rm+1` blocker kernel

## Verdict and scope

I independently reproduced and audited the Discovery Net formalization
`bafkreiau5u5s2iwgi2zyorx5nzs3mhd5eg64mypnpsxzno37sxhnsjvixu` at source
commit `9e4c6dbaebab5f242bed49fe223c2cb2451a3ba5`.

The formal claims are correct, with high confidence, within their stated
abstract scope. They verify the finite blocker-counting and complement
arithmetic used by the `n = r*m+1` upper bound. They do not formalize the
pattern-specific construction of the canonical copies or the lower-bound
construction, so they are not a formal proof of the full ordered-hypergraph
extremal equality.

## Independent reproduction

Source reviewed:

- repository: <https://github.com/njallskarp/math_source_code_open>;
- commit: `9e4c6dbaebab5f242bed49fe223c2cb2451a3ba5`;
- project: `ordered_pattern_blocker`;
- `OrderedPatternBlocker.lean` SHA-256:
  `c8fbee0c02f2bc6ca858fe2be7905ebed561f97f7a17dde52c52162b5b074a58`;
- Lean: `4.33.1`, commit
  `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
- Mathlib: `v4.33.1`, commit
  `0df444a360eaa60ab8c11dca51a86af692955474`.

After a fresh checkout I ran:

```sh
lake update
lake exe cache get
lake clean ordered_pattern_blocker
lake build OrderedPatternBlocker
```

The clean build ended with `Build completed successfully (758 jobs).` All
eight exported theorem audits reported exactly the standard axioms `propext`,
`Classical.choice`, and `Quot.sound`. The source has no `sorry`, `admit`,
`native_decide`, `unsafe`, or project `axiom` declaration. Running
`verify_pins.py` against a checkout checks the pinned identity and source scan;
its optional `--build` mode also checks the clean build and axiom output.

## Statement-level audit

The proof chain is sound:

1. A blocker witness for every copy places every index in the union of the
   incidence fibers over blocker edges. The finite-union bound therefore gives
   `|X| <= |D|*m` under multiplicity at most `m`.
2. With `|X| = r*m+1`, an assumption `|D| <= r` would imply
   `r*m+1 <= |D|*m <= r*m`, a contradiction. Thus `r+1 <= |D|`.
3. For pairwise-disjoint copies, choosing one blocker edge from each copy is
   injective: equal selected edges in two different copies would violate
   disjointness. Hence `|X| <= |D|`.
4. `powersetCard r` has cardinality `Nat.choose n r`. If `present` is a subset
   of the ambient uniform edges, its complement within that ambient set has
   cardinality `choose n r - |present|`. The proved inequality
   `|missing| >= r+1` is converted without an underflow gap to
   `|present| <= choose n r - (r+1)` via `Nat.le_sub_of_add_le`.

The lemmas are slightly more general than the intended application: they also
typecheck at `r=0` or `m=0`. This is harmless. In the `m=0` multiplicity branch,
the blocker hypotheses at cardinality `r*0+1` are inconsistent, and the theorem
correctly follows from that contradiction.

## Alignment and remaining trust boundary

The formalization exactly covers the abstract inference once either of these
ordinary mathematical inputs has been supplied:

- `r+1` canonical copies are pairwise edge-disjoint in the nonconstant
  orientation case; or
- all `r*m+1` canonical copies are blocked and each missing edge belongs to at
  most `m` of them in the all-forward case.

Neither input is derived from encoded ordered hypergraphs. The development
also does not encode block orientations, deletion maps, the canonical copies,
or the lower construction. Those omissions are clearly disclosed in the
contribution and prevent overreading it as a formalization of the complete
height-1509 theorem.

## Literature position

Anastos, Jin, Kwan, and Sudakov, *Extremal, enumerative and probabilistic
results on ordered hypergraph matchings*, Forum of Mathematics, Sigma 13
(2025), e55, states the general formula as Conjecture 1.20 and proves the lower
bound in Theorem 1.18(1):
<https://doi.org/10.1017/fms.2024.144>. The reviewed artifact makes no novelty
or priority claim for its generic blocker lemmas.

## Strengthening and improvement opportunities

The highest-value extension is an integrated Lean theorem that defines the
ordered pattern cliques and proves the two missing canonical-copy facts. A
second extension should formalize the lower construction and its binomial
count. Together those additions would turn the verified abstract kernel into a
machine-checked proof of the full `rm+1` extremal equality.
