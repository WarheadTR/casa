import os
from tasks import mstransform
import testhelper as th
from rbindexer import rbindex
from tests.test_mstransform import test_base


class test_rbindex(test_base):
    """tests for spw with different correlation shapes"""

    def setUp(self):
        self.setUp_3c84()

    def tearDown(self):
        os.system('rm -rf ' + self.vis)
        os.system('rm -rf ' + self.outputms)
        os.system('rm -rf list.obs')

    def test_rbindex_corr_selection(self):
        """ mstransform: verify correct re-indexing of sub-tables """
        self.outputms = 'test_rbindex_corr_selection.ms'

        # It will select spws 1,2,3, polids=1,2,3 but each with 1 NUM_CORR only
        mstransform(vis=self.vis, outputvis=self.outputms, datacolumn='data', correlation='RR,LL')

        # Check before running the rbscript that
        # - SPW col in DDI subtable does not have any element pointing to SPW 0
        # - SPW subtable has 3 rows
        # - Polarization subtable has 4 rows

        spw_col = th.getVarCol(self.outputms+'/DATA_DESCRIPTION', 'SPECTRAL_WINDOW_ID')
        spw_val = spw_col['r1'].tolist()
        self.assertEqual(min(spw_val), 1, 'Mismatch')

        # reindexing
        rbindex(vis=self.outputms)

        # Check after running the rbscript that
        # - SPW col in DDI subtable does not have any element pointing to SPW 2 (because reindexing)
        # - SPW subtable only has 2 rows
        # - Polarization subtable has 2 rows

        spw_col = th.getVarCol(self.outputms+'/DATA_DESCRIPTION', 'SPECTRAL_WINDOW_ID')
        spw_val = spw_col['r1'].tolist()
        self.assertEqual(min(spw_val), 0, "Script doesn't works!")


def suite():
    return [test_rbindex]
