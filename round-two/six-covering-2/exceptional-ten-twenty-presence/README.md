# Ten and twenty must be original classes in the exceptional case

**six-covering-2, researcher.** For distinct covers by divisors of10080 with
minimum EXACTLY8, actual12 of eight parity and no PRESENT opposing10, both
original10 and20 are present, and a20-a8 is odd iff a20-a10=0mod5.
The credited8837/8923 reductions and the newly checked20:1 exclusion leave
three exceptional seven-class roots, at20 phases2,4,5. They remain OPEN.
The five-class frontier stays14; no numerical bound changes.

Read [proof.md](proof.md). From a checkout with adjacent parent engine and
credited proof directories intact:

```sh
python3 -m venv /tmp/covering-presence-env
/tmp/covering-presence-env/bin/pip install -r round-two/six-covering-2/requirements-discovery.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /tmp/covering-presence-env/bin/python -B round-two/six-covering-2/exceptional-ten-twenty-presence/reproduce.py --generate
python3 -B round-two/six-covering-2/exceptional-ten-twenty-presence/reproduce.py --require-manifest
```

Generation is optional if a complete tree is already available in
`generated/tree-twenty-one.json`. The voluntary default is12 batches;
each batch has unchanged180second/700-new-node limits. An exhausted allowance
stops INCOMPLETE and asserts no exclusion. Resuming uses the same source.
Memory scope1CPU/2GiB suffices; no multi-threading or resource increase.

Python3.12.14/NumPy2.4.6/SciPy1.17.1 were used for generation; stdlib
Python3.11.2 for literal replay. Only(3) of the proof is directly replayed.
The first literal replay checks2354nodes/2103strictleaves in about72seconds.
An alternate exact valid certificate can pass despite different author
hashes; `--require-manifest` requests this author's exact record.
No large certificate, solver environment or private data is published.
Author checked, written proof unformalized; no reviewer verdict asserted.
