#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
using Mask=uint64_t;
using Adj=std::array<Mask,43>;
unsigned n=0,target=21; uint64_t nodes=0,leaves=0; Adj graph{};
std::array<std::vector<Mask>,12341> link3;
std::ofstream proof;
unsigned choose2(unsigned v){return v*(v-1)/2;}
unsigned choose3(unsigned v){return v*(v-1)*(v-2)/6;}
unsigned triple(unsigned a,unsigned b,unsigned c){std::array<unsigned,3>x{a,b,c};std::sort(x.begin(),x.end());return x[0]+choose2(x[1])+choose3(x[2]);}
unsigned count(Mask x){return unsigned(__builtin_popcountll(x));}
unsigned bit(Mask x){return unsigned(__builtin_ctzll(x));}
std::vector<Mask> groups(Mask C,const Adj& conflict){
 std::vector<Mask> out;
 while(C){Mask group=0,possible=C;
  while(possible){unsigned v=bit(possible),best=0;for(Mask t=possible;t;t&=t-1){unsigned w=bit(t),d=count(conflict[w]&possible);if(d>best){best=d;v=w;}}
   Mask z=Mask(1)<<v;group|=z;C&=~z;possible&=conflict[v];}
  out.push_back(group);
 }return out;
}
bool solve(Mask S,Mask C,const Adj& conflict){
 ++nodes;if(nodes%1000000==0)std::cerr<<"nodes "<<nodes<<"\n";
 if(count(S)>=target){std::cout<<"WITNESS "<<S<<"\n";return true;}
 auto cliques=groups(C,conflict);
 if(count(S)+cliques.size()<target){proof<<"L "<<cliques.size();for(Mask q:cliques)proof<<' '<<q;proof<<'\n';++leaves;return false;}
 unsigned v=bit(C),best=0;for(Mask t=C;t;t&=t-1){unsigned w=bit(t),d=count(conflict[w]&C);if(d>best){best=d;v=w;}}
 Mask vb=Mask(1)<<v;proof<<"B "<<v<<'\n';
 Mask D=(C&~vb)&~conflict[v];Adj next=conflict;
 std::vector<unsigned> selected;for(Mask t=S;t;t&=t-1)selected.push_back(bit(t));
 for(unsigned i=0;i<selected.size();++i)for(unsigned j=i+1;j<selected.size();++j){
  for(Mask pair:link3[triple(selected[i],selected[j],v)])if((pair&D)==pair){unsigned x=bit(pair);unsigned y=bit(pair&(pair-1));next[x]|=Mask(1)<<y;next[y]|=Mask(1)<<x;}}
 if(solve(S|vb,D,next))return true;
 return solve(S,C&~vb,conflict);
}
int main(int argc,char** argv){
 try{if(argc!=3)throw std::runtime_error("usage: cover GRAPH PROOF");
 std::ifstream in(argv[1]);unsigned m;if(!(in>>n>>m)||n<5||n>43)throw std::runtime_error("header");
 for(unsigned k=0;k<m;k++){unsigned a,b;if(!(in>>a>>b)||a>=b||b>=n||(graph[a]>>b&1))throw std::runtime_error("edge");graph[a]|=Mask(1)<<b;graph[b]|=Mask(1)<<a;}std::string extra;if(in>>extra)throw std::runtime_error("trailing graph input");
 uint64_t cycles=0;for(unsigned a=0;a<n;a++)for(unsigned b=a+1;b<n;b++)for(unsigned c=b+1;c<n;c++)for(unsigned d=c+1;d<n;d++)for(unsigned e=d+1;e<n;e++){
 std::array<unsigned,5>x{a,b,c,d,e};Mask P=0;for(unsigned v:x)P|=Mask(1)<<v;bool ok=true;for(unsigned v:x)if(count(graph[v]&P)!=2){ok=false;break;}if(!ok)continue;++cycles;
 for(unsigned i=0;i<5;i++)for(unsigned j=i+1;j<5;j++)for(unsigned k=j+1;k<5;k++){Mask T=(Mask(1)<<x[i])|(Mask(1)<<x[j])|(Mask(1)<<x[k]);link3[triple(x[i],x[j],x[k])].push_back(P^T);}}
 proof.open(argv[2]);if(!proof)throw std::runtime_error("proof output");proof<<"C5COVER 1 "<<n<<' '<<target<<'\n';Adj conflict{};
 bool witness=solve(0,(Mask(1)<<n)-1,conflict);proof.close();if(!proof)throw std::runtime_error("proof write");
 std::cout<<"cycles "<<cycles<<" nodes "<<nodes<<" leaves "<<leaves<<" status "<<(witness?"C5_FREE_21_FOUND":"COMPLETE_21_COVER")<<'\n';return witness?10:0;
 }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 2;}}
