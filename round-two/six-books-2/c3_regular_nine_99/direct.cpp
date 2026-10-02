#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using U = std::uint32_t;
using Clock = std::chrono::steady_clock;
struct Frame { U word; std::array<U,9> X; std::array<U,12> columns; };
struct KWord { U word; std::array<U,12> rows; };
using Edge = std::pair<int,int>;
using Orbit = std::array<Edge,3>;

static int pop(U value) { return __builtin_popcount(value); }
static void require(bool ok, const char* message) { if (!ok) throw std::runtime_error(message); }

static std::vector<Orbit> orbits(int count) {
    std::vector<Orbit> result;
    for (int i=0;i<count;++i) {
        Orbit orbit{};
        for (int t=0;t<3;++t) orbit[static_cast<std::size_t>(t)]={3*i+t,3*i+(t+1)%3};
        result.push_back(orbit);
    }
    for (int i=0;i<count;++i) for (int j=i+1;j<count;++j) for (int shift=0;shift<3;++shift) {
        Orbit orbit{};
        for (int t=0;t<3;++t) orbit[static_cast<std::size_t>(t)]={3*i+t,3*j+(t+shift)%3};
        result.push_back(orbit);
    }
    return result;
}

template<std::size_t N>
static std::array<U,N> local(U word,const std::vector<Orbit>& slots) {
    std::array<U,N> result{};
    for (std::size_t bit=0;bit<slots.size();++bit) if ((word>>bit)&1U) {
        for (auto [u,v]:slots[bit]) {
            result[static_cast<std::size_t>(u)] |= 1U<<v;
            result[static_cast<std::size_t>(v)] |= 1U<<u;
        }
    }
    return result;
}

int main(int argc,char** argv) {
    try {
        require(argc==3,"usage: direct frames.txt output-directory");
        const auto start=Clock::now();
        auto guard=[&]() { require(std::chrono::duration<double>(Clock::now()-start).count()<25.0,"INCOMPLETE: fixed25-second native guard"); };
        const auto Aorbits=orbits(3),Borbits=orbits(4);
        require(Aorbits.size()==12 && Borbits.size()==22,"edge orbit partition");
        std::ifstream input(argv[1]);require(static_cast<bool>(input),"frame input unreadable");
        std::vector<Frame> frames;std::set<std::string> unique;
        std::string line;
        while (std::getline(input,line)) {
            std::istringstream fields(line);long long value=0;Frame frame{};
            require(static_cast<bool>(fields>>value) && value>=0 && value<4096,"local word domain");
            frame.word=static_cast<U>(value);
            require(frame.word==78 || frame.word==540 || frame.word==1616,"canonical local class");
            std::ostringstream key;key<<frame.word;
            for (auto& row:frame.X) {
                require(static_cast<bool>(fields>>value) && value>=0 && value<4096,"incidence row domain");
                row=static_cast<U>(value);key<<' '<<row;
            }
            std::string extra;require(!(fields>>extra),"extra incidence field");
            require(unique.insert(key.str()).second,"duplicate frame");
            const auto H=local<9>(frame.word,Aorbits);
            for (std::size_t a=0;a<9;++a) {
                require(pop(H[a])+pop(frame.X[a])+1==9,"A degree9");
                for (std::size_t b=0;b<12;++b) if ((frame.X[a]>>b)&1U) frame.columns[b]|=1U<<a;
            }
            for (U col:frame.columns) require(pop(col)==4,"B column degree4");
            for (int a=0;a<9;++a) for (int b=0;b<12;++b) {
                const int aa=3*(a/3)+(a+1)%3,bb=3*(b/3)+(b+1)%3;
                require(((frame.X[static_cast<std::size_t>(a)]>>b)&1U)==((frame.X[static_cast<std::size_t>(aa)]>>bb)&1U),"C3 incidence invariance");
            }
            for (int a=0;a<9;++a) for (int b=a+1;b<9;++b) {
                const auto u=static_cast<std::size_t>(a),v=static_cast<std::size_t>(b);
                if ((H[u]>>b)&1U) require(1+pop(H[u]&H[v])+pop(frame.X[u]&frame.X[v])<=3,"red A cap");
                else {
                    const U ba=511U^H[u]^(1U<<a),bc=511U^H[v]^(1U<<b);
                    require(pop(ba&bc)+pop((4095U^frame.X[u])&(4095U^frame.X[v]))<=6,"blue A cap");
                }
            }
            frames.push_back(frame);
        }
        require(frames.size()==37,"complete37 frame prerequisite");
        std::vector<KWord> candidates;
        std::uint64_t degree_words=0;
        const std::array<Edge,6> links={{{0,1},{0,2},{0,3},{1,2},{1,3},{2,3}}};
        const std::string prefix=std::string(argv[2])+"/";
        std::ofstream kstream(prefix+"direct-K-words.txt");require(static_cast<bool>(kstream),"K output");
        for (U word=0;word<(1U<<22);++word) {
            if ((word&16383U)==0) guard();
            std::array<int,4> degrees{};
            for (int i=0;i<4;++i) degrees[static_cast<std::size_t>(i)]=2*static_cast<int>((word>>i)&1U);
            for (std::size_t i=0;i<6;++i) {
                const int weight=pop((word>>(4+3*i))&7U);
                degrees[static_cast<std::size_t>(links[i].first)]+=weight;
                degrees[static_cast<std::size_t>(links[i].second)]+=weight;
            }
            bool degree_ok=true;for (int degree:degrees) if (degree!=5) degree_ok=false;
            if (!degree_ok) continue;
            ++degree_words;const auto rows=local<12>(word,Borbits);
            for (U row:rows) require(pop(row)==5,"literal K degree");
            bool good=true;
            for (int u=0;u<12 && good;++u) for (int v=u+1;v<12;++v) {
                const auto a=static_cast<std::size_t>(u),b=static_cast<std::size_t>(v);
                if ((rows[a]>>v)&1U) { if (pop(rows[a]&rows[b])>3) {good=false;break;} }
                else {
                    const U bu=4095U^rows[a]^(1U<<u),bv=4095U^rows[b]^(1U<<v);
                    if (pop(bu&bv)>4) {good=false;break;}
                }
            }
            if (good) {candidates.push_back({word,rows});kstream<<word<<'\n';}
        }
        kstream.close();require(static_cast<bool>(kstream),"K stream complete write");
        std::ofstream flags(prefix+"direct-outcomes.txt",std::ios::binary);require(static_cast<bool>(flags),"outcomes output");
        std::uint64_t choices=0,valid=0,red_rejected=0,blue_rejected=0;
        std::vector<std::uint64_t> per_frame_valid;
        for (const auto& frame:frames) {
            const auto H=local<9>(frame.word,Aorbits);std::uint64_t frame_valid=0;
            for (std::size_t index=0;index<candidates.size();++index) {
                if ((index&1023U)==0) guard();
                const auto& K=candidates[index];std::array<U,22> rows{};
                for (std::size_t a=0;a<9;++a) rows[a]=H[a]|(frame.X[a]<<9)|(1U<<21);
                for (std::size_t b=0;b<12;++b) rows[9+b]=frame.columns[b]|(K.rows[b]<<9);
                rows[21]=511U;for (U row:rows) require(pop(row)==9,"literal whole host degree");
                int bad_color=0;
                for (int u=0;u<22 && bad_color==0;++u) for (int v=u+1;v<22;++v) {
                    const auto a=static_cast<std::size_t>(u),b=static_cast<std::size_t>(v);
                    if ((rows[a]>>v)&1U) {
                        if (pop(rows[a]&rows[b])>3) {bad_color=1;break;}
                    } else {
                        const U bu=((1U<<22)-1U)^rows[a]^(1U<<u),bv=((1U<<22)-1U)^rows[b]^(1U<<v);
                        if (pop(bu&bv)>6) {bad_color=2;break;}
                    }
                }
                ++choices;
                if (bad_color==0) {++valid;++frame_valid;flags.put('1');std::cerr<<"VALID "<<frame.word<<' '<<K.word<<'\n';}
                else {flags.put('0');if (bad_color==1) ++red_rejected;else ++blue_rejected;}
            }
            per_frame_valid.push_back(frame_valid);
        }
        flags.close();require(static_cast<bool>(flags),"outcome stream complete write");guard();
        std::ostringstream json;
        json<<"{\"status\":\"COMPLETE_LITERAL_REGULAR9_C3_CENSUS\",\"K_words_checked\":4194304,\"K_degree_words\":"<<degree_words
            <<",\"K_local_cap_words\":"<<candidates.size()<<",\"frames\":"<<frames.size()<<",\"completion_choices\":"<<choices
            <<",\"valid\":"<<valid<<",\"red_rejected\":"<<red_rejected<<",\"blue_rejected\":"<<blue_rejected<<",\"per_frame_valid\":[";
        for (std::size_t i=0;i<per_frame_valid.size();++i) {if (i) json<<',';json<<per_frame_valid[i];}
        json<<"],\"seconds\":"<<std::setprecision(9)<<std::chrono::duration<double>(Clock::now()-start).count()<<"}";
        std::ofstream summary(prefix+"direct-summary.json");summary<<json.str()<<'\n';summary.close();require(static_cast<bool>(summary),"summary complete write");
        std::cout<<json.str()<<'\n';return 0;
    } catch (const std::exception& error) {std::cerr<<error.what()<<'\n';return 2;}
}
