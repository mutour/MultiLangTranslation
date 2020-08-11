#!/usr/bin/python
# -*- coding:utf-8 -*-

"""用于读写Excel表"""

import xlrd
import xlwt

import log


class ExcelHelper(object):
    def __init__(self, excelPath):
        self.data = xlrd.open_workbook(excelPath)
        self.table = None

    def openSheet(self, index):
        self.table = self.data.sheet_by_index(index)  # 通过索引顺序获取

    def sheet_names(self):
        return self.data.sheet_names()

    def cell(self, row, col):
        return self.table.cell(row, col).value

    def row(self, row):
        return self.table.row_values(row)

    def col(self, col):
        return self.table.col_values(col)

    def nrow(self):
        return self.table.nrows

    def ncol(self):
        return self.table.ncols


class ExcelWriteHelper(object):
    def __init__(self, encoding='utf8'):
        self.workbook = xlwt.Workbook(encoding=encoding)
        self.current_worksheet = None

        self.head_style = None

    def support_colors(self):
        return xlwt.Style.colour_map

    def add_sheet(self, sheet):
        self.current_worksheet = self.workbook.add_sheet(sheet)
        return self.current_worksheet

    def set_head_style(self, text_color=None, background_color=None, bold=True):
        self.head_style = self.get_style(text_color=text_color, background_color=background_color, bold=bold)

    def get_style(self, text_color=None, background_color=None, bold=False):
        styles = []
        if background_color is not None:
            styles.append('pattern: pattern solid, fore_colour %s' % background_color)
        if text_color is not None:
            styles.append('font:colour_index %s' % text_color)
        if bold is True:
            styles.append('font: bold on')

        if len(styles) > 0:
            style = xlwt.easyxf('; '.join(styles))
        else:
            style = xlwt.Style.default_style
        return style

    def writeCell(self, row, col, label, worksheet=None, style=None):
        if worksheet is None:
            worksheet = self.current_worksheet
        if worksheet is None:
            log.e("must first call add_sheet")
            return
        worksheet.write(row, col, label=label, style=style)

    def save(self, path):
        self.workbook.save(path)

    def default_transform(self, key, obj, row, col):
        # {'text': value, 'text_color': '', 'background_color': ''}
        if key is None and col == -1:
            # 对整行处理
            return {'text_color': None, 'background_color': None}
        return {'text': str(obj)}

    def write(self, headers, objs, transform=None, worksheet=None):
        '''
        :param header: [{'key': value, 'name': value}]
        :param rows:
        :return:
        '''

        if transform is None:
            transform = self.default_transform

        names = [header['name'] for header in headers]
        keys = [header['key'] for header in headers]

        col_count = len(names)
        # 写头
        for i in range(col_count):
            self.writeCell(0, i, names[i], style=self.head_style)
        for i in range(len(objs)):
            obj = objs[i]
            row = i + 1
            row_info = transform(None, obj, row, -1)
            row_text_color = row_info.get('text_color')
            row_background_color = row_info.get('background_color')
            row_style = self.get_style(text_color=row_text_color, background_color=row_background_color)

            for col in range(col_count):
                key = keys[col]
                value_info = transform(key, obj, row, col)
                text = value_info.get('text')
                text_color = value_info.get('text_color')
                background_color = value_info.get('background_color')
                style = row_style
                if text_color is not None and background_color is not None:
                    style = self.get_style(text_color=text_color, background_color=background_color)
                elif text_color != row_text_color or background_color != row_background_color:
                    style = self.get_style(text_color=text_color, background_color=background_color)
                self.writeCell(row, col, text, style=style)


if __name__ == '__main__':
    pass
