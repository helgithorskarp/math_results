#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include <chrono>
using I=std::int64_t;
using V=std::array<I,2>;
struct Pair{int a,b;V v;};
struct Row{V m;std::vector<Pair> pairs;};
I p,Q;
I mod(I x){x%=p;return x<0?x+p:x;}
I det(V a,V b){return mod(a[0]*b[1]-a[1]*b[0]);}
I norm(V a){return mod(a[0]*a[0]+3*a[1]*a[1]);}
V sub(V a,V b){return {mod(a[0]-b[0]),mod(a[1]-b[1])};}
bool keep(const std::array<V,3>& ms,const std::array<V,3>& ds){
 std::array<std::array<I,3>,3> lines{};
 for(std::size_t i=0;i<3;i++)lines[i]={mod(-ds[i][1]),ds[i][0],mod(ds[i][1]*ms[i][0]-ds[i][0]*ms[i][1])};
 I den=0,ox=0,oy=0;
 for(const auto&ij:std::array<std::array<int,2>,3>{{{0,1},{0,2},{1,2}}}){
  const auto&a=lines[static_cast<std::size_t>(ij[0])];const auto&b=lines[static_cast<std::size_t>(ij[1])];
  den=mod(a[0]*b[1]-b[0]*a[1]);
  if(den){ox=mod(a[1]*b[2]-b[1]*a[2]);oy=mod(a[2]*b[0]-b[2]*a[0]);break;}
 }
 if(!den)return true;
 I side=norm(sub(ms[1],ms[0]));I den2=mod(den*den);
 for(std::size_t i=0;i<3;i++){
  const auto&l=lines[i];if(mod(l[0]*ox+l[1]*oy+l[2]*den))return false;
  V offset{mod(ms[i][0]*den-ox),mod(ms[i][1]*den-oy)};
  if(mod(4*mod(Q-side)*norm(offset))!=mod(mod(side*mod(4*Q-norm(ds[i])))*den2))return false;
 }
 return true;
}
int main(int argc,char**argv){try{
 if(argc!=5)throw std::runtime_error("usage: screen input triangles output triangle_limit(0=all)");
 if(argv[4][0]=='-')throw std::runtime_error("negative limit");
 auto limit=std::stoull(argv[4]);std::ifstream in(argv[1]),ts(argv[2]);std::ofstream out(argv[3]);
 if(!in||!ts||!out)throw std::runtime_error("open failure");
 int ng;if(!(in>>p>>Q>>ng)||p<5||p>20000||Q<0||Q>=p||ng<1||ng>100)throw std::runtime_error("header");
 std::vector<std::vector<Row>> data(static_cast<std::size_t>(ng));
 for(auto&g:data){int n;if(!(in>>n)||n<1||n>100000)throw std::runtime_error("group size");g.resize(static_cast<std::size_t>(n));
  for(auto&r:g){int k;if(!(in>>r.m[0]>>r.m[1]>>k)||k<1||k>100000)throw std::runtime_error("row");
   for(auto x:r.m)if(x<0||x>=p)throw std::runtime_error("midpoint range");
   r.pairs.resize(static_cast<std::size_t>(k));for(auto&a:r.pairs){if(!(in>>a.a>>a.b>>a.v[0]>>a.v[1])||a.a<0||a.a>=a.b||a.b>=506)throw std::runtime_error("pair");for(auto x:a.v)if(x<0||x>=p)throw std::runtime_error("chord range");}
  }
 }
 std::string extra;if(in>>extra)throw std::runtime_error("extra input");
 const auto start=std::chrono::steady_clock::now();std::uint64_t tri=0,total=0,kept=0;
 int gi,i,j,k,e;
 while(ts>>gi){
  if(!(ts>>i>>j>>k>>e))throw std::runtime_error("incomplete triangle row");
  if(gi<0||gi>=ng||i<0||i>=j||j>=k||static_cast<std::size_t>(k)>=data[static_cast<std::size_t>(gi)].size()||(e!=1&&e!=-1))throw std::runtime_error("triangle row");
  const auto&g=data[static_cast<std::size_t>(gi)];const auto&a=g[static_cast<std::size_t>(i)];const auto&b=g[static_cast<std::size_t>(j)];const auto&c=g[static_cast<std::size_t>(k)];
  std::array<V,3> ms{a.m,b.m,c.m};tri++;
  for(const auto&x:a.pairs)for(const auto&y:b.pairs)for(const auto&z:c.pairs){
   total++;if(keep(ms,{x.v,y.v,z.v})){kept++;out<<gi<<' '<<i<<' '<<j<<' '<<k<<' '<<e<<' '<<x.a<<' '<<x.b<<' '<<y.a<<' '<<y.b<<' '<<z.a<<' '<<z.b<<'\n';}
  }
  if(limit && tri==limit)break;
 }
 if(!ts.eof() && !(limit && tri==limit))throw std::runtime_error("malformed triangle stream");
 out.flush();if(!out)throw std::runtime_error("write failure");
 std::cerr<<"triangles "<<tri<<" assignments "<<total<<" kept "<<kept<<" seconds "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<'\n';return 0;
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
