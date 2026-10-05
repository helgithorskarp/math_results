# A failed simple-input completion mechanism

Theo, literature-researcher-4, 2026-10-05. Separate exact finite author
certificate awaiting Lyra's different-researcher check. Full target410 is
unchanged and unsolved. This is not part of the accepted inflation packet,
its public source or its pending graph original.

I tested the sufficient hypothesis: every simple permutation pi of length
m>=4 admits a boxed2143-avoiding word

    (2*pi_1-1),2*rho_1,(2*pi_2-1),...,2*rho_(m-1),(2*pi_m-1),

where rho avoids classical132 and its maximum lies in a gap immediately
before or after the old maximum of pi. All lower scaffold choices are
unrestricted. This was prompted by the proper intervals in the earlier
root-adjacency obstruction, not by evidence that simplicity guarantees it.

This hypothesis really would suffice for the full negative growth answer.
All simple-permutation counts t_m satisfy t_m~m!/e^2, by Albert–Atkinson–Klazar,
*The enumeration of simple permutations*, Journal of Integer Sequences6
(2003), article03.4.4. Primary author manuscript
https://cs.otago.ac.nz/research/publications/oucs-2003-05.pdf,
Theorem5 and Observation8, freshly checked live. For each successful input
choose a lexicographically least allowed scaffold. Odd positions recover
pi, so a_(2m-1)>=t_m. The factorial estimate forces infinite limsup of the
root counts; for example m!>=(floor(m/2))^(ceil(m/2)) already gives an
unbounded root lower bound. This is a conditional bridge, not a growth proof.
Here t_m counts all simple permutations, and is distinct from the simple
boxed-avoider count s_m in the inflation reduction.

The exact simple input

    pi=(3,1,6,4,2,7,5)

refutes the hypothesis. Its old maximum is at zero-based position5, so
rho's maximum6 must be at position4 or5. There are14+42=56 such132-avoiding
scaffolds, and **every one** gives at least one boxed2143. The compact JSON
retains the entire list with a literal-checkable selected quadruple for
each scaffold. Simplicity of pi is checked by every proper contiguous
position segment; no segment of length2..6 has consecutive values.

Completeness of the scaffold list follows from the usual maximum grammar:
in a132 avoider, every value left of the maximum exceeds every value right
of it, or left-smallest/maximum/right-largest would be132. Both sides must
themselves avoid132. Conversely those conditions exclude a triple crossing
the split. Thus the root at position4 has4 left entries and1 right entry,
giving C4*C1=14 possibilities; root at position5 gives C5*C0=42. The
program generates both sides recursively, checks no duplicates, and
directly tests the132 condition. No lower adjacency restriction is imposed.

This finite counterexample has an unrestricted-root avoiding completion:

    rho=(4,5,3,6,2,1),
    word=(5,8,1,10,11,6,7,12,3,4,13,2,9).

The scaffold has no132, the full word has no boxed2143 and its odd entries
recover pi. Thus failure concerns only the two allowed full-root choices.
It does not refute all-simple unrestricted completion, all-input
unrestricted completion, factorial growth or the original410 statement.

Finite controls exhaust all2,6,46 simple inputs of lengths4,5,6, all of which
have an allowed witness. The search stops at this73rd lexicographic simple
input of length7; it does not claim to have exhausted length7 or8. Length7
minimality among simple inputs of length>=4 is supported by the complete
smaller searches, and is a separate finite claim requested for checking.
The saved earlier success stream is
8934bd27ab88eb8beb8118dea1cf91a64c96f805e40f2e1a59e61a57814fe693.
There were942 tested allowed scaffolds before stopping. The author code
does not enlarge the census once the mechanism is falsified.

Reproduce with CPython3.11+, standard library, one process/thread:

    python3 -B simple_completion_probe_v1.py --max-m 8 --output /tmp/simple-root.json

The output remains at m7. Files: `simple_completion_probe_v1.py`,
`simple-completion-probe-v1.json`, `rectangle_checker.py` and this note.
Author runtime0.252seconds,18920KiB peak RSS. The rectangle checker has a
separately accepted arbitrary-size equivalence with the boxed definition,
but that older review does not independently accept this new complete
scaffold list, simplicity, minimality or bridge. A different literal
quadruple enumeration/factorial scaffold filter can check all these finite
claims without calling the author generator or rectangle scanner.

Next obligation: a root-selection or guard mechanism needs more flexibility
even on simple input. No convenient narrower statement has replaced the
fixed full target. No publication priority or external-review claim is made.
