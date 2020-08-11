#!/usr/bin/python
# -*- coding:utf-8 -*-

from googletrans import Translator
from googletrans import constants

'''
https://github.com/ssut/py-googletrans

Request URL: 
google网站的请求连接
https://translate.google.cn/translate_a/single?client=webapp&sl=auto&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=sos&dt=ss&dt=t&source=bh&ssel=0&tsel=0&xid=45662847&kc=1&tk=656796.835900&q=GET%20IT%20NOW
googletrans插件请求连接
https://translate.google.cn/translate_a/single?otf=1&tsel=0&hl=zh-cn&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&q=GET+IT+NOW&tl=zh-cn&client=t&tk=656796.835900&sl=auto&ssel=0

经过分析吧client=t改为client=webapp,翻译会和网站的一样
https://translate.google.cn/translate_a/single?otf=1&tsel=0&hl=zh-cn&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&q=GET+IT+NOW&tl=zh-cn&client=webapp&tk=656796.835900&sl=auto&ssel=0

遇到问题, client=t会出现全大写无法翻译, 而且翻译结果和网站不一样

'''


class GoogleTrans:
    def __init__(self):
        self.translator = Translator(service_urls=[
            'translate.google.cn'
            # , 'translate.google.com'
        ])

    def translate(self, source, dest='en', src='auto'):
        '''

        :param source: str or list
        :param dest:
        :param src:
        :return:
        '''
        # 这里改成首字母大写, 否则全大写英文不翻译
        # source = source.capitalize()
        result = self.translator.translate(source, dest=dest, src=src)
        if isinstance(result, list):
            return [r.text for r in result]
        return result.text

    @staticmethod
    def supportLanguages():
        return constants.LANGUAGES


if __name__ == '__main__':
    gt = GoogleTrans()
    # for text in gt.translate([
    #     "GET IT NOW",
    #     "GET it NOW",
    #     "GET it now",
    #     "get it now",
    #     "Get it now",
    # ], dest="zh-cn"):
    #     print text
    #
    # for text in gt.translate([
    #     "GET VIP\nGET VIP",
    # ], dest="zh-cn"):
    #     print text
    # text = ur'You can 😁😁😁😁Cancel anytime😁😁😁. I Can😁😁😁😁Cancel anytime😁😁😁.'
    # print gt.translate(text, dest="zh-cn", src='en')

    for i in range(100):
        text = "'Understand and agree to the'"
        print gt.translate(text, dest='ko', src='en')

    '''
    https://translate.google.cn/translate_a/single?otf=1&amp;tsel=0&amp;hl=ko&amp;dt=at&amp;dt=bd&amp;dt=ex&amp;dt=ld&amp;dt=md&amp;dt=qca&amp;dt=rw&amp;dt=rm&amp;dt=ss&amp;dt=t&amp;ie=UTF-8&amp;oe=UTF-8&amp;q=Understand+and+agree+to+the&amp;tl=ko&amp;client=t&amp;tk=550453.959179&amp;sl=en&amp;ssel=0
    '''
