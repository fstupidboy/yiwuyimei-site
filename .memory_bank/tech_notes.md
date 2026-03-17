# 技术备注

## 图片处理
- 图片路径保持英文: `/images/products/humidifiers/`
- 翻译脚本会自动保留路径，不翻译目录名

## 翻译工作流
1. 添加映射到 `scripts/translate_product_specs.py`
2. 运行 `python scripts/translate_product_specs.py en <lang>`
3. 创建 `i18n/<lang>.yaml`
4. 添加到 `config.toml`
5. 创建 service/contact 页面

## 服务页面图标匹配
模板使用 `eq .Title` 匹配翻译后的标题：
- 产品开发: Produktentwicklung, Développement de Produits, etc.
- 质量控制: Qualitätskontrolle, Contrôle Qualité, etc.
- 物流: Logistikdienstleistungen, Services Logistiques, etc.

## 移动端导航栏
- 桌面端: 水平语言列表 (10个语言代码)
- 移动端: 下拉菜单，只显示当前语言 + 下拉箭头
