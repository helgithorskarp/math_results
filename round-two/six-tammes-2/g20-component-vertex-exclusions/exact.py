"""Complete sparse integer identities; no sign inferred from sampling."""
from fractions import Fraction as Q
from polynomials import P,dot
from frame import make
from scope import require
NAMES={'excess067','excess579','excess6911','excess067_square','excess579_square','R'}
def load(d):
    require(set(d)=={'schema_version','variable_order','coefficient_domain','rows'} and type(d['schema_version'])is int and d['schema_version']==1 and d['variable_order']==['t','z','w'] and d['coefficient_domain']=='Z','factor domain')
    require(set(d['rows'])==NAMES,'entire six-factor input')
    out={}
    for name,rows in d['rows'].items():
        terms={};keys=[]
        for row in rows:
            require(type(row)is list and len(row)==4,'literal coefficient row')
            i,j,k,v=row
            require(all(type(x)is int and x>=0 for x in (i,j,k)) and k<=1,'affine radical and nonnegative integer exponents')
            require(type(v)is str and str(int(v))==v and int(v)!=0,'canonical nonzero integer coefficient')
            key=(i,j,k);require(key not in terms,'unique monomial');keys.append(key);terms[key]=int(v)
        require(bool(rows) and keys==sorted(keys),'complete canonical rows');out[name]=P(terms)
    require(all(k[2]==0 for n in ('R','excess067_square','excess579_square') for k in out[n].c),'bivariate square factors')
    return out
def parts(f):return P({(i,j,0):v for (i,j,k),v in f.c.items() if k==0}),P({(i,j,0):v for (i,j,k),v in f.c.items() if k==1})
def product(names,t,z):
    a,b,c=1+t,1-t,1+2*t;D=b*b*c;C=1+D*z*z;J=9*t**3-t*t-t+1;Qp=a*D*z*z-2*D*z+2*t*t-t+1
    bs={'t':t,'a':a,'b':b,'c':c,'3t-1':3*t-1,'J':J,'C':C,'Q':Qp,'bz+1':b*z+1};p=t*0+1
    for name in names:require(name in bs,'positive-factor recipe name');p*=bs[name]
    return p
def raw_residuals(t,z,w):
    m=make(t,z,w);Y=m['points'];a,b,c=m['a'],m['b'],m['c'];O=m['Omega'];L=7*t*t+2*t-1
    out={}
    for name,(central,i,j,normal,rhs) in {'excess067':(0,6,7,[-5,-14,20],15),
                                        'excess579':(5,7,9,m['B_num'][10],t*a*a),
                                        'excess6911':(11,6,9,[-8,12,-5],9)}.items():
        T=[t*(a*a*(Y[i][v]+Y[j][v])-L*Y[central][v]) for v in range(3)]
        out[name]=dot(T,normal,t)-rhs*b*b*c*O
    return m,out
def identities(s,document):
    f=load(document);t,z,w=[P.var(i) for i in range(3)];m,raw=raw_residuals(t,z,w);R=m['root_squared'];Y=m['points'];a,b,c=m['a'],m['b'],m['c'];K=t*(9*t*t-2*t-3);L=7*t*t+2*t-1
    require(f['R']==R,'complete original radical square')
    for name,p in raw.items():require(p==product(s['positive_factor_recipes'][name],t,z)*f[name],'whole cleared vertex excess identity: '+name)
    for name in ('excess067','excess579'):
        A,B=parts(f[name]);target=name+'_square'
        require(B*B*R-A*A==s['square_integer_multipliers'][target]*product(s['positive_factor_recipes'][target],t,z)*f[target],'whole sign-aware square identity: '+name)
    # The normalized points themselves bind the shared intrinsic Gram.
    for i,j in ((6,7),(6,9),(7,9)):
        require((a*a*dot(Y[i],Y[j],t)-K*m['Omega']**2).reduced(R)==0,'whole intrinsic A-Gram identity')
    N=m['B_num'];zero=t*0
    for i,j in ((4,12),(8,10)):require(dot(N[i],N[j],t)==a*a*K,'whole intrinsic B-Gram identity')
    require((a*a-K)*(a*a+K-2*t*t*a*a)==b**4*c*(3*t+1)**2,'whole positive determinant identity')
    require(-L+2*t*a*a==b*b*c and -L*t+a*a+K==b*b*c,'whole active-equation solution identities')
    require(-L+2*a*a==b*(5*t+3) and t*t*(5*t+3)-b*c==a*(5*t*t-1),'whole norm and strict longness identities')
    for v in range(3):
        require(a*N[8][v]+a*N[1][v]==2*t*(N[2][v]+N[4][v]),'whole B8 circuit')
        require(a*N[10][v]+a*N[4][v]==2*t*(N[1][v]+N[2][v]),'whole B10 circuit')
        require(a*a*N[12][v]==(2*t*a+4*t*t)*N[1][v]+(4*t*t-a*a)*N[2][v]-2*t*a*N[4][v],'whole B12 circuit')
    q=a*m['D']*z*z-2*m['D']*z+2*t*t-t+1
    require(a*q==m['D']*(a*z-1)**2+4*t*t,'positive Q identity')
    return f,{'whole_radical_square':1,'whole_vertex_excesses':3,'whole_squared_excesses':2,'whole_component_Gram_bindings':5,
              'whole_intrinsic_determinant_active_solution_norm_longness':5,'whole_B_circuit_components':9,'whole_positive_Q_identity':1}
