#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using I=std::int64_t;
constexpr I LIMIT=1000000000;
constexpr I SCALE=12*(I{1}<<20);
constexpr I UNIT=SCALE*SCALE;
// Endpoints are in [-10^9,10^9]. Differences <=2*10^9, so each square
// <=4*10^18 and each sum <=8*10^18 < INT64_MAX. No signed overflow occurs.
std::array<I,2> square(I a,I b){
    const I aa=a*a,bb=b*b;
    return {a<=0 && b>=0 ? 0 : std::min(aa,bb),std::max(aa,bb)};
}
int main(){
 try{
  I raw=0;if(!(std::cin>>raw)||raw<0||raw>200000)throw std::runtime_error("bad count");
  const auto n=static_cast<std::size_t>(raw);
  std::vector<std::array<I,4>> points(n);
  for(auto& p:points){
   for(auto& v:p)if(!(std::cin>>v)||v < -LIMIT||v>LIMIT)throw std::runtime_error("bad interval");
   if(p[0]>p[1]||p[2]>p[3])throw std::runtime_error("reversed interval");
  }
  std::string extra;if(std::cin>>extra)throw std::runtime_error("trailing input");
  for(std::size_t i=0;i<n;++i){
   const auto& a=points[i];
   for(std::size_t j=i+1;j<n;++j){
    const auto& b=points[j];
    const auto x=square(a[0]-b[1],a[1]-b[0]);
    if(x[0]>UNIT)continue;
    const auto y=square(a[2]-b[3],a[3]-b[2]);
    if(x[0]+y[0]<=UNIT && x[1]+y[1]>=UNIT)std::cout<<i<<' '<<j<<'\n';
   }
  }
  if(!std::cout)throw std::runtime_error("write failed");
 }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 2;}
}
