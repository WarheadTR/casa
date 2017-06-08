About
===============

After running split on one MS there is some metadata still present in the sub-tables but none of the rows from
the main file point to this metadata.

Script removes unnecessary rows in sub tables (such as DATA_DESC_ID, FIELD, etc.) and re-index IDs in main table.

Script is absolutely free and distributed with GPLv3 license.

You can use it without restrictive licenses.

Developer: Recep BALBAY <rbalbay@gmail.com>


rb_indexer
===============

Before installation you have to define your CASAPATH into PATH. Otherwise script gives PATH error!

1) $ export CASAPATH=/where/is/your/casa/
2) $ export PATH=/where/is/your/casa/bin:$PATH


For all GNU/Linux distributions, script requires the following package:

numpy >= 1.8.2


Installation
===============
$ tar -xzvf rbalbay.tar.gz

$ cd rbalbay

$ python setup.py


Usage in CASA
===============

You can use this rbindex after mstransform, split or split2 operations.

Also rbmap function converts old input strings ('0-10:200' to '0-9:200') in spw and field.
Then you can use new string values in tools like clean, tclean or etc.

[0] from rbindexer import rbindex, rbmap

[1] rbindex(vis='splitted_new.ms')
# it removes unneccessary rows in related subtables and re-index.

# think script removed 7th row and reindexed #

[2] rbmap('0~10', 'field')
# it will create new string '0~9' for field.

[3] rbmap('10~100', 'spw')
# it will create new string '9~99' for spectral_window.

[4] rbmap('0~5', 'field')
# it will create new string '0~5' for field.

[5] rbmap('7', 'spw')
# it will create new string '6' for spectral_window.
