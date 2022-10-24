from __future__ import annotations
from typing import List, Tuple
from typing import Union


class ConjunctiveNormalForm:

    class Variable:
        def __init__(self, truth_value=None):
            self._truth_value: Union[bool, None] = None
            self.set_truth_value(truth_value)

        def set_truth_value(self, truth_value: Union[bool, int, None]):
            if type(truth_value) == bool:
                self._truth_value = truth_value
            elif isinstance(truth_value, int):
                if truth_value == 0:
                    self._truth_value = False
                elif truth_value == 1:
                    self._truth_value = True
                else:
                    raise ValueError("truth_value is integer but is not 0 nor 1.")
            else:
                self._truth_value = truth_value

        def get_truth_value(self):
            return self._truth_value

    class Literal:
        def __eq__(self, other):
            try:
                return (self.variable is other.variable) and (self.get_positivity() == other.get_positivity())
            except Exception as e:
                print("Error: something went wrong while trying to compare a literal object with ==")
                raise e

        def __init__(self, variable: Union[ConjunctiveNormalForm.Variable, None],
                     is_positive_literal: Union[bool, int] = True):
            self.variable: Union[ConjunctiveNormalForm.Variable, None] = None
            if isinstance(variable, ConjunctiveNormalForm.Variable):
                self.variable = variable
            else:
                raise ValueError("variable is not an instance of class ConjunctiveNormalForm.Variable, but %s" %
                                 type(variable))
            self._is_positive_literal: Union[bool, int] = True
            self.set_positivity(is_positive_literal=is_positive_literal)

        def set_truth_value(self, truth_value: Union[bool, int, None]):
            truth_value_to_set: Union[bool, int, None] = None
            if type(truth_value) == bool:
                if self.get_positivity():
                    truth_value_to_set = truth_value
                else:
                    truth_value_to_set = not truth_value
            elif type(truth_value) == int:
                if truth_value == 0:
                    if self.get_positivity():
                        truth_value_to_set = False
                    else:
                        truth_value_to_set = True
                elif truth_value == 1:
                    if self.get_positivity():
                        truth_value_to_set = True
                    else:
                        truth_value_to_set = False
                else:
                    raise ValueError("truth_value is integer but is not 0 nor 1.")
            else:
                truth_value_to_set = truth_value
            self.variable.set_truth_value(truth_value_to_set)

        def set_positivity(self, is_positive_literal=True):
            if type(is_positive_literal) == bool:
                self._is_positive_literal = is_positive_literal
            elif isinstance(is_positive_literal, int) and (is_positive_literal == 0 or is_positive_literal == 1):
                if is_positive_literal == 0:
                    self._is_positive_literal = False
                else:
                    self._is_positive_literal = True
            else:
                if isinstance(is_positive_literal, int):
                    raise ValueError("is_positive_literal is integer but is not 0 nor 1.")
                else:
                    raise ValueError("is_positive_literal is not boolean nor integer")

        def get_positivity(self):
            return self._is_positive_literal

        def get_truth_value(self):
            if type(self.variable.get_truth_value()) == bool:
                if self._is_positive_literal:
                    return self.variable.get_truth_value()
                else:
                    return not self.variable.get_truth_value()
            else:
                return self.variable.get_truth_value()

    class Clause:
        def __init__(self, list_of_literal: List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]] = None):
            if list_of_literal is None:
                list_of_literal = []
            self.list_of_literal_or_variable: List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]] = list_of_literal

        def get_truth_value(self):
            # empty clause is false
            if len(self.list_of_literal_or_variable) == 0:
                return False
            else:
                contain_variable_or_literal_without_truth_value = False
                # if at least one literal is true, then clause is true
                for literal_or_variable in self.list_of_literal_or_variable:
                    if isinstance(literal_or_variable, (ConjunctiveNormalForm.Literal, ConjunctiveNormalForm.Variable)):
                        if literal_or_variable.get_truth_value() is None:
                            contain_variable_or_literal_without_truth_value = True
                        elif literal_or_variable.get_truth_value():
                            return True
                    else:
                        contain_variable_or_literal_without_truth_value = True
                # if no literal that is true, and no literal without truth value, then false
                if not contain_variable_or_literal_without_truth_value:
                    return False
                # if no literal that is true, but exist literal without truth value, then truth value unknown
                else:
                    return None

    # init method or constructor
    def __init__(self, list_of_clause: List[ConjunctiveNormalForm.Clause] = None):
        if list_of_clause is None:
            list_of_clause = []
        self.list_of_clause: List[ConjunctiveNormalForm.Clause] = list_of_clause

    # return true if able to split, return false otherwise
    def split_clause_to_at_most_n_literal(self, n):
        n = int(n)
        if n < 3:
            for clause in self.list_of_clause:
                if len(clause.list_of_literal_or_variable) > n:
                    # if n is less than 3, and the amount of literal in a clause is bigger than n, then
                    # not able to split
                    return False
            # all clause have at most n literal
            return True
        else:
            original_len_list_of_clause = len(self.list_of_clause)
            for i in range(original_len_list_of_clause):
                clause = self.list_of_clause[i]
                if len(clause.list_of_literal_or_variable) > n:
                    right = clause
                    split_variable = ConjunctiveNormalForm.Variable()
                    left_split_literal = ConjunctiveNormalForm.Literal(split_variable, is_positive_literal=True)
                    right_split_literal = ConjunctiveNormalForm.Literal(split_variable, is_positive_literal=False)
                    left = ConjunctiveNormalForm.Clause()
                    # n-1 instead of n because we want to append split literal
                    left.list_of_literal_or_variable.extend(right.list_of_literal_or_variable[0:n - 1])
                    left.list_of_literal_or_variable.append(left_split_literal)
                    next_right = ConjunctiveNormalForm.Clause()
                    next_right.list_of_literal_or_variable.extend(right.list_of_literal_or_variable[n - 1:
                                                                            len(right.list_of_literal_or_variable)])
                    next_right.list_of_literal_or_variable.append(right_split_literal)
                    right = next_right
                    self.list_of_clause[i] = left
                    while True:
                        # the amount of literal is bigger than n
                        if len(right.list_of_literal_or_variable) > n:
                            split_variable = ConjunctiveNormalForm.Variable()
                            left_split_literal = ConjunctiveNormalForm.Literal(split_variable, is_positive_literal=True)
                            right_split_literal = ConjunctiveNormalForm.Literal(split_variable, is_positive_literal=False)
                            left = ConjunctiveNormalForm.Clause()
                            # n-1 instead of n because we want to append split literal
                            left.list_of_literal_or_variable.extend(right.list_of_literal_or_variable[0:n - 1])
                            left.list_of_literal_or_variable.append(left_split_literal)
                            next_right = ConjunctiveNormalForm.Clause()
                            next_right.list_of_literal_or_variable.extend(right.list_of_literal_or_variable[n - 1:])
                            next_right.list_of_literal_or_variable.append(right_split_literal)
                            right = next_right
                            self.list_of_clause.append(left)
                        # the amount of literal is less than or equal to n
                        else:
                            self.list_of_clause.append(right)
                            break
            return True

    # return None is not solved, return truth value if solved
    def is_already_solved(self):
        # empty formula is true
        if len(self.list_of_clause) == 0:
            return True
        else:
            contain_clause_without_truth_value = False
            # if at least one clause is false, then false
            for clause in self.list_of_clause:
                if isinstance(clause, ConjunctiveNormalForm.Literal):
                    if clause.get_truth_value() is None:
                        contain_clause_without_truth_value = True
                    elif not clause.get_truth_value():
                        return False
                else:
                    contain_clause_without_truth_value = True
            # if no clause that is false, and no clause without truth value, then true
            if not contain_clause_without_truth_value:
                return True
            # if no clause that is false, but exist clause without truth value, then truth value unknown
            else:
                return None

    # return: clause_count, literal_count
    def count_clause_and_literal(self) -> Tuple[int, int]:
        clause_count = len(self.list_of_clause)
        literal_count = 0
        for clause in self.list_of_clause:
            literal_count += len(clause.list_of_literal_or_variable)
        return clause_count, literal_count

    def solve_as_one_satisfiability(self, set_truth_value_inplace=False) -> \
            Tuple[bool, List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]], List[Union[bool, None]]]:
        list_of_unassigned_variable: List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]] = []
        previously_set_truth_value = True
        contain_unsatisfiable_clause = False
        contain_clause_without_answer = True
        while previously_set_truth_value and not contain_unsatisfiable_clause and contain_clause_without_answer:
            contain_clause_without_answer = False
            previously_set_truth_value = False
            for clause in self.list_of_clause:
                contain_one_true_literal_or_variable = False
                contain_exactly_one_unassigned_literal_or_variable: \
                    Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal, None] = None
                contain_at_least_two_unassigned_literal_or_variable = False
                for literal_or_variable in clause.list_of_literal_or_variable:
                    if isinstance(literal_or_variable, (ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal)):
                        if type(literal_or_variable.get_truth_value()) == bool and \
                                literal_or_variable.get_truth_value():
                            contain_one_true_literal_or_variable = True
                            break
                        elif not type(literal_or_variable.get_truth_value()) == bool:
                            if not contain_at_least_two_unassigned_literal_or_variable and \
                                    contain_exactly_one_unassigned_literal_or_variable is None:
                                contain_exactly_one_unassigned_literal_or_variable = literal_or_variable
                            elif contain_exactly_one_unassigned_literal_or_variable is not None:
                                contain_exactly_one_unassigned_literal_or_variable = None
                                contain_at_least_two_unassigned_literal_or_variable = True
                    else:
                        raise TypeError("Error: literal_or_variable is not variable nor literal. Got ",
                                        type(literal_or_variable))
                if not contain_one_true_literal_or_variable:
                    if contain_exactly_one_unassigned_literal_or_variable is not None:
                        contain_exactly_one_unassigned_literal_or_variable.set_truth_value(True)
                        contain_one_true_literal_or_variable = True
                        if not set_truth_value_inplace:
                            list_of_unassigned_variable.append(contain_exactly_one_unassigned_literal_or_variable)
                        previously_set_truth_value = True
                    if contain_at_least_two_unassigned_literal_or_variable:
                        contain_clause_without_answer = True
                if not contain_one_true_literal_or_variable and contain_exactly_one_unassigned_literal_or_variable is None \
                        and not contain_at_least_two_unassigned_literal_or_variable:
                    contain_unsatisfiable_clause = True
                    break
        if contain_unsatisfiable_clause or contain_clause_without_answer:
            if not set_truth_value_inplace:
                while len(list_of_unassigned_variable) > 0:
                    list_of_unassigned_variable.pop().set_truth_value(None)
            return False, [], []
        else:
            if set_truth_value_inplace:
                return True, [], []
            else:
                for clause in self.list_of_clause:
                    for literal_or_variable in clause.list_of_literal_or_variable:
                        if isinstance(literal_or_variable, (ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal)):
                            if not type(literal_or_variable.get_truth_value()) == bool:
                                list_of_unassigned_variable.append(literal_or_variable)
                        else:
                            raise TypeError("Error: literal_or_variable is not variable nor literal. Got ",
                                            type(literal_or_variable))
                unassigned_variable_truth_value: List[Union[bool, None]] = []
                for literal_or_variable in list_of_unassigned_variable:
                    if type(literal_or_variable.get_truth_value()) == bool:
                        unassigned_variable_truth_value.append(literal_or_variable.get_truth_value())
                    else:
                        unassigned_variable_truth_value.append(None)
                return True, list_of_unassigned_variable, unassigned_variable_truth_value

    @staticmethod
    def not_gate(input_one: Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]) -> \
            Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]:
        if type(input_one) == ConjunctiveNormalForm.Variable:
            return ConjunctiveNormalForm.Literal(input_one, is_positive_literal=False)
        elif type(input_one) == ConjunctiveNormalForm.Literal and input_one.get_positivity():
            return ConjunctiveNormalForm.Literal(input_one.variable, is_positive_literal=False)
        elif type(input_one) == ConjunctiveNormalForm.Literal and not input_one.get_positivity():
            return input_one.variable
        else:
            raise TypeError("Error: only type ConjunctiveNormalForm.Variable or ConjunctiveNormalForm.Literal is allowed for"
                            "input_one, got ", type(input_one))

    @staticmethod
    def not_bitwise(input_one: List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]]) -> \
            List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]]:
        result_variable: List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]] = []

        # shallow copy
        for i in range(len(input_one)):
            result_variable.append(input_one[i])

        for i in range(len(input_one)):
            result_variable[i] = ConjunctiveNormalForm.not_gate(result_variable[i])
        return result_variable

    @staticmethod
    def or_gate_two_input(input_one: Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal],
                          input_two: Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]) -> \
            Tuple[ConjunctiveNormalForm.Variable, List[ConjunctiveNormalForm.Clause]]:
        result_variable: ConjunctiveNormalForm.Variable = ConjunctiveNormalForm.Variable()
        result_clause: List[ConjunctiveNormalForm.Clause] = []
        # A -> B OR C = NOT A OR B OR C
        # NOT A -> NOT B AND NOT C = A OR (NOT B AND NOT C) = (A OR NOT B) AND (A OR NOT C)

        # A -> B OR C = NOT A OR B OR C
        # NOT A OR B OR C
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            ConjunctiveNormalForm.not_gate(result_variable), input_one, input_two
        ]))

        # NOT A -> NOT B AND NOT C = A OR (NOT B AND NOT C) = (A OR NOT B) AND (A OR NOT C)
        # (A OR NOT B)
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            result_variable, ConjunctiveNormalForm.not_gate(input_one)
        ]))

        # (A OR NOT C)
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            result_variable, ConjunctiveNormalForm.not_gate(input_two)
        ]))

        return result_variable, result_clause

    @staticmethod
    def or_bitwise_two_input_same_size(input_one: List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]],
                                       input_two: List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]]) -> \
            Tuple[List[ConjunctiveNormalForm.Variable], List[ConjunctiveNormalForm.Clause]]:
        if len(input_one) != len(input_two):
            raise ValueError("Error: len(input_one) != len(input_two)")
        size = len(input_one)
        result_variable: List[ConjunctiveNormalForm.Variable] = []
        result_clause: List[ConjunctiveNormalForm.Clause] = []
        for i in range(size):
            or_gate_result = ConjunctiveNormalForm.or_gate_two_input(input_one[i], input_two[i])
            result_variable.append(or_gate_result[0])
            result_clause.extend(or_gate_result[1])
        return result_variable, result_clause

    @staticmethod
    def and_gate_two_input(input_one: Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal],
                           input_two: Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]) -> \
            Tuple[ConjunctiveNormalForm.Variable, List[ConjunctiveNormalForm.Clause]]:
        result_variable: ConjunctiveNormalForm.Variable = ConjunctiveNormalForm.Variable()
        result_clause: List[ConjunctiveNormalForm.Clause] = []
        # A -> B AND C = NOT A OR (B AND C) = (NOT A OR B) AND (NOT A OR C)
        # NOT A -> NOT B OR NOT C = A OR NOT B OR NOT C

        # (NOT A OR B)
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            ConjunctiveNormalForm.not_gate(result_variable), input_one
        ]))

        # (NOT A OR B)
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            ConjunctiveNormalForm.not_gate(result_variable), input_two
        ]))

        # A OR NOT B OR NOT C
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            result_variable, ConjunctiveNormalForm.not_gate(input_one), ConjunctiveNormalForm.not_gate(input_two)
        ]))

        return result_variable, result_clause

    @staticmethod
    def and_bitwise_two_input_same_size(input_one: List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]],
                                        input_two: List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]]) -> \
            Tuple[List[ConjunctiveNormalForm.Variable], List[ConjunctiveNormalForm.Clause]]:
        if len(input_one) != len(input_two):
            raise ValueError("Error: len(input_one) != len(input_two)")
        size = len(input_one)
        result_variable: List[ConjunctiveNormalForm.Variable] = []
        result_clause: List[ConjunctiveNormalForm.Clause] = []
        for i in range(size):
            and_gate_result = ConjunctiveNormalForm.and_gate_two_input(input_one[i], input_two[i])
            result_variable.append(and_gate_result[0])
            result_clause.extend(and_gate_result[1])
        return result_variable, result_clause

    @staticmethod
    def right_shift(num: List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]],
                    shift: int) -> List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]]:
        # num[:(len(num)-shift)].zfill(size)
        result_variable = []
        for i in range(shift):
            result_variable.append(ConjunctiveNormalForm.Variable())
            result_variable[i].set_truth_value(False)
        for i in range(len(num)-shift):
            result_variable.append(num[i])
        return result_variable

    @staticmethod
    def xor_gate_two_input(input_one: Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal],
                           input_two: Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]) -> \
            Tuple[ConjunctiveNormalForm.Variable, List[ConjunctiveNormalForm.Clause]]:
        result_variable: ConjunctiveNormalForm.Variable = ConjunctiveNormalForm.Variable()
        result_clause: List[ConjunctiveNormalForm.Clause] = []
        # A -> (B OR C) AND (NOT B OR NOT C) = NOT A OR ((B OR C) AND (NOT B OR NOT C))
        # = (NOT A OR B OR C) AND (NOT A OR NOT B OR NOT C)
        # NOT A -> (B OR NOT C) AND (NOT B OR C) = A OR ((B OR NOT C) AND (NOT B OR C))
        # = (A OR B OR NOT C) AND (A OR NOT B OR C)

        # A -> (B OR C) AND (NOT B OR NOT C) = NOT A OR ((B OR C) AND (NOT B OR NOT C))
        # = (NOT A OR B OR C) AND (NOT A OR NOT B OR NOT C)
        # NOT A OR B OR C
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            ConjunctiveNormalForm.not_gate(result_variable), input_one, input_two
        ]))

        # NOT A OR NOT B OR NOT C
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            ConjunctiveNormalForm.not_gate(result_variable), ConjunctiveNormalForm.not_gate(input_one),
            ConjunctiveNormalForm.not_gate(input_two)
        ]))

        # NOT A -> (B OR NOT C) AND (NOT B OR C) = A OR ((B OR NOT C) AND (NOT B OR C))
        # = (A OR B OR NOT C) AND (A OR NOT B OR C)
        # A OR B OR NOT C
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            result_variable, input_one, ConjunctiveNormalForm.not_gate(input_two)
        ]))

        # A OR NOT B OR C
        result_clause.append(ConjunctiveNormalForm.Clause(list_of_literal=[
            result_variable, ConjunctiveNormalForm.not_gate(input_one), input_two
        ]))
        return result_variable, result_clause

    @staticmethod
    def xor_bitwise_two_input_same_size(input_one: List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]],
                                        input_two: List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]]) -> \
            Tuple[List[ConjunctiveNormalForm.Variable], List[ConjunctiveNormalForm.Clause]]:
        if len(input_one) != len(input_two):
            raise ValueError("Error: len(input_one) != len(input_two)")
        size = len(input_one)
        result_variable: List[ConjunctiveNormalForm.Variable] = []
        result_clause: List[ConjunctiveNormalForm.Clause] = []
        for i in range(size):
            xor_gate_result = ConjunctiveNormalForm.xor_gate_two_input(input_one[i], input_two[i])
            result_variable.append(xor_gate_result[0])
            result_clause.extend(xor_gate_result[1])
        return result_variable, result_clause

    @staticmethod
    def xor_bitwise_multiple_input_same_size(num: List[List[Union[ConjunctiveNormalForm.Variable, ConjunctiveNormalForm.Literal]]])\
            -> Tuple[List[ConjunctiveNormalForm.Variable], List[ConjunctiveNormalForm.Clause]]:
        result_variable: List[ConjunctiveNormalForm.Variable] = []
        result_clause: List[ConjunctiveNormalForm.Clause] = []
        if len(num) == 0:
            return result_variable, result_clause
        else:
            size = len(num[0])
            result_variable = num[0]
            for i in range(1, len(num)):
                xor_bitwise_result = ConjunctiveNormalForm.xor_bitwise_two_input_same_size(result_variable, num[i])
                result_clause.extend(xor_bitwise_result[1])
                result_variable = xor_bitwise_result[0]
            return result_variable, result_clause


