# Multilingual Translation Guide for YiwuYimei

## Overview

This guide explains how to add new languages to the YiwuYimei Hugo multilingual site.

## Supported Languages

| Language | Code | Status |
|----------|------|--------|
| English | en | ✅ Source |
| Korean | ko | ✅ Active |
| Japanese | ja | ✅ Active |
| Spanish | es | ✅ Active |
| German | de | 📋 Template ready |
| Arabic | ar | 📋 Template ready |

## Quick Start: Adding a New Language

### Step 1: Configure Hugo

Add the new language to `config.toml`:

```toml
[languages]
  [languages.en]
    contentDir = "content/en"
    languageName = "English"
    weight = 1
  [languages.ko]
    contentDir = "content/ko"
    languageName = "한국어"
    weight = 2
  # ... add new language here
  [languages.de]
    contentDir = "content/de"
    languageName = "Deutsch"
    weight = 5
```

### Step 2: Create i18n File

Create `i18n/{lang}.yaml` with UI translations:

```yaml
# Example: i18n/de.yaml
home: "Startseite"
products: "Produkte"
services: "Dienstleistungen"
contact: "Kontakt"
# ... see i18n/es.yaml for full reference
```

**Required keys:**
- Navigation: `home`, `products`, `services`, `contact`
- Product categories: `fans`, `shoes_dryers`, `scent_diffusers`, etc.
- UI elements: `read_more`, `view_details`, `product_specs`, etc.

### Step 3: Add Product Specification Translations

Edit `scripts/translate_product_specs.py` and add translations to:

1. **SPEC_LABELS** - Parameter labels (e.g., "Material", "Color")
2. **SPEC_VALUES** - Parameter values (e.g., "White", "Zinc alloy")

Example for German:

```python
SPEC_LABELS = {
    # ... existing languages ...
    "de": {
        "Material": "Material",
        "Color": "Farbe",
        "Product size": "Produktgröße",
        # ... add all labels
    },
}

SPEC_VALUES = {
    # ... existing languages ...
    "de": {
        "White": "Weiß",
        "Black": "Schwarz",
        "Zinc alloy": "Zinklegierung",
        # ... add all values
    },
}
```

### Step 4: Create Content Directory

```bash
mkdir -p content/{lang}/products
mkdir -p content/{lang}/services
mkdir -p content/{lang}/contact
mkdir -p content/{lang}/posts
```

### Step 5: Translate Content Files

#### Option A: Automated Translation (Recommended)

Run the translation script:

```bash
cd /path/to/your/site
python3 scripts/translate_product_specs.py en de
```

This will:
1. Copy all English product files
2. Automatically translate specification labels and values
3. Save to the target language directory

#### Option B: Manual Translation

Copy and translate files manually:

```bash
cp -r content/en/products/* content/de/products/
# Edit each file to translate front matter and content
```

### Step 6: Translate Service Pages

Create service pages in the new language:

```bash
# content/de/services/_index.md
---
title: "Dienstleistungen"
description: "Umfassende Exportlösungen für Ihr Unternehmen"
---
```

### Step 7: Translate Contact Page

```bash
# content/de/contact/_index.md
---
title: "Kontakt"
description: "Kontaktieren Sie uns für Anfragen"
---
```

### Step 8: Build and Test

```bash
hugo server -D
# Visit http://localhost:1313/de/ to test
```

## Translation Reference

### Product Specification Labels (Most Common)

| English | Spanish (es) | German (de) | Arabic (ar) |
|---------|--------------|-------------|-------------|
| Material | Material | Material | المادة |
| Color | Color | Farbe | اللون |
| Product size | Tamaño del Producto | Produktgröße | حجم المنتج |
| Product name | Nombre del Producto | Produktname | اسم المنتج |
| Product type | Tipo de Producto | Produkttyp | نوع المنتج |
| Product Certification | Certificación del Producto | Produktzertifizierung | شهادة المنتج |
| Product weight | Peso del Producto | Produktgewicht | وزن المنتج |
| Power | Potencia | Leistung | الطاقة |
| Capacity | Capacidad | Kapazität | السعة |
| Carton size | Tamaño del Cartón | Kartongröße | حجم الكرتون |
| Rated Voltage | Voltaje Nominal | Nennspannung | الجهد المقدر |
| Package | Paquete | Verpackung | العبوة |
| Packaging | Embalaje | Verpackung | التعبئة |
| Net/Gross Weight | Peso Neto/Bruto | Netto-/Bruttogewicht | الوزن الصافي/الإجمالي |

### Common Specification Values

| English | Spanish (es) | German (de) |
|---------|--------------|-------------|
| White | Blanco | Weiß |
| Black | Negro | Schwarz |
| Red | Rojo | Rot |
| Blue | Azul | Blau |
| Zinc alloy | Aleación de zinc | Zinklegierung |
| Stainless steel | Acero inoxidable | Edelstahl |
| Aluminum | Aluminio | Aluminium |
| Plastic | Plástico | Kunststoff |
| customize | Personalizado | Anpassbar |
| OEM | OEM | OEM |
| Cotton pads | Almohadillas de algodón | Baumwollpads |

## Advanced: RTL Languages (Arabic, Hebrew)

For RTL (Right-to-Left) languages:

1. Add RTL support to templates:
```html
<html lang="ar" dir="rtl">
```

2. Add RTL CSS:
```css
[dir="rtl"] {
  text-align: right;
}
```

3. Mirror layout adjustments as needed

## Troubleshooting

### Issue: Specifications not translating
- Check that the label exists in `SPEC_LABELS`
- Check that the value exists in `SPEC_VALUES`
- Run script with verbose output to debug

### Issue: Special characters not displaying
- Ensure files are saved with UTF-8 encoding
- Check that the font supports the language

### Issue: Layout breaks with long words
- Use CSS `word-wrap: break-word`
- Adjust column widths for the language

## Tips for Quality Translations

1. **Consistency**: Use consistent terminology across all pages
2. **Context**: Some terms need context (e.g., "Fan" could be "Ventilador" or "Aficionado")
3. **Review**: Have a native speaker review translations
4. **Testing**: Always test on actual devices

## Resources

- [Hugo Multilingual Documentation](https://gohugo.io/content-management/multilingual/)
- Translation Script: `scripts/translate_product_specs.py`
- i18n Examples: `i18n/es.yaml`, `i18n/ko.yaml`, `i18n/ja.yaml`
