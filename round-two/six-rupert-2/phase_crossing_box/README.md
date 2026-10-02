# Reproduce the J74 phase-crossing receiving-box certificate

six-rupert-2, researcher. Complete exact replay passed in ordinary and
optimized Python execution. The closed-fit classification includes the whole raw box about
`((2315-453sqrt5)/1798,(2211+205sqrt5)/1798,-1)` of halfwidth1/1000, both actual
17-corner receiver phases and their16-corner closed seam. Every original
proper source, planar physical translation and scale>=1 is retained.
Global J74 remains open; the author proof is unformalized and unreviewed.

Read [PROOF.md](PROOF.md) for all quantifiers, the actual twelve equal shadows
and the continuum arguments. No source-entry or body-centrality assumption
is made. A,AH,B,BH are partial-shadow poses and cannot quotient arbitrary Q.

Use a full clone of the authorized publication repository, Python3.11+, and
the standard library. Public relative dependencies are hash-checked before
import; [DEPENDENCIES.json](DEPENDENCIES.json) records their exact provenance.
No private packet, coefficient corpus, numerical optimizer or ledger is needed.

From this directory, run these jobs SEQUENTIALLY, one CPU-intensive child at a
time. Keep every numeric thread one and the existing130-second per-child
guard. Each bounded source job verifies at most512 complete closed leaves.

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
mkdir -p .generated/normal .generated/optimized
timeout 130 python3 check.py --local > .generated/normal/local.json
timeout 130 python3 check.py --controls > .generated/normal/controls.json
for i in $(seq 0 20); do
  timeout 130 python3 check.py --chunk "$i" > .generated/normal/chunk-$(printf '%02d' "$i").json || exit
done
timeout 130 python3 check.py --assemble .generated/normal > .generated/normal/complete.json
timeout 130 python3 -O check.py --local > .generated/optimized/local.json
timeout 130 python3 -O check.py --controls > .generated/optimized/controls.json
for i in $(seq 0 20); do
  timeout 130 python3 -O check.py --chunk "$i" > .generated/optimized/chunk-$(printf '%02d' "$i").json || exit
done
timeout 130 python3 -O check.py --assemble .generated/optimized > .generated/optimized/complete.json
diff -r .generated/normal .generated/optimized
```

All21 contiguous chunks in EACH mode, local proof and controls are mandatory;
the final source chunk has408 leaves. Each default command compares its
WHOLE mathematical output with [expected.json](expected.json). `--emit`
additionally prints exact computed records without that expected comparison;
it does not disable mathematical signs or geometry checks. `--profile 128`
with a source chunk checks ONLY that prefix and is not the theorem. Assembly
rejects missing, partial, mismatched or reordered source records. Assembly
alone does not establish the signs: its input records must come from running
every advertised exact checker job.

No all-source conclusion may be drawn from a timeout, memory termination,
pause barrier, wrong-sign leaf or incomplete enumeration. Stop and preserve
the exact cursor if an operational guard interrupts work. All discovered
bases and leaf labels are untrusted choices until their exact checks pass.

The mathematical output contains108 positive common-support stresses,1944
force-polynomial component identities,10648 complete source leaves
(10603CUT/45HOLE), and2577744 strict exact signs. Whole-box local masses7,12,18
give the Euclidean Cayley1/30 collar with squared absorption517/576. Both
true closed receiver phases are checked with8160 actual receiver and48960
actual source comparisons. This does not claim a fixed17-corner polygon on
the far side of the wall or a global non-Rupert theorem.

Generated records under `.generated/`, discovery floats, logs and coefficient
streams are private and need not be published. The compact [certificate.json](certificate.json)
has only exact original contact choices and integer forest addresses; its
coefficients are regenerated from public source. [VALIDATION.json](VALIDATION.json)
records complete ordinary/optimized checks and the remaining trust boundary.
