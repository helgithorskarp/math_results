#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <vector>
using I=long long;
I p;
I norm(I x){x%=p;return x<0?x+p:x;}
I mul(I a,I b){return a*b%p;}
I power(I a,I b){I r=1;for(;b;b>>=1,a=mul(a,a))if(b&1)r=mul(r,a);return r;}
struct Group{std::array<I,3> row;std::vector<std::pair<int,int>> edges;};
int main(int argc,char**argv){try{
 if(argc!=3)throw std::runtime_error("input output-prefix required");
 std::ifstream in(argv[1]);int n,k;in>>p>>n>>k;
 if(!in||p>1000001000||p<1000||n!=509||k<1)throw std::runtime_error("bad header");
 std::vector<std::array<I,2>> P(n);for(auto&v:P)in>>v[0]>>v[1];
 std::vector<Group> gs(k);int total=0;
 for(auto&g:gs){int s;in>>g.row[0]>>g.row[1]>>g.row[2]>>s;g.edges.resize(s);for(auto&e:g.edges)in>>e.first>>e.second;total+=s;}
 if(!in||total!=n*(n-1)/2)throw std::runtime_error("bad input");
 std::map<std::array<I,3>,std::vector<std::pair<int,int>>> metrics;
 std::ofstream singular(std::string(argv[2])+"_singular.txt");int zero=0;
 for(int i=1;i<n;i++)for(int j=i+1;j<n;j++){
  auto[ax,ay]=P[i];auto[bx,by]=P[j];I d=norm(mul(ax,by)-mul(ay,bx));
  if(!d){singular<<i<<' '<<j<<'\n';zero++;continue;}
  I xx=norm(mul(by,by)-mul(by,ay)+mul(ay,ay));
  I xy=norm(mul(by,ax)+mul(ay,bx)-2*(mul(by,bx)+mul(ax,ay)));
  I yy=norm(mul(bx,bx)-mul(bx,ax)+mul(ax,ax));I iv=power(mul(d,d),p-2);
  metrics[{mul(xx,iv),mul(xy,iv),mul(yy,iv)}].push_back({i,j});
 }
 std::ofstream residual(std::string(argv[2])+"_residual.txt"),all(std::string(argv[2])+"_metrics.txt");
 int three=0,rest=0,maxedge=0;long long instances=0;int mid=0;
 for(const auto&entry:metrics){
  const auto&q=entry.first;std::vector<std::vector<int>> adj(n);std::vector<int> ids;int edges=0;
  for(int z=0;z<k;z++){const auto&g=gs[z];I val=norm(mul(q[0],g.row[0])+mul(q[1],g.row[1])+mul(q[2],g.row[2]));
   if(val==1){ids.push_back(z);for(auto [a,b]:g.edges){adj[a].push_back(b);adj[b].push_back(a);edges++;}}
  }
  std::vector<int> deg(n),queue;std::vector<bool> gone(n,false);
  for(int v=0;v<n;v++){deg[v]=adj[v].size();if(deg[v]<4)queue.push_back(v);}
  for(size_t z=0;z<queue.size();z++){int v=queue[z];gone[v]=true;for(int u:adj[v])if(!gone[u]&&--deg[u]==3)queue.push_back(u);}
  bool ok=queue.size()==size_t(n);if(ok)three++;else rest++;
  all<<mid<<' '<<q[0]<<' '<<q[1]<<' '<<q[2]<<' '<<edges<<' '<<int(ok)<<' '<<entry.second.size();
  for(auto [i,j]:entry.second)all<<' '<<i<<' '<<j;
  all<<' '<<ids.size();for(int z:ids)all<<' '<<z;
  all<<'\n';
  if(!ok){residual<<mid<<' '<<ids.size();for(int z:ids)residual<<' '<<z;residual<<'\n';}
  maxedge=std::max(maxedge,edges);instances+=entry.second.size();mid++;
 }
 std::cout<<"{\"frames\":"<<instances<<",\"mod_singular\":"<<zero<<",\"mod_metrics\":"<<metrics.size()<<",\"three_degenerate\":"<<three<<",\"residual\":"<<rest<<",\"max_edges\":"<<maxedge<<"}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
