# !/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import os
from taskinit import tbtool, casalog


class rbkit(object):
    def __init__(self, vis):
        self.vis = vis
        self.vis_ddi = vis + '/DATA_DESCRIPTION'
        self.vis_feed = vis + '/FEED'
        self.vis_field = vis + '/FIELD'
        self.vis_spec_win = vis + '/SPECTRAL_WINDOW'
        self.vis_source = vis + '/SOURCE'
        self.vis_syscal = vis + '/SYSCAL'
        self.vis_caldev = vis + '/CALDEVICE'
        self.vis_pol = vis + '/POLARIZATION'
        self.vis_list = [self.vis_ddi, self.vis_feed, self.vis_field, self.vis_pol, self.vis_spec_win,
                         self.vis_source, self.vis_caldev, self.vis_syscal]
        self.tb = tbtool()
        self.cslog = casalog
        self.vis_uniqs = self.rb_get_uniqs()
        self.vis_rows_number = self.rb_get_rows()
        self.vis_progress = self.rb_subtable_decide()
        self.map_field = []
        self.map_spw = []
        self.rb_begin()

    def rb_get_uniqs(self):
        uniq_list = []
        self.tb.open(self.vis)
        uniq_list.append(np.unique(self.tb.getcol('DATA_DESC_ID')).tolist())
        uniq_list.append(np.unique(self.tb.getcol('FIELD_ID')).tolist())
        self.tb.close()
        self.tb.open(self.vis_field)
        uniq_list.append(np.unique(self.tb.getcol('SOURCE_ID')).tolist())
        self.tb.close()
        self.tb.open(self.vis_ddi)
        uniq_list.append(np.unique(self.tb.getcol('POLARIZATION_ID')).tolist())
        uniq_list.append(np.unique(self.tb.getcol('SPECTRAL_WINDOW_ID')).tolist())
        self.tb.close()
        return uniq_list

    def rb_save(self, map_name, calculated_map):
        if map_name == 'field':
            if os.path.exists('map_field'):
                pass
            else:
                f = open('map_field', 'w+')
                f.write(str(calculated_map))
                f.close()
        elif map_name == 'spw':
            if os.path.exists('map_spw'):
                pass
            else:
                f = open('map_spw', 'w+')
                f.write(str(calculated_map))
                f.close()
        else:
            print 'Wrong map_name!'

    def rb_mapper(self, old_map, deleted_rows):
        rb_map = list(old_map)
        if len(deleted_rows) > 0:
            for i in range(len(deleted_rows)):
                rb_map.remove(deleted_rows[i])
        else:
            pass
        fark = len(old_map)-len(rb_map)
        for i in range(fark):
            rb_map.append('None')
        rb_new_map = dict(zip(rb_map, old_map))
        if 'None' in rb_new_map:
            del rb_new_map['None']
        return rb_new_map

    def rb_get_rows(self):
        subtable_row_numbers = []
        for subtable in self.vis_list:
            self.tb.open(subtable)
            rows = self.tb.rownumbers()
            subtable_row_numbers.append(rows.tolist())
            self.tb.close()
        return subtable_row_numbers

    def rb_subtable_decide(self):
        subtable = []
        for i in self.vis_rows_number:
            if len(i) > 0:
                subtable.append(True)
            else:
                subtable.append(False)
        rb_dict = dict(zip(self.vis_list, subtable))
        return rb_dict

    def rb_indexer(self, vis, field, uniq):
        rb_list = []
        rb_vals = [i for i in range(0, len(uniq))]
        rb_dict = dict(zip(uniq, rb_vals))
        self.cslog.post("Reindexing " + field + " in: " + vis, origin="rbindex")
        self.tb.open(vis, nomodify=False)
        rb_columns = self.tb.getcol(field)
        for i in range(0, len(rb_columns)):
            rb_list.append(rb_dict[rb_columns[i]])
        rb_list = np.asarray(rb_list, dtype=np.int32)
        if len(rb_list) > 0:
            self.tb.putcol(field, rb_list)
            self.tb.flush()
            self.tb.close()
            self.cslog.post("Reindexed: " + vis, origin="rbindex")
        else:
            self.tb.close()
            self.cslog.post("Everything is ok in: " + vis, origin="rbindex")

    def rb_unused_list(self, array, uniq):
        unused_list = []
        for i in range(0, len(array)):
            if array[i] not in uniq:
                unused_list.append(i)
        return unused_list

    def rb_rm_field(self, vis, field, uniq):
        self.cslog.post("Removing unused rows in: " + field, origin="rbindex")
        self.tb.open(vis, nomodify=False)
        id_cols = self.tb.getcol(field)
        unused_rows = self.rb_unused_list(id_cols, uniq)
        if len(unused_rows) > 0:
            self.tb.removerows(unused_rows)
            self.tb.flush()
            self.tb.close()
            self.cslog.post("Unused row(s) removed in: " + vis, origin="rbindex")
        else:
            self.tb.close()
            self.cslog.post("Everything is ok in: " + vis, origin="rbindex")

    def rb_rm_rows(self, vis, uniq):
        self.cslog.post("Removing unused rows in: " + vis, origin="rbindex")
        self.tb.open(vis, nomodify=False)
        row_numbers = self.tb.rownumbers()
        rows = self.rb_unused_list(row_numbers, uniq)
        if len(rows) > 0:
            self.tb.removerows(rows)
            self.tb.flush()
            self.tb.close()
            self.cslog.post("Unused row(s) removed in: " + vis, origin="rbindex")
        else:
            self.tb.close()
            self.cslog.post("Everything is ok in: " + vis, origin="rbindex")

    def rb_begin(self):
        self.cslog.post("", origin="rbindex")
        self.cslog.post("##########################################", origin="rbindex")
        self.cslog.post("##### Begin Task: rbindex #####", origin="rbindex")
        self.cslog.post("Data Description IDs " + str(self.vis_uniqs[0]), priority="WARN", origin="rbindex")
        self.cslog.post("Field IDs " + str(self.vis_uniqs[1]), priority="WARN", origin="rbindex")
        self.cslog.post("rbindex(vis=" + self.vis + ")", origin="rbindex")

        self.rb_indexer(self.vis, 'DATA_DESC_ID', self.vis_uniqs[0])
        self.rb_indexer(self.vis, 'FIELD_ID', self.vis_uniqs[1])

        if self.vis_progress[self.vis_ddi]:
            self.rb_rm_rows(self.vis_ddi, self.vis_uniqs[0])
            self.rb_indexer(self.vis_ddi, 'POLARIZATION_ID', self.vis_uniqs[3])
            self.rb_indexer(self.vis_ddi, 'SPECTRAL_WINDOW_ID', self.vis_uniqs[4])

        if self.vis_progress[self.vis_feed]:
            self.rb_rm_field(self.vis_feed, 'SPECTRAL_WINDOW_ID', self.vis_uniqs[4])
            self.rb_indexer(self.vis_feed, 'SPECTRAL_WINDOW_ID', self.vis_uniqs[4])

        if self.vis_progress[self.vis_field]:
            self.rb_rm_rows(self.vis_field, self.vis_uniqs[1])
            self.rb_indexer(self.vis_field, 'SOURCE_ID', self.vis_uniqs[1])

        if self.vis_progress[self.vis_pol]:
            self.rb_rm_rows(self.vis_pol, self.vis_uniqs[3])

        if self.vis_progress[self.vis_spec_win]:
            self.rb_rm_rows(self.vis_spec_win, self.vis_uniqs[4])

        if self.vis_progress[self.vis_source]:
            self.rb_rm_rows(self.vis_source, self.vis_uniqs[1])
            self.rb_indexer(self.vis_source, 'SOURCE_ID', self.vis_uniqs[1])
            self.rb_rm_rows(self.vis_source, self.vis_uniqs[4])
            self.rb_indexer(self.vis_source, 'SPECTRAL_WINDOW_ID', self.vis_uniqs[4])

        if self.vis_progress[self.vis_caldev]:
            self.rb_rm_field(self.vis_caldev, 'SPECTRAL_WINDOW_ID', self.vis_uniqs[4])
            self.rb_indexer(self.vis_caldev, 'SPECTRAL_WINDOW_ID', self.vis_uniqs[4])

        if self.vis_progress[self.vis_syscal]:
            self.rb_rm_field(self.vis_syscal, 'SPECTRAL_WINDOW_ID', self.vis_uniqs[4])
            self.rb_indexer(self.vis_syscal, 'SPECTRAL_WINDOW_ID', self.vis_uniqs[4])

        field_unused_rows = self.rb_unused_list(self.vis_rows_number[2], self.vis_uniqs[1])
        self.map_field = self.rb_mapper(self.vis_rows_number[2], field_unused_rows)
        self.rb_save('field', self.map_field)

        spw_unused_rows = self.rb_unused_list(self.vis_rows_number[4], self.vis_uniqs[4])
        self.map_spw = self.rb_mapper(self.vis_rows_number[4], spw_unused_rows)
        self.rb_save('spw', self.map_spw)

        self.cslog.post("##### End Task: rbindex #####", origin="rbindex")

if __name__ == '__main__':
    pass
