// Independent literal subset census. No producer code or libraries imported.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
int main(int argc,char** argv){
 try {
  if(argc!=2) throw std::runtime_error("usage: checker cache");
  for(std::size_t n: {3U,7U,11U,15U}) {
   std::ifstream f(std::string(argv[1])+"/r44_"+std::to_string(n)+".g6",std::ios::binary);
   if(!f) throw std::runtime_error("input");
   std::string line; std::uint64_t index=0;
   while(std::getline(f,line)) {
    const std::size_t m=n*(n-1)/2;
    if(line.size()!=static_cast<std::size_t>(1+(m+5)/6) || static_cast<unsigned char>(line[0])!=n+63)throw std::runtime_error("shape");
    for(char ch:line)if(static_cast<unsigned char>(ch)<63 || static_cast<unsigned char>(ch)>126)throw std::runtime_error("alphabet");
    std::array<std::array<int,15>,15> a{};std::size_t bit=0;
    for(std::size_t v=1;v<n;++v)for(std::size_t u=0;u<v;++u){
     int c=(static_cast<unsigned char>(line[1+bit/6])-63)>>(5-bit%6)&1;
     a[u][v]=a[v][u]=c;++bit;
    }
    for(;bit<6*((m+5)/6);++bit)if(((static_cast<unsigned char>(line[1+bit/6])-63)>>(5-bit%6)&1)!=0)throw std::runtime_error("padding");
    int edges=0,red3=0,blue3=0;std::size_t k=0;std::uint64_t lo=0,hi=0;
    for(std::size_t u=0;u<n;++u)for(std::size_t v=u+1;v<n;++v){
     edges+=a[u][v];if(a[u][v]){if(k<64)lo|=std::uint64_t{1}<<k;else hi|=std::uint64_t{1}<<(k-64);}++k;
     for(std::size_t w=v+1;w<n;++w){
      int s=a[u][v]+a[u][w]+a[v][w];red3+=(s==3);blue3+=(s==0);
      for(std::size_t x=w+1;x<n;++x){int t=s+a[u][x]+a[v][x]+a[w][x];if(t==0||t==6)throw std::runtime_error("monochromatic K4");}
     }
    }
    std::cout<<n<<' '<<index<<' '<<edges<<' '<<red3<<' '<<blue3<<' '<<lo<<' '<<hi<<'\n';++index;
   }
   if(!f.eof())throw std::runtime_error("stream");
  }
 }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}
 return 0;
}
