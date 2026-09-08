#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
constexpr std::uint64_t prime=1000000009ULL;
struct Point {std::int64_t x,y;};
int main(int argc,char**argv) {
 try {
  if(argc!=4) throw std::runtime_error("usage: strict_sieve residues.tsv maximum_n output.bin");
  std::ifstream in(argv[1]);std::size_t n;std::uint64_t den,p;
  if(!(in>>n>>p>>den) || p!=prime || den!=96 || n!=64513)throw std::runtime_error("input header");
  std::vector<Point> pts(n);
  for(auto &q:pts)if(!(in>>q.x>>q.y)||q.x<0||q.y<0||q.x>=static_cast<std::int64_t>(p)||q.y>=static_cast<std::int64_t>(p))throw std::runtime_error("point range");
  std::string extra;if(in>>extra)throw std::runtime_error("extra input");
  std::size_t cap=std::stoull(argv[2]);if(cap<2||cap>n)throw std::runtime_error("cap");n=cap;
  std::ofstream out(argv[3],std::ios::binary);if(!out)throw std::runtime_error("output open");
  auto start=std::chrono::steady_clock::now();std::uint64_t hits=0,pairs=0;
  for(std::uint32_t i=0;i<n;i++)for(std::uint32_t j=i+1;j<n;j++) {
   std::int64_t dx=pts[i].x-pts[j].x,dy=pts[i].y-pts[j].y;
   // |dx|,|dy| <= p-1; dx^2+dy^2 < 2.01e18 < INT64_MAX.
   std::uint64_t v=static_cast<std::uint64_t>(dx*dx+dy*dy);pairs++;
   if(v%prime==den*den%prime){
    // Specify little-endian uint32 labels independently of host byte order.
    for(std::uint32_t label:{i,j}) {
     for(unsigned k=0;k<4;k++) out.put(static_cast<char>((label>>(8*k))&255));
    }
    hits++;
   }
  }
  out.close();if(!out)throw std::runtime_error("output write");
  double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::cout<<"{\"vertices\":"<<n<<",\"pairs\":"<<pairs<<",\"survivors\":"<<hits<<",\"elapsed_seconds\":"<<sec<<"}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}
}
