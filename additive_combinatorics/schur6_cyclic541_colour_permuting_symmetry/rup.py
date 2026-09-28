"""Independent reverse-unit-propagation checker. No solver package is imported.

Deletion lines are ignored: all retained additions are logical consequences of
the original formula. The certificate must actually derive the empty clause.
"""


class RUP:
    def __init__(self, variables, clauses):
        if type(variables) is not int or variables < 1:
            raise ValueError("invalid variable count")
        self.variables = variables
        self.clauses, self.units = [], []
        self.watches = {i: [] for i in range(-variables, variables + 1) if i}
        self.empty = False
        for clause in clauses:
            self.add(clause)

    def validate(self, clause):
        if any(type(x) is not int or not 1 <= abs(x) <= self.variables for x in clause):
            raise ValueError("literal outside domain")

    def add(self, clause):
        self.validate(clause)
        clause = list(dict.fromkeys(clause))
        if not clause:
            self.empty = True
        elif len(clause) == 1:
            self.units.append(clause[0])
        else:
            i = len(self.clauses)
            self.clauses.append(clause)
            self.watches[clause[0]].append(i)
            self.watches[clause[1]].append(i)

    def implied(self, clause):
        self.validate(clause)
        if self.empty:
            return True
        values, trail = [0] * (self.variables + 1), []

        def assign(literal):
            variable = abs(literal)
            wanted = 1 if literal > 0 else -1
            if values[variable]:
                return values[variable] == wanted
            values[variable] = wanted
            trail.append(literal)
            return True

        def value(literal):
            return values[abs(literal)] * (1 if literal > 0 else -1)

        for literal in self.units + [-x for x in clause]:
            if not assign(literal):
                return True
        position = 0
        while position < len(trail):
            false_literal = -trail[position]
            position += 1
            watched, i = self.watches[false_literal], 0
            while i < len(watched):
                clause_id = watched[i]
                current = self.clauses[clause_id]
                if current[0] == false_literal:
                    current[0], current[1] = current[1], current[0]
                if current[1] != false_literal:
                    raise RuntimeError("corrupt watched-literal list")
                other = current[0]
                if value(other) == 1:
                    i += 1
                    continue
                for j in range(2, len(current)):
                    if value(current[j]) != -1:
                        current[1], current[j] = current[j], current[1]
                        self.watches[current[1]].append(clause_id)
                        watched[i] = watched[-1]
                        watched.pop()
                        break
                else:
                    if value(other) == -1 or not assign(other):
                        return True
                    i += 1
        return False

    def check(self, lines):
        additions = deletions = 0
        for line_number, line in enumerate(lines, 1):
            tokens = line.split()
            if not tokens:
                continue
            deletion = tokens[0] == "d"
            if deletion:
                tokens = tokens[1:]
            literals = list(map(int, tokens))
            if not literals or literals[-1] != 0 or 0 in literals[:-1]:
                raise ValueError(f"malformed certificate line {line_number}")
            clause = literals[:-1]
            self.validate(clause)
            if deletion:
                deletions += 1
                continue
            if not self.implied(clause):
                raise ValueError(f"non-RUP addition at line {line_number}")
            additions += 1
            if not clause:
                return {"additions": additions, "deletions_ignored": deletions,
                        "final_line": line_number}
            self.add(clause)
        raise ValueError("no derived empty clause")
