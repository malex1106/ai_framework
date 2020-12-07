"""
Author: Alexander Fichtinger
"""

from sympy import *


class LogicalOperator:
    def __init__(self):
        self.syntax = False

    @staticmethod
    def create_clause(*args) -> object:
        logic_node = LogicalOperator()

        for arg in args:
            arg = str(arg)
            pos = arg.find('~')
            if pos != -1:
                literal = Not(symbols(arg[pos + 1:]))
            else:
                literal = symbols(str(arg))
            logic_node.syntax = Or(logic_node.syntax, literal)

        return logic_node

    @staticmethod
    def create_implication(s_node: object, c_node: object) -> object:
        logic_node = LogicalOperator()
        logic_node.syntax = Implies(s_node.syntax, c_node.syntax)

        return logic_node

    @staticmethod
    def create_conjunction(clauses: list) -> object:
        logic_node = LogicalOperator()
        logic_node.syntax = True
        for element in clauses:
            logic_node.syntax = And(logic_node.syntax, element.syntax)

        return logic_node

    @staticmethod
    def resolution(clause_1: object, clause_2: object) -> object:
        if isinstance(clause_1.syntax, Implies):
            clause_1 = LogicalOperator.create_clause(f'~{clause_1.syntax.args[0]}', *clause_1.syntax.args[1].args)
        if isinstance(clause_2.syntax, Implies):
            clause_2 = LogicalOperator.create_clause(f'~{clause_2.syntax.args[0]}', *clause_2.syntax.args[1].args)

        logic_node = LogicalOperator.create_conjunction([clause_1, clause_2])
        logic_node.syntax = to_cnf(logic_node.syntax)

        help_list = []

        for clause in logic_node.syntax.args:
            if isinstance(clause, Or):
                for literal in clause.args:
                    help_list.append(literal)
            else:
                help_list.append(clause)

        for element in help_list:
            if Not(element) in help_list:
                help_list.remove(element)
                help_list.remove(Not(element))

                break

        out_node = LogicalOperator.create_clause(*[str(elem) for elem in help_list])

        return out_node
