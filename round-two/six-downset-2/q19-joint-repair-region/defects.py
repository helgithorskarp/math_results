"""Actual mathematical adverse checks for the new four-coordinate proof.

Faults are introduced after the complete source binding has passed. They
are mathematical countermodels or damaged proof identities, not timeouts,
source-hash mismatches, or assertions disabled by optimized Python.
"""
from binding import check_current
check_current()
from fractions import Fraction as F
import copy
import json
import resource
import time
from joint import model, physical, table_at, PARENT
import certify
import geometry
import polyhedron
from entries import affine_rows


def run():
    start=time.monotonic()
    raw=model.coefficient_input(PARENT/'COEFFICIENTS.json')
    V,coverage=polyhedron.vertices_of(polyhedron.facets())
    tmax=F(19967,229376)
    top=next(x for x in sorted(V) if x[0]==tmax and x[1]==F(1780389,28672))
    q=F(1,1024)
    checks=[]
    def reject(name,fn):
        try:fn()
        except ValueError as error:
            checks.append(dict(name=name,exception='ValueError',reason=str(error)))
            return
        raise ValueError('semantic damage did not reject: '+name)
    # Two endpoint entry rows are the genuine sharp template obstruction.
    reject('release below anchor-YY floor',lambda:certify.original_entry_check(raw,top[:3]+(top[3]-q,)))
    reject('release above actual empty-anchor floor',lambda:certify.original_entry_check(raw,top[:3]+(top[3]+q,)))
    # At this vertex XX and X good-supply capacities are actual original rows.
    both=next(x for x in V if x[0]==tmax and x[1]==F(1780389,28672) and x[2]==F(30062061,458752))
    reject('XX supply above original empty-XX cap',lambda:certify.original_entry_check(raw,(both[0],both[1]+q,both[2],both[3])))
    reject('X supply above original empty-X cap',lambda:certify.original_entry_check(raw,(both[0],both[1],both[2]+q,both[3])))
    ycap=next(x for x in V if x[0]==tmax and x[1]==F(6207571,229376))
    reject('Y supply above original empty-Y cap',lambda:certify.original_entry_check(raw,(ycap[0],ycap[1]-q,ycap[2],ycap[3])))
    # Domain premises are explicit, not supplied by a numerical solver.
    reject('negative template floor',lambda:certify.original_entry_check(raw,(-q,)+top[1:]))
    reject('floating-point coordinate',lambda:certify.original_entry_check(raw,(float(top[0]),)+top[1:]))
    reject('negative GG mass',lambda:certify.original_entry_check(raw,(top[0],-q,top[2],top[3])))
    reject('negative X mass',lambda:certify.original_entry_check(raw,(top[0],top[1],-q,top[3])))
    reject('negative eliminated Y mass',lambda:certify.original_entry_check(raw,(top[0],F(8421443,65536)+38*top[0]+q,top[2],top[3])))
    reject('negative star-release domain',lambda:certify.original_entry_check(raw,top[:3]+(-q,)))
    table=table_at(raw,*top)[0]
    bad=table.copy();bad[((0,0,2),(7,0,0))]+=top[3]
    reject('omit all45 abc-YY release edges',lambda:certify.original_entry_check(raw,top,bad))
    bad=table.copy();b=model.type_budgets(model.comparison(raw,9,10),9,10)
    bad[((0,1,0),(1,0,1))]-=(b['ell'][(1,0,1)]-top[0])/9
    reject('omit positive aY star-supply source',lambda:certify.original_entry_check(raw,top,bad))
    bad=table.copy();bad[((0,2,0),(0,2,0))]+=q
    reject('change total GG cost without paying loop',lambda:certify.original_entry_check(raw,top,bad))
    # One valid-shaped affine coefficient is damaged. It must reach an
    # original entry, rather than a fixture/source gate or summary count.
    x=(F(0),F(0),F(0),F(1));rows=affine_rows(raw)
    z=list(rows[('empty_anchor',)]);z[4]+=q;rows[('empty_anchor',)]=tuple(z)
    point=model.literal_point(table_at(raw,*x)[0],9,10)
    reject('wrong affine release coefficient at original entry',lambda:certify.entire_affine_surplus(point,x,rows))
    # An entire inverse and an exact nonzero null vector are required.
    saved=polyhedron.inverse_or_null
    def damaged_inverse(A):
        inv,null=saved(A)
        if inv is not None:inv[0][0]+=q
        return inv,null
    polyhedron.inverse_or_null=damaged_inverse
    try:reject('wrong active-subset full inverse',lambda:polyhedron.vertices_of(polyhedron.facets()))
    finally:polyhedron.inverse_or_null=saved
    # The second geometric algorithm must detect count-preserving set loss.
    saved_geo=geometry.vertices_of
    def damaged_census(fs):
        vertices,record=saved_geo(fs)
        old=next(iter(vertices));data=vertices.pop(old)
        new=(old[0]+q,)+old[1:];vertices[new]=data
        return vertices,record
    geometry.vertices_of=damaged_census
    try:reject('count-preserving false vertex coordinate',geometry.run)
    finally:geometry.vertices_of=saved_geo
    reject('missing original domain facet',lambda:polyhedron.vertices_of(polyhedron.facets()[:-1]))
    # Both original lifted endpoints and physical actions matter.
    physical_point=physical.original(table,9,10)
    basis,gram=physical.complete_basis(physical_point)
    badpoint=copy.deepcopy(physical_point);badpoint['cap'][0][0]+=1
    reject('one wrong full upper physical action entry',lambda:physical.literal_actions(badpoint,table,basis))
    block=model.sector_forms(table,9,10)['trivial_lower']
    metric=block['metric'].copy();metric[0]=0
    reject('missing positive physical orbit metric',lambda:model.exact_ldl(block['matrix'],metric,F(1,1024)))
    badform=[row.copy() for row in block['matrix']];badform[0][1]+=q
    reject('unweighted/asymmetric physical block',lambda:model.exact_ldl(badform,block['metric'],F(1,1024)))
    badform=[row.copy() for row in block['matrix']];badform[0][0]=F(-1)
    negative=model.exact_ldl(badform,block['metric'],F(0))
    model.require(not negative['positive_definite'] and F(negative['witness_quadratic'])<0,
                  'full exact rational negative-vector evidence for damaged physical form')
    reject('negative physical direction cannot certify PSD',lambda:model.require(negative['positive_definite'],'explicit rational negative physical direction'))
    model.require(len(checks)==22,'all22 mathematical damages actually rejected')
    return dict(agent='six-downset-2',role='researcher',rejection_count=len(checks),
                semantic_rejections=checks,negative_physical_witness=negative,
                no_source_hash_timeout_or_resource_status_counted_as_math_rejection=True,
                all_guards_are_ValueError_not_assert=True,
                observed_seconds=time.monotonic()-start,
                peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
