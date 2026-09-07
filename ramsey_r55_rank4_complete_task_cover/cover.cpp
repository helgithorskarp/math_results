#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using U=std::uint32_t;
using W=std::uint64_t;

static int weight(U code,int points){
  int sum=0;
  for(int i=0;i<points;++i){sum+=static_cast<int>(code&3U);code>>=2U;}
  return sum;
}
static int rowrank(U code,int rank){
  U span=1U;
  for(int x=1;x<(1<<rank);++x)if((code>>(2*(x-1)))&3U){
    U old=span;
    for(int y=0;y<(1<<rank);++y)if((old>>y)&1U)span|=1U<<(y^x);
  }
  int result=0;for(int size=__builtin_popcount(span);size>1;size>>=1)++result;
  return result;
}

int main(int argc,char**argv){
 try{
  if(argc!=5&&argc!=6)throw std::runtime_error("usage: cover rank lower_weight upper_weight output.tsv [--selftest]");
  bool selftest=argc==6;if(selftest&&std::string(argv[5])!="--selftest")throw std::runtime_error("unknown option");
  int rank=std::stoi(argv[1]),lo=std::stoi(argv[2]),hi=std::stoi(argv[3]);
  if(rank<2||rank>4||hi!=lo+1)throw std::runtime_error("invalid domain");
  int points=(1<<rank)-1,bits=2*points,blocks=(points+4)/5;
  U limit=1U<<bits;
  std::vector<std::vector<int>> maps;
  for(int k=0;k<rank-1;++k){
    std::vector<int> map(points+1);
    for(int x=1;x<=points;++x){int y=x;if(((x>>k)^(x>>(k+1)))&1)y^=(1<<k)|(1<<(k+1));map[x]=y;}
    maps.push_back(map);
  }
  std::vector<int> trans(points+1);
  for(int x=1;x<=points;++x)trans[x]=x^(((x>>1)&1)?1:0);
  maps.push_back(trans);
  std::vector<std::vector<std::array<U,1024>>> tables(maps.size(),std::vector<std::array<U,1024>>(blocks));
  for(std::size_t g=0;g<maps.size();++g)for(int b=0;b<blocks;++b)for(U z=0;z<1024;++z){
    U image=0;
    for(int t=0;t<5;++t){int x=5*b+t+1;if(x<=points)image|=((z>>(2*t))&3U)<<(2*(maps[g][x]-1));}
    tables[g][b][z]=image;
  }
  if(selftest){
    U state=12345U;W tests=0;
    for(U i=0;i<65536U;++i){
      state=state*1664525U+1013904223U;U code=state&(limit-1U);
      for(std::size_t g=0;g<maps.size();++g){
        U fast=0,slow=0;
        for(int b=0;b<blocks;++b)fast|=tables[g][b][(code>>(10*b))&1023U];
        for(int x=1;x<=points;++x)slow|=((code>>(2*(x-1)))&3U)<<(2*(maps[g][x]-1));
        if(fast!=slow||weight(fast,points)!=weight(code,points)||rowrank(fast,rank)!=rowrank(code,rank))throw std::runtime_error("map selftest");
        ++tests;
      }
    }
    std::cout<<"{\"status\":\"VERIFIED_MAP_CONTROLS\",\"map_checks\":"<<tests<<"}\n";return 0;
  }
  std::vector<W> seen((static_cast<W>(limit)+63U)/64U,0);
  auto mark=[&](U x){W bit=W{1}<<(x&63U);W &slot=seen[x>>6U];bool fresh=(slot&bit)==0;slot|=bit;return fresh;};
  auto visited=[&](U x){return (seen[x>>6U]>>(x&63U))&W{1};};
  std::ofstream out(argv[4]);if(!out)throw std::runtime_error("cannot open output");
  out<<"code\tzero\torbit_size\tsupport\ttriples\n";
  W raw[2]={0,0},orbits[2]={0,0},nonfull[2]={0,0},nonfull_orbits[2]={0,0},covered[2]={0,0};
  std::vector<U> queue;queue.reserve(20160);
  for(U code=0;code<limit;++code){
    int w=rank==4?__builtin_popcount(code&0x15555555U)+2*__builtin_popcount((code>>1U)&0x15555555U):weight(code,points);
    if(w!=lo&&w!=hi)continue;
    int category=w-lo;++raw[category];if(visited(code))continue;
    queue.clear();queue.push_back(code);mark(code);
    for(std::size_t q=0;q<queue.size();++q){
      U current=queue[q];
      for(std::size_t g=0;g<maps.size();++g){
        U next=0;for(int b=0;b<blocks;++b)next|=tables[g][b][(current>>(10*b))&1023U];
        if(mark(next))queue.push_back(next);
      }
      if(queue.size()>20160)throw std::runtime_error("group orbit exceeds GL(4,2)");
    }
    covered[category]+=queue.size();
    if(rowrank(code,rank)!=rank){nonfull[category]+=queue.size();++nonfull_orbits[category];continue;}
    ++orbits[category];int support=0,triples=0;
    for(int x=0;x<points;++x){int m=static_cast<int>((code>>(2*x))&3U);support+=(m>0);triples+=(m==3);}
    out<<code<<'\t'<<hi-w<<'\t'<<queue.size()<<'\t'<<support<<'\t'<<triples<<'\n';
  }
  out.close();if(!out)throw std::runtime_error("output write failed");
  if(raw[0]!=covered[0]||raw[1]!=covered[1])throw std::runtime_error("orbit mass mismatch");
  std::cout<<"{\"rank\":"<<rank<<",\"lower_weight\":"<<lo<<",\"upper_weight\":"<<hi
    <<",\"raw\":["<<raw[0]<<','<<raw[1]<<"],\"nonspanning\":["<<nonfull[0]<<','<<nonfull[1]
    <<"],\"nonspanning_orbits\":["<<nonfull_orbits[0]<<','<<nonfull_orbits[1]
    <<"],\"spanning_orbits\":["<<orbits[0]<<','<<orbits[1]<<"],\"status\":\"COMPLETE_GENERATOR_ORBIT_COVER\"}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}
}
