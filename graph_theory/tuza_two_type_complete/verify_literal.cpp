// Independent traversal and literal-cut evaluation of the finite bound.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using I=std::int64_t;
I choose2(I n){return n*(n-1)/2;}
I colors(I n){if(n<2)return 1;return n-1+(n%2);}
I ceiling(I numerator,I denominator){I result=numerator/denominator;if(numerator%denominator>0)++result;return result;}
I complete_packing(I n){if(n<3)return 0;const I r=n%6;I leave=0;if(r==0||r==2)leave=n/2;if(r==4)leave=n/2+1;if(r==5)leave=4;return (choose2(n)-leave)/3;}
struct Bounds{I k,a,b,c,d;
 I cover(I m,I n)const{
  // All independent vertices of one type may be put on a best side.
  // Try the two possibilities for the second type after fixing the first.
  I best=choose2(k)+m*(a+c)+n*(b+c);
  for(int side=0;side<2;++side){
   std::vector<I> weights;
   for(I i=0;i<a;++i)weights.push_back(m);
   for(I i=0;i<b;++i)weights.push_back(side?-n:n);
   for(I i=0;i<c;++i)weights.push_back(side?m-n:m+n);
   for(I i=0;i<d;++i)weights.push_back(0);
   std::sort(weights.rbegin(),weights.rend());
   I removed=m*(a+c)+(side?0:n*(b+c));
   for(I left=0;left<=k;++left){
    best=std::min(best,choose2(left)+choose2(k-left)+removed);
    if(left<k)removed-=weights[static_cast<std::size_t>(left)];
   }
  }
  return best;
 }
 I lower(I m,I n)const{
  const I s=a+c,t=b+c,u=a+b+c;
  const I x=colors(s),y=colors(t),z=colors(u);
  I h=ceiling(m*choose2(s)*y+n*choose2(t)*x-m*n*choose2(c),x*y);
  // Maximize a two-item linear allocation explicitly over its two endpoints.
  I ml=std::max(I(0),std::min(m,z-n));
  I mh=std::min(m,z);
  for(I used_s:{ml,mh}){
   I used_t=std::min(n,z-used_s);
   h=std::max(h,ceiling(used_s*choose2(s)+used_t*choose2(t),z));
  }
  const I p=complete_packing(k),edges=choose2(k)-h;
  const I den=k*k*(k-1)*(k-2)/2; // 3 k binomial(k,3)
  // Expanded numerator of h + p e(4e-k^2)/(3 k binomial(k,3)).
  return std::max({p,h,ceiling(h*den+p*edges*(4*edges-k*k),den)});
 }
};
struct Stats{I cases=0,boxes=0,nodes=0,failures=0,shapes=0;};
void verify(const Bounds&g,I ml,I mh,I nl,I nh,Stats&s){
 ++s.nodes;
 if(g.lower(ml,nl)*2>=g.cover(mh,nh)){s.cases+=(mh-ml+1)*(nh-nl+1);++s.boxes;return;}
 if(ml==mh&&nl==nh){
  ++s.cases;++s.failures;std::cout<<"FAIL "<<g.a<<' '<<g.b<<' '<<g.c<<' '<<g.d<<' '<<ml<<' '<<nl<<'\n';return;
 }
 // Split by parameter width, in the opposite tie convention to the producer.
 if(nh-nl>=mh-ml&&nl<nh){const I mid=(nl+nh)/2;verify(g,ml,mh,nl,mid,s);verify(g,ml,mh,mid+1,nh,s);}
 else{const I mid=(ml+mh)/2;verify(g,ml,mid,nl,nh,s);verify(g,mid+1,mh,nl,nh,s);}
}
int main(int argc,char**argv){
 try{
  std::size_t used=0;
  I last=argc==2?std::stoll(argv[1],&used):112;
  if(argc==2 && used!=std::string(argv[1]).size())throw std::runtime_error("invalid integer");
  if(argc>2||last<3||last>112)throw std::runtime_error("usage: verify [3..112]");
  Stats total;
  for(I k=3;k<=last;++k){
   Stats row;
   // Independent shape traversal: intersection and outside cells first.
   for(I c=0;c<=k;++c)for(I d=0;d<=k-c;++d){
    const I rem=k-c-d;
    for(I b=0;2*b<=rem;++b){I a=rem-b;Bounds g{k,a,b,c,d};++row.shapes;
     verify(g,0,std::max(I(0),a+c-1),0,std::max(I(0),b+c-1),row);
    }
   }
   total.cases+=row.cases;total.boxes+=row.boxes;total.nodes+=row.nodes;total.failures+=row.failures;total.shapes+=row.shapes;
   std::cout<<"ROW "<<k<<' '<<row.shapes<<' '<<row.cases<<' '<<row.boxes<<' '<<row.nodes<<' '<<row.failures<<std::endl;
  }
  std::cout<<"TOTAL "<<total.shapes<<' '<<total.cases<<' '<<total.boxes<<' '<<total.nodes<<' '<<total.failures<<std::endl;
  return total.failures?1:0;
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 2;}
}
