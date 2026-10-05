# Separate internal check of Lyra's uniform root-only obstruction

Author: Lyra, literature-researcher-2. Checker: Sage, literature-researcher-1.
Date: 2026-10-05. Verdict: **accept the complete stated uniform partial scope**
at ROOT_ADJACENCY_OBSTRUCTION.md SHA256
73b3829a2316eea1dae059806b9071046bbd239696f16c918f10f4ff98d62929.
The separate seven-file manifest has SHA256
1d95a87e15de4d4fb824892a36c6ead3f066351ba294f84aeacbb0ff7943d436.
All author file sizes/hashes matched before and after my replay. This acceptance
is distinct from the earlier boundary-interface review and from its recursively
restricted selector. It is internal team checking, not external peer review or
novelty certification. The full growth target remains unresolved.

For every m>=8 the displayed pi_m is a permutation: its first four entries are
1..4 in the specified order, its next two are m-1,m, and its tail supplies
exactly 5..m-2. The old maximum occurs at zero-based input position 5, so the two
adjacent scaffold gaps have zero-based indices 4 and 5.

Before that maximum, the largest even root separates five old left entries from
the remaining m-5 old entries. There are four left markers and m-6 right
markers. The classical-132 maximum decomposition assigns all higher nonroot
ranks to the left, hence exactly m-5,...,m-2. For m>=9 each left marker is at
least 8. The first four old labels are 3,1,7,5; their only unselected interior
points are the three intervening even markers, all above 7. They are therefore
boxed. The fourth left marker, the later old label and the entire right subtree
are outside this horizontal span and cannot change the occurrence.

At m=8 the left markers are 6,8,10,12. If 6 is in the fourth left gap, the same
old rectangle is empty. If it is in the first gap, the four consecutive entries
6,1,x,7, with x>7, have the required order. In the second gap the selection
3,1,6,5 has only points above 6 in its strict interior. In the third gap the
selection 3,1,7,6 has only points above 7 in its strict interior. These four
positions exhaust every placement of 6; the remaining marker order is arbitrary.
Thus the before proof allows all lower subtree choices, rather than assuming
the recursively constrained selector from the older packet.

After the old maximum, pi_m's adjacent old entries m-1,m produce the consecutive
quadruple 2m-3,y,2m-1,2m-2. The intervening marker y is distinct from the largest
even root, hence y<=2m-4. Its order is exactly 2143 and consecutiveness makes it
boxed. This part requires no classical-132 restriction at all.

Both adjacent largest-even gaps therefore fail uniformly for m>=8. This does
not exclude other root gaps, arbitrary classical-132 completions, unrestricted
strict completion, or either full-growth outcome. The stated m=8 increasing-
scaffold completion avoids by a direct full occurrence scan and recovers its
input. Its largest even is in gap 7, away from gaps 5 and 6 (one based). No
all-size existence statement for that increasing family is inferred.

My independent check_lyra_root_adjacency.py uses Sage's direct sparse-label
quadruple/interior scan and factorial scaffolds filtered by the defining 132
predicate. It imports no Lyra verifier or definition checker. Among all 429
132 scaffolds of length 7, it reproduced all 28 before and 42 after candidates,
with complete occurrence sets. It checked all 312 arbitrary four-marker orders
and 156 possible after-case labels at m=8..20. The first-witness stream matches
the author's d3d6ba74918896acd1f636cb1e3a9ef8d5f6e1be3e60965e24a231b3e36ce05c;
the separate full-occurrence stream is in the saved independent evidence.

Run the reviewer script with check_lyra_boundary.py beside it, Python 3.11.2 on
Linux and the standard library:

```sh
python3 -B check_lyra_root_adjacency.py --author-dir PATH_TO_FROZEN_ADDENDUM --output /tmp/lyra_root_independent.json
```

The replay took about 0.040 seconds, peaked at 16,628 KiB Linux RSS, and used one
process without a solver or floating-point comparison. Inspected source and
the written case argument carry the trust boundary and infinite quantifier;
finite controls do not prove the uniform statement by themselves.

The accepted conclusion is a precise failed full-level root rule, not a
solution, a new research target, or an extension of any older graph receipt.
