#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
using U=std::uint64_t;
const std::vector<std::vector<int>> groups={{10,12,15,16,18,20},{24,30},{36,40},{45,48},{60,72},{80,90},{120,144},{180,240},{360,720}};
void need(bool b,const std::string& m){if(!b)throw std::runtime_error(m);}
bool F(int x){return x%8!=5&&x%9!=6&&x%18!=3&&x%4!=0;}
int mod(int a,int m){return ((a%m)+m)%m;}
struct Term {int group;U weight;std::vector<std::pair<int,int>> rows;std::vector<int> selected;};
std::array<int,5> counts(const std::vector<int>& selected){
    std::array<int,5> c{};
    for(int x:selected)if(x%4==0&&x%9!=6){int t=x/4;
        for(int p=0;p<2;++p)for(int b=1;b<=2;++b)c[2*p+b-1]+=static_cast<int>(t%2!=p&&t%3!=b);
        c[4]+=static_cast<int>(t%3==0);
    }return c;
}
void caps_ok(const std::vector<int>& selected){auto c=counts(selected);for(int j=0;j<5;++j)need(c[j]<=(j==4?27:34),"coverage cap violated");}
int main(int argc,char**argv){try{
    need(argc==2,"certificate path required");std::ifstream in(argv[1]);need(bool(in),"cannot open compact certificate");
    int period,ng,num,den,n;U D;in>>period>>D>>ng>>num>>den>>n;
    need(period==720&&D==129870&&ng==2880&&num==377&&den==370&&n==18,"certificate header/domain");
    std::vector<Term> terms;std::array<U,9> group_mass{};int class_occurrences=0;
    for(int i=0;i<n;++i){Term t;int nr;in>>t.group>>t.weight>>nr;
        need(bool(in)&&0<=t.group&&t.group<9&&t.weight>0&&t.weight<=D&&nr>=0&&nr<=6,"term inventory");std::set<int> labels;
        for(int j=0;j<nr;++j){int a,m;in>>a>>m;need(bool(in)&&std::find(groups[t.group].begin(),groups[t.group].end(),m)!=groups[t.group].end()&&a>=0&&a<m&&labels.insert(m).second,"original class syntax");t.rows.emplace_back(a,m);++class_occurrences;}
        if(t.group==0)need(std::any_of(t.rows.begin(),t.rows.end(),[](auto r){return r.second==12&&r.first!=0;}),"twelve absent or phase0");
        for(int x=0;x<720;++x)if(std::any_of(t.rows.begin(),t.rows.end(),[x](auto r){return x%r.second==r.first;}))t.selected.push_back(x);
        caps_ok(t.selected);if(t.group==0)need(std::count_if(t.selected.begin(),t.selected.end(),F)>=204,"core gain below204");
        group_mass[t.group]+=t.weight;terms.push_back(t);
    }std::string extra;need(!(in>>extra),"trailing certificate material");for(U x:group_mass)need(x==D,"group probability not one");
    std::array<U,720> mass{};int transformations=0;U original_progression_points=0,transformed_point_checks=0,term_images=0;
    for(int k=0;k<12;++k)for(int ell=0;ell<2;++ell){int u=1+12*k,v=36*(k%2)+72*ell;
        std::array<int,5> permutation{{0,1,2,3,4}};
        do{std::array<int,720> image{};std::array<bool,720> used{};
            for(int x=0;x<720;++x){int y=mod(u*(x%144)+v,144),f=permutation[x%5];int z=y+144*mod(4*(f-y),5);need(z>=0&&z<720&&!used[z],"CRT map not bijection");used[z]=true;image[x]=z;need(F(x)==F(z),"compulsory set not preserved");++transformed_point_checks;}
            need(image[5]%8==5&&image[6]%9==6,"fixed classes changed");
            for(const auto&t:terms){std::vector<int> moved;for(int x:t.selected)moved.push_back(image[x]);caps_ok(moved);
                for(auto row:t.rows){int a=row.first,m=row.second,new_a=image[a]%m;for(int x=a;x<720;x+=m){need(image[x]%m==new_a,"transport changes original modulus/class");++original_progression_points;}
                    if(m==12)need(new_a!=0,"transport hits forbidden12phase");}
                if(t.group==0)need(std::count_if(moved.begin(),moved.end(),F)>=204,"transport core gain below204");
                for(int x:moved){if(F(x))mass[x]+=t.weight;}
                ++term_images;
            }++transformations;
        }while(std::next_permutation(permutation.begin(),permutation.end()));
    }
    need(transformations==ng&&class_occurrences==44,"full group/term count differs");
    U product=D*static_cast<U>(ng)*static_cast<U>(num);need(product%static_cast<U>(den)==0,"fractional scaled mass not integral");U expected=product/static_cast<U>(den);int checked=0;
    for(int x=0;x<720;++x)if(F(x)){need(mass[x]==expected,"literal pointwise fractional supply differs");++checked;}else need(mass[x]==0,"mass outside compulsory set");
    need(checked==370,"wrong physical compulsory size");
    std::cout<<"{\"terms\":18,\"original_class_occurrences\":44,\"group_average_size\":"<<transformations<<",\"compulsory_points\":"<<checked<<",\"common_denominator\":"<<D<<",\"scaled_point_mass\":"<<expected<<",\"original_progression_points_audited\":"<<original_progression_points<<",\"permutation_points_audited\":"<<transformed_point_checks<<",\"term_images_checked\":"<<term_images<<",\"pointwise_supply_verified\":true,\"full_cover_found\":false}\n";return 0;
}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
