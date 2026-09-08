#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <vector>
int main(int argc,char**argv){
 try{
  if(argc!=2)throw std::runtime_error("usage: scan proof.drat");
  std::ifstream f(argv[1],std::ios::binary);if(!f)throw std::runtime_error("open");
  std::vector<std::pair<int,int>> edge(842);int id=2;
  for(int i=0;i<43;i++)for(int j=i+1;j<43;j++)if(!(i<40&&i/4==j/4)&&!(i>=40))edge[id++]={i,j};
  if(id!=842)throw std::runtime_error("edge map");
  std::uint64_t at=0,records=0,adds=0,dels=0,start=0;bool truncated=false;
  std::map<int,std::uint64_t> widths;std::map<std::vector<int>,std::pair<std::uint64_t,std::uint64_t>> candidates;
  std::uint64_t physical=0,small=0,maxvar=0;int tag;
  while((tag=f.get())!=EOF){
   start=at++;if(tag!='a'&&tag!='d')throw std::runtime_error("bad tag");
   std::vector<int> clause;std::uint64_t val=0;int shift=0,ch;
   bool complete=false;
   while((ch=f.get())!=EOF){
    ++at;if(ch==0){if(shift)throw std::runtime_error("noncanonical zero");complete=true;break;}
    val|=std::uint64_t(ch&127)<<shift;
    if(ch&128){shift+=7;if(shift>28)throw std::runtime_error("overflow");continue;}
    if(val<2||val>2147483647)throw std::runtime_error("literal range");
    maxvar=std::max(maxvar,val>>1);
    clause.push_back((val&1)?-static_cast<int>(val>>1):static_cast<int>(val>>1));val=0;shift=0;
   }
   if(!complete){truncated=true;break;}
   ++records;if(tag=='d'){++dels;continue;}++adds;++widths[int(clause.size())];
   if(!std::all_of(clause.begin(),clause.end(),[](int x){return std::abs(x)>=2&&std::abs(x)<=841;}))continue;
   ++physical;if(clause.size()>4||clause.empty())continue;++small;
   std::sort(clause.begin(),clause.end());if(std::adjacent_find(clause.begin(),clause.end())!=clause.end())throw std::runtime_error("duplicate");
   std::set<int> atoms;for(int x:clause){if(std::binary_search(clause.begin(),clause.end(),-x))throw std::runtime_error("tautology");auto [i,j]=edge[std::abs(x)];atoms.insert(i<40?i/4:i-30);atoms.insert(j<40?j/4:j-30);}
   if(atoms.size()>=3)candidates.emplace(clause,std::pair{records,start});
  }
  std::cout<<"{\"complete_records\":"<<records<<",\"additions\":"<<adds<<",\"deletions\":"<<dels<<",\"bytes_read\":"<<at<<",\"truncated_final_record\":"<<(truncated?"true":"false")<<",\"last_record_start\":"<<start<<",\"maximum_variable\":"<<maxvar<<",\"physical_additions\":"<<physical<<",\"small_physical_additions\":"<<small<<",\"candidates\":[";
  bool sep=false;for(const auto&[c,pos]:candidates){if(sep)std::cout<<',';sep=true;std::cout<<"{\"record\":"<<pos.first<<",\"offset\":"<<pos.second<<",\"clause\":[";for(std::size_t i=0;i<c.size();++i){if(i)std::cout<<',';std::cout<<c[i];}std::cout<<"]}";}
  std::cout<<"],\"width_histogram\":{";sep=false;for(auto [w,n]:widths){if(sep)std::cout<<',';sep=true;std::cout<<'"'<<w<<"\":"<<n;}std::cout<<"}}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}
}
