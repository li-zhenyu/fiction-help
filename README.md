# 小说下载器（第三版）

## 功能

从网站批量下载网络小说，用latex生成pdf，用pandoc生成epub。

仅用于数据分析的样本采集，请勿用于其他用途。所产生的文档请勿传播。

## 依赖

- texlive
- Python3
- pandoc
- ``` pip install pylatex lxml requests ```

## 测试网站（2021年）

http://www.b5200.net

## 后记

当初完成这几行代码，是2020年，我上初三的时候。那时突发奇想，想要创建一个好用的小说下载工具。虽有Fiction-Down珠玉在前，而彼时尚不完善，难以胜任大型小说的处理。

设计之初，我将小说按章节拆分，并且使用LaTeX排版，这个思路一直未曾改变。后来又引入pandoc来生成epub，满足使用移动设备阅读的需要。虽然十分简陋，但依旧可以满足个人对这一功能的需求。

后来我上了高中，不仅没有时间维护这几行代码，连网络小说本身都罢却了。当时选的是理科，日夜繁忙，自不待言。

高中三年，有感能力低位，资质谫陋。大学遂攻读法律。虽然仍喜爱网络小说，然而敲打代码，研究相关问题的兴致，早已烟消云散，今非昔比了。

谨以这一repository纪念我的少年岁月。

li-zhenyu
2024年4月14日
