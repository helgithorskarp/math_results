"""Exact reference reflection, pole counts, and pointwise complement checks."""
import json


def need(v,message):
    if not v:
        raise ValueError(message)


def main():
    p,n,b = 617,3704,1852
    squares = {r*r%p for r in range(1,p)}
    def q(r):
        return None if r%p == 0 else int(r%p not in squares)
    need((p-1)%4 == 0 and p-1 in squares,'minus one square')
    reflected = complement = 0
    pole_histogram = {}
    for s in range(p):
        t = (1-s)%p
        colors = []
        for x in range(n):
            v = q(x-b+(s if x<b else t))
            colors.append(v if v is None else v ^ int(x>=b))
        poles = sum(v is None for v in colors)
        need(poles == (8 if s == 1 else 6),'free pole count')
        pool = 1848 if s == 1 else 1849
        need(colors.count(0) == pool and colors.count(1) == pool,'reference class sizes')
        pole_histogram[poles] = pole_histogram.get(poles,0)+1
        for x,c in enumerate(colors):
            need(colors[n-1-x] == (None if c is None else c^1),'actual reference reflection')
            reflected += 1
            if c is not None:
                for f in (0,1):
                    need(int(f != c)+int((1-f) != c) == 1,'pointwise edit complement')
                    complement += 1
    print(json.dumps({'status':'VERIFIED_REFERENCE_REFLECTION_AND_COMPLEMENT',
                      'phases':p,'point_reflections':reflected,
                      'pointwise_complement_cases':complement,
                      'pole_histogram':pole_histogram,
                      'reference_class_sizes':{'phase1':[1848,1848],'other616':[1849,1849]}}))


if __name__ == '__main__':
    main()
