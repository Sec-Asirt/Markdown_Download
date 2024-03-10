## 背景
就是最近在学习一些东西，搜资料时，某些网站要登陆，要关注，要付费， 不让复制啥的，搞得我很烦

## 思路
我用的是EDGE浏览器，微软的套google内核的浏览器，我不知道其他的浏览器有没有这个功能们，就是就是进入阅读模式。

当找到需要的文章时，可能不给复制，当时我也想过禁用js啥的，后来怎么折腾都不行，最后发现可以使用阅读模式，进入阅读模式后可以直接复制，文章内容，因为阅读模式下只显示文章内容。

将复制到的内容粘贴到Markdown文档上，然后通过Python解析markdown文档，然后获取到其中的所有图片，再把图片按md文件名保存到markdown文件所在目录下

## 简介

```powershell
PS D:\WorkingModule\Markdown-Image2Local> python .\md_image2local.py --help
usage: md_image2local.py [-h] [-path PATH] [--modify_source] [--absolute_path]

options:
  -h, --help       show this help message and exit
  -path PATH       markdown directory
  --modify_source  whether to modify source md file directly
  --absolute_path  Modify in absolute address mode
PS D:\WorkingModule\Markdown-Image2Local>
```

-path (必须项)                     md文档所在路径

 --modify_sourc (附加)项   修改源文件，将下载的图片路径(相对路径)替换原文件中的网络路径

--absolute_path (附加项)   在--modify_sourc参数的基础上以绝对路径的方式替换原文件中的路径



## 使用

运行环境

```powershell
pip install  -r .\requirements.txt
```

只下载图片

```powershell
python .\md_image2local.py -path=G:\学习文档\漏洞挖掘
```

修改原文件

```powershell
python .\md_image2local.py -path=G:\学习文档\漏洞挖掘 --modify_source
```



```powershell
PS D:\WorkingModule\Markdown-Image2Local> python .\md_image2local.py -path=G:\学习文档\漏洞挖掘 --modify_source
[+] Processing... G:\学习文档\漏洞挖掘\PWN入门.md
[-] Discover images 33 sheet
[-] Downloading (33/33)|████████████████████████████████████████████████████████████████████████████████████████████████████|100.00%
[+] Completed successfully
PS D:\WorkingModule\Markdown-Image2Local>
```

