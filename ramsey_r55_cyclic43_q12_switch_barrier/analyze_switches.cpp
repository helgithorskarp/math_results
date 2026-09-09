// Exhaustively classify degree-preserving alternating 2-switches at the 238
// saved objective-12 Cyclic(43) addition representatives.
#include <algorithm>
#include <array>
#include <atomic>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <mutex>
#include <sstream>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

constexpr int N=43,M=903;
using Adj=std::array<uint64_t,N>;

struct Input {
  std::array<std::array<int,N>,N> eid{};
  std::array<std::pair<int,int>,M> endpoints{};
  std::array<uint8_t,M> base{};
  std::vector<std::vector<int>> rows;
  explicit Input(const std::string& path){
    int ne=0;for(int a=0;a<N;++a)for(int b=a+1;b<N;++b){eid[a][b]=eid[b][a]=ne;endpoints[ne++]={a,b};}
    const std::array<int,11>L{1,2,7,10,12,13,14,16,18,20,21};
    for(int e=0;e<M;++e){auto[a,b]=endpoints[e];int d=std::min(b-a,N-(b-a));base[e]=std::find(L.begin(),L.end(),d)!=L.end();}
    std::ifstream in(path);if(!in)throw std::runtime_error("cannot open input");
    std::string s((std::istreambuf_iterator<char>(in)),{});auto key=s.find("\"complete_additional_objective_12_rotation_representatives\"");
    if(key==std::string::npos)throw std::runtime_error("key absent");
    size_t i=s.find('[',key);int depth=0;std::vector<int>row;
    for(;i<s.size();++i){char ch=s[i];if(ch=='['){++depth;if(depth==2)row.clear();}
      else if(ch==']'){if(depth==2){rows.push_back(row);row.clear();}if(--depth==0)break;}
      else if(depth==2&&ch>='0'&&ch<='9'){int x=0;do{x=10*x+s[i]-'0';++i;}while(i<s.size()&&s[i]>='0'&&s[i]<='9');--i;row.push_back(x);}}
    if(rows.size()!=238)throw std::runtime_error("expected 238 rows");
  }
};

int induced_triangles(uint64_t set,const Adj& adj){
  int count=0;
  while(set){int x=std::countr_zero(set);set&=set-1;uint64_t xn=adj[x]&set;
    while(xn){int y=std::countr_zero(xn);xn&=xn-1;count+=std::popcount(adj[y]&xn);}}
  return count;
}

int flip_delta(Adj& red,int u,int v){
  constexpr uint64_t MASK=(UINT64_C(1)<<N)-1;
  bool is_red=(red[u]>>v)&1U;
  uint64_t rc=red[u]&red[v];int rt=induced_triangles(rc,red);
  Adj blue{};for(int x=0;x<N;++x)blue[x]=MASK&~(red[x]|(UINT64_C(1)<<x));
  uint64_t bc=blue[u]&blue[v];int bt=induced_triangles(bc,blue);
  red[u]^=UINT64_C(1)<<v;red[v]^=UINT64_C(1)<<u;
  return is_red ? -rt+bt : rt-bt;
}

int direct_q(const Adj& red){
 int q=0;
 for(int a=0;a<N;++a)for(int b=a+1;b<N;++b)for(int c=b+1;c<N;++c)
 for(int d=c+1;d<N;++d)for(int e=d+1;e<N;++e){int vs[5]{a,b,c,d,e};int k=0;for(int i=0;i<5;++i)for(int j=i+1;j<5;++j)k+=(red[vs[i]]>>vs[j])&1U;q+=(k==0||k==10);}
 return q;
}

struct Result{uint64_t switches=0,descending=0,neutral=0,min_count=0;int min_q=100000;std::array<int,4>best{};};

Result analyze(const Input& in,int index){
  std::array<uint8_t,M> color=in.base;for(int e:in.rows[index])color[e]^=1;
  Adj adj{};std::array<int,N>deg{};for(int e=0;e<M;++e)if(color[e]){auto[u,v]=in.endpoints[e];adj[u]|=UINT64_C(1)<<v;adj[v]|=UINT64_C(1)<<u;++deg[u];++deg[v];}
  if(direct_q(adj)!=12)throw std::runtime_error("input is not q12");
  if(*std::min_element(deg.begin(),deg.end())<18||*std::max_element(deg.begin(),deg.end())>24)throw std::runtime_error("degree interval");
  Result r;
  for(int a=0;a<N;++a)for(int b=a+1;b<N;++b)for(int c=b+1;c<N;++c)for(int d=c+1;d<N;++d){
    std::array<std::array<int,2>,3> match{{{{in.eid[a][b],in.eid[c][d]}},{{in.eid[a][c],in.eid[b][d]}},{{in.eid[a][d],in.eid[b][c]}}}};
    for(int i=0;i<3;++i)for(int j=i+1;j<3;++j){bool ci=color[match[i][0]],cj=color[match[j][0]];
      if(color[match[i][1]]!=ci||color[match[j][1]]!=cj||ci==cj)continue;
      ++r.switches;std::array<int,4> move{match[i][0],match[i][1],match[j][0],match[j][1]};Adj work=adj;int q=12;
      for(int e:move){auto[u,v]=in.endpoints[e];q+=flip_delta(work,u,v);}
      if(q<12)++r.descending;else if(q==12)++r.neutral;
      if(q<r.min_q){if(direct_q(work)!=q)throw std::runtime_error("incremental delta mismatch");r.min_q=q;r.best=move;r.min_count=1;}
      else if(q==r.min_q)++r.min_count;
    }
  }
  return r;
}

int main(int argc,char**argv){
  if(argc<3){std::cerr<<"usage: analyze INPUT.json OUTPUT.tsv [workers]\n";return 2;}
  Input in(argv[1]);int workers=argc>3?std::stoi(argv[3]):std::max(1u,std::thread::hardware_concurrency());
  std::vector<Result> results(in.rows.size());std::atomic<int> next{0};std::vector<std::thread>threads;
  for(int w=0;w<workers;++w)threads.emplace_back([&]{for(;;){int i=next.fetch_add(1);if(i>=(int)in.rows.size())break;results[i]=analyze(in,i);}});
  for(auto&t:threads)t.join();
  std::ofstream out(argv[2]);out<<"index\ttoggles\tswitches\tdescending\tneutral\tminimum_q\tminimum_multiplicity\tbest_edges\n";
  uint64_t total=0,down=0,neutral=0;int local_minima=0,minimum=100000;
  for(int i=0;i<(int)results.size();++i){auto&r=results[i];total+=r.switches;down+=r.descending;neutral+=r.neutral;local_minima+=(r.descending==0);minimum=std::min(minimum,r.min_q);
    out<<i<<'\t'<<in.rows[i].size()<<'\t'<<r.switches<<'\t'<<r.descending<<'\t'<<r.neutral<<'\t'<<r.min_q<<'\t'<<r.min_count<<'\t';
    for(int k=0;k<4;++k){auto[u,v]=in.endpoints[r.best[k]];if(k)out<<',';out<<u<<'-'<<v;}out<<'\n';}
  std::cout<<"seeds="<<results.size()<<" switches="<<total<<" descending="<<down<<" neutral="<<neutral
           <<" local_minima="<<local_minima<<" global_minimum_neighbor_q="<<minimum<<"\n";
  return 0;
}
