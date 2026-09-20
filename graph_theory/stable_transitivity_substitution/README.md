# Exact substitution and strong-component laws for stable transitivity

## Result

Let `m(T)` be the stable-transitivity number of a `k`-tournament.  If `Q` and
`T_1,...,T_r` all have degree `k`, and `Q[T_1,...,T_r]` denotes tournament
substitution, then

```text
m(Q[T_1,...,T_r]) = max(m(Q),m(T_1),...,m(T_r)).
```

This parameter-uniform identity has two immediate structural consequences:

1. An ordinal sum has stable-transitivity number equal to the maximum over
   its summands.
2. For every `k`-tournament `T`,

   ```text
   m(T) = max { m(T[C]) : C is a strong component of the support digraph }.
   ```

Thus the extremal parameter `m(n,k)` is exactly the maximum over strongly
connected `k`-tournaments of every order at most `n`, and it is nondecreasing
in `n`.  See [THEOREM.md](THEOREM.md) for the complete proof.

The formula also turns known finite obstructions into exact infinite
families.  Each of the accepted ordinary order-eight examples with `m=2`
can be ordinal-sum padded to every order `n>=8` while retaining exact value
`2`.  Likewise, the complete `G8` mixture theorem supplies degree-`k`
examples of every order `n>=8` with exact value `ceil(7k/6)`.

## Proof mechanism

The lower bound is restriction: a stabilizer and completed decomposition
restrict to each block, and to one representative per block.  For the upper
bound, pad optimal witnesses to the same degree.  Align their total-order
decompositions, then replace every vertex of each quotient order by the
corresponding block order.  These lexicographically composed orders give the
global stabilizer and completed decomposition.

For the component formula, the support condensation of a `k`-tournament is
an acyclic tournament.  All `k` arcs across each component pair point in its
condensation direction, so the original tournament is an ordinal sum of its
support strong components.

## Reproduction

The theorem is proved without computation.  A small exact checker audits the
definitions and formulas exhaustively in two independent bounded regimes:

```bash
cd graph_theory/stable_transitivity_substitution
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
sha256sum -c SHA256SUMS
```

Expected checker output is in `EXPECTED_OUTPUT.txt`.  The recorded run used
CPython 3.11.2 on Debian 12 and completed in under one second.

## Files and trust boundary

- `THEOREM.md` gives the universal proof, including padding, boundary cases,
  support components, and extremal consequences.
- `verify.py` builds all small TTD profile sets from total orders and computes
  stable-transitivity numbers from the definition.
- `test_verify.py` checks orientation conventions, the directed-triangle
  boundary, substitution, and support-component extraction.
- `SOURCES.md` records the primary-literature status check and dependencies.
- `EXPECTED_OUTPUT.txt` and `SHA256SUMS` make the compact audit reproducible.

The checker uses exact integer tuples, the Python standard library, and no
solver, floating point, randomness, or external data.  Its finite exhaustion
does not prove the unbounded theorem; the proof in `THEOREM.md` does.

## Scope and novelty status

Davis and Schroeder introduced stable transitivity and asked about `m(n,k)`
in [*Relating tournaments and permutations with xrays*](https://arxiv.org/abs/2606.21532v1)
(2026).  Their current v1 does not give a tournament-substitution or
strong-component formula.  Targeted primary-source and Discovery Net searches
through 2026-09-20 found no such result.  The theorem is therefore apparently
new relative to those searches, not a historical-priority claim.
