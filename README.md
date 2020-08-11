# LangTranslation

该工具主要用于对文本进行多语言翻译, 暂时适用于Android平台的语言翻译,其他平台可以考虑自行生成excel格式再运行

```
usage: main.py [-h] [-i INPUT_PATH] [-o OUTPUT_PATH] [-p PLATFORM]
               [-it INPUT_TYPE] [-ot OUTPUT_TYPE] [-l LANGUAGES] [-s]

多语言翻译

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_PATH, --input INPUT_PATH
                        输入文件
  -o OUTPUT_PATH, --output OUTPUT_PATH
                        输出文件or目录
  -p PLATFORM, --platform PLATFORM
                        平台, 暂时只支持android
  -it INPUT_TYPE, --inputtype INPUT_TYPE
                        输入文件类型:excel或者xml
  -ot OUTPUT_TYPE, --outputtype OUTPUT_TYPE
                        输出文件类型:excel或者xml
  -l LANGUAGES, --languages LANGUAGES
                        处理语言,逗号分隔
  -s, --supportlanguages
                        支持的语言

```

检查支持的翻译语言:
> python main.py -s 

android的strings.xml文件转excel:
> python main.py strings.xml strings.xlsx -p android -ot excel -l zh-cn,zh-tw,ko

其中-p android 和 -ot excel可忽略

excel文件转excel: 主要用于补充和手动修改多语言文案, 已经存在的内容原样输出, 不存在的翻译才会在线进行翻译
> python main.py strings.xlsx strings2.xlsx -p android -ot excel -l zh-cn,zh-tw,ko

### 已知问题:
- 在线翻译不是很稳定, 带有特殊字符的会被翻译出错, 而且不好控制位置,所以生成的excel文件会标红,提示需要检查和手动修改
- 特殊字符包括emoji符号,html标签,转义字符等

