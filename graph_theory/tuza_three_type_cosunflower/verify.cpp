// Exact co-sunflower finite closure. C++20; signed 64-bit arithmetic.
// Mathematical reduction and integer bounds: PROOF.md.
// Extends ../tuza_two_type_complete/verify_rectangles.cpp to three types
// and treats outside clique vertices as a fourth monotone coordinate.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
using Z=std::int64_t;
Z pairs(Z k){return k*(k-1)/2;}
Z triples(Z k){return k*(k-1)*(k-2)/6;}
Z colors(Z k){return k<2?1:(k%2?k:k-1);}
Z ceildiv(Z a,Z b){return a>=0?(a+b-1)/b:a/b;}
Z packing(Z k){Z r=k%6; Z l=(r==1||r==3)?0:(r==5?4:k/2+(r==4));return (pairs(k)-l)/3;}
using Point=std::array<Z,4>; // multiplicities m0,m1,m2, outside clique count d
struct Shape{
 std::array<Z,3> p,s,r; Z c,u;
 Shape(Z a,Z b,Z d,Z cc):p{a,b,d},c(cc),u(a+b+d+cc){for(int i=0;i<3;++i){s[i]=u-p[i];r[i]=colors(s[i]);}}
 // Independent palettes use inclusion-exclusion; shared palettes use
 // disjoint colors and descending neighborhood sizes.
 Z centered(const Point& v)const{
  Z den=r[0]*r[1]*r[2], num=0;
  for(int i=0;i<3;++i)num+=v[i]*pairs(s[i])*(den/r[i]);
  for(int i=0;i<3;++i)for(int j=i+1;j<3;++j)num-=v[i]*v[j]*pairs(u-p[i]-p[j])*(den/(r[i]*r[j]));
  num+=v[0]*v[1]*v[2]*pairs(c);
  Z h=ceildiv(num,den),left=colors(u),shared=0;
  for(int i=0;i<3;++i){Z a=std::min(left,v[i]);shared+=a*pairs(s[i]);left-=a;}
  return std::max(h,ceildiv(shared,colors(u)));
 }
 Z lower(const Point& v)const{
  Z k=u+v[3], q=pairs(k), bp=packing(k), h=centered(v),e=q-h;
  return std::max({bp,h,h+ceildiv(bp*e*(4*e-k*k),3*k*triples(k))});
 }
 Z cover(const Point& v)const{
  Z k=u+v[3],q=pairs(k),answer=q;
  for(int mask=0;mask<4;++mask){
   std::array<Z,3> w{v[0],(mask&1)?-v[1]:v[1],(mask&2)?-v[2]:v[2]};
   Z sum=w[0]+w[1]+w[2],constant=0;
   for(int i=0;i<3;++i)if(w[i]>0)constant+=w[i]*s[i];
   std::array<std::pair<Z,Z>,5> cells{{{sum-w[0],p[0]},{sum-w[1],p[1]},{sum-w[2],p[2]},{sum,c},{0,v[3]}}};
   std::sort(cells.begin(),cells.end(),std::greater<>());
   Z before=0,prefix=0;
   for(auto [weight,count]:cells){
    // If k+weight is negative, floor and truncation both clamp to zero.
    Z l=std::clamp((k+weight)/2,before,before+count);
    answer=std::min(answer,q-l*(k-l)+constant-prefix-(l-before)*weight);
    before+=count;prefix+=weight*count;
   }
  }
  return answer;
 }
};
struct Counts{Z shapes=0,cells=0,rectangles=0,nodes=0,analytic=0,failures=0;void add(const Counts& b){shapes+=b.shapes;cells+=b.cells;rectangles+=b.rectangles;nodes+=b.nodes;analytic+=b.analytic;failures+=b.failures;}};
void check(const Shape& g,const Point& lo,const Point& hi,Counts& n){
 // Monotonicity is needed only for the true nu and tau, not these formulas.
 ++n.nodes;
 if(2*g.lower(lo)>=g.cover(hi)){
  Z volume=1;for(int i=0;i<4;++i)volume*=hi[i]-lo[i]+1;
  n.cells+=volume;++n.rectangles;return;
 }
 int axis=-1;Z score=-1;
 for(int i=0;i<4;++i)if(hi[i]>lo[i]){Z v=(hi[i]-lo[i])*(i==3?g.u+hi[3]:g.s[i]);if(v>score){score=v;axis=i;}}
 if(axis<0){
  ++n.cells;++n.failures;
  std::cout<<"FAIL "<<g.p[0]<<' '<<g.p[1]<<' '<<g.p[2]<<' '<<g.c;
  for(auto x:lo)std::cout<<' '<<x;
  std::cout<<' '<<g.lower(lo)<<' '<<g.cover(lo)<<std::endl;return;
 }
 Z mid=(lo[axis]+hi[axis])/2;Point a=hi,b=lo;a[axis]=mid;b[axis]=mid+1;
 check(g,lo,a,n);check(g,b,hi,n);
}
void print(const std::string& s,const Counts& n){std::cout<<s<<' '<<n.shapes<<' '<<n.cells<<' '<<n.rectangles<<' '<<n.nodes<<' '<<n.analytic<<' '<<n.failures<<std::endl;}
Z parse(const char* arg){std::string s(arg);std::size_t used=0;Z v=std::stoll(s,&used);if(used!=s.size())throw std::runtime_error("integer");return v;}
int main(int argc,char** argv){try{
 bool dump=argc==3&&std::string(argv[1])=="--dump";
 if(argc>3||(argc==3&&!dump))throw std::runtime_error("usage");
 Z last=dump?parse(argv[2]):argc==2?parse(argv[1]):198;
 if(last<3||last>(dump?10:198))throw std::runtime_error("range");
 Counts total;
 for(Z u=3;u<=last;++u){Counts row;
  for(Z a=0;a<=u/3;++a)for(Z b=std::max(Z(1),a);a+2*b<=u;++b)for(Z p=b;a+b+p<=u;++p){
   Shape g(a,b,p,u-a-b-p);if(g.s[2]<2)continue;
   ++row.shapes;Point lo{1,1,1,0},hi{g.s[0]-1,g.s[1]-1,g.s[2]-1,last-u};
   if(dump){for(Z d=0;d<=last-u;++d)for(Z m=1;m<g.s[0];++m)for(Z n=1;n<g.s[1];++n)for(Z t=1;t<g.s[2];++t){
    Point v{m,n,t,d};std::cout<<a<<' '<<b<<' '<<p<<' '<<g.c<<' '<<d<<' '<<m<<' '<<n<<' '<<t<<' '<<g.centered(v)<<' '<<g.lower(v)<<' '<<g.cover(v)<<'\n';}}
   else {
    // Section 2: k>=55 and d>=3 are already certified analytically.
    const Z finite_d=std::min(last-u,std::max(Z(2),Z(54)-u));
    const Z skipped=(last-u-finite_d)*(g.s[0]-1)*(g.s[1]-1)*(g.s[2]-1);
    row.cells+=skipped;row.analytic+=skipped;hi[3]=finite_d;
    check(g,lo,hi,row);
   }
  }
  if(!dump){total.add(row);print("ROW "+std::to_string(u),row);}
 }
 if(!dump)print("TOTAL",total);
 return total.failures?1:0;
 }catch(const std::exception& e){std::cerr<<"ERROR "<<e.what()<<" (expected [3..198] or --dump [3..10])\n";return 2;}}
