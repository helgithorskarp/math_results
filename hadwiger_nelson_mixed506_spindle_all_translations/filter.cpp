#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
struct Table {int p; std::vector<int> accept; std::vector<std::array<int,2>> x,y;};
int main(int argc,char** argv){try{
 if(argc!=5)throw std::runtime_error("usage: filter INPUT OUTPUT BEGIN END");
 std::ifstream in(argv[1]); if(!in)throw std::runtime_error("cannot open input");
 int nx=0,ny=0,ns=0;
 if(!(in>>nx>>ny>>ns))throw std::runtime_error("truncated dimensions");
 if(nx<1||nx>20000||ny<1||ny>5000||ns<1||ns>40)throw std::runtime_error("invalid dimensions");
 std::vector<Table> ts(static_cast<std::size_t>(ns));
 for(auto& t:ts){in>>t.p;if(t.p<3||t.p>10000)throw std::runtime_error("invalid modulus");
  t.accept.resize(static_cast<std::size_t>(t.p));for(int& a:t.accept){in>>a;if(a!=0&&a!=1)throw std::runtime_error("invalid square flag");}
  t.x.resize(static_cast<std::size_t>(nx));t.y.resize(static_cast<std::size_t>(ny));
  for(auto* vs:{&t.x,&t.y})for(auto& xy:*vs)for(int& a:xy){in>>a;if(a<0||a>=t.p)throw std::runtime_error("coordinate out of range");}
 }
 if(!in)throw std::runtime_error("truncated input");
 std::string extra;
 if(in>>extra)throw std::runtime_error("trailing input");
 int begin=std::stoi(argv[3]),end=std::stoi(argv[4]);if(begin<0||end>nx||begin>end)throw std::runtime_error("invalid interval");
 std::ofstream out(argv[2]);if(!out)throw std::runtime_error("cannot open output");
 std::vector<std::uint64_t> counts(static_cast<std::size_t>(ns));std::uint64_t survivors=0;
 for(int i=begin;i<end;++i)for(int j=0;j<ny;++j){bool ok=true;
  for(int s=0;s<ns;++s){const auto& t=ts[static_cast<std::size_t>(s)];
   std::int64_t dx=t.x[static_cast<std::size_t>(i)][0]-t.y[static_cast<std::size_t>(j)][0];
   std::int64_t dy=t.x[static_cast<std::size_t>(i)][1]-t.y[static_cast<std::size_t>(j)][1];
   auto d=static_cast<std::size_t>((dx*dx+dy*dy)%t.p);
   if(t.accept[d]==0){ok=false;break;}++counts[static_cast<std::size_t>(s)];
  }
  if(ok){out<<i<<' '<<j<<'\n';++survivors;}
 }
 out.close();if(!out)throw std::runtime_error("output failure");
 std::cout<<"{\"begin\":"<<begin<<",\"end\":"<<end<<",\"pairs\":"<<static_cast<std::uint64_t>(end-begin)*static_cast<std::uint64_t>(ny)<<",\"survivors\":"<<survivors<<",\"stages\":[";
 for(int s=0;s<ns;++s){if(s)std::cout<<',';std::cout<<counts[static_cast<std::size_t>(s)];}std::cout<<"]}\n";
 }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;} }
