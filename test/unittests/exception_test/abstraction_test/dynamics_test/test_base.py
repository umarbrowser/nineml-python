from builtins import next
import unittest
from nineml.abstraction.dynamics.base import (Dynamics)
from nineml.utils.comprehensive_example import instances_of_all_types
from nineml.exceptions import (NineMLRuntimeError)


class TestDynamicsExceptions(unittest.TestCase):

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test__resolve_transition_regimes_ninemlruntimeerror(self):
        """
        line #: 476
        message: Can't find regime '{}' referenced from '{}' transition

        context:
        --------
    def _resolve_transition_regimes(self):
        # Check that the names of the regimes are unique:
        assert_no_duplicates([r.name for r in self.regimes])
        # We only worry about 'target' regimes, since source regimes are taken
        # care of for us by the Regime objects they are attached to.
        for regime in self.regimes:
            for trans in regime.transitions:
                trans.set_source_regime(regime)
                target = trans.target_regime_name
                if target is None:
                    target = regime  # to same regime
                else:
                    try:
                        target = self.regime(target)  # Lookup by name
                    except KeyError:
                        self.regime(target)
        """

        dynamics = next(iter(instances_of_all_types['Dynamics'].values()))
        self.assertRaises(
            NineMLRuntimeError,
            dynamics._resolve_transition_regimes)

