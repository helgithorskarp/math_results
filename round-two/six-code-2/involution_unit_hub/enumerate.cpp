#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
constexpr int W=14;
using Bits=std::array<std::uint64_t,W>;
bool empty(const Bits &a) {for(auto w:a)if(w)return false;return true;}
int first(const Bits &a) {for(int i=0;i<W;i++)if(a[i])return i*64+std::countr_zero(a[i]);return -1;}
void reset(Bits &a,int v){a[v/64]&=~(std::uint64_t(1)<<(v%64));}
void set(Bits &a,int v){a[v/64]|=std::uint64_t(1)<<(v%64);}
std::vector<Bits> adjacency;
std::vector<std::uint32_t> masks;
std::vector<std::uint64_t> mandatory;
std::array<Bits,60> column_rows{};
std::array<Bits,18> point_rows{};
std::array<int,18> reps{};
std::uint64_t nodes=0, covers=0, node_limit=0;
std::chrono::steady_clock::time_point start;
double seconds=0;
std::ofstream output;

void search(Bits pool,std::uint64_t columns,std::vector<int> &chosen) {
  nodes++;
  if((nodes&1023u)==0 && (nodes>node_limit || std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()>seconds))
    throw std::runtime_error("INCOMPLETE");
  if(columns==0) {
    if(chosen.size()!=16)return;
    for(int a=2;a<18;a++)if(reps[a]!=4)return;
    auto solution=chosen;std::sort(solution.begin(),solution.end());
    for(std::size_t i=0;i<solution.size();i++){if(i)output<<' ';output<<solution[i];}output<<'\n';covers++;return;
  }
  if(chosen.size()>=16)return;
  for(int a=2;a<18;a++) {
    if(reps[a]>4)return;
    if(reps[a]==4)for(int w=0;w<W;w++)pool[w]&=~point_rows[a][w];
  }
  for(int a=2;a<18;a++) {
    int possible=0;for(int w=0;w<W;w++)possible+=std::popcount(pool[w]&point_rows[a][w]);
    if(possible<4-reps[a])return;
  }
  Bits branch{};int least=865;
  auto rest=columns;
  while(rest) {
    int c=std::countr_zero(rest);rest&=rest-1;
    Bits available{};int count=0;
    for(int w=0;w<W;w++){available[w]=pool[w]&column_rows[c][w];count+=std::popcount(available[w]);}
    if(count==0)return;
    if(count<least){least=count;branch=available;if(count==1)break;}
  }
  while(!empty(branch)) {
    int v=first(branch);reset(branch,v);
    if((mandatory[v]&columns)!=mandatory[v])throw std::runtime_error("repeated mandatory pair");
    chosen.push_back(v);for(int a=2;a<18;a++)if(masks[v]&(1u<<a))reps[a]++;
    Bits next{};for(int w=0;w<W;w++)next[w]=pool[w]&adjacency[v][w];
    search(next,columns^mandatory[v],chosen);
    chosen.pop_back();for(int a=2;a<18;a++)if(masks[v]&(1u<<a))reps[a]--;
  }
}

int run(int argc,char **argv) {
  if(argc!=6)throw std::runtime_error("model root nodes seconds output");
  std::ifstream input(argv[1]);int n;input>>n;
  if(n!=864)throw std::runtime_error("bad model size");
  masks.resize(n);adjacency.resize(n);mandatory.resize(n);
  std::array<std::array<int,18>,18> column_id{};for(auto &r:column_id)r.fill(-1);
  int cols=0;
  for(int a=2;a<18;a++)for(int b=a+1;b<18;b++) {
    if((a>=14&&b>=14) || (a<14&&b<14 && (a-2)/6*2+a%2 != (b-2)/6*2+b%2))
      column_id[a][b]=cols++;
  }
  if(cols!=60)throw std::runtime_error("bad mandatory pair count");
  for(int v=0;v<n;v++) {
    int degree;input>>masks[v]>>degree;
    if(!input || std::popcount(masks[v])!=4 || (masks[v]&3u) || masks[v]>=(1u<<18) || degree<0 || degree>=n)throw std::runtime_error("bad row");
    for(int j=0;j<degree;j++){int w;input>>w;if(!input||w<0||w>=n||w==v||(adjacency[v][w/64]&(std::uint64_t(1)<<(w%64))))throw std::runtime_error("bad edge");set(adjacency[v],w);}
    for(int a=2;a<18;a++)if(masks[v]&(1u<<a)) {
      set(point_rows[a],v);
      for(int b=a+1;b<18;b++)if((masks[v]&(1u<<b))&&column_id[a][b]>=0) {
        int c=column_id[a][b];mandatory[v]|=std::uint64_t(1)<<c;set(column_rows[c],v);
      }
    }
    if(mandatory[v]==0)throw std::runtime_error("empty column row");
  }
  if(!input)throw std::runtime_error("truncated model");
  std::string extra;if(input>>extra)throw std::runtime_error("trailing input");
  auto flip=[](std::uint32_t b){return ((b&0x15555u)<<1)|((b&0x2aaaau)>>1);};
  for(int v=0;v<n;v++)for(int w=0;w<n;w++){
    bool edge=(adjacency[v][w/64]&(std::uint64_t(1)<<(w%64)))!=0;
    bool expected=v!=w&&std::popcount(masks[v]&masks[w])<=1&&std::popcount(masks[v]&flip(masks[w]))<=2;
    if(edge!=expected)throw std::runtime_error("wrong graph edge");
  }
  int root=std::stoi(argv[2]);node_limit=std::stoull(argv[3]);seconds=std::stod(argv[4]);
  if(root<0||root>=n||node_limit<1||seconds<=0)throw std::runtime_error("bad root/guard");
  std::vector<int> chosen{root};for(int a=2;a<18;a++)if(masks[root]&(1u<<a))reps[a]++;
  output.open(argv[5]);if(!output)throw std::runtime_error("output failure");
  start=std::chrono::steady_clock::now();std::string status="COMPLETE";
  try{search(adjacency[root],((std::uint64_t(1)<<60)-1)^mandatory[root],chosen);}catch(const std::runtime_error &e){status=e.what();}
  output.close();
  std::cout<<status<<" root "<<root<<" nodes "<<nodes<<" covers "<<covers<<" seconds "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<std::endl;
  if(status!="COMPLETE")return 2;
  return 0;
}
int main(int argc,char **argv){try{return run(argc,argv);}catch(const std::exception&e){std::cerr<<"ERROR "<<e.what()<<'\n';return 2;}}
