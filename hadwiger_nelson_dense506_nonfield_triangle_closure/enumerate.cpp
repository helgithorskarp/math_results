#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
#include <algorithm>
#include <chrono>
using Point=std::array<std::int64_t,8>;
struct Hash { std::size_t operator()(const Point& a) const {
 std::uint64_t h=1469598103934665603ULL;
 for(auto x:a) {h^=static_cast<std::uint64_t>(x);h*=1099511628211ULL;}
 return static_cast<std::size_t>(h);
}};
int main(int argc,char**argv){try{
 if(argc!=4)throw std::runtime_error("usage: enumerate input output first-index-limit(0=all)");
 const int limit=std::stoi(argv[3]);if(limit<0)throw std::runtime_error("negative limit");
 std::ifstream in(argv[1]);std::ofstream out(argv[2]);if(!in||!out)throw std::runtime_error("open failure");
 int ng;if(!(in>>ng)||ng<1||ng>100)throw std::runtime_error("group count");
 const auto start=std::chrono::steady_clock::now();
 for(int g=0;g<ng;g++){
  int n;if(!(in>>n)||n<1||n>100000)throw std::runtime_error("point count");
  std::vector<Point> ps(static_cast<std::size_t>(n));
  std::unordered_map<Point,int,Hash> index;index.reserve(static_cast<std::size_t>(n)*2U);
  for(int i=0;i<n;i++){
   Point doubled{};
   for(int t=0;t<8;t++){
    auto& x=ps[static_cast<std::size_t>(i)][static_cast<std::size_t>(t)];
    if(!(in>>x)||x < -100000000 || x>100000000)throw std::runtime_error("coordinate range");
    doubled[static_cast<std::size_t>(t)]=2*x;
   }
   if(!index.emplace(doubled,i).second)throw std::runtime_error("duplicate point");
   if(i>0 && !(ps[static_cast<std::size_t>(i-1)]<ps[static_cast<std::size_t>(i)]))throw std::runtime_error("unordered points");
  }
  std::uint64_t tested=0,triangles=0;
  for(int i=0;i<(limit==0?n:std::min(n,limit));i++){
   const auto&a=ps[static_cast<std::size_t>(i)];
   for(int j=i+1;j<n;j++){
    tested++;const auto&b=ps[static_cast<std::size_t>(j)];
    for(int e : {-1,1}){
     Point c{};
     for(int t=0;t<4;t++){
      const auto k=static_cast<std::size_t>(t);
      c[k]=a[k]+b[k]-3*e*(b[k+4]-a[k+4]);
      c[k+4]=a[k+4]+b[k+4]+e*(b[k]-a[k]);
     }
     auto it=index.find(c);
     if(it!=index.end() && it->second>j){out<<g<<' '<<i<<' '<<j<<' '<<it->second<<' '<<e<<'\n';triangles++;}
    }
   }
  }
  std::cerr<<g<<' '<<n<<' '<<tested<<' '<<triangles<<'\n';
 }
 std::string extra;if(in>>extra)throw std::runtime_error("trailing input");
 out.flush();if(!out)throw std::runtime_error("output failure");
 std::cerr<<"seconds "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<'\n';
 return 0;
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
