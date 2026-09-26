"""Exact low-plane inequalities and conditional plane-pair systems at 71."""
from incidence import system


def unique_low_system(spectra, size):
    if size not in (8,9):
        raise ValueError("the conditional certificate requires size eight or nine")
    columns,names,matrix,rhs=system(spectra)
    def sizes(kind,value):
        return value if kind=='p' else value[1] if kind=='l' else ()
    low=[int(kind=='s' and value[0]<=9) for kind,value in columns]
    pairs=[]
    for kind,value in columns:
        count=sum(m<=9 for m in sizes(kind,value))
        pairs.append(count*(count-1)//2)
    matrix+= [low,pairs]
    rhs+= [1,0]
    names+= ['one_low_plane','no_low_plane_pair']
    for m in range(10,17):
        matrix.append([sum(n<=9 for n in sizes(kind,value))*sizes(kind,value).count(m)
                       -int(kind=='s' and value[0]==m) for kind,value in columns])
        rhs.append(0);names.append(f'low_by_size_{m}_pairs')
    matrix.append([int(kind=='s' and value[0]==size) for kind,value in columns])
    rhs.append(1);names.append(f'the_low_plane_has_size_{size}')
    return columns,names,matrix,rhs


def check_lower_bound(spectra,certificate):
    columns,_,matrix,rhs=system(spectra)
    cutoff=certificate['cutoff'];D=certificate['D'];z=certificate['multipliers']
    if cutoff not in (9,10) or type(D) is not int or D<=0:
        raise ValueError("invalid objective or denominator")
    if len(z)!=len(matrix) or any(type(v) is not int for v in z):
        raise ValueError("invalid exact multiplier vector")
    objective=[int(kind=='s' and value[0]<=cutoff) for kind,value in columns]
    slacks=[D*objective[j]-sum(z[i]*matrix[i][j] for i in range(len(matrix)))
            for j in range(len(columns))]
    value=sum(a*b for a,b in zip(z,rhs))
    if min(slacks)<0 or min(slacks)!=certificate['min_slack'] or value!=certificate['bound_numerator']:
        raise ValueError("invalid lower-bound certificate")
    bound=(value+D-1)//D
    if bound!=certificate['integer_bound'] or bound!={9:1,10:2}[cutoff]:
        raise ValueError("the required integer bound was not obtained")
    return {'cutoff':cutoff,'numerator':value,'denominator':D,'integer_lower_bound':bound,
            'rows':len(matrix),'columns':len(columns)}


def check_unique_low(spectra,certificate):
    columns,_,matrix,rhs=unique_low_system(spectra,certificate['size'])
    z=certificate['multipliers']
    if len(z)!=len(matrix) or any(type(v) is not int for v in z):
        raise ValueError("invalid exact Farkas vector")
    slacks=[sum(z[i]*matrix[i][j] for i in range(len(matrix))) for j in range(len(columns))]
    value=sum(a*b for a,b in zip(z,rhs))
    if min(slacks)<0 or value>=0 or min(slacks)!=certificate['minimum_slack'] or value!=certificate['rhs_product']:
        raise ValueError("invalid conditional Farkas certificate")
    return {'unique_low_size':certificate['size'],'rhs_product':value,'minimum_slack':min(slacks),
            'rows':len(matrix),'columns':len(columns)}
