// Exact outward-rounded dyadic enumeration. Floating point proposes indices only;
// integer dot-product inequalities certify that no other indices are possible.
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <stdexcept>
#include <vector>
using namespace std; using Z=__int128_t; using L=int64_t;
L SCALE;
L floorq(Z a,Z b){if(b<=0)throw runtime_error("nonpositive denominator");Z q=a/b,r=a%b;if(r<0)--q;if(q<INT64_MIN||q>INT64_MAX)throw runtime_error("overflow");return (L)q;}
L ceilq(Z a,Z b){if(b<=0)throw runtime_error("nonpositive denominator");Z q=a/b,r=a%b;if(r>0)++q;if(q<INT64_MIN||q>INT64_MAX)throw runtime_error("overflow");return (L)q;}
struct I {L l,h;};
I integer(L a){return {a*SCALE,a*SCALE};}
I add(I a,I b){return {floorq((Z)a.l+b.l,1),floorq((Z)a.h+b.h,1)};}
I neg(I a){return {floorq(-(Z)a.h,1),floorq(-(Z)a.l,1)};}
I sub(I a,I b){return add(a,neg(b));}
I mul(I a,I b){array<Z,4>p={(Z)a.l*b.l,(Z)a.l*b.h,(Z)a.h*b.l,(Z)a.h*b.h};return {floorq(*min_element(p.begin(),p.end()),SCALE),ceilq(*max_element(p.begin(),p.end()),SCALE)};}
I divide(I a,I b){if(b.l<=0)throw runtime_error("division through zero");array<L,4>lo,hi;int i=0;for(L x:{a.l,a.h})for(L y:{b.l,b.h}){lo[i]=floorq((Z)x*SCALE,y);hi[i]=ceilq((Z)x*SCALE,y);i++;}return {*min_element(lo.begin(),lo.end()),*max_element(hi.begin(),hi.end())};}
L isqrt(Z a){if(a<0)throw runtime_error("negative root");L s=(L)sqrt((long double)a);while((Z)s*s>a)--s;while((Z)(s+1)*(s+1)<=a)++s;return s;}
I root(I a){if(a.h<0)throw runtime_error("empty root");L l=isqrt((Z)max((L)0,a.l)*SCALE),h=isqrt((Z)a.h*SCALE);if((Z)h*h<(Z)a.h*SCALE)++h;return {l,h};}
struct C{I x,y;};
C conj(C a){return {a.x,neg(a.y)};}
C cmul(C a,C b){return {sub(mul(a.x,b.x),mul(a.y,b.y)),add(mul(a.x,b.y),mul(a.y,b.x))};}
I dot(C a,C b){return add(mul(a.x,b.x),mul(a.y,b.y));}
bool overlap(I a,I b){return max(a.l,b.l)<=min(a.h,b.h);}
vector<vector<C>> tables;
int n;long long states=0,core_states=0,index_calls=0,fallbacks=0;
set<string> seen;
int mod(int k,int t){return (k%t+t)%t;}
vector<int> grid(C a,int factor){
 // factor=1: n roots; factor=2: 2n roots, all from the same table.
 ++index_calls;int N=n*factor,step=2/factor;
 double x=((double)a.x.l+(double)a.x.h)/(2*SCALE),y=((double)a.y.l+(double)a.y.h)/(2*SCALE);
 int k=mod((int)llround(atan2(y,x)*N/(2*acos(-1.))),N);
#ifdef GATE_ZERO_GUESS
 k=0; // Validation mode: a deliberately poor proposal must remain sound.
#endif
 vector<int> cand;
 I d=dot(a,tables[n][step*k]);
 if(d.l>tables[n][step].x.h){for(int j=-1;j<=1;j++)cand.push_back(mod(k+j,N));}
 else{++fallbacks;for(int j=0;j<N;j++)cand.push_back(j);}
 vector<int> out;for(int j:cand){C w=tables[n][step*j];if(overlap(a.x,w.x)&&overlap(a.y,w.y))out.push_back(j);}
 sort(out.begin(),out.end());out.erase(unique(out.begin(),out.end()),out.end());return out;
}
vector<C> contact(I r,I s){
 I q=divide(sub(add(mul(r,r),mul(s,s)),integer(1)),mul(integer(2),mul(r,s)));
 if(q.l>SCALE||q.h< -SCALE)return {};
 q={max(-SCALE,q.l),min(SCALE,q.h)};
 I d=sub(integer(1),mul(q,q));if(d.h<0)return {};
 I y=root(d);return {{q,y},{q,neg(y)}};
}
set<int> edges(C p,C q,const vector<C>& ac){
 set<int> out;C rot=cmul(p,conj(q));
 for(C a:ac)for(int k:grid(cmul(rot,a),1))out.insert(k);
 return out;
}
void emit(const vector<int>&ks,const vector<int>&axis,const vector<set<int>>&es){
 ++states;int h=ks.size();vector<int>deg(h);
 for(int i=0;i<h;i++)deg[i]=(ks[i]?(2*ks[i]==n?1:2):0)+axis[i];
 int t=0;for(int i=0;i<h;i++)for(int j=i+1;j<h;j++,t++){deg[i]+=es[t].size();deg[j]+=es[t].size();}
 // Lower-circle families have been handled independently, so remove an orbit
 // of degree <=3 and extend greedily if this necessary condition fails.
 if(*min_element(deg.begin(),deg.end())<4)return;
 ++core_states;ostringstream os;os<<n<<' '<<h;for(int k:ks)os<<' '<<k;for(int a:axis)os<<' '<<a;
 for(auto e:es){os<<' '<<e.size();for(int a:e)os<<' '<<a;}
 if(seen.insert(os.str()).second)cout<<os.str()<<'\n';
}
int main(int argc,char**argv){
 if(argc<2)throw runtime_error("usage: enumerate tables.txt [max_three=169] [max_two=254]");
 int max3=argc>2?stoi(argv[2]):169,max2=argc>3?stoi(argv[3]):254,maxn=max(max3,max2),cap;
 ifstream f(argv[1]);f>>cap>>SCALE;if(cap<maxn||SCALE!=(1LL<<48))throw runtime_error("bad table header");tables.resize(cap+1);
 for(int t=3;t<=cap;t++){tables[t].resize(2*t);for(int m=0;m<2*t;m++){int a,b;I s,c;f>>a>>b>>s.l>>s.h>>c.l>>c.h;if(!f||a!=t||b!=m||s.l>s.h||c.l>c.h)throw runtime_error("bad table row");tables[t][m]={c,s};}}
 for(n=3;n<=maxn;n++){
  vector<I> r;vector<int> k,axis;
  for(int j=1;j<=n/2;j++){r.push_back(divide(integer(1),mul(integer(2),tables[n][j].y)));k.push_back(j);axis.push_back(6*j==n);}
  int internal=r.size();if(n%6){r.push_back(integer(1));k.push_back(0);axis.push_back(1);}
  int size=r.size();vector<vector<vector<C>>> ac(size,vector<vector<C>>(size));
  for(int i=0;i<size;i++)for(int j=i+1;j<size;j++)ac[j][i]=ac[i][j]=contact(r[i],r[j]);
  C one={integer(1),integer(0)};
  if(n<=max2)for(int a=0;a<internal;a++)for(int b=a+1;b<internal;b++)for(C p:ac[a][b])
   emit({k[a],k[b]},{axis[a],axis[b]},{edges(one,p,ac[a][b])});
  if(n<=max3){
   // Fixed radii: each radius either supports an internal edge or equals 1.
   for(int a=0;a<size;a++)for(int b=a+1;b<size;b++)for(int c=b+1;c<size;c++){
    array<int,3> ids={a,b,c};
    for(int center=0;center<3;center++){
     int j=(center+1)%3,l=(center+2)%3;
     for(C p:ac[ids[center]][ids[j]])for(C q:ac[ids[center]][ids[l]]){
      array<C,3> z={one,one,one};z[j]=p;z[l]=q;
      emit({k[a],k[b],k[c]},{axis[a],axis[b],axis[c]},
        {edges(z[0],z[1],ac[a][b]),edges(z[0],z[2],ac[a][c]),edges(z[1],z[2],ac[b][c])});
     }
    }
   }
   // Exactly two internal rings, and a third radius neither internal nor 1.
   for(int a=0;a<internal;a++)for(int b=a+1;b<internal;b++)for(int m=1;m<n;m++){
    vector<I> rc;
    if(axis[a]){ // The other quadratic root is exactly zero.
     if(2*m<n)rc.push_back(mul(integer(2),tables[n][m].x));
    }else{
     I d=sub(integer(1),mul(mul(r[a],r[a]),mul(tables[n][m].y,tables[n][m].y)));
     if(d.h<0)continue;
     I base=mul(r[a],tables[n][m].x),h=root(d);rc={add(base,h),sub(base,h)};
    }
    for(I s:rc){
     if(s.h<=0)continue;
     if(s.l<=0)throw runtime_error("unresolved positive radius boundary");
     for(C z:contact(s,r[b]))for(int j:grid(z,2)){
      if(j==0||j==n)continue; // Two distinct contacts are necessary.
      C p=tables[n][mod(m+j,2*n)];
      emit({k[a],k[b],0},{axis[a],axis[b],0},
       {edges(one,p,ac[a][b]),{0,mod(-m,n)},{0,mod(j,n)}});
     }
    }
   }
  }
  cerr<<n<<" states "<<states<<" cores "<<core_states<<" unique "<<seen.size()<<" index_calls "<<index_calls<<" fallbacks "<<fallbacks<<'\n';
 }
 return 0;
}
