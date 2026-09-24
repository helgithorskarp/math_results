#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>
using Row=std::array<int,6>;
struct Choice { int source,target; Row row; };
struct Cover { Row value; int sum; bool extra; };
std::vector<Cover> covers;
std::uint64_t chambers=0,blocked=0,positive=0,extras=0;
void need(bool ok,const char*message){if(!ok)throw std::runtime_error(message);}
void enumerate_choices(const std::array<std::vector<Choice>,6>&opts,std::array<int,6>&selected,int p,std::uint32_t code){
 if(p<6){for(int k=0;k<static_cast<int>(opts[static_cast<size_t>(p)].size());k++){selected[static_cast<size_t>(p)]=k;enumerate_choices(opts,selected,p+1,code);}return;}
 chambers++;
 for(const auto&c:covers){bool good=true;
  for(int j=0;j<6;j++){int sum=0;for(int i=0;i<6;i++)sum+=c.value[static_cast<size_t>(i)]*opts[static_cast<size_t>(i)][static_cast<size_t>(selected[static_cast<size_t>(i)])].row[static_cast<size_t>(j)];if(sum>0){good=false;break;}}
  if(good){blocked++;extras+=c.extra;
   if(c.extra){std::cout<<"EXTRA "<<code;for(int i=0;i<6;i++)std::cout<<" "<<opts[static_cast<size_t>(i)][static_cast<size_t>(selected[static_cast<size_t>(i)])].source;for(int x:c.value)std::cout<<" "<<x;std::cout<<"\n";}
   return;}
 }
 positive++;std::cout<<"OPEN "<<code;
 for(int i=0;i<6;i++)std::cout<<" "<<opts[static_cast<size_t>(i)][static_cast<size_t>(selected[static_cast<size_t>(i)])].source;
 std::cout<<"\n";
}
int main(){try{
 constexpr std::uint32_t total=14348907; // 3^15; unordered pairs in lexicographic order.
 std::array<std::uint32_t,15> power{};power[0]=1;for(int k=1;k<15;k++)power[static_cast<size_t>(k)]=3*power[static_cast<size_t>(k-1)];
 std::array<std::array<int,6>,6> pair{};std::array<int,15> first{},second{};int index=0;
 for(int i=0;i<6;i++)for(int j=i+1;j<6;j++){pair[static_cast<size_t>(i)][static_cast<size_t>(j)]=index;pair[static_cast<size_t>(j)][static_cast<size_t>(i)]=index;first[static_cast<size_t>(index)]=i;second[static_cast<size_t>(index)]=j;index++;}
 using Move=std::array<std::array<std::uint32_t,3>,15>;std::vector<Move>maps;Row permutation{0,1,2,3,4,5};
 do{Move move{};for(int k=0;k<15;k++){int a=permutation[static_cast<size_t>(first[static_cast<size_t>(k)])],b=permutation[static_cast<size_t>(second[static_cast<size_t>(k)])];auto w=power[static_cast<size_t>(pair[static_cast<size_t>(a)][static_cast<size_t>(b)])];move[static_cast<size_t>(k)][1]=(a<b?1U:2U)*w;move[static_cast<size_t>(k)][2]=(a<b?2U:1U)*w;}maps.push_back(move);}while(std::next_permutation(permutation.begin(),permutation.end()));
 need(maps.size()==720,"permutation coverage");
 for(int word=1;word<4096;word++){int x=word;Cover c{{},0,false};for(int i=0;i<6;i++){c.value[static_cast<size_t>(i)]=x&3;c.sum+=x&3;x>>=2;}covers.push_back(c);}
 std::sort(covers.begin(),covers.end(),[](const Cover&a,const Cover&b){return a.sum<b.sum||(a.sum==b.sum&&a.value<b.value);});
 for(int i=0;i<6;i++)for(int j=i+1;j<6;j++){Cover c{{1,1,1,1,1,1},12,true};c.value[static_cast<size_t>(i)]=4;c.value[static_cast<size_t>(j)]=4;covers.push_back(c);}
 need(covers.size()==4110,"cover count");
 std::vector<std::uint8_t>seen(total,0);std::uint64_t covered=0;int types=0,zero=0;
 for(std::uint32_t code=0;code<total;code++){
  if(seen[code])continue;
  types++;std::array<int,15>states{};Row g{};auto x=code;
  for(int k=0;k<15;k++){int state=static_cast<int>(x%3U);x/=3U;states[static_cast<size_t>(k)]=state;int a=first[static_cast<size_t>(k)],b=second[static_cast<size_t>(k)];if(state==1)g[static_cast<size_t>(a)]|=1<<b;if(state==2)g[static_cast<size_t>(b)]|=1<<a;}
  int orbit=0;
  for(const auto&move:maps){std::uint32_t image=0;for(int k=0;k<15;k++)image+=move[static_cast<size_t>(k)][static_cast<size_t>(states[static_cast<size_t>(k)])];need(image>=code&&image<total,"orbit canonicalization");if(!seen[image]){seen[image]=1;orbit++;covered++;}}
  need(orbit>0&&720%orbit==0,"invalid orbit size");
  auto before=chambers;std::array<std::vector<Choice>,6>opts;bool has_zero=false;
  for(int p=0;p<6;p++){int out=g[static_cast<size_t>(p)],right=63^(out|(1<<p));
   for(int s=out;s;s=(s-1)&out){int target=0;for(int j=0;j<6;j++)if(s>>j&1)target|=g[static_cast<size_t>(j)]&right;int closure=0;for(int j=0;j<6;j++)if((out>>j&1)&&!(g[static_cast<size_t>(j)]&right&~target))closure|=1<<j;
    if(s==closure){Choice c{s,target,{}};for(int j=0;j<6;j++)c.row[static_cast<size_t>(j)]=((s>>j)&1)-((target>>j)&1);opts[static_cast<size_t>(p)].push_back(c);}}
   if(opts[static_cast<size_t>(p)].empty())has_zero=true;
  }
  if(has_zero)zero++;else{std::array<int,6>selected{};enumerate_choices(opts,selected,0,code);}
  std::cout<<"ORBIT "<<code<<" "<<orbit<<" "<<chambers-before<<"\n";
 }
 need(covered==total&&std::all_of(seen.begin(),seen.end(),[](std::uint8_t b){return b==1;}),"incomplete labeled coverage");
 std::cout<<"SUMMARY "<<types<<" "<<covered<<" "<<zero<<" "<<chambers<<" "<<blocked<<" "<<positive<<" "<<extras<<"\n";
 return 0;
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}}
