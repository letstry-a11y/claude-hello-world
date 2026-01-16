# HTML 转 PowerPoint 转换器

将 HTML 文件转换为 PowerPoint 演示文稿的工具。

## 功能特点

- **自动检测幻灯片分隔**: 支持 `slide-container`、`section`、`article`、`<hr>` 等多种分隔方式
- **丰富的内容支持**: 标题、副标题、列表、图片、表格、卡片布局
- **FontAwesome 图标转换**: 自动将 FontAwesome 图标转换为 Unicode 符号
- **自定义主题颜色**: 支持自定义主色和强调色
- **双模式运行**: GUI 图形界面 + 命令行两种使用方式

## 安装依赖

```bash
pip install python-pptx beautifulsoup4 requests
```

## 使用方法

### GUI 模式（推荐）

直接运行程序，无需参数：

```bash
python html_to_pptx.py
```

或双击运行 `HTML转PPT转换器.exe`（如已打包）

### 命令行模式

```bash
python html_to_pptx.py <输入HTML文件> [输出PPTX文件]
```

示例：
```bash
python html_to_pptx.py report.html report.pptx
```

## 支持的 HTML 结构

### 幻灯片分隔

```html
<!-- 方式1: 使用 class -->
<div class="slide-container">...</div>

<!-- 方式2: 使用 section 标签 -->
<section>...</section>

<!-- 方式3: 使用 hr 分隔 -->
<h1>第一页</h1>
<p>内容...</p>
<hr>
<h1>第二页</h1>
```

### 标题和副标题

```html
<div class="slide-title">主标题</div>
<div class="slide-subtitle">副标题</div>
<!-- 或使用标准标签 -->
<h1>主标题</h1>
<h3>副标题</h3>
```

### 列表项

```html
<ul class="text-list">
    <li class="strength">
        <strong>优势项目</strong>
        详细说明文字
    </li>
    <li class="gap">
        <strong>待改进项</strong>
        详细说明文字
    </li>
</ul>
```

### 卡片布局

```html
<!-- 平铺卡片 -->
<div class="tile-grid">
    <div class="tile-card">
        <div class="tile-card-img"><img src="..."></div>
        <div class="tile-card-body">
            <h3>标题</h3>
            <p>描述</p>
        </div>
    </div>
</div>

<!-- 路线图卡片 -->
<div class="roadmap-grid">
    <div class="roadmap-card">
        <div class="card-header">
            <div class="icon-box"><i class="fas fa-globe"></i></div>
            <h4>标题</h4>
        </div>
        <p>描述内容</p>
    </div>
</div>
```

## 支持的 FontAwesome 图标

| 图标类名 | 转换结果 |
|---------|---------|
| fa-check-circle | ✓ |
| fa-exclamation-triangle | ⚠ |
| fa-globe-asia | 🌏 |
| fa-robot | 🤖 |
| fa-microchip | 💡 |
| fa-file-medical-alt | 📋 |
| fa-star | ★ |
| fa-chart-bar | 📊 |

## 自定义主题

在 GUI 中可以设置：
- **主色** (Primary): 标题颜色，默认 `#003366`
- **强调色** (Accent): 装饰线和图标背景，默认 `#0066CC`

## 打包为 EXE

使用 PyInstaller 打包：

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "HTML转PPT转换器" html_to_pptx.py
```

生成的 exe 文件在 `dist/` 目录中。

## 示例文件

项目包含示例文件 `skywalker_report.html`，展示了：
- 双栏布局（列表 + 图片）
- 卡片网格布局
- 路线图布局

## 注意事项

1. **图片下载**: 外部图片需要网络连接，如下载失败会显示警告
2. **字体支持**: 建议系统安装微软雅黑等中文字体
3. **幻灯片尺寸**: 默认 16:9 宽屏比例 (13.333" x 7.5")

## 文件说明

| 文件 | 说明 |
|-----|------|
| `html_to_pptx.py` | HTML 转 PPTX 转换器主程序 |
| `create_pptx.py` | 使用 Anthropic API 创建 PPT |
| `skywalker_report.html` | 示例 HTML 报告 |

## License

MIT License
