# 参考项目快照

这里保存 Lumenbook 设计时使用的两个参考项目。它们以普通目录随仓库一并提供，便于直接查阅类文件、样式、说明与示例。

| 目录 | 来源 | 在 Lumenbook 中的作用 |
| --- | --- | --- |
| [subook/](subook/) | [chancey922/subook](https://github.com/chancey922/subook) | 主要依据：标准 book 基类、宽边栏、边注写作接口和彩色数学环境 |
| [kaobook-master/](kaobook-master/) | [fmarotta/kaobook](https://github.com/fmarotta/kaobook) | 次要参考：浅底色框、配置拆分和双面书籍的外侧边栏 |

## 快照信息

- `subook/subook.cls` 标注作者为 Changxing Su，类日期为 2021/12/27；原始说明见 [README](subook/README.md) 和 [中文 README](subook/README_CN.md)。
- `kaobook-master/kaobook.cls` 标注版本 0.9.8、日期 2021/08/23；原始说明见 [README](kaobook-master/README.md)，文件清单与分发说明见 [MANIFEST](kaobook-master/MANIFEST.md)。
- 这些是本项目收到的本地快照；没有可核验的上游提交 ID，因此不将快照日期或类版本冒充某个 Git 提交。

## 保留范围与许可

原始文件内容保持不变，包含源码、示例、图片和已有的 PDF 文档。TeX 编译缓存等中间文件留在本地，由根目录 `.gitignore` 排除。两个项目不是 Git 子模块，克隆本仓库即可获取已提交的参考文件。

- subook 的许可文本：[License](subook/License)。
- kaobook 的许可文本：[LICENSE](kaobook-master/LICENSE)；具体文件说明以其原始说明为准。

Lumenbook 是独立实现，不加载这里的类文件或样式文件。哪些设计思路被保留、哪些部分重新实现，见根目录 [SOURCES.md](../SOURCES.md)。上游项目的作者信息与许可归属保留不变。
