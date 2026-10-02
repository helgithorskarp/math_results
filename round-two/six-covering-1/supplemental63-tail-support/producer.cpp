// Complete relaxed shared-set majorizer with a fourth (virtual TOP)9 resource.
#include <algorithm>
#include <array>
#include <bitset>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>
using Mask=std::bitset<180>;
using Hist=std::array<int,11>;
void need(bool ok,const char* msg){if(!ok)throw std::runtime_error(msg);}
int top(const Hist& h,int target){int left=target,score=0;for(int k=10;k>=0;--k){int n=std::min(left,h[k]);left-=n;score+=n*k;}need(left==0,"short top domain");return score;}
void partitions(std::array<int,7>& p,int at,int largest,std::vector<std::array<int,7>>& out){
 if(at==7){out.push_back(p);return;}
 for(int s=0;s<=std::min(largest+1,4);++s){p[at]=s;partitions(p,at+1,std::max(largest,s),out);}
}
int main(int argc,char** argv){try{
 need(argc==2,"usage: virtual9 target_size");int target=std::stoi(argv[1]);need(target>=111&&target<=124,"target size scope");
 const int threshold=5*target-144;
 Mask F;std::array<std::vector<Mask>,10> family;
 for(int e:std::vector<int>{2,3,5,9,4}){family[e].resize(e);for(int t=0;t<180;++t)if((4*t+3)%9!=6){family[e][t%e].set(t);F.set(t);}}
 need(F.count()==160,"literal S3 domain");
 std::vector<int> selected{8,3,6,12,5,10,20,9,18,36,16};
 int total=0,other=0;long original_phases=0,original_points=0;
 for(int d=2;d<=720;++d)if(720%d==0&&d!=2&&d!=4){
  int maximum=0,e=d/std::gcd(d,4);
  for(int a=0;a<7*d;++a){Mask hits;for(int x=a;x<5040;x+=7*d){++original_points;if(x%4==3&&x%9!=6)hits.set((x%720-3)/4);}
   maximum=std::max(maximum,static_cast<int>(hits.count()));++original_phases;
   if(std::find(selected.begin(),selected.end(),d)!=selected.end()){
    Mask expected;for(int t=0;t<180;++t)if(F[t]&&(4*t+3)%d==a%d)expected.set(t);
    need(hits==expected,"original resource phase projection differs");
    if(hits.any()){int r=-1;for(int z=0;z<e;++z)if((4*z+3)%d==a%d)r=z;need(r>=0&&family[e][r]==hits,"visible original family differs");}
   }
  }
  total+=maximum;if(std::find(selected.begin(),selected.end(),d)==selected.end())other+=maximum;
 }
 need(total==600&&other==144,"physical original capacities");
 std::array<int,7> p{};std::vector<std::array<int,7>> parts;partitions(p,1,0,parts);need(parts.size()==855,"complete five-copy RGS inventory");
 long phases=0,cases=0,active=0,active9=0,joint=0,at_threshold=0,full9_controls=0,ordered4=0;
 int maximum_extra_union=0,minimum_extra_loss=80;
 int max7=0,prune7=0,prune9=0,maxjoint=0,max_total=0;
 std::array<int,7> best_phase{},best_copy{};std::array<int,4> best_selectors{};Hist best_hist{};
 for(int b=0;b<2;++b)for(int a0=0;a0<3;++a0)for(int a1=a0;a1<3;++a1)for(int a2=a1;a2<3;++a2)
 for(int c0=0;c0<5;++c0)for(int c1=c0;c1<5;++c1)for(int c2=c1;c2<5;++c2){
  ++phases;std::array<int,7> phase{b,a0,a1,a2,c0,c1,c2};
  std::array<Mask,7> chosen{family[2][b],family[3][a0],family[3][a1],family[3][a2],family[5][c0],family[5][c1],family[5][c2]};
  for(const auto& copies:parts){++cases;std::array<Mask,5> Q;for(int j=0;j<7;++j)Q[copies[j]]|=chosen[j];
   Mask one,two,four;for(const auto& q:Q){Mask x=one&q;one^=q;Mask y=two&x;two^=x;four^=y;}
   std::array<Mask,6> Z;Hist h0{};for(int k=0;k<=5;++k){Z[k]=(k&1?one:F^one)&(k&2?two:F^two)&(k&4?four:F^four);h0[k]=static_cast<int>(Z[k].count());}
   int score7=top(h0,target);max7=std::max(max7,score7);
   if(score7+120<threshold){prune7=std::max(prune7,score7+120);continue;}
   ++active;
   for(int s9=0;s9<5;++s9)for(int r9=0;r9<9;++r9){
    Mask V=family[9][r9]&~Q[s9];std::array<Mask,10> Z9;Hist h9{};
    for(int k=0;k<=5;++k){Mask a=Z[k]&V,rest=Z[k]&~V;Z9[k]|=rest;Z9[k+4]|=a;h9[k]+=static_cast<int>(rest.count());h9[k+4]+=static_cast<int>(a.count());}
    int score9=top(h9,target);if(score9+40<threshold){prune9=std::max(prune9,score9+40);continue;}++active9;
    for(int s4=0;s4<5;++s4)for(int r4=0;r4<4;++r4){
     Mask W=family[4][r4]&~Q[s4];Hist h{};for(int k=0;k<=9;++k){int a=static_cast<int>((Z9[k]&W).count());h[k]+=h9[k]-a;h[k+1]+=a;}
     int score=top(h,target);++joint;if(score>=threshold)++at_threshold;
     if(target==117){
      need(score<=threshold,"new majorizer threshold exceeded");
      if(score==threshold){
       need(a0==a1&&a1==a2&&a0!=0&&c0<c1&&c1<c2,"equality projected phases");
       need(copies==std::array<int,7>{0,1,2,3,4,4,4},"equality five-copy allocation");
       need(s9>=1&&s9<=3&&r9%3!=a0&&r9!=3&&s4==0&&r4%2!=b,"equality selectors");
       need(h==Hist{8,36,36,6,29,36,9,0,0,0,0},"equality weight histogram");
       Mask mandatory,optional;
       // Directly reconstruct the threshold sets: selected W adds exactly1.
       for(int t=0;t<180;++t)if(F[t]){
        int w=0;for(const auto& q:Q)w+=q[t];w+=4*V[t]+W[t];
        if(w>=2)mandatory.set(t);else if(w==1)optional.set(t);
       }
       need(mandatory.count()==116&&optional.count()==36,"equality117 support shape");
       std::vector<std::array<int,2>> full;
       for(int ss=0;ss<5;++ss)for(int rr=0;rr<9;++rr){
        Mask candidate=family[9][rr]&~Q[ss];int possible=static_cast<int>((candidate&mandatory).count())
           +std::min(1,static_cast<int>((candidate&optional).count()));++full9_controls;
        need(possible<=20,"equality fine9 possible gain");
        if(possible==20)full.push_back({ss,rr});
       }
       need(full==std::vector<std::array<int,2>>{{1,r9},{2,r9},{3,r9}},"full20 fine9 resource domains not forced");
       for(const auto& aa:full)for(const auto& bb:full)for(const auto& cc:full)for(const auto& dd:full){
        std::array<Mask,5> extra;for(const auto& rr:std::array<std::array<int,2>,4>{aa,bb,cc,dd})extra[rr[0]]|=family[9][rr[1]]&~Q[rr[0]];
        int gain=0;for(const auto& e:extra)gain+=static_cast<int>(e.count());++ordered4;
        need(gain<=60,"four fine9 resources avoid necessary copy overlap");
        maximum_extra_union=std::max(maximum_extra_union,gain);minimum_extra_loss=std::min(minimum_extra_loss,80-gain);
       }
      }
     }
     if(score>maxjoint){maxjoint=score;best_phase=phase;best_copy=copies;best_selectors={s9,r9,s4,r4};best_hist=h;}
    }
   }
  }
 }
 max_total=std::max({prune7,prune9,maxjoint});
 std::cout<<"{\"status\":\"EXACT_VIRTUAL9_RELAXATION_CENSUS\",\"target_K\":"<<target<<",\"threshold\":"<<threshold
  <<",\"original_phase_checks\":"<<original_phases<<",\"original_progression_points\":"<<original_points
  <<",\"physical_total_capacity\":"<<total<<",\"other_resource_capacity\":"<<other
  <<",\"canonical_phases\":"<<phases<<",\"copy_partitions\":"<<parts.size()<<",\"canonical_cases\":"<<cases
  <<",\"active_seven\":"<<active<<",\"V_selectors\":"<<45*active<<",\"active_V\":"<<active9<<",\"joint_profiles\":"<<joint
  <<",\"max_seven_score\":"<<max7<<",\"pruned_seven_ceiling\":"<<prune7<<",\"pruned_V_ceiling\":"<<prune9
  <<",\"max_expanded_score\":"<<maxjoint<<",\"all_cases_ceiling\":"<<max_total<<",\"at_or_above_threshold\":"<<at_threshold
  <<",\"strict_exclusion\":"<<(max_total<threshold?"true":"false")
  <<",\"equality_full9_controls\":"<<full9_controls<<",\"ordered_four_resource_controls\":"<<ordered4
  <<",\"equality_max_extra_union\":"<<maximum_extra_union<<",\"equality_min_overlap_loss\":"<<minimum_extra_loss
  <<",\"equality117_excluded\":"<<(target==117&&max_total==441&&at_threshold==1200&&maximum_extra_union==60&&minimum_extra_loss==20?"true":"false")<<",\"best_phases\":[";
 for(int j=0;j<7;++j){std::cout<<(j?",":"")<<best_phase[j];}std::cout<<"],\"best_copies\":[";
 for(int j=0;j<7;++j){std::cout<<(j?",":"")<<best_copy[j];}std::cout<<"],\"best_selectors\":[";
 for(int j=0;j<4;++j){std::cout<<(j?",":"")<<best_selectors[j];}std::cout<<"],\"best_histogram\":[";
 for(int j=0;j<11;++j){std::cout<<(j?",":"")<<best_hist[j];}std::cout<<"]}\n";
 return 0;
 }catch(const std::exception& e){std::cerr<<e.what()<<"\n";return 1;}}
