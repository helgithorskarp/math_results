// Definition-level checker: no SAT encoder, solver or Python graph parser.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using G=std::array<unsigned,15>;
static void require(bool p,const char *s){if(!p)throw std::runtime_error(s);}
static bool clique(const G&a,unsigned remaining,int k){
 if(k==0)return true;
 while(__builtin_popcount(remaining)>=k){
  unsigned u=__builtin_ctz(remaining);remaining&=remaining-1;
  if(clique(a,remaining&a[u],k-1))return true;
 }
 return false;
}
static G complement(const G&a,int n){G b{};for(int i=0;i<n;++i)b[i]=((1U<<n)-1)^a[i]^(1U<<i);return b;}
int main(int argc,char**argv){try{
 require(argc==4,"usage: check_witnesses CATALOG WITNESSES BLOCKED_IDS");
 std::ifstream cat(argv[1]),wit(argv[2],std::ios::binary),ids(argv[3]);
 require(bool(cat)&&bool(wit)&&bool(ids),"open inputs");
 std::vector<unsigned> blocked;unsigned id;while(ids>>id)blocked.push_back(id);
 require(ids.eof(),"bad blocked ID");
 for(unsigned i=1;i<blocked.size();++i)require(blocked[i-1]<blocked[i],"blocked order");
 unsigned count=0,sat=0,unsat=0,max_edges=0,max_count=0;std::string line;
 while(std::getline(cat,line)){
  require(line.size()==11 && line[0]=='J',"graph6 shape");
  for(char c:line)require(c>=63 && c<=126,"graph6 alphabet");
  G a{};unsigned bit=0;
  for(unsigned j=1;j<11;++j)for(unsigned i=0;i<j;++i,++bit)
   if(((line[1+bit/6]-63)>>(5-bit%6))&1){a[i]|=1U<<j;a[j]|=1U<<i;}
  require(((line.back()-63)&31)==0,"graph6 padding");
  require(!clique(a,2047,4)&&!clique(complement(a,11),2047,4),"non R44 core");
  unsigned edges=0;for(unsigned u=0;u<11;++u)edges+=__builtin_popcount(a[u]);edges/=2;
  if(edges>max_edges){max_edges=edges;max_count=1;}else if(edges==max_edges)++max_count;
  uint64_t word=0;for(unsigned b=0;b<6;++b){int c=wit.get();require(c!=EOF,"truncated witness");word|=uint64_t(c)<<(8*b);}
  if(word==((1ULL<<48)-1)){
   require(unsat<blocked.size()&&blocked[unsat]==count,"UNSAT sentinel mismatch");++unsat;
  }else{
   require(word<(1ULL<<44),"nonzero witness padding");
   unsigned k=0;
   for(unsigned u=0;u<11;++u)for(unsigned v=11;v<15;++v,++k)
    if((word>>k)&1){a[u]|=1U<<v;a[v]|=1U<<u;}
   require(!clique(a,32767,4),"red K4 in witness");
   require(!clique(complement(a,15),32767,5),"blue K5 in witness");++sat;
  }
  ++count;
 }
 require(count==546356,"catalog count");require(unsat==blocked.size(),"unconsumed blocked IDs");
 require(wit.get()==EOF,"extra witness bytes");
 std::cout<<"{\"status\":\"ALL_SAT_WITNESSES_VERIFIED\",\"cores\":"<<count<<",\"sat\":"<<sat<<",\"unsat_requires_separate_proofs\":"<<unsat<<",\"maximum_core_red_edges\":"<<max_edges<<",\"maximum_core_count\":"<<max_count<<"}\n";
}catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}}
