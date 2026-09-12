// Independent graph-definition checker. Witness bits are read byte by byte;
// graph neighborhoods use at most 19 bits. No 104-bit arithmetic is required.
#include <array>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using G=std::array<unsigned,19>;
static void need(bool x,const char*s){if(!x)throw std::runtime_error(s);}
static bool clique(const G&a,unsigned remaining,int size){
 if(size==0)return true;
 while(__builtin_popcount(remaining)>=size){
  unsigned u=__builtin_ctz(remaining);remaining&=remaining-1;
  if(clique(a,remaining&a[u],size-1))return true;
 }
 return false;
}
static G complement(const G&a,unsigned n){G b{};for(unsigned u=0;u<n;++u)b[u]=((1U<<n)-1)^a[u]^(1U<<u);return b;}
int main(int argc,char**argv){try{
 need(argc==4,"usage: checker CATALOG WITNESSES BLOCKED_IDS");
 std::ifstream cat(argv[1]),wit(argv[2],std::ios::binary),ids(argv[3]);need(bool(cat)&&bool(wit)&&bool(ids),"input open");
 std::vector<unsigned> blocked;unsigned index;while(ids>>index)blocked.push_back(index);need(ids.eof(),"invalid blocked IDs");
 for(unsigned i=1;i<blocked.size();++i)need(blocked[i-1]<blocked[i],"blocked ID order");
 unsigned count=0,sat=0,bad=0;std::string line;
 while(std::getline(cat,line)){
  need(line.size()==11&&line[0]=='J',"graph6 shape");for(char c:line)need(c>=63&&c<=126,"graph6 alphabet");need(((line.back()-63)&31)==0,"graph6 padding");
  G a{};unsigned bit=0;
  for(unsigned v=1;v<11;++v)for(unsigned u=0;u<v;++u,++bit)if(((line[1+bit/6]-63)>>(5-bit%6))&1){a[u]|=1U<<v;a[v]|=1U<<u;}
  need(!clique(a,2047,4)&&!clique(complement(a,11),2047,4),"not R44 core");
  std::array<unsigned,14> word{};bool sentinel=true;
  for(auto &byte:word){int c=wit.get();need(c!=EOF,"truncated witness");byte=unsigned(c);sentinel=sentinel&&(byte==255);}
  if(sentinel){need(bad<blocked.size()&&blocked[bad]==count,"UNSAT sentinel mismatch");++bad;}
  else{
   need(word[13]==0,"nonzero witness padding");unsigned k=0;
   for(unsigned u=0;u<19;++u)for(unsigned v=u+1;v<19;++v){
    bool fixed=(v<11)||(u>=11&&v<15)||(u>=15);
    if(fixed)continue;
    if((word[k/8]>>(k%8))&1){a[u]|=1U<<v;a[v]|=1U<<u;}++k;
   }
   need(k==104,"physical cross-edge count");
   need(!clique(a,(1U<<19)-1,4),"red K4 in model");need(!clique(complement(a,19),(1U<<19)-1,5),"blue K5 in model");++sat;
  }
  ++count;
 }
 need(count==546356,"incomplete core catalog");need(bad==blocked.size(),"extra blocked IDs");need(wit.get()==EOF,"trailing witness bytes");
 std::cout<<"{\"status\":\"ALL_NINETEEN_VERTEX_WITNESSES_VERIFIED\",\"cores\":"<<count<<",\"sat\":"<<sat<<",\"unsat_requiring_certificates\":"<<bad<<"}\n";
}catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}}
