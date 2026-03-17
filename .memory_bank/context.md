# YIWUYIMEI Website - Work Context

## 项目概述
- **项目名称**: yiwuyimei.com (B2B export company)
- **技术栈**: Hugo v0.157.0+extended, Theme: PaperMod
- **部署**: Netlify (GitHub: fstupidboy/yiwuyimei-site)
- **工作目录**: /Volumes/ZHITAI2T/kimi2/website_design/www.yiwuyimei.com.backup

## 当前状态
- **总页面数**: ~1,673 页 (10种语言)
- **产品数**: 136 个产品 × 10 种语言

### 语言支持 (10种)
| 语言 | 代码 | 页面数 | 状态 |
|------|------|--------|------|
| English | en | 171 | ✅ 完整 |
| Korean | ko | 169 | ✅ 完整 |
| Japanese | ja | 169 | ✅ 完整 |
| Spanish | es | 169 | ✅ 完整 |
| German | de | 165 | ✅ 完整 |
| French | fr | 165 | ✅ 完整 |
| Italian | it | 165 | ✅ 完整 |
| Polish | pl | 165 | ✅ 完整 |
| Finnish | fi | 165 | ✅ 完整 |
| Irish | ga | 165 | ✅ 完整 |

## 最近完成的任务
1. ✅ 移动端导航栏修复 - 语言选择器改为下拉菜单
2. ✅ 产品列表页面多语言翻译 (10种语言)
3. ✅ 服务子页面内容补充 (DE/FR/IT/PL/FI/GA)
4. ✅ 服务页面图标修复 (DE/FR/IT/PL/FI/GA)
5. ✅ 法语 YAML 转义问题修复

## 关键文件位置

### 配置文件
- `config.toml` - Hugo 主配置 (10语言)
- `netlify.toml` - 部署配置

### 国际化
- `i18n/*.yaml` - 10种语言的翻译文件

### 布局模板
- `layouts/partials/navbar.html` - 导航栏 (含移动端语言下拉)
- `layouts/_default/list.html` - 产品列表页
- `layouts/_default/single.html` - 产品详情页
- `layouts/services/list.html` - 服务列表
- `layouts/services/single.html` - 服务详情
- `layouts/index.html` - 首页

### 内容目录
- `content/en/products/` - 英文产品 (源语言)
- `content/{lang}/products/` - 各语言产品
- `content/{lang}/services/` - 服务页面

### 工具脚本
- `scripts/translate_product_specs.py` - 产品规格翻译器

## 已知问题 / 待办事项
- [ ] 暂无已知问题

## Git 状态
- 分支: main
- 最后提交: 2ef8dda - fix YAML escaping in French i18n
- 已推送至 GitHub, Netlify 自动部署

## 常用命令
```bash
# 本地预览
hugo server -D

# 构建
hugo

# 推送更新
git add .
git commit -m "message"
git push origin main
```

## 上次会话时间
2026-03-17
