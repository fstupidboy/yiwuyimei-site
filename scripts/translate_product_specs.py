#!/usr/bin/env python3
"""
Product Specification Translator
================================
Translates product specification labels and values for Hugo multilingual sites.

Usage:
    python translate_product_specs.py <source_lang> <target_lang>
    
Examples:
    python translate_product_specs.py en es  # English to Spanish
    python translate_product_specs.py en de  # English to German
    python translate_product_specs.py en ar  # English to Arabic

How to add a new language:
    1. Add translation mappings to SPEC_LABELS and SPEC_VALUES dicts below
    2. Run the script with the new language code
"""

import os
import re
import sys
from pathlib import Path

# =============================================================================
# TRANSLATION MAPPINGS
# Add new languages here following the same pattern
# =============================================================================

SPEC_LABELS = {
    # English to Spanish
    "es": {
        "Material": "Material",
        "Color": "Color",
        "Product size": "Tamaño del Producto",
        "Product Size": "Tamaño del Producto",
        "Products Size (cm)": "Tamaño del Producto (cm)",
        "Product name": "Nombre del Producto",
        "Product type": "Tipo de Producto",
        "Product Certification": "Certificación del Producto",
        "Product weight": "Peso del Producto",
        "Product Weight": "Peso del Producto",
        "Power": "Potencia",
        "Capacity": "Capacidad",
        "Carton size": "Tamaño del Cartón",
        "Surface Finish": "Acabado Superficial",
        "Rated Voltage": "Voltaje Nominal",
        "Product Packaging size": "Tamaño del Embalaje",
        "Product Model": "Modelo del Producto",
        "Power Rating": "Potencia Nominal",
        "Packing quantity": "Cantidad por Embalaje",
        "Package": "Paquete",
        "Packaging": "Embalaje",
        "Net/Gross Weight": "Peso Neto/Bruto",
        "Input voltage": "Voltaje de Entrada",
        "QTY/CTN (pcs)": "Cantidad por Cartón (uds)",
        "Packing Size (cm)": "Tamaño de Embalaje (cm)",
        "Light source": "Fuente de Luz",
        "Feature": "Características",
        "Color temperature": "Temperatura de Color",
        "Color Rendering Index": "Índice de Reproducción Cromática",
        "G.W/N.W (kg)": "Peso Bruto/Neto (kg)",
        "G.W/N.W(kg)": "Peso Bruto/Neto (kg)",
        "Voltage": "Voltaje",
        "Rated power": "Potencia Nominal",
        "Battery capacity": "Capacidad de Batería",
        "Charging power": "Potencia de Carga",
        "Package size": "Tamaño del Paquete",
        "Carton Gross Weight": "Peso Bruto del Cartón",
        "Aromatherapist fragrance": "Fragancia Aromaterapéutica",
        "Model": "Modelo",
        "Size": "Tamaño",
        "Weight": "Peso",
        "Accessories": "Accesorios",
        "Inner box": "Caja Interior",
        "Logo": "Logo",
        "Printing": "Impresión",
        "MOQ": "Cantidad Mínima",
        "Function": "Función",
        "Design": "Diseño",
        "Usage": "Uso",
        "Application": "Aplicación",
        "Certification": "Certificación",
        "Warranty": "Garantía",
        "OEM/ODM": "OEM/ODM",
        "Customized": "Personalizado",
        "Sample": "Muestra",
        "Sample Time": "Tiempo de Muestra",
        "Lead Time": "Tiempo de Entrega",
        "Delivery": "Entrega",
        "Shipping": "Envío",
        "Payment": "Pago",
        "Payment Terms": "Términos de Pago",
        "Port": "Puerto",
        "Origin": "Origen",
        "Supply Ability": "Capacidad de Suministro",
        "Factory": "Fábrica",
        "Place of Origin": "Lugar de Origen",
        "Brand Name": "Nombre de la Marca",
        "Model Number": "Número de Modelo",
        "Style": "Estilo",
        "Including": "Incluyendo",
        "Scent": "Fragancia",
        "Weight": "Peso",
        "Remark": "Nota",
        "Working time": "Tiempo de Trabajo",
        "Logo": "Logo",
        "Product": "Producto",
        "Including": "Incluyendo",
        "Working voltage": "Voltaje de Trabajo",
        "Working gear": "Velocidad de Trabajo",
        "Battery Capacity": "Capacidad de Batería",
    },
    
    # English to German (template for future use)
    "de": {
        "Material": "Material",
        "Color": "Farbe",
        "Product size": "Produktgröße",
        "Product Size": "Produktgröße",
        "Products Size (cm)": "Produktgröße (cm)",
        "Product name": "Produktname",
        "Product type": "Produkttyp",
        "Product Certification": "Produktzertifizierung",
        "Product weight": "Produktgewicht",
        "Product Weight": "Produktgewicht",
        "Power": "Leistung",
        "Capacity": "Kapazität",
        "Carton size": "Kartongröße",
        "Surface Finish": "Oberflächenfinish",
        "Rated Voltage": "Nennspannung",
        "Product Packaging size": "Verpackungsgröße",
        "Product Model": "Produktmodell",
        "Power Rating": "Nennleistung",
        "Packing quantity": "Packungsmenge",
        "Package": "Verpackung",
        "Packaging": "Verpackung",
        "Net/Gross Weight": "Netto-/Bruttogewicht",
        "Input voltage": "Eingangsspannung",
        "QTY/CTN (pcs)": "Menge pro Karton (Stk)",
        "Packing Size (cm)": "Verpackungsgröße (cm)",
        "Light source": "Lichtquelle",
        "Feature": "Merkmale",
        "Color temperature": "Farbtemperatur",
        "Color Rendering Index": "Farbwiedergabeindex",
        "G.W/N.W (kg)": "Brutto/Netto (kg)",
        "G.W/N.W(kg)": "Brutto/Netto (kg)",
        "Voltage": "Spannung",
        "Rated power": "Nennleistung",
        "Battery capacity": "Batteriekapazität",
        "Charging power": "Ladeleistung",
        "Package size": "Verpackungsgröße",
        "Carton Gross Weight": "Kartonbruttogewicht",
        "Aromatherapist fragrance": "Aromatherapie-Duft",
    },
    
    # English to Arabic (template for future use)
    "ar": {
        "Material": "المادة",
        "Color": "اللون",
        "Product size": "حجم المنتج",
        "Product Size": "حجم المنتج",
        "Product name": "اسم المنتج",
        "Product type": "نوع المنتج",
        "Product Certification": "شهادة المنتج",
        "Product weight": "وزن المنتج",
        "Power": "الطاقة",
        "Capacity": "السعة",
        "Carton size": "حجم الكرتون",
        "Rated Voltage": "الجهد المقدر",
        "Package": "العبوة",
        "Packaging": "التعبئة",
        "Net/Gross Weight": "الوزن الصافي/الإجمالي",
        "Voltage": "الجهد",
        "Battery capacity": "سعة البطارية",
    },
}

SPEC_VALUES = {
    # English to Spanish
    "es": {
        # Colors
        "White": "Blanco",
        "Black": "Negro",
        "Red": "Rojo",
        "Blue": "Azul",
        "Green": "Verde",
        "Yellow": "Amarillo",
        "Pink": "Rosa",
        "Purple": "Morado",
        "Orange": "Naranja",
        "Gray": "Gris",
        "Grey": "Gris",
        "Brown": "Marrón",
        "Silver": "Plateado",
        "Gold": "Dorado",
        "Transparent": "Transparente",
        "Clear": "Transparente",
        " customize": " Personalizado",
        "customize": "personalizado",
        "OEM": "OEM",
        "ODM": "ODM",
        
        # Materials (including standalone)
        "Material": "Material",
        "Zinc alloy": "Aleación de zinc",
        "Stainless steel": "Acero inoxidable",
        "Zinc alloy/ Stainless steel": "Aleación de zinc / Acero inoxidable",
        "Zinc alloy/Stainless steel": "Aleación de zinc / Acero inoxidable",
        "Aluminum": "Aluminio",
        "Aluminium": "Aluminio",
        "Plastic": "Plástico",
        "ABS": "ABS",
        "PP": "PP",
        "Silicone": "Silicona",
        "Rubber": "Goma",
        "Leather": "Cuero",
        "PU leather": "Cuero PU",
        "Genuine leather": "Cuero genuino",
        "Metal": "Metal",
        "Iron": "Hierro",
        "Copper": "Cobre",
        "Brass": "Latón",
        "Wood": "Madera",
        "Bamboo": "Bambú",
        "Glass": "Vidrio",
        "Ceramic": "Cerámica",
        "Paper": "Papel",
        "Cardboard": "Cartón",
        "Cotton": "Algodón",
        "Linen": "Lino",
        "Nylon": "Nailon",
        "Polyester": "Poliéster",
        "PVC": "PVC",
        "TPE": "TPE",
        
        # Packaging
        "Cotton pads": "Almohadillas de algodón",
        "With white Cotton pads": "Con almohadillas de algodón blancas",
        "With white Almohadillas de algodón": "Con almohadillas de algodón blancas",
        "Gift box": "Caja de regalo",
        "Retail box": "Caja minorista",
        "Blister card": "Tarjeta blister",
        "Polybag": "Bolsa de plástico",
        "White box": "Caja blanca",
        "Color box": "Caja de color",
        "Display box": "Caja de exhibición",
        
        # Features
        "Eco-friendly": "Ecológico",
        "Rechargeable": "Recargable",
        "Portable": "Portátil",
        "Wireless": "Inalámbrico",
        "Waterproof": "Impermeable",
        "Adjustable": "Ajustable",
        "Foldable": "Plegable",
        "Extendable": "Extensible",
        "Removable": "Removible",
        "Washable": "Lavable",
        "Durable": "Duradero",
        "Lightweight": "Ligero",
        "Compact": "Compacto",
        
        # Certifications
        "CE": "CE",
        "RoHS": "RoHS",
        "FCC": "FCC",
        "FDA": "FDA",
        "LFGB": "LFGB",
        "ISO9001": "ISO9001",
        "BSCI": "BSCI",
        "SGS": "SGS",
        "CE/FCC/ROHS": "CE/FCC/RoHS",
        "CE / FCC / ROHS": "CE / FCC / RoHS",
        
        # Product Types & Names
        "Aroma Diffuser": "Difusor de Aroma",
        "Portable Fan": "Ventilador Portátil",
        "Badges": "Insignias",
        "YIWUYIMEI": "YIWUYIMEI",
        
        # Materials Extended
        "Zinc Alloy": "Aleación de Zinc",
        "Zinc Alloy + Wood": "Aleación de Zinc + Madera",
        "Aluminium + ABS": "Aluminio + ABS",
        "Aluminum + ABS": "Aluminio + ABS",
        "Lithium Battery": "Batería de Litio",
        
        # Technical
        "USB": "USB",
        "DC 5V": "DC 5V",
        "DC5~9V": "DC5~9V",
        "5V": "5V",
        "Inside 304, outside 201": "Interior 304, exterior 201",
        "inside 304,outside 201": "interior 304, exterior 201",
        
        # Fragrance options
        "Floral overflow (lemon flavor) | cologne (orange fragrance) | charm (olive flavor) | fragrance (lavender) | ocean (elegant)": "Desbordamiento floral (limón) | colonia (naranja) | encanto (oliva) | fragancia (lavanda) | océano (elegante)",
        
        # Features Extended
        "Asymmetric Light Source Design | Touch Dimming | 3 Lighting Modes | 3 Color Temperatures": "Diseño Asimétrico de Fuente de Luz | Atenuación Táctil | 3 Modos de Iluminación | 3 Temperaturas de Color",
        "LED(Touch dimming)": "LED (Atenuación táctil)",
        
        # Client requests
        "Base on Client Request": "Según Solicitud del Cliente",
        "Base on client request": "Según solicitud del cliente",
        
        # Colors Extended
        "Dark Grey": "Gris Oscuro",
        "Silver | Gold | Black": "Plateado | Dorado | Negro",
        "White / Pink / Purple": "Blanco / Rosa / Morado",
        
        # Materials Extended
        "Fabric": "Tela",
        "Fabric+zinc+ABS+PP": "Tela+zinc+ABS+PP",
        "Fabric + zinc": "Tela + zinc",
        "PET + PC + ABS": "PET + PC + ABS",
        "ABS+PP+steel+semiconductor": "ABS+PP+acero+semiconductor",
        "Inside 304 outside 201": "Interior 304 exterior 201",
        
        # Technical Values
        "USB": "USB",
        "Type-C": "Tipo-C",
        "DC 5V": "DC 5V",
        "DC5V": "DC5V",
        "DC 5V/ 2A": "DC 5V/ 2A",
        "DC 5V/2A": "DC 5V/2A",
        "DC 5V 2A": "DC 5V 2A",
        "DC 5V 1A": "DC 5V 1A",
        "DC5~9V": "DC5~9V",
        "5V": "5V",
        "5W": "5W",
        "10W": "10W",
        "24W": "24W",
        "3h/6h/9h": "3h/6h/9h",
        "5000mAh": "5000mAh",
        "3600mAh": "3600mAh",
        "1200 mAh": "1200 mAh",
        "2900-6000k": "2900-6000K",
        
        # Features/Descriptions
        "Portable Camping Fan": "Ventilador de Camping Portátil",
        "Fan 3rd gear": "Ventilador 3ra velocidad",
        "Fan 4rd gear": "Ventilador 4ta velocidad",
        "Three scents": "Tres fragancias",
        "One car vent clip": "Un clip de ventilación para coche",
        "one car vent clip": "un clip de ventilación para coche",
        
        # Scents
        "Orange": "Naranja",
        "Lemon": "Limón",
        "Olive": "Oliva",
        
        # Places/Origins
        "Guangdong,China": "Guangdong, China",
        "Guangdong, China": "Guangdong, China",
        
        # Product Types
        "PORTABLE": "PORTÁTIL",
        "Portable": "Portátil",
        
        # Product Names
        "Mini Silicone Car Diffuser Vent Clip": "Mini Difusor de Silicona para Coche con Clip de Ventilación",
        
        # Time/Duration
        "2 Months": "2 Meses",
        "Months": "Meses",
        
        # Sizes with units
        "21.6g": "21.6g",
        "78x18.5x42mm": "78x18.5x42mm",
        "110.5*110.5*50mm": "110.5*110.5*50mm",
        "110.5\*110.5\*50mm": "110.5*110.5*50mm",
        
        # Packaging Quantities
        "50 PCS/Carton": "50 uds/Cartón",
    },
    
    # English to German (template)
    "de": {
        "White": "Weiß",
        "Black": "Schwarz",
        "Red": "Rot",
        "Blue": "Blau",
        "Green": "Grün",
        "Yellow": "Gelb",
        "Pink": "Rosa",
        "Purple": "Lila",
        "Orange": "Orange",
        "Gray": "Grau",
        "Grey": "Grau",
        " customize": " Anpassbar",
        "customize": "anpassbar",
        "Zinc alloy": "Zinklegierung",
        "Stainless steel": "Edelstahl",
        "Plastic": "Kunststoff",
        "Cotton pads": "Baumwollpads",
    },
    
    # English to Arabic (template)
    "ar": {
        "White": "أبيض",
        "Black": "أسود",
        "Red": "أحمر",
        "Blue": "أزرق",
        "Green": "أخضر",
        "Yellow": "أصفر",
        " customize": " قابل للتخصيص",
        "Zinc alloy": "سبائك الزنك",
        "Stainless steel": "الفولاذ المقاوم للصدأ",
        "Cotton pads": "قطع قطنية",
    },
}


def translate_spec_segment(segment, target_lang):
    """Translate a single **Label:** value segment."""
    if target_lang not in SPEC_LABELS:
        return segment
    
    # Match pattern: **Label:** value
    match = re.match(r'^(\*\*)([^:]+):\s*\*\*\s*(.+)$', segment)
    if not match:
        # Try without extra ** after colon: **Label:** value
        match = re.match(r'^(\*\*)([^:]+):\s*(.+)$', segment)
        if not match:
            return segment
    
    prefix = match.group(1)  # **
    label = match.group(2).strip()  # Label
    value = match.group(3).strip()  # value
    
    # Translate label
    labels_map = SPEC_LABELS.get(target_lang, {})
    translated_label = labels_map.get(label, label)
    
    # Translate value (handle compound values like "Zinc alloy/ Stainless steel")
    values_map = SPEC_VALUES.get(target_lang, {})
    translated_value = value
    
    # Try to translate each part separated by "/", ",", or "|"
    for sep in ['/', ',', '|']:
        if sep in translated_value:
            parts = translated_value.split(sep)
            translated_parts = []
            for part in parts:
                part_stripped = part.strip()
                # Try exact match first
                if part_stripped in values_map:
                    translated_parts.append(values_map[part_stripped])
                else:
                    # Try case-insensitive match
                    for en_val, tr_val in values_map.items():
                        if part_stripped.lower() == en_val.lower():
                            translated_parts.append(tr_val)
                            break
                    else:
                        translated_parts.append(part_stripped)
            translated_value = (sep + ' ').join(translated_parts)
            break
    else:
        # Single value - try direct translation
        if value in values_map:
            translated_value = values_map[value]
        else:
            # Case-insensitive match
            for en_val, tr_val in values_map.items():
                if value.lower() == en_val.lower():
                    translated_value = tr_val
                    break
    
    return f"{prefix}{translated_label}:** {translated_value}"


def translate_spec_line(line, target_lang):
    """Translate a line containing one or more **Label:** value segments."""
    if target_lang not in SPEC_LABELS:
        return line
    
    # Check if line contains | separator (multiple specs in one line)
    if '|' in line:
        segments = line.split('|')
        translated_segments = []
        for segment in segments:
            translated_segment = translate_spec_segment(segment.strip(), target_lang)
            translated_segments.append(translated_segment)
        return ' | '.join(translated_segments)
    
    # Single segment
    # Match pattern: **Label:** value or **Label:** value / value
    match = re.match(r'^(\*\*)([^:]+):?\*\*\s*(.+)$', line)
    if not match:
        # Try matching lines without colon like "**With white Cotton pads"
        match = re.match(r'^(\*\*)(.+)$', line)
        if not match:
            return line
        prefix = match.group(1)  # **
        content = match.group(2).strip()
        
        # Try to translate the entire content as a value
        values_map = SPEC_VALUES.get(target_lang, {})
        translated_content = content
        if content in values_map:
            translated_content = values_map[content]
        else:
            for en_val, tr_val in values_map.items():
                if content.lower() == en_val.lower():
                    translated_content = tr_val
                    break
        return f"{prefix}{translated_content}"
    
    prefix = match.group(1)  # **
    label = match.group(2).strip()  # Label
    value = match.group(3).strip()  # value
    
    # Translate label
    labels_map = SPEC_LABELS.get(target_lang, {})
    translated_label = labels_map.get(label, label)
    
    # Translate value (handle compound values like "Zinc alloy/ Stainless steel")
    values_map = SPEC_VALUES.get(target_lang, {})
    translated_value = value
    
    # Try to translate each part separated by "/" or ","
    for sep in ['/', ',']:
        if sep in translated_value:
            parts = translated_value.split(sep)
            translated_parts = []
            for part in parts:
                part_stripped = part.strip()
                # Try exact match first
                if part_stripped in values_map:
                    translated_parts.append(values_map[part_stripped])
                else:
                    # Try case-insensitive match
                    for en_val, tr_val in values_map.items():
                        if part_stripped.lower() == en_val.lower():
                            translated_parts.append(tr_val)
                            break
                    else:
                        translated_parts.append(part_stripped)
            translated_value = (sep + ' ').join(translated_parts)
            break
    else:
        # Single value - try direct translation
        if value in values_map:
            translated_value = values_map[value]
        else:
            # Case-insensitive match
            for en_val, tr_val in values_map.items():
                if value.lower() == en_val.lower():
                    translated_value = tr_val
                    break
    
    return f"{prefix}{translated_label}:** {translated_value}"


def translate_product_file(src_path, dst_path, target_lang):
    """Translate a product markdown file."""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split front matter and body
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            front_matter = parts[1]
            body = parts[2]
            
            # Translate body (specifications)
            lines = body.strip().split('\n')
            translated_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('**'):
                    translated_line = translate_spec_line(line, target_lang)
                    translated_lines.append(translated_line)
                else:
                    translated_lines.append(line)
            
            translated_body = '\n'.join(translated_lines)
            translated_content = f"---{front_matter}---\n{translated_body}"
            
            with open(dst_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            return True
    
    # If no front matter or invalid format, copy as-is
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return False


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    
    source_lang = sys.argv[1]
    target_lang = sys.argv[2]
    
    if target_lang not in SPEC_LABELS:
        print(f"Error: No translations available for language '{target_lang}'")
        print(f"Available languages: {', '.join(SPEC_LABELS.keys())}")
        print("\nTo add a new language, edit SPEC_LABELS and SPEC_VALUES in this script.")
        sys.exit(1)
    
    base_dir = Path("content")
    src_dir = base_dir / source_lang / "products"
    dst_dir = base_dir / target_lang / "products"
    
    if not src_dir.exists():
        print(f"Error: Source directory not found: {src_dir}")
        sys.exit(1)
    
    if not dst_dir.exists():
        print(f"Error: Target directory not found: {dst_dir}")
        print(f"Please create the language structure first: {dst_dir}")
        sys.exit(1)
    
    # Find all product files
    src_files = list(src_dir.rglob("*.md"))
    translated = 0
    skipped = 0
    
    print(f"Translating {len(src_files)} product files from {source_lang} to {target_lang}...")
    print()
    
    for src_path in src_files:
        # Calculate relative path
        rel_path = src_path.relative_to(src_dir)
        dst_path = dst_dir / rel_path
        
        if dst_path.exists():
            # File exists, translate it
            if translate_product_file(src_path, dst_path, target_lang):
                translated += 1
                print(f"✓ {rel_path}")
            else:
                skipped += 1
                print(f"⚠ {rel_path} (no front matter)")
        else:
            # Target file doesn't exist - copy and translate
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            if translate_product_file(src_path, dst_path, target_lang):
                translated += 1
                print(f"✓ {rel_path} (created)")
            else:
                skipped += 1
                print(f"⚠ {rel_path} (created, no front matter)")
    
    print()
    print(f"Done! Translated: {translated}, Skipped: {skipped}")
    print()
    print(f"Language '{target_lang}' specification mappings used:")
    print(f"  Labels: {len(SPEC_LABELS[target_lang])}")
    print(f"  Values: {len(SPEC_VALUES[target_lang])}")


if __name__ == "__main__":
    main()
