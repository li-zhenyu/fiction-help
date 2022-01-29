# 小说阅读辅助工具 3

完全重写。python单文件实现。

## 功能

从 网站 批量 下载 网络 小说 并且 用 latex 生成 pdf，用 pandoc 生成 epub。
## 依赖

texlive 2021	http://tug.org

Python3.8+

``` pip install pylatex lxml requests ```

Windows 10 (only)

## 特性
1. 使用一个 links.txt 输入多个目录链接
2. 使用 lualatex 编译为pdf
3. 完成后有提示音
4. 超时重连
5. 使用 IE 的 UA
6. 简单净化文本
7. 去除非正式章节
8. 重排章节序号

## 测试平台

Windows 10

texlive 2021

Python 3.9

## 支持网站

http://www.b5200.net

以及与其结构完全相同的网站（换皮网站）
## 作者

li-zhenyu
