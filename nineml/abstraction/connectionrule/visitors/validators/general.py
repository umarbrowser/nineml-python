"""
docstring needed

:copyright: Copyright 2010-2013 by the Python lib9ML team, see AUTHORS.
:license: BSD-3, see LICENSE for details.
"""
from ....componentclass.visitors.validators import (
    AliasesAreNotRecursiveComponentValidator,
    NoUnresolvedSymbolsComponentValidator,
    NoDuplicatedObjectsComponentValidator,
    CheckNoLHSAssignmentsToMathsNamespaceComponentValidator)
from ..base import BaseConnectionRuleVisitor


class AliasesAreNotRecursiveConnectionRuleValidator(
        AliasesAreNotRecursiveComponentValidator,
        BaseConnectionRuleVisitor):

    """Check that aliases are not self-referential"""

    pass


class NoUnresolvedSymbolsConnectionRuleValidator(
        NoUnresolvedSymbolsComponentValidator,
        BaseConnectionRuleVisitor):
    """
    Check that aliases and timederivatives are defined in terms of other
    parameters, aliases, statevariables and ports
    """
    pass


class NoDuplicatedObjectsConnectionRuleValidator(
        NoDuplicatedObjectsComponentValidator,
        BaseConnectionRuleVisitor):

    def action_connectionrule(self, connectionrule, **kwargs):  # @UnusedVariable @IgnorePep8
        self.all_objects.append(connectionrule)


class CheckNoLHSAssignmentsToMathsNamespaceConnectionRuleValidator(
        CheckNoLHSAssignmentsToMathsNamespaceComponentValidator,
        BaseConnectionRuleVisitor):

    """
    This class checks that there is not a mathematical symbols, (e.g. pi, e)
    on the left-hand-side of an equation
    """
    pass
