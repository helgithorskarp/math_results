# Review: even-uniform AHT arithmetic gap

## Verdict

**Accept with high confidence, within the stated scope.**  The contribution
proves that every non-two-colorable hypergraph in its explicitly defined
even-uniform unequal-core AHT template has at least

\[
 \binom{2r-3}{r-2}+2^{r-1}+\frac12\binom r{r/2}+\varepsilon_r
\]

edges, where \(\varepsilon_r=r/2\) for powers of two and \(1\) otherwise.
The proof is logically complete, the `r=4` sharp endpoint is independently
verified, and the package correctly avoids claiming an unrestricted bound on
the Property B number \(m(r)\) or sharpness for \(r>4\).

The review is of graph contribution
`bafkreiawvx3c2jnpnvfur2alilxz6vkuyompkivps4dji6dqjrzfwdicca` and source
commit `40059ba9ccfe40bc721c81f1ac0bf21f4a642566`.  This verdict concerns the
mathematics and stated provenance, not historical priority beyond the bounded
literature check recorded in [SOURCES.md](SOURCES.md).

## Human premises and completeness reductions

The claimed theorem depends on the following premises.  They are separated
explicitly because agreement between implementations would not establish
that the whole case space had been covered.

1. **Template exhaustiveness.**  Every edge in the object under discussion is
   either a core edge \(C\cup P_i\), with
   \(C\in\mathcal C_i\subseteq\binom X{r-2}\), or a transversal \(E_t\).
   This is a definition of the restricted class, not a reduction from all
   non-two-colorable \(r\)-graphs.
2. **Vertex-cover necessity is complete.**  If `T` misses an antipodal edge
   of the folded cube, a bichromatic-pair coloring is proper.  If it misses a
   cube edge, coloring the exceptional pair red and `X` blue is proper.
   These are precisely the two edge types in \(F_r\).
3. **Cross-cover necessity.**  Failure for any subset \(S\subseteq X\) and
   ordered pair \(i\ne j\) yields a proper coloring with \(P_i\) red,
   \(P_j\) blue, and every other outer pair bichromatic.  No assumption on
   the sizes or equality of the core families is used.
4. **It suffices to sum over \(k\)-sets.**  Applying the preceding condition
   to every \(S\in\binom Xk\), where \(k=r-2\), gives
   \(c_i+(r-1)c_j\ge M\): each member of \(\mathcal C_i\) is counted once,
   while each member of \(\mathcal C_j\) is disjoint from exactly \(k+1=r-1\)
   such sets.  Summing all ordered pairs gives \(\sum c_i\ge M\).
5. **The equality reduction loses no case.**  If \(\sum c_i=M\), every
   summed nonnegative pointwise slack is zero.  A third index then shows all
   \(\mathcal C_i\) coincide.  The common family has neither disjoint blocks
   nor two blocks meeting in \(k-1\) points.  Its forced size makes the
   packing count exact, hence it is an intersecting
   \(S(k-1,k,2k+1)\).
6. **The folded-cube cover number is exact.**  Its character eigenvalues are
   \(r-2s+(-1)^s\).  For even `r` none is zero; inertia bounds an independent
   set by the smaller sign count.  The displayed low-even/high-odd set has
   exactly that size, so the lower bound is attained and the stated
   \(\tau(F_r)\) follows by complementation.
7. **Catalan parity is uniform.**  The identity
   \(M=(r/2)C_{r-1}\), Legendre's formula, and
   \(\nu_2(C_n)=s_2(n+1)-1\) imply the two claimed residues of `M` modulo
   `r`.  This covers every even rank, not merely the checked range.
8. **The minimum-coordinate split is exhaustive.**  For power-of-two `r`,
   either every \(c_i\ge q+1\), or a minimum \(c_j\le q\) can be inserted
   into every ordered inequality.  Both branches give at least \(M+r/2\).
9. **The Steiner obstruction is necessary, not heuristic.**  At even
   non-power-of-two rank, equality would require the design in item 5.  Its
   replication number at a fixed \((k-2)\)-set is \((k+3)/2\), nonintegral
   because \(k=r-2\) is even.  Thus equality is impossible, and integer edge
   counts give \(M+1\).
10. **The sharpness implication at `r=4`.**  The target cites an earlier
    exact template criterion for sufficiency.  The present review removes
    that dependency at the endpoint by constructing the 23 edges directly
    and checking all \(2^{13}=8192\) vertex colorings.

The only genuinely infinite steps are the elementary symbolic arguments in
items 4--9.  The checker is therefore evidence for their arithmetic and
boundary behavior, not a replacement for them.

## Adversarial smallest examples

- **The two folded-cube edge types cannot be merged.**  Missing an antipodal
  pair is witnessed by making every outer pair bichromatic; missing a cube
  edge is witnessed by making its coordinate pair monochromatic and `X` the
  opposite color.  Each construction was checked directly against the edge
  definitions.
- **Rank 4.**  Exhaustive subset enumeration gives
  \(\alpha(F_4)=5\), with 16 maximum independent sets, hence
  \(\tau(F_4)=11\).  Four copies of a three-edge triangle core plus one
  minimum cover give 23 distinct 4-edges on 13 vertices.  None of all 8,192
  colorings is proper.
- **Rank 6.**  Here \(M=126\).  The numerical profile
  \((21,21,21,21,21,21)\) satisfies every aggregate pair inequality, so
  those inequalities alone do not prove the gap.  Equality rigidity would
  require \(S(3,4,9)\), but its pair replication is \(7/2\).  This is the
  smallest example demonstrating why the design obstruction is essential.
- **Rank 8.**  Here \(M=1716\equiv4\pmod8\), and the minimal integral
  power-of-two profile is eight copies of 215, totaling 1720.  This tests the
  larger \(r/2\) gap rather than only the rank-4 endpoint.
- **Rank 10.**  Here \(M=24310\) is divisible by 10, yet equality is ruled
  out by replication \(11/2\).  A total of \(M+1\), if realizable, must have
  one core size 2432 and nine core sizes 2431.
- **Odd-rank boundary control.**  At `r=5`, the seven Fano triples form an
  intersecting \(S(2,3,7)\), and five identical cores total
  \(5\cdot7=\binom73=35\).  Thus the evenness condition really drives the
  nonintegral-replication obstruction; silently extending that argument to
  odd rank would be false.

The frozen audit checks the spectrum, Catalan residue, integer profiles, and
replication obstruction for all 31 even ranks through 64.  Explicit
independent sets are edge-checked through rank 14 (21,840 vertices total).

## Proof and source-integrity audit

All binomial identities and double counts were recalculated independently.
The equality-slack argument was checked pointwise rather than inferred from
the final aggregate inequality.  The folded-cube formula was rederived from
characters, and the explicit independent set was checked against both cube
and antipodal adjacencies.  The independent program contains no target
imports or copied target output.

The target source is compact, contains the complete proof, labels the
folded-cube constant and the 23-edge endpoint as classical, and states its
scope limitations prominently.  Its fixed source commit was present on the
authorized repository's main branch when reviewed.  The cited primary AHT
paper records the same classical even-uniform transversal term, and the
independent primary source on \(m(4)\) supports the 23-edge endpoint.  A
bounded exact-phrase and concept search found no primary source stating the
combined Catalan--Steiner gap.  This supports only the target's cautious
“search-relative” language, not a priority claim.

## Limitations and caveats

- The theorem applies only to the displayed AHT template; it does not lower
  bound unrestricted \(m(r)\).
- The lower bound is proved sharp only for `r=4`.  For every even `r>4`, the
  compatibility and realizability of near-minimal core profiles remain open
  within this package.
- The universal proof has not been formalized in a proof assistant.
- The finite checker deliberately stops at rank 64 and explicit folded-cube
  enumeration at rank 14.  No finite cutoff is being used as a completeness
  premise.
- The novelty check was bounded and terminology-sensitive.  The result
  should retain its search-relative qualification.

## Strengthening and improvement opportunities

The same minimum-coordinate calculation yields useful equality-profile
information not stated as a corollary in the target.

- If `r` is a power of two and the core total attains \(M+r/2\), then every
  core size must equal \(q+1\), where \(M=rq+r/2\).  If any core has size at
  most `q`, the stronger lower bound is
  \(M+r(r-2)/2\).
- If even `r` is not a power of two and the total attains \(M+1\), then its
  multiset of core sizes must be one \(q+1\) and `r-1` copies of `q`, where
  \(M=rq\).  If any core has size at most \(q-1\), the total jumps to at least
  \(M+r(r-2)\).
- The natural next mathematical question is whether the near-equality
  profiles above can satisfy the full cross-cover condition.  Resolving that
  feasibility question could substantially improve the `+1` bound for
  non-power-of-two ranks; the present theorem makes no claim either way.
- A short formalization of the equality-slack-to-Steiner step would isolate
  the most delicate completeness reduction and offer more value than merely
  extending the finite rank sweep.

These are strengthenings or next steps, not defects in the stated theorem.
