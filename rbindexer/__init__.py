# !/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def rbindex(**keywords):
    if len(keywords) == 0:
        print "No entry"
    elif len(keywords) > 0 and 'vis' in keywords:
        vis = keywords['vis']
        import main
        main.rbkit(vis)
    else:
        print "Please specify a vis file!"


def rb_subtable(subtable=''):
    if subtable == 'spw':
        f = open('map_spw', 'r')
        return f
    elif subtable == 'field':
        f = open('map_field', 'r')
        return f
    else:
        raise ValueError


def rb_dict(f):
    map_spw = f.read()
    f.close()
    sep = []
    for i in range(len(map_spw)):
        if map_spw[i].isalnum():
            sep.append(str(map_spw[i]))
        else:
            if map_spw[i] == ':':
                sep.append(str(map_spw[i]))
            elif map_spw[i] == ",":
                sep.append(str(map_spw[i]))
            else:
                pass
    new_map = (''.join(sep)).split(',')
    dict_list = []
    for i in range(len(new_map)):
        dict_list.append(new_map[i].split(':'))
    first = []
    last = []
    for i in range(len(dict_list)):
        first.append(dict_list[i][0])
        last.append(dict_list[i][1])
    calc_map = dict(zip(first, last))
    calc_map[';'] = ';'
    calc_map[':'] = ':'
    calc_map['~'] = '~'
    return calc_map


def rbmap(inp='', subtable=''):
    if subtable == 'spw':
        if str(inp) == '*':
            return '*'
        elif ',' in inp:
            inp_str = str(inp).split(',')
            slist = []
            for vals in inp_str:
                slist += [vals.split(':')]
            firstlist = []
            lastlist = []
            for vals in slist:
                firstlist += [str(vals[0])]
                lastlist += [str(vals[1])]
            mylist = []
            for i in firstlist:
                mylist.append(re.findall(r"[^\W\d_]+|\d+|:|;|~", i))
            calc_list = mylist
            mydict = rb_subtable(subtable='spw')
            calc_map = rb_dict(mydict)
            for i in range(len(mylist)):
                for j in range(len(mylist[i])):
                    if mylist[i][j] in calc_map:
                        calc_list[i][j] = calc_map[mylist[i][j]]
            calc_list2 = []
            for i in range(len(calc_list)):
                calc_list2.append(calc_list[i])
                calc_list2.append(':')
                calc_list2.append(lastlist[i])
                calc_list2.append(',')
            del calc_list2[-1]
            calc_list3 = []
            for i in range(len(calc_list2)):
                if type(calc_list2[i]) == list:
                    calc_list3.append(''.join(str(j) for j in calc_list2[i]))
                else:
                    calc_list3.append(calc_list2[i])
            return ''.join(calc_list3)

        elif '~' and ':' in inp:
            inp_str = str(inp).split(':')
            mydict = rb_subtable(subtable='spw')
            calc_map = rb_dict(mydict)
            mylist = []
            for i in inp_str[0]:
                mylist.append(calc_map[i])
            mylist.append(':')
            mylist.append(inp_str[1])
            return ''.join(mylist)

        elif '~' in inp:
            mydict = rb_subtable(subtable='spw')
            calc_map = rb_dict(mydict)
            mylist = re.findall(r"[^\W\d_]+|\d+|:|;|~", inp)
            calc_list = []
            for i in mylist:
                calc_list.append(calc_map[i])
            return ''.join(calc_list)

        elif str(inp).isalnum():
            mydict = rb_subtable(subtable='spw')
            calc_map = rb_dict(mydict)
            return str(calc_map[inp])

        else:
            return None

    elif subtable == 'field':
        if str(inp) == '*':
            return ['*']

        elif '~' in inp:
            mydict = rb_subtable(subtable='field')
            calc_map = rb_dict(mydict)
            mylist = re.findall(r"[^\W\d_]+|\d+|:|;|~", inp)
            calc_list = []
            for i in mylist:
                calc_list.append(calc_map[i])
            return ''.join(calc_list)

        elif str(inp).isalnum():
            mydict = rb_subtable(subtable='field')
            calc_map = rb_dict(mydict)
            return str(calc_map[inp])

        else:
            return None


if __name__ == '__main__':
    pass
