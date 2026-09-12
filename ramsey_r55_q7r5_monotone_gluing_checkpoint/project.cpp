#include <fstream>
#include <iostream>
#include <vector>
#include <string>
#include <charconv>
#include <stdexcept>
#include <iomanip>
using namespace std;
void req(bool b,const char*s){if(!b)throw runtime_error(s);}
int main(int argc,char**argv){try{
 req(argc==4,"input base-count cores-tsv");ifstream in(argv[1]);string p,c;int nv,nc;in>>p>>c>>nv>>nc;req(p=="p"&&c=="cnf","header");int base=stoi(argv[2]);vector<int>lit;vector<uint32_t>off{0};lit.reserve(15000000);off.reserve(base+1);
 for(int i=0;i<base;i++){int z;while(in>>z&&z)lit.push_back(z);req(bool(in),"truncated input");off.push_back(lit.size());}
 ifstream f(argv[3]);int core,want;string bits;
 while(f>>core>>bits>>want){req(bits.size()==105,"core length");int count=0;vector<unsigned char>sat(base);
  for(int i=0;i<base;i++){bool drop=false;for(auto j=off[i];j<off[i+1];j++){int a=abs(lit[j]);if(a>=758&&a<=862&&((bits[a-758]=='1')==(lit[j]>0))){drop=true;break;}}sat[i]=drop;count+=!drop;}
  req(count==want,"parent clause count");cout<<core<<' '<<count<<'\n';string buf="p cnf 817 "+to_string(count)+"\n";uint64_t bytes=0;
  auto send=[&](){uint32_t size=buf.size();char h[4];for(int i=0;i<4;i++)h[i]=char((size>>(8*i))&255);cout.write(h,4);cout.write(buf.data(),buf.size());bytes+=buf.size();buf.clear();};char num[24];
  for(int i=0;i<base;i++){if(sat[i])continue;for(auto j=off[i];j<off[i+1];j++){int x=lit[j],a=abs(x);if(a>=758&&a<=862)continue;if(a>=863)x+=(x>0?-105:105);auto rr=to_chars(num,num+24,x);buf.append(num,rr.ptr);buf+=' ';}buf+="0\n";if(buf.size()>=1048576)send();}if(!buf.empty())send();char zero[4]={0,0,0,0};cout.write(zero,4);cout.flush();

 }
}catch(const exception&e){cerr<<e.what()<<'\n';return 1;}}
