#!/usr/bin/python
# -*- coding:utf-8 -*-

import argparse
import sys
from languagetranslation import *
from module import log

VERSION = '1.0'


def main():
    '''
    各个参数的含义：
        dest：用于保存输入的临时变量，其值通过options的属性进行访问，存储的内容是-f或 --file之后输入的参数
        help：用于生成帮助信息
        default: 给dest的默认值，如果用户没有在命令行参数给dest分配值，则使用默认值
        type: 用于检查命令行参数传入的参数的数据类型是否符合要求，有string，int，float等类型
        action: 用于指导程序在遇到命令行参数时候该如何处理，有三种值可选： store,store_false和store_true,默认值是store
          store：读取参数，如果参数类型符合type的要求，则将参数值传递给dest变量，作为options的一个属性供使用。
          store_true/store_false: 一般作为一个标记使用，分别设置dest变量的值为True和False
        metavar: 占位字符串，用于在输出帮助信息时，代替当前命令选项的附加参数的值进行输出，只在帮助信息里有用，注意其和default的区别
    :return:
    '''

    opt = argparse.ArgumentParser(description="多语言翻译", version=VERSION)
    opt.add_argument("input", action="store", help="输入文件")
    opt.add_argument("output", action="store", help="输出文件or目录")
    opt.add_argument("-p", "--platform", action="store", dest="platform", default='android',
                     help="平台, 暂时只支持android")
    opt.add_argument("-it", "--inputtype", action="store", dest='input_type',
                     help="输入文件类型:excel或者xml, 不设置则自行通过文件后缀判断")
    opt.add_argument("-ot", "--outputtype", action="store", dest='output_type',
                     help="输出文件类型:excel或者xml, 不设置则自行通过文件后缀判断")
    opt.add_argument("-l", "--languages", action="store", default='', dest='languages', help="处理语言,逗号分隔")
    opt.add_argument("-s", "--supportlanguages", action="store_true", default=False, dest='support_languages',
                     help="支持的语言")
    if len(sys.argv) < 2:
        opt.print_help()
        sys.exit(1)
    options = opt.parse_args()

    if options.support_languages:
        gt = GoogleTrans()
        print '\n'.join([kv[0] + " >> " + kv[1] for kv in gt.supportLanguages().items()])
        return

    lt = LanguageTranslation()
    languages = options.languages.split(',')
    lt.run(options.input, options.output, options.platform, options.input_type, options.output_type,
           languages=languages)


def test():
    input_path = 'out/strings.xlsx'
    output_path = 'out/strings2'
    platform = PLATFORM_ANDROID
    input_type = FILE_TYPE_EXCEL
    output_type = FILE_TYPE_XML
    languages = ['zh-cn', 'zh-tw', 'ko', 'ja']
    translation = True
    if False:
        input_path = 'out/strings.xml'
        output_path = 'out/strings.xlsx'
        platform = PLATFORM_ANDROID
        input_type = FILE_TYPE_XML
        output_type = FILE_TYPE_EXCEL
        languages = ['zh-cn', 'zh-tw', 'ko', 'ja']
    elif False:
        input_path = 'out/strings.xlsx'
        output_path = 'out/strings2.xlsx'
        platform = PLATFORM_ANDROID
        input_type = FILE_TYPE_EXCEL
        output_type = FILE_TYPE_EXCEL
        languages = ['zh-cn', 'zh-tw', 'ko', 'ja']
    elif True:
        input_path = 'out/strings.xlsx'
        output_path = 'out/strings2'
        platform = PLATFORM_ANDROID
        input_type = FILE_TYPE_EXCEL
        output_type = FILE_TYPE_XML
        languages = ['zh-cn', 'zh-tw', 'ko', 'ja']

    lt = LanguageTranslation()
    lt.run(input_path, output_path, platform, input_type, output_type, languages=languages)


if __name__ == '__main__':
    #  python main.py out/strings.xml out/strings2.xlsx -p android -a xml -b excel -l zh-cn,zh-tw,ko
    main()
