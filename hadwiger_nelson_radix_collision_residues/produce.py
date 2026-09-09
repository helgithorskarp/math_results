#!/usr/bin/env python3
"""Deterministic discovery of two linear F3 colouring certificates; stdlib only."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def field(modulus):
    d = len(modulus)-1
    q = 3**d
    digits = [tuple(a//3**i % 3 for i in range(d)) for a in range(q)]
    def add(a, b):
        return sum((digits[a][i]+digits[b][i]) % 3 * 3**i for i in range(d))
    def mul(a, b):
        v = [0]*(2*d-1)
        for i in range(d):
            for j in range(d):
                v[i+j] += digits[a][i]*digits[b][j]
        for k in range(2*d-2, d-1, -1):
            for j in range(d):
                v[k-d+j] -= v[k]*modulus[j]
        return sum(v[i] % 3 * 3**i for i in range(d))
    def power(a, n):
        out = 1
        while n:
            if n % 2:
                out = mul(out, a)
            a = mul(a, a)
            n //= 2
        return out
    return q, digits, add, power


def generate():
    result = {'schema': 1, 'graphs': {}}
    for name, modulus in [('norm81', [2,1,0,0,1]), ('hyperbola81', [1,0,1])]:
        q, digits, add, power = field(modulus)
        if any(power(a,q-1) != 1 for a in range(1,q)):
            raise ValueError('invalid field presentation')
        if name == 'norm81':
            connection = [a for a in range(1,q) if power(a,10)==1]
            S = [digits[a] for a in connection]
            vertices = digits
            E = sorted({tuple(sorted((v,add(v,a)))) for v in range(q) for a in connection})
        else:
            connection = [(a,power(a,q-2)) for a in range(1,q)]
            S = [digits[a]+digits[b] for a,b in connection]
            vertices = [digits[v%q]+digits[v//q] for v in range(q*q)]
            E = sorted({tuple(sorted((v,add(v%q,a)+q*add(v//q,b))))
                        for v in range(q*q) for a,b in connection})
        weights = next(w for w in itertools.product(range(3),repeat=4)
                       if all(sum(x*y for x,y in zip(w,s))%3 for s in S))
        word = ''.join(str(sum(x*y for x,y in zip(weights,v))%3) for v in vertices)
        if any(word[u]==word[v] for u,v in E):
            raise ValueError('invalid generated colouring')
        result['graphs'][name] = {
            'modulus_low_first': modulus, 'weights': weights,
            'colour_word': word, 'connection': connection,
            'vertices': len(vertices), 'edges': len(E), 'edge_sha256': digest(E)}
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    args.out.write_text(json.dumps(generate(),sort_keys=True,indent=2)+'\n')
    print(json.dumps({'certificate_sha256': hashlib.sha256(args.out.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
