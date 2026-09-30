#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>
// six-reviewer-4, independent mathematical reviewer.
// Complete normalized seven-uniform/two-red quotient classification.
// No author source imported. Output is private generated evidence.
// All indices <=10; all sums have absolute value <=36; counts fit uint64.
constexpr int N=11;
using Matrix=std::array<std::array<int,N>,N>;
struct Edge {int i,j;};
int main() try {
 const auto start=std::chrono::steady_clock::now();
 for(int adjacent=0;adjacent<=1;++adjacent) {
  Matrix w{};
  std::vector<Edge> red={{0,1},adjacent?Edge{0,2}:Edge{2,3}};
  for(auto e:red) w[e.i][e.j]=w[e.j][e.i]=1;
  std::vector<Edge> available;
  for(int i=0;i<N;++i) for(int j=i+1;j<N;++j) if(!w[i][j]) available.push_back({i,j});
  std::array<int,5> choice={0,1,2,3,4};
  std::uint64_t total=0,cover=0,square=0;
  std::uint64_t patterns=0,flags=0;
  bool done=false;
  while(!done) {
   ++total;
   for(auto c:choice) {auto e=available[c];w[e.i][e.j]=w[e.j][e.i]=-1;}
   bool ok=true;
   for(auto e:red) {
    int distinct=0;
    for(int k=0;k<N;++k) if(k!=e.i&&k!=e.j&&(w[e.i][k]==-1||w[e.j][k]==-1)) ++distinct;
    if(distinct<3) {ok=false;break;}
   }
   if(ok) {
    ++cover;
    for(int i=0;i<N&&ok;++i) for(int j=i+1;j<N;++j) if(!w[i][j]) {
     int s=0;for(int k=0;k<N;++k) s+=w[i][k]*w[j][k];
     if(s>0) {ok=false;break;}
    }
   }
   if(ok) {
    ++square;
    std::array<int,N> nr{},nb{};
    std::vector<std::array<int,4>> bounds;
    for(int i=0;i<N;++i) for(int j=0;j<N;++j) {nr[i]+=(w[i][j]==1);nb[i]+=(w[i][j]==-1);}
    for(int i=0;i<N;++i) for(int j=i+1;j<N;++j) if(w[i][j]) {
     int outside=0;
     for(int k=0;k<N;++k) if(k!=i&&k!=j) outside+=(1+w[i][j]*w[i][k])*(1+w[i][j]*w[j][k]);
     bounds.push_back({i,j,w[i][j],outside});
    }
    bool found=false;
    std::vector<unsigned> valid;
    for(unsigned word=0;word<(1u<<N);++word) {
     std::array<int,N> eps{};
     for(int i=0;i<N;++i) eps[i]=int((word>>i)&1u);
     bool good=true;
     for(int i=0;i<N;++i) if((eps[i]&&2*nr[i]>3)||(!eps[i]&&2*nb[i]>6)) {good=false;break;}
     if(!good) continue;
     for(auto b:bounds) {
      int pages=b[3]+2*(b[2]==1?eps[b[0]]+eps[b[1]]:2-eps[b[0]]-eps[b[1]]);
      if(pages>(b[2]==1?6:12)) {good=false;break;}
     }
     if(!good) continue;
     ++flags;found=true;valid.push_back(word);
    }
    patterns+=found;
    if(found) {
     std::cout<<"{\"record\":true,\"adjacent_red\":"<<adjacent<<",\"blue\":[";
     for(int i=0;i<5;++i) {if(i) std::cout<<",";auto e=available[choice[i]];std::cout<<"["<<e.i<<","<<e.j<<"]";}
     std::cout<<"],\"flags\":[";for(unsigned i=0;i<valid.size();++i) {if(i)std::cout<<",";std::cout<<valid[i];}std::cout<<"]}\n";
    }
   }
   for(auto c:choice) {auto e=available[c];w[e.i][e.j]=w[e.j][e.i]=0;}
   int at=4;
   while(at>=0&&choice[at]==int(available.size())-5+at) --at;
   if(at<0) done=true;
   else {++choice[at];for(int i=at+1;i<5;++i) choice[i]=choice[i-1]+1;}
  }
  std::cout<<"{\"adjacent_red\":"<<adjacent<<",\"complete\":true,\"all_patterns\":"<<total<<",\"blue_cover_pass\":"<<cover<<",\"matching_square_pass\":"<<square<<",\"survivor_patterns\":"<<patterns<<",\"survivor_flags\":"<<flags<<"}\n"<<std::flush;
 }
 std::cerr<<"seconds="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"\n";
} catch(const std::exception& e) {std::cerr<<e.what()<<"\n";return 2;}
