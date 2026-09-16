#!/usr/bin/env python3
"""Semantic corruption controls for the EI19 lens certificate."""

from intervals import I
from verify import (first_lens_closure, replay_source_geometry, require,
                    source_intervals, validate_word)

def rejected(call):
    try:
        call()
    except (ValueError, ZeroDivisionError):
        return True
    return False

def main():
    cert,_=replay_source_geometry()
    source=source_intervals(cert)
    points,_=first_lens_closure(source)
    word=open(__file__.replace("controls.py","four_word.txt")).read().strip()
    tests=[]
    tests.append(rejected(lambda:validate_word(points,word[:-1])))
    tests.append(rejected(lambda:validate_word(points,"x"+word[1:])))
    edge_word=list(word); edge_word[1]=edge_word[0]
    tests.append(rejected(lambda:validate_word(points,"".join(edge_word))))
    overlap=None
    for i in range(len(points)):
        for j in range(i+1,len(points)):
            if word[i]==word[j] and not any(a.hi<b.lo or b.hi<a.lo
                                            for a,b in zip(points[i],points[j])):
                overlap=(i,j);break
        if overlap:break
    require(overlap is not None,"duplicate-label control fixture")
    collision_word=list(word)
    collision_word[overlap[1]]=str((int(collision_word[overlap[0]])+1)%4)
    tests.append(rejected(lambda:validate_word(points,"".join(collision_word))))
    bad_source=list(source);bad_source[1]=bad_source[0]
    tests.append(rejected(lambda:first_lens_closure(bad_source)))
    tests.append(rejected(lambda:I.rational(-1).sqrt()))
    require(all(tests),"a corruption was accepted")
    print("6/6 semantic corruptions rejected")

if __name__=="__main__": main()
