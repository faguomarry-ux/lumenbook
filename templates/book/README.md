# Lumenbook 写书净版

这是可以直接开始写作的源码包，保留 PDE 封面、双面边注排版、数学环境、
代码、文字标记及学习工具。仅包含必需的类／样式文件、写作骨架和简短说明。

## 开始写作

1. 解压整个文件夹，不要单独移动 `main.tex`。
2. 修改 `book-info.tex` 中的书名、作者和日期。
3. 在 `chapters/01-introduction.tex` 中开始正文。
4. 新增章节时，在 `main.tex` 中添加对应的 `\input{chapters/文件名}`。

需要安装较完整的 TeX Live 或 MiKTeX，使用 **XeLaTeX**；输入文件为 UTF-8。
在本文件夹打开终端后运行：

```powershell
latexmk -xelatex main.tex
```

成品位于 `build/main.pdf`，编译产物统一放在 `build/`，源码目录保持整洁。
没有 latexmk 时可运行两次：

```powershell
xelatex -no-shell-escape -interaction=nonstopmode main.tex
xelatex -no-shell-escape -interaction=nonstopmode main.tex
```

第二种方式会在根目录生成 PDF 和中间文件。LuaLaTeX 用户可改用
`latexmk -lualatex main.tex`。不支持 pdfLaTeX。

## 最常用的设置

- 默认 A4 双面排版，边注在外侧，装订余量为 4 mm。屏幕阅读时把类选项中的
  `print,bindingoffset=4mm` 改为 `screen`。
- 默认使用 TeX 自带的 TeX Gyre / Fandol 字体，不需要本地字体文件或系统宋体。
- 中文界面名称：在类选项中增加 `language=chinese`。
- 原暖纸色封面：把 `cover=pde` 改成 `cover=editorial`。
- 灰度：增加 `theme=mono`。更换封面方程：修改 `\coverequation{...}`。
- PDE 封面的书名建议保留三行；文字明显变长时需调整 `lumen-cover.sty`
  中的字号或坐标，并查看编译后的页面。

正文可直接使用 `definition`、`theorem`、`lemma`、`proof`、`example`、
`exercise` 环境，边注写作 `\mn{这里写边注}`，编号边注写作 `\sn{这里写边注}`。
图片可自行创建 `figures/` 文件夹后用 `\includegraphics` 插入。

## 文件分工

| 文件 | 用途 |
| --- | --- |
| `main.tex` | 编译入口、章节顺序 |
| `book-info.tex` | 书名、作者及封面信息 |
| `chapters/` | 正文 |
| `lumenbook.cls`、`lumen-*.sty` | 排版引擎，通常不必修改 |
| `latexmkrc` | 编译方式和输出目录 |
| `LICENSE`、`SOURCES.md` | 许可和来源 |

本包未附带 PDF 预览、字体二进制文件、参考项目、测试、演示、历史文档和
编译产物。它仍需依赖已安装的 TeX 发行版；缺失宏包由发行版安装。
