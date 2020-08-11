#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import codecs
import os
from lxml import etree

import log

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import re


class AndroidResString(object):
    KEY_NAME = 'name'
    KEY_TEXT = 'text'
    KEY_TRANSLATION = 'translation'
    KEY_MANUAL_TRANSLATION = 'manual_translation'

    infos = []  # [{'name': name, 'text': text, 'translation': True, 'manual_translation': False} ]

    def __init__(self):
        pass

    def _get_text(self, node):
        text = node.text
        if text is None:
            text = ''

        children = node.getchildren()
        child_count = len(children)

        has_child = False
        if child_count > 0:
            has_child = True
            for i in range(child_count):
                child_node = children[i]

                child_text = self._get_text(child_node)[0]

                if child_node.tag == 'Data':
                    text += '<Data><![CDATA[%s]]></Data>' % child_text
                else:
                    text += '<%s>%s</%s>' % (child_node.tag, child_text, child_node.tag)
                if not (child_node.tail is None):
                    text += child_node.tail
        return text.strip(), has_child

    def _load(self, root):
        '''
            &#160; 会被转义
        '''
        for node in root.xpath('//resources/string', smart_strings=False):
            if node.attrib.get("translatable") == "false":
                continue
            name = node.attrib.get("name")

            manual_translation = False
            text, hasChildNode = self._get_text(node)
            if hasChildNode:
                manual_translation = True
            if len(re.findall('(%[a-z])', text, re.M | re.I)) > 0:
                manual_translation = True
            elif len(re.findall(r'(&#[\d]+;)', text, re.M | re.I)) > 0:
                manual_translation = True
            elif '\'' in text:
                manual_translation = True
            log.i("read: " + str(node.attrib) + " " + text)
            translation = True
            if text.startswith("@string/"):
                translation = False
            self.infos.append({
                'name': name,
                'text': text,
                'translation': translation,
                'manual_translation': manual_translation
            })

    def loadText(self, xmltext):
        parser = etree.XMLParser(recover=True, remove_blank_text=True)
        root = etree.fromstring(xmltext, parser=parser)
        self._load(root)

    def load(self, xmlpath):
        parser = etree.XMLParser(recover=True, remove_blank_text=True)
        root = etree.parse(xmlpath, parser=parser)
        self._load(root)

    def get_infos(self):
        return self.infos

    # def _indent(self, elem, level=0):
    #     fill = "\n" + level * " "
    #     childs = elem.getchildren()
    #     count = len(childs)
    #     if count > 0:
    #         elem.text = fill
    #     elif not elem.tail:
    #         elem.tail = fill
    #
    #     for index in range(count):
    #         child = childs[index]
    #         if index + 1 == count:
    #             self._indent(child)
    #         else:
    #             self._indent(child, level)
    #
    # def _add_sub_element(self, parent, name, attrib=None, text=None):
    #     if attrib is None:
    #         child = ET.SubElement(parent, name)
    #     else:
    #         child = ET.SubElement(parent, name, attrib)
    #     child.text = text
    #     return child
    #
    # def write(self, kvs, output_path):
    #     # kvs = [{"name": key, "translatable": False, "value": value}]
    #     root = ET.Element('resources')
    #     # 添加子节点SubElement(父节点Element对象， Tag字符串格式， Attribute字典格式)
    #     for kv in kvs:
    #         attrib = {'name': kv['name']}
    #         if kv['translatable'] == 'false':
    #             attrib['translatable'] = 'false'
    #         element = self._add_sub_element(root, 'string', attrib, kv['value'])
    #
    #     self._indent(root, 4)
    #     # 将根目录转化为xml树状结构(即ElementTree对象)
    #     tree = ET.ElementTree(root)
    #     # 在终端显示整个xml内容
    #     ET.dump(root)
    #     # 写入xml文件
    #     tree.write(output_path, encoding="utf-8", xml_declaration=True)

    def _toAndroidString(self, key, value):
        # <string name="app_name">BusinessDemo</string>
        return u'''<string name="{0}">{1}</string>'''.format(key, value)

    def write(self, kvs, output_path):
        # kvs = [{"name": key, "translatable": False, "value": value}]
        print 'start generate: ', output_path
        fp = codecs.open(output_path, 'wb', encoding='utf8')
        fp.write('''<?xml version="1.0" encoding="utf-8"?>
<resources>\n''')
        for kv in kvs:
            name = kv["name"]
            value = kv["value"]
            outvalue = self._toAndroidString(name, value)
            fp.write(u'''    {}\n'''.format(outvalue))
        fp.write('''</resources>\n''')
        fp.close()
        print "ok........."


test_text = '''
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="key1">You can <u>u1<u>u3</u></u>. I Can<u>u2</u>.</string>
</resources>
'''

if __name__ == '__main__':
    androidResString = AndroidResString()
    # androidResString.load('../out/strings.xml')
    androidResString.load(
        '../out/strings.xml')
    # androidResString.loadText(test_text)
