import sympy
from itertools import izip, chain
import re
from .base import BaseDualVisitor
from nineml.exceptions import (NineMLDualVisitException,
                               NineMLDualVisitTypeException,
                               NineMLDualVisitKeysMismatchException,
                               NineMLDualVisitValueException,
                               NineMLNotBoundException,
                               NineMLDualVisitAnnotationsMismatchException,
                               NineMLDualVisitNoneChildException,
                               NineMLNameError)
from nineml.utils import nearly_equal


class EqualityChecker(BaseDualVisitor):

    def __init__(self, annotations_ns=[], **kwargs):  # @UnusedVariable
        super(EqualityChecker, self).__init__()
        self.annotations_ns = annotations_ns

    def check(self, obj1, obj2, **kwargs):
        try:
            self.visit(obj1, obj2, **kwargs)
        except NineMLDualVisitException:
            return False
        return True

    def action(self, obj1, obj2, nineml_cls, **kwargs):
        try:
            annotations_keys = set(chain(obj1.annotations.branch_keys,
                                         obj2.annotations.branch_keys))
            skip_annotations = False
        except AttributeError:
            skip_annotations = True
        if not skip_annotations:
            for key in annotations_keys:
                if key[1] in self.annotations_ns:
                    try:
                        annot1 = obj1.annotations.branch(key)
                    except NineMLNameError:
                        raise NineMLDualVisitAnnotationsMismatchException(
                            nineml_cls, obj1, obj2, key, self.contexts1,
                            self.contexts2)
                    try:
                        annot2 = obj2.annotations.branch(key)
                    except NineMLNameError:
                        raise NineMLDualVisitAnnotationsMismatchException(
                            nineml_cls, obj1, obj2, key, self.contexts1,
                            self.contexts2)
                    self.visit(annot1, annot2, **kwargs)
        return super(EqualityChecker, self).action(obj1, obj2, nineml_cls,
                                                   **kwargs)

    def default_action(self, obj1, obj2, nineml_cls, **kwargs):  # @UnusedVariable @IgnorePep8
        for attr_name in nineml_cls.nineml_attr:
            if attr_name == 'rhs':  # need to use Sympy equality checking
                self._check_rhs(obj1, obj2, nineml_cls)
            else:
                self._check_attr(obj1, obj2, attr_name, nineml_cls)

    def action_reference(self, ref1, ref2, nineml_cls, **kwargs):  # @UnusedVariable @IgnorePep8
        self._check_attr(ref1, ref2, 'url', nineml_cls)

    def action_definition(self, def1, def2, nineml_cls, **kwargs):  # @UnusedVariable @IgnorePep8
        self._check_attr(def1, def2, 'url', nineml_cls)

    def action_singlevalue(self, val1, val2, nineml_cls, **kwargs):  # @UnusedVariable @IgnorePep8
        if not nearly_equal(val1.value, val2.value):
            raise NineMLDualVisitValueException(
                'value', val1, val2, self.contexts1, self.contexts2)

    def action_arrayvalue(self, val1, val2, nineml_cls, **kwargs):  # @UnusedVariable @IgnorePep8
        if not all(nearly_equal(s, o)
                   for s, o in izip(val1.values, val1.values)):
            raise NineMLDualVisitValueException(
                'values', val1, val2, self.contexts1, self.contexts2)

    def action_unit(self, unit1, unit2, nineml_cls, **kwargs):  # @UnusedVariable @IgnorePep8
        # Ignore name
        self._check_attr(unit1, unit2, 'power', nineml_cls)
        self._check_attr(unit1, unit2, 'offset', nineml_cls)

    def action_dimension(self, dim1, dim2, nineml_cls, **kwargs):  # @UnusedVariable @IgnorePep8
        # Ignore name
        for sym in nineml_cls.dimension_symbols:
            self._check_attr(dim1, dim2, sym, nineml_cls)

    def action__annotationsbranch(self, branch1, branch2, nineml_cls, **kwargs):  # @UnusedVariable @IgnorePep8
        for attr in nineml_cls.nineml_attr:
            if attr != 'abs_index':
                self._check_attr(branch1, branch2, attr, nineml_cls)

    def _check_rhs(self, expr1, expr2, nineml_cls):
        try:
            expr_eq = (sympy.expand(expr1.rhs - expr2.rhs) == 0)
        except TypeError:
            expr_eq = sympy.Equivalent(expr1.rhs, expr2.rhs) == sympy.true
        if not expr_eq:
            raise NineMLDualVisitValueException(
                'rhs', expr1, expr2, nineml_cls, self.contexts1,
                self.contexts2)

    def _check_attr(self, obj1, obj2, attr_name, nineml_cls):
        try:
            if getattr(obj1, attr_name) != getattr(obj2, attr_name):
                raise NineMLDualVisitValueException(
                    attr_name, obj1, obj2, nineml_cls, self.contexts1,
                    self.contexts2)
        except NineMLNotBoundException:
            pass


class MismatchFinder(EqualityChecker):

    def find(self, obj1, obj2):
        self.mismatch = ''
        self.visit(obj1, obj2)
        assert not self.contexts1
        assert not self.contexts2
        return self.mismatch

    def visit(self, *args, **kwargs):
        try:
            super(MismatchFinder, self).visit(*args, **kwargs)
        except NineMLDualVisitTypeException as e:
            self.mismatch += (
                "{} - types: [{}] | [{}] (expected={})\n"
                .format(self._format_contexts(e.contexts1, e.contexts2),
                        type(e.obj1), type(e.obj2), e.nineml_cls))
        except NineMLDualVisitAnnotationsMismatchException as e:
            self.mismatch += (
                "{} - '{}' annotations: [{}] | [{}]\n"
                .format(self._format_contexts(e.contexts1, e.contexts2),
                        e.key, ', '.join(re.sub('\s', '', str(a))
                                         for a in e.obj1.annotations.namespace(
                                             e.key[1])),
                        ', '.join(re.sub('\s', '', str(a))
                                  for a in e.obj2.annotations.namespace(
                                      e.key[1]))))

    def _compare_child(self, obj1, obj2, nineml_cls, results, action_result,
                       child_name, child_type, **kwargs):
        try:
            super(MismatchFinder, self)._compare_child(
                obj1, obj2, nineml_cls, results, action_result, child_name,
                child_type, **kwargs)
        except NineMLDualVisitNoneChildException as e:
            self.mismatch += (
                "{} - '{}' child: [{}] | [{}]\n"
                .format(self._format_contexts(e.contexts1, e.contexts2),
                        e.child_name, e.obj1, e.obj2))
            self._pop_contexts()

    def _compare_children(self, obj1, obj2, nineml_cls, results, action_result,
                          children_type, **kwargs):
        try:
            super(MismatchFinder, self)._compare_children(
                obj1, obj2, nineml_cls, results, action_result, children_type,
                **kwargs)
        except NineMLDualVisitKeysMismatchException as e:
            self.mismatch += (
                "{} - {} keys: {} | {}\n"
                .format(self._format_contexts(e.contexts1, e.contexts2),
                        e.children_type.nineml_type,
                        sorted(e.obj1._member_keys_iter(e.children_type)),
                        sorted(e.obj2._member_keys_iter(e.children_type))))
            self._pop_contexts()

    def _check_attr(self, obj1, obj2, attr_name, nineml_cls, **kwargs):
        try:
            super(MismatchFinder, self)._check_attr(
                obj1, obj2, attr_name, nineml_cls, **kwargs)
        except NineMLDualVisitValueException as e:
            self.mismatch += (
                "{} - '{}' attr: [{}] | [{}]\n"
                .format(self._format_contexts(e.contexts1, e.contexts2,
                                              obj1=e.obj1, obj2=e.obj2),
                        e.attr_name,
                        getattr(e.obj1, e.attr_name),
                        getattr(e.obj2, e.attr_name)))

    def _check_rhs(self, obj1, obj2, attr_name, **kwargs):
        try:
            super(MismatchFinder, self)._check_rhs(
                obj1, obj2, attr_name, **kwargs)
        except NineMLDualVisitValueException as e:
            self.mismatch += (
                "{} - '{}' attr: [{}] | [{}]\n"
                .format(self._format_contexts(e.contexts1, e.contexts2,
                                              obj1=e.obj1, obj2=e.obj2),
                        e.attr_name,
                        getattr(e.obj1, e.attr_name),
                        getattr(e.obj2, e.attr_name)))

    def _pop_contexts(self):
        self.contexts1.pop()
        self.contexts2.pop()

    @classmethod
    def _format_contexts(self, contexts1, contexts2, obj1=None, obj2=None):
        l1 = [(type(c.parent).__name__, c.parent.key) for c in contexts1]
        l2 = [(type(c.parent).__name__, c.parent.key) for c in contexts2]
        if obj1 is not None:
            l1.append((type(obj1).__name__, obj1.key))
        if obj2 is not None:
            l2.append((type(obj2).__name__, obj2.key))
        out = '[' + '>'.join("{}('{}')".format(t, k) for t, k in l1) + ']'
        if l2 != l1:
            out += (' | [' + '>'.join("{}('{}')".format(t, k) for t, k in l2) +
                    ']')
        return out
