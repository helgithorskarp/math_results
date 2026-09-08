// Independent streaming RUP-only LRAT checker for the h3927 certificate.
#include <climits>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {
enum class TokenKind { kEnd, kInteger, kWord };

struct Token {
  TokenKind kind = TokenKind::kEnd;
  int integer = 0;
  std::string word;
};

class Scanner {
 public:
  explicit Scanner(const char* path) : file_(std::fopen(path, "rb")) {
    if (file_ == nullptr) {
      throw std::runtime_error("input open");
    }
  }
  ~Scanner() { std::fclose(file_); }

  Token Next() {
    int character = Get();
    while (character != EOF && IsSpace(character)) {
      character = Get();
    }
    if (character == EOF) {
      return {};
    }
    if ((character >= 'a' && character <= 'z') ||
        (character >= 'A' && character <= 'Z')) {
      std::string word;
      do {
        word.push_back(static_cast<char>(character));
        character = Get();
      } while ((character >= 'a' && character <= 'z') ||
               (character >= 'A' && character <= 'Z'));
      PutBack(character);
      return {TokenKind::kWord, 0, std::move(word)};
    }
    bool negative = false;
    if (character == '-') {
      negative = true;
      character = Get();
    }
    if (character < '0' || character > '9') {
      throw std::runtime_error("token syntax");
    }
    std::uint64_t magnitude = 0;
    do {
      const unsigned digit = static_cast<unsigned>(character - '0');
      if (magnitude >
          (static_cast<std::uint64_t>(INT_MAX) - digit) / 10) {
        throw std::runtime_error("integer range");
      }
      magnitude = 10 * magnitude + digit;
      character = Get();
    } while (character >= '0' && character <= '9');
    PutBack(character);
    int value = static_cast<int>(magnitude);
    if (negative) {
      value = -value;
    }
    return {TokenKind::kInteger, value, {}};
  }

  void SkipLine() {
    int character = Get();
    while (character != EOF && character != '\n') {
      character = Get();
    }
  }

 private:
  static constexpr std::size_t kBuffer = 1U << 20;
  FILE* file_;
  std::vector<unsigned char> buffer_ = std::vector<unsigned char>(kBuffer);
  std::size_t position_ = 0;
  std::size_t available_ = 0;
  int pushed_ = -2;

  static bool IsSpace(int character) {
    return character == ' ' || character == '\t' || character == '\r' ||
           character == '\n';
  }

  int Get() {
    if (pushed_ != -2) {
      const int answer = pushed_;
      pushed_ = -2;
      return answer;
    }
    if (position_ == available_) {
      available_ = std::fread(buffer_.data(), 1, buffer_.size(), file_);
      position_ = 0;
      if (available_ == 0) {
        if (std::ferror(file_)) {
          throw std::runtime_error("input read");
        }
        return EOF;
      }
    }
    return buffer_[position_++];
  }

  void PutBack(int character) {
    if (character != EOF) {
      if (pushed_ != -2) {
        throw std::runtime_error("scanner pushback");
      }
      pushed_ = character;
    }
  }
};

struct Clause {
  bool active = false;
  std::vector<int> literals;
};

void Need(bool condition, const std::string& message) {
  if (!condition) {
    throw std::runtime_error(message);
  }
}

Token NextNoncomment(Scanner& scanner) {
  for (;;) {
    Token token = scanner.Next();
    if (token.kind == TokenKind::kWord && token.word == "c") {
      scanner.SkipLine();
      continue;
    }
    return token;
  }
}

int Integer(Token token, const std::string& message) {
  Need(token.kind == TokenKind::kInteger, message);
  return token.integer;
}

std::pair<int, std::vector<Clause>> ReadFormula(const char* path) {
  Scanner scanner(path);
  Token token = NextNoncomment(scanner);
  Need(token.kind == TokenKind::kWord && token.word == "p", "CNF p header");
  token = scanner.Next();
  Need(token.kind == TokenKind::kWord && token.word == "cnf", "CNF type");
  const int variables = Integer(scanner.Next(), "CNF variables");
  const int declared = Integer(scanner.Next(), "CNF clauses");
  Need(variables > 0 && declared >= 0, "CNF dimensions");
  std::vector<Clause> database(1);
  std::vector<int> pending;
  for (;;) {
    token = NextNoncomment(scanner);
    if (token.kind == TokenKind::kEnd) {
      break;
    }
    const int literal = Integer(std::move(token), "CNF literal");
    if (literal == 0) {
      database.push_back({true, std::move(pending)});
      pending.clear();
    } else {
      Need(std::abs(literal) <= variables, "CNF variable range");
      pending.push_back(literal);
    }
  }
  Need(pending.empty() && static_cast<int>(database.size()) == declared + 1,
       "CNF clause count");
  return {variables, std::move(database)};
}
}  // namespace

int main(int argc, char** argv) {
  try {
    Need(argc == 3, "usage: review_lrat formula.cnf proof.lrat");
    auto formula = ReadFormula(argv[1]);
    const int variables = formula.first;
    std::vector<Clause> database = std::move(formula.second);
    const int original_clauses = static_cast<int>(database.size()) - 1;
    int last_addition = original_clauses;
    std::vector<signed char> assignment(static_cast<std::size_t>(variables) + 1, 0);
    std::vector<int> touched;
    std::uint64_t additions = 0;
    std::uint64_t deletions = 0;
    std::uint64_t hints_used = 0;
    std::uint64_t deletion_records = 0;
    bool checked_empty = false;
    Scanner proof(argv[2]);

    for (;;) {
      Token head = NextNoncomment(proof);
      if (head.kind == TokenKind::kEnd) {
        break;
      }
      const int identifier = Integer(std::move(head), "LRAT record label");
      Need(identifier >= 0, "negative LRAT label");
      Token second = proof.Next();
      if (second.kind == TokenKind::kWord && second.word == "d") {
        ++deletion_records;
        for (;;) {
          const int target = Integer(proof.Next(), "deletion target");
          if (target == 0) {
            break;
          }
          Need(target > 0 && target < static_cast<int>(database.size()) &&
                   database[target].active,
               "missing/repeated deletion");
          database[target].active = false;
          std::vector<int>().swap(database[target].literals);
          ++deletions;
        }
        continue;
      }

      Need(identifier > last_addition, "nonincreasing addition label");
      last_addition = identifier;
      std::vector<int> learned;
      int literal = Integer(std::move(second), "learned literal");
      while (literal != 0) {
        Need(std::abs(literal) <= variables, "learned variable range");
        learned.push_back(literal);
        literal = Integer(proof.Next(), "learned literal");
      }

      bool conflict = false;
      touched.clear();
      for (const int member : learned) {
        const int variable = std::abs(member);
        const signed char assumed = member > 0 ? -1 : 1;
        if (assignment[variable] == 0) {
          assignment[variable] = assumed;
          touched.push_back(variable);
        } else if (assignment[variable] != assumed) {
          conflict = true;
        }
      }

      for (;;) {
        const int hint = Integer(proof.Next(), "RUP hint");
        if (hint == 0) {
          break;
        }
        Need(hint > 0 && hint < static_cast<int>(database.size()) &&
                 database[hint].active,
             "missing/deleted RUP hint");
        if (conflict) {
          continue;
        }
        ++hints_used;
        bool satisfied = false;
        int unit = 0;
        bool multiple = false;
        for (const int member : database[hint].literals) {
          const int variable = std::abs(member);
          const signed char sign = member > 0 ? 1 : -1;
          if (assignment[variable] == sign) {
            satisfied = true;
            break;
          }
          if (assignment[variable] == 0) {
            if (unit == 0) {
              unit = member;
            } else if (unit != member) {
              multiple = true;
            }
          }
        }
        if (satisfied) {
          continue;
        }
        Need(!multiple, "hint is not unit or conflicting");
        if (unit == 0) {
          conflict = true;
        } else {
          const int variable = std::abs(unit);
          Need(assignment[variable] == 0, "internal propagation state");
          assignment[variable] = unit > 0 ? 1 : -1;
          touched.push_back(variable);
        }
      }
      Need(conflict, "RUP sequence ended without conflict");
      for (const int variable : touched) {
        assignment[variable] = 0;
      }
      if (database.size() <= static_cast<std::size_t>(identifier)) {
        database.resize(static_cast<std::size_t>(identifier) + 1);
      }
      Need(!database[identifier].active, "reused active addition label");
      database[identifier] = {true, std::move(learned)};
      ++additions;
      if (database[identifier].literals.empty()) {
        checked_empty = true;
      }
    }
    Need(checked_empty, "no checked empty clause");
    std::cout << "VERIFIED_INDEPENDENT_RUP_LRAT\n";
    std::cout << "{\"variables\":" << variables
              << ",\"original_clauses\":" << original_clauses
              << ",\"additions\":" << additions
              << ",\"deletions\":" << deletions
              << ",\"deletion_records\":" << deletion_records
              << ",\"hints_used\":" << hints_used << "}\n";
  } catch (const std::exception& error) {
    std::cerr << "REJECTED: " << error.what() << '\n';
    return 1;
  }
}
