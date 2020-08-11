#!/usr/bin/python
# -*- coding:utf-8 -*-

import os

from module import AndroidResString
from module import log
from module import ExcelWriteHelper
from module import ExcelHelper
from module import DB
from module import GoogleTrans

PLATFORM_ANDROID = 'android'
PLATFORM_IOS = 'ios'

FILE_TYPE_XML = 'xml'
FILE_TYPE_EXCEL = 'excel'


class LanguageTranslation(object):
    KEY_NAME = 'name'
    KEY_TEXT = 'text'
    KEY_TRANSLATION = 'translation'
    KEY_MANUAL_TRANSLATION = 'manual_translation'
    KEY_TRANSLATION_RESULT = "results"

    header_name_2_key = {
        'key': KEY_NAME,
        'translation': KEY_TRANSLATION,
        'manual_translation': KEY_MANUAL_TRANSLATION,
        'text': KEY_TEXT
    }

    basic_headers = [
        {'key': KEY_NAME, 'name': 'key'},
        {'key': KEY_TRANSLATION, 'name': 'translation'},
        {'key': KEY_MANUAL_TRANSLATION, 'name': 'manual_translation'},
        {'key': KEY_TEXT, 'name': 'text'},
    ]

    def __init__(self):
        self.db = DB('cache')
        self.gt = GoogleTrans()
        self.infos = []
        self.languages = set()

    def _translation_impl(self, text, dst, src='en'):
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        dbkey = "%s:%s" % (dst, text)
        result = self.db[dbkey]
        if result is None:
            result = self.gt.translate(text, dest=dst, src=src)
            self.db[dbkey] = result
        # if isinstance(result, str):
        #     result = result.decode('utf-8')
        return result

    def _format_text(self, text, reverse=False):
        codes = [
            ('\\n', '\n'),
            # ('<Data>', '@@@@@@'),
            # ('</Data>', '@@@@@'),
            # ('<u>', '@@@@'),
            # ('</u>', '@@@'),
            # ('%s', '@@'),
            # ('%d', '@')
        ]
        for code in codes:
            if reverse:
                old = code[1]
                new = code[0]
            else:
                old = code[0]
                new = code[1]
            text = text.replace(old, new)
        return text

    def _load_xml(self, input_path, platform=PLATFORM_ANDROID):
        if platform != PLATFORM_ANDROID:
            log.w("不支持的平台: " + platform)
            return
        ars = AndroidResString()
        ars.load(input_path)
        infos = [
            {
                self.KEY_NAME: info[AndroidResString.KEY_NAME],
                self.KEY_TEXT: info[AndroidResString.KEY_TEXT],
                self.KEY_TRANSLATION: info[AndroidResString.KEY_TRANSLATION],
                self.KEY_MANUAL_TRANSLATION: info[AndroidResString.KEY_MANUAL_TRANSLATION],
            }
            for info in ars.get_infos()
        ]
        self.infos.extend(infos)

    def _load_excel(self, input_path, platform=PLATFORM_ANDROID):
        if platform != PLATFORM_ANDROID:
            log.w("不支持的平台: " + platform)
            return
        eh = ExcelHelper(input_path)
        eh.openSheet(0)
        cols = eh.ncol()
        rows = eh.nrow()
        header = eh.row(0)
        if cols < 4 or header[:4] != [u'key', u'translation', u'manual_translation', u'text']:
            log.e("excel 必须最少4列,分别是key, translation, manual_translation, text")
            return
        for i in range(1, rows):
            row = eh.row(i)
            key = row[0]
            translation = row[1]
            manual_translation = row[2]
            text = row[3]

            infos = {
                self.KEY_NAME: key,
                self.KEY_TEXT: text,
                self.KEY_TRANSLATION: translation,
                self.KEY_MANUAL_TRANSLATION: manual_translation,
                self.KEY_TRANSLATION_RESULT: {}
            }
            for col in range(4, cols):
                lang = header[col]
                self.languages.add(lang)
                infos[self.KEY_TRANSLATION_RESULT][lang] = {'text': row[col], 'need_check': False}
            self.infos.append(infos)

        print self.infos

    def load(self, input_path, file_type=FILE_TYPE_XML, platform=PLATFORM_ANDROID):
        if file_type == FILE_TYPE_XML:
            self._load_xml(input_path, platform=platform)
        elif file_type == FILE_TYPE_EXCEL:
            self._load_excel(input_path, platform=platform)

    def translation(self, languages):
        for info in self.infos:
            name = info[self.KEY_NAME]
            text = info[self.KEY_TEXT]
            need_translation = info[self.KEY_TRANSLATION]
            manual_translation = info[self.KEY_MANUAL_TRANSLATION]
            translation_result = info.get(self.KEY_TRANSLATION_RESULT)
            if translation_result is None:
                translation_result = {}
                info[self.KEY_TRANSLATION_RESULT] = translation_result
            if len(text.strip()) == 0:
                continue
            if need_translation == True:
                format_text = self._format_text(text)
                log.i("format: " + text + ' >>> ' + format_text)
                for dst_lang in languages:
                    oldvalue = translation_result.get(dst_lang)
                    if oldvalue is not None and len(oldvalue['text'].strip()) > 0:
                        continue
                    result_text = self._translation_impl(format_text, dst=dst_lang)
                    translation_result[dst_lang] = {'text': self._format_text(result_text, True), 'need_check': True}
            else:
                for dst_lang in languages:
                    translation_result[dst_lang] = {'text': text, 'need_check': False}

    def export(self, output_path, platform=PLATFORM_ANDROID, output_file_type=FILE_TYPE_EXCEL, languages=None):
        if output_file_type == FILE_TYPE_EXCEL:
            self._export_2_excel(output_path, languages=languages)
        elif output_file_type == FILE_TYPE_XML:
            self._export_2_xml(output_path, platform=PLATFORM_ANDROID, languages=languages)
        else:
            log.e("未知输出文件类型")
            return
        log.i("output: " + output_path)

    def _export_2_excel(self, output_path, languages=[]):
        headers = []
        headers.extend(self.basic_headers)
        language_prefix = 'translation:'
        for l in languages:
            headers.append({'key': language_prefix + l, 'name': l})

        def default_transform(key, obj, row, col):
            # {'text': value, 'text_color': '', 'background_color': ''}
            text_color = None
            translation = obj.get('translation')
            manual_translation = obj.get('manual_translation')
            if translation == True and manual_translation == True:
                text_color = 'red'

            if key is None and col == -1:
                # 对整行处理
                return {'text_color': text_color, 'background_color': None}
            value = ""
            if key.startswith(language_prefix):
                language_result = obj.get(self.KEY_TRANSLATION_RESULT)
                if language_result is not None:
                    lang = key.replace(language_prefix, '')
                    value = language_result.get(lang).get('text')
                    if language_result.get(lang).get('need_check') is False:
                        text_color = None
                pass
            else:
                value = obj.get(key)
            return {'text': value, 'text_color': text_color}

        ewh = ExcelWriteHelper()
        ewh.set_head_style(text_color='black', background_color='ice_blue')
        ewh.add_sheet("languages")
        ewh.write(headers, self.infos, transform=default_transform)
        ewh.save(output_path)

    def _export_2_xml(self, output_path, platform=PLATFORM_ANDROID, languages=[]):
        if platform != PLATFORM_ANDROID:
            log.e("不支持的平台: " + platform)
            return
        if os.path.isfile(output_path):
            log.e("输入路径必须是目录或不存在")
            return
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        self.languages = self.languages | set(languages)
        for lang in languages:
            self._export_2_xml_by_language(output_path, lang)

    def _export_2_xml_by_language(self, output_dir_path, language):
        output_path = os.path.join(output_dir_path, language + '.xml')
        ars = AndroidResString()

        # kvs = [{"name": key, "translatable": False, "value": value}]
        def getKV(info):
            text = info[self.KEY_TRANSLATION_RESULT].get(language).get('text')
            print text
            if not isinstance(text, unicode):
                text = text.decode('utf-8')
            return {
                "name": info[self.KEY_NAME],
                "translatable": info[self.KEY_TRANSLATION],
                "value": text
            }

        kvs = [
            getKV(info)
            for info in self.infos
        ]
        ars.write(kvs, output_path)

    def _check_file_type(self, file_type, path):
        if file_type not in [FILE_TYPE_XML, FILE_TYPE_EXCEL]:
            ext = os.path.splitext(path)[1][1:].lower()
            if ext == 'xml':
                file_type = FILE_TYPE_XML
            elif ext == 'xlsx':
                file_type = FILE_TYPE_EXCEL
            else:
                log.e("位置文件类型:" + path)
                return None
        return file_type

    def run(self, input_path, out_path, platform=PLATFORM_ANDROID, input_type=FILE_TYPE_XML,
            output_type=FILE_TYPE_EXCEL, translation=True, languages=None):
        nosupportLanguages = set(languages) - set(GoogleTrans.supportLanguages().keys())
        if len(nosupportLanguages) > 0:
            log.e("不支持的语言" + str(list(nosupportLanguages)))
            return
        if input_path == out_path:
            log.e("暂时不支持覆盖文件, 请修改输出文件名")
            return

        input_type = self._check_file_type(input_type, input_path)
        output_type = self._check_file_type(output_type, out_path)
        if input_type is None or output_type is None:
            log.e("必须指定正确的文件类型")
            return

        self.load(input_path, file_type=input_type, platform=platform)
        if translation:
            self.translation(languages)
        self.export(out_path, platform=platform, output_file_type=output_type, languages=languages)


if __name__ == '__main__':
    pass
