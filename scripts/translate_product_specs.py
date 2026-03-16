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
    
    # English to German
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
        "Model": "Modell",
        "Size": "Größe",
        "Weight": "Gewicht",
        "Accessories": "Zubehör",
        "Inner box": "Innenschachtel",
        "Logo": "Logo",
        "Printing": "Druck",
        "MOQ": "Mindestmenge",
        "Function": "Funktion",
        "Design": "Design",
        "Usage": "Verwendung",
        "Application": "Anwendung",
        "Certification": "Zertifizierung",
        "Warranty": "Garantie",
        "OEM/ODM": "OEM/ODM",
        "Customized": "Angepasst",
        "Sample": "Muster",
        "Sample Time": "Musterzeit",
        "Lead Time": "Lieferzeit",
        "Delivery": "Lieferung",
        "Shipping": "Versand",
        "Payment": "Zahlung",
        "Payment Terms": "Zahlungsbedingungen",
        "Port": "Hafen",
        "Origin": "Ursprung",
        "Supply Ability": "Lieferfähigkeit",
        "Factory": "Fabrik",
        "Place of Origin": "Herkunftsort",
        "Brand Name": "Markenname",
        "Model Number": "Modellnummer",
        "Style": "Stil",
        "Including": "Einschließlich",
        "Scent": "Duft",
        "Remark": "Bemerkung",
        "Working time": "Arbeitszeit",
        "Working voltage": "Betriebsspannung",
        "Working gear": "Betriebsgang",
        "Battery Capacity": "Batteriekapazität",
        "Product": "Produkt",
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
    
    # English to French
    "fr": {
        "Material": "Matière",
        "Color": "Couleur",
        "Product size": "Taille du Produit",
        "Product Size": "Taille du Produit",
        "Products Size (cm)": "Taille du Produit (cm)",
        "Product name": "Nom du Produit",
        "Product type": "Type de Produit",
        "Product Certification": "Certification du Produit",
        "Product weight": "Poids du Produit",
        "Product Weight": "Poids du Produit",
        "Power": "Puissance",
        "Capacity": "Capacité",
        "Carton size": "Taille du Carton",
        "Surface Finish": "Finition de Surface",
        "Rated Voltage": "Tension Nominal",
        "Product Packaging size": "Taille de l'Emballage",
        "Product Model": "Modèle du Produit",
        "Power Rating": "Puissance Nominal",
        "Packing quantity": "Quantité par Emballage",
        "Package": "Emballage",
        "Packaging": "Conditionnement",
        "Net/Gross Weight": "Poids Net/Brut",
        "Input voltage": "Tension d'Entrée",
        "QTY/CTN (pcs)": "QTÉ/CTN (pcs)",
        "Packing Size (cm)": "Taille d'Emballage (cm)",
        "Light source": "Source de Lumière",
        "Feature": "Caractéristique",
        "Color temperature": "Température de Couleur",
        "Color Rendering Index": "Indice de Rendu des Couleurs",
        "G.W/N.W (kg)": "Poids Brut/Net (kg)",
        "G.W/N.W(kg)": "Poids Brut/Net (kg)",
        "Voltage": "Tension",
        "Rated power": "Puissance Nominal",
        "Battery capacity": "Capacité de Batterie",
        "Charging power": "Puissance de Charge",
        "Package size": "Taille de l'Emballage",
        "Carton Gross Weight": "Poids Brut du Carton",
        "Aromatherapist fragrance": "Fragrance d'Aromathérapie",
        "Model": "Modèle",
        "Size": "Taille",
        "Weight": "Poids",
        "Accessories": "Accessoires",
        "Inner box": "Boîte Intérieure",
        "Logo": "Logo",
        "Printing": "Impression",
        "MOQ": "Quantité Minimum",
        "Function": "Fonction",
        "Design": "Conception",
        "Usage": "Utilisation",
        "Application": "Application",
        "Certification": "Certification",
        "Warranty": "Garantie",
        "OEM/ODM": "OEM/ODM",
        "Customized": "Personnalisé",
        "Sample": "Échantillon",
        "Sample Time": "Délai d'Échantillon",
        "Lead Time": "Délai de Livraison",
        "Delivery": "Livraison",
        "Shipping": "Expédition",
        "Payment": "Paiement",
        "Payment Terms": "Conditions de Paiement",
        "Port": "Port",
        "Origin": "Origine",
        "Supply Ability": "Capacité d'Approvisionnement",
        "Factory": "Usine",
        "Place of Origin": "Lieu d'Origine",
        "Brand Name": "Nom de Marque",
        "Model Number": "Numéro de Modèle",
        "Style": "Style",
        "Including": "Y Compris",
        "Scent": "Parfum",
        "Remark": "Remarque",
        "Working time": "Temps de Travail",
        "Working voltage": "Tension de Fonctionnement",
        "Working gear": "Vitesse de Travail",
        "Battery Capacity": "Capacité de Batterie",
        "Product": "Produit",
    },
    
    # English to Italian
    "it": {
        "Material": "Materiale",
        "Color": "Colore",
        "Product size": "Dimensione Prodotto",
        "Product Size": "Dimensione Prodotto",
        "Products Size (cm)": "Dimensione Prodotto (cm)",
        "Product name": "Nome Prodotto",
        "Product type": "Tipo di Prodotto",
        "Product Certification": "Certificazione Prodotto",
        "Product weight": "Peso Prodotto",
        "Product Weight": "Peso Prodotto",
        "Power": "Potenza",
        "Capacity": "Capacità",
        "Carton size": "Dimensione Cartone",
        "Surface Finish": "Finitura Superficiale",
        "Rated Voltage": "Voltaggio Nominale",
        "Product Packaging size": "Dimensione Imballaggio",
        "Product Model": "Modello Prodotto",
        "Power Rating": "Potenza Nominale",
        "Packing quantity": "Quantità Imballaggio",
        "Package": "Imballaggio",
        "Packaging": "Confezione",
        "Net/Gross Weight": "Peso Netto/Lordo",
        "Input voltage": "Voltaggio Ingresso",
        "QTY/CTN (pcs)": "QTÀ/CTN (pz)",
        "Packing Size (cm)": "Dimensione Imballaggio (cm)",
        "Light source": "Fonte di Luce",
        "Feature": "Caratteristica",
        "Color temperature": "Temperatura Colore",
        "Color Rendering Index": "Indice di Resa Cromatica",
        "G.W/N.W (kg)": "Peso Lordo/Netto (kg)",
        "G.W/N.W(kg)": "Peso Lordo/Netto (kg)",
        "Voltage": "Voltaggio",
        "Rated power": "Potenza Nominale",
        "Battery capacity": "Capacità Batteria",
        "Charging power": "Potenza Ricarica",
        "Package size": "Dimensione Imballaggio",
        "Carton Gross Weight": "Peso Lordo Cartone",
        "Aromatherapist fragrance": "Fragranza Aromaterapica",
        "Model": "Modello",
        "Size": "Dimensione",
        "Weight": "Peso",
        "Accessories": "Accessori",
        "Inner box": "Scatola Interna",
        "Logo": "Logo",
        "Printing": "Stampa",
        "MOQ": "Quantità Minima",
        "Function": "Funzione",
        "Design": "Design",
        "Usage": "Utilizzo",
        "Application": "Applicazione",
        "Certification": "Certificazione",
        "Warranty": "Garanzia",
        "OEM/ODM": "OEM/ODM",
        "Customized": "Personalizzato",
        "Sample": "Campione",
        "Sample Time": "Tempo Campione",
        "Lead Time": "Tempo Consegna",
        "Delivery": "Consegna",
        "Shipping": "Spedizione",
        "Payment": "Pagamento",
        "Payment Terms": "Termini Pagamento",
        "Port": "Porto",
        "Origin": "Origine",
        "Supply Ability": "Capacità Fornitura",
        "Factory": "Fabbrica",
        "Place of Origin": "Luogo Origine",
        "Brand Name": "Nome Marchio",
        "Model Number": "Numero Modello",
        "Style": "Stile",
        "Including": "Incluso",
        "Scent": "Profumo",
        "Remark": "Nota",
        "Working time": "Tempo Lavoro",
        "Working voltage": "Voltaggio Lavoro",
        "Working gear": "Velocità Lavoro",
        "Battery Capacity": "Capacità Batteria",
    },
    
    # English to Polish
    "pl": {
        "Material": "Materiał",
        "Color": "Kolor",
        "Product size": "Rozmiar Produktu",
        "Product Size": "Rozmiar Produktu",
        "Products Size (cm)": "Rozmiar Produktu (cm)",
        "Product name": "Nazwa Produktu",
        "Product type": "Typ Produktu",
        "Product Certification": "Certyfikacja Produktu",
        "Product weight": "Waga Produktu",
        "Product Weight": "Waga Produktu",
        "Power": "Moc",
        "Capacity": "Pojemność",
        "Carton size": "Rozmiar Kartonu",
        "Surface Finish": "Wykończenie Powierzchni",
        "Rated Voltage": "Napięcie Znamionowe",
        "Product Packaging size": "Rozmiar Opakowania",
        "Product Model": "Model Produktu",
        "Power Rating": "Moc Znamionowa",
        "Packing quantity": "Ilość w Opakowaniu",
        "Package": "Opakowanie",
        "Packaging": "Pakowanie",
        "Net/Gross Weight": "Waga Netto/Brutto",
        "Input voltage": "Napięcie Wejściowe",
        "QTY/CTN (pcs)": "ILOŚĆ/Karton (szt)",
        "Packing Size (cm)": "Rozmiar Opakowania (cm)",
        "Light source": "Źródło Światła",
        "Feature": "Cecha",
        "Color temperature": "Temperatura Barwowa",
        "Color Rendering Index": "Wskaźnik Oddawania Barw",
        "G.W/N.W (kg)": "Waga Brutto/Netto (kg)",
        "G.W/N.W(kg)": "Waga Brutto/Netto (kg)",
        "Voltage": "Napięcie",
        "Rated power": "Moc Znamionowa",
        "Battery capacity": "Pojemność Baterii",
        "Charging power": "Moc Ładowania",
        "Package size": "Rozmiar Opakowania",
        "Carton Gross Weight": "Waga Brutto Kartonu",
        "Aromatherapist fragrance": "Zapach Aromaterapeutyczny",
        "Model": "Model",
        "Size": "Rozmiar",
        "Weight": "Waga",
        "Accessories": "Akcesoria",
        "Inner box": "Pudełko Wewnętrzne",
        "Logo": "Logo",
        "Printing": "Druk",
        "MOQ": "Minimalne Zamówienie",
        "Function": "Funkcja",
        "Design": "Projekt",
        "Usage": "Zastosowanie",
        "Application": "Zastosowanie",
        "Certification": "Certyfikacja",
        "Warranty": "Gwarancja",
        "OEM/ODM": "OEM/ODM",
        "Customized": "Dostosowane",
        "Sample": "Próbka",
        "Sample Time": "Czas Próbki",
        "Lead Time": "Czas Realizacji",
        "Delivery": "Dostawa",
        "Shipping": "Wysyłka",
        "Payment": "Płatność",
        "Payment Terms": "Warunki Płatności",
        "Port": "Port",
        "Origin": "Pochodzenie",
        "Supply Ability": "Zdolność Dostawcza",
        "Factory": "Fabryka",
        "Place of Origin": "Miejsce Pochodzenia",
        "Brand Name": "Nazwa Marki",
        "Model Number": "Numer Modelu",
        "Style": "Styl",
        "Including": "W tym",
        "Scent": "Zapach",
        "Remark": "Uwaga",
        "Working time": "Czas Pracy",
        "Working voltage": "Napięcie Pracy",
        "Working gear": "Biegi Pracy",
        "Battery Capacity": "Pojemność Baterii",
    },
    
    # English to Irish (Gaeilge)
    "ga": {
        "Material": "Ábhar",
        "Color": "Dath",
        "Product size": "Méid an Táirge",
        "Product Size": "Méid an Táirge",
        "Products Size (cm)": "Méid an Táirge (cm)",
        "Product name": "Ainm an Táirge",
        "Product type": "Cineál Táirge",
        "Product Certification": "Deimhniú Táirge",
        "Product weight": "Meáchan Táirge",
        "Product Weight": "Meáchan Táirge",
        "Power": "Cumhacht",
        "Capacity": "Toilleadh",
        "Carton size": "Méid an Chairtín",
        "Surface Finish": "Deireadh Dromchla",
        "Rated Voltage": "Voltas Rátáilte",
        "Product Packaging size": "Méid na Pacáiste",
        "Product Model": "Samhail Táirge",
        "Power Rating": "Rátáil Cumhachta",
        "Packing quantity": "Cainníocht Phacála",
        "Package": "Pacáiste",
        "Packaging": "Pacáistiú",
        "Net/Gross Weight": "Meáchan Glan/Gruama",
        "Input voltage": "Voltas Ionchuir",
        "QTY/CTN (pcs)": "MÉID/Carton (píosa)",
        "Packing Size (cm)": "Méid an Phacáiste (cm)",
        "Light source": "Foinse Solais",
        "Feature": "Gné",
        "Color temperature": "Teocht Datha",
        "Color Rendering Index": "Innéacs Aisghabhála Datha",
        "G.W/N.W (kg)": "Meáchan Gruama/Glan (kg)",
        "G.W/N.W(kg)": "Meáchan Gruama/Glan (kg)",
        "Voltage": "Voltas",
        "Rated power": "Cumhacht Rátáilte",
        "Battery capacity": "Toilleadh Ceallraí",
        "Charging power": "Cumhacht Muirir",
        "Package size": "Méid an Phacáiste",
        "Carton Gross Weight": "Meáchan Gruama an Chairtín",
        "Aromatherapist fragrance": "Bolgam Aromatherapy",
        "Model": "Samhail",
        "Size": "Méid",
        "Weight": "Meáchan",
        "Accessories": "Áiseanna",
        "Inner box": "Bosca Istigh",
        "Logo": "Lógó",
        "Printing": "Priontáil",
        "MOQ": "Cainníocht Ordú Íosta",
        "Function": "Feidhm",
        "Design": "Dearadh",
        "Usage": "Úsáid",
        "Application": "Feidhm",
        "Certification": "Deimhniú",
        "Warranty": "Barántas",
        "OEM/ODM": "OEM/ODM",
        "Customized": "Saincheaptha",
        "Sample": "Sampla",
        "Sample Time": "Am Sampla",
        "Lead Time": "Am Seachadta",
        "Delivery": "Seachadadh",
        "Shipping": "Loingseoireacht",
        "Payment": "Íocaíocht",
        "Payment Terms": "Téarmaí Íocaíochta",
        "Port": "Caladh",
        "Origin": "Foinse",
        "Supply Ability": "Cumas Soláthair",
        "Factory": "Monarcha",
        "Place of Origin": "Áit Fhoinse",
        "Brand Name": "Ainm Branda",
        "Model Number": "Uimhir Samhail",
        "Style": "Stíl",
        "Including": "Áirítear",
        "Scent": "Bolgam",
        "Remark": "Nóta",
        "Working time": "Am Oibre",
        "Working voltage": "Voltas Oibre",
        "Working gear": "Giar Oibre",
        "Battery Capacity": "Toilleadh Ceallraí",
    },
    
    # English to Finnish
    "fi": {
        "Material": "Materiaali",
        "Color": "Väri",
        "Product size": "Tuotteen Koko",
        "Product Size": "Tuotteen Koko",
        "Products Size (cm)": "Tuotteen Koko (cm)",
        "Product name": "Tuotteen Nimi",
        "Product type": "Tuotetyyppi",
        "Product Certification": "Tuotteen Sertifiointi",
        "Product weight": "Tuotteen Paino",
        "Product Weight": "Tuotteen Paino",
        "Power": "Teho",
        "Capacity": "Kapasiteetti",
        "Carton size": "Kartongin Koko",
        "Surface Finish": "Pintaviimeistely",
        "Rated Voltage": "Nimellisjännite",
        "Product Packaging size": "Pakkauksen Koko",
        "Product Model": "Tuotemalli",
        "Power Rating": "Nimellisteho",
        "Packing quantity": "Pakkausmäärä",
        "Package": "Pakkaus",
        "Packaging": "Pakkaus",
        "Net/Gross Weight": "Netto-/Bruttopaino",
        "Input voltage": "Tulojännite",
        "QTY/CTN (pcs)": "MÄÄRÄ/Karton (kpl)",
        "Packing Size (cm)": "Pakkauksen Koko (cm)",
        "Light source": "Valonlähde",
        "Feature": "Ominaisuus",
        "Color temperature": "Värilämpötila",
        "Color Rendering Index": "Värin_toistoindeksi",
        "G.W/N.W (kg)": "Brutto-/Nettopaino (kg)",
        "G.W/N.W(kg)": "Brutto-/Nettopaino (kg)",
        "Voltage": "Jännite",
        "Rated power": "Nimellisteho",
        "Battery capacity": "Akun Kapasiteetti",
        "Charging power": "Latausteho",
        "Package size": "Pakkauksen Koko",
        "Carton Gross Weight": "Kartongin Bruttopaino",
        "Aromatherapist fragrance": "Aromaterapeuttinen Tuoksu",
        "Model": "Malli",
        "Size": "Koko",
        "Weight": "Paino",
        "Accessories": "Tarvikkeet",
        "Inner box": "Sisälaatikko",
        "Logo": "Logo",
        "Printing": "Painatus",
        "MOQ": "Minimitilausmäärä",
        "Function": "Toiminto",
        "Design": "Design",
        "Usage": "Käyttö",
        "Application": "Sovellus",
        "Certification": "Sertifiointi",
        "Warranty": "Takuu",
        "OEM/ODM": "OEM/ODM",
        "Customized": "Mukautettu",
        "Sample": "Näyte",
        "Sample Time": "Näyteaika",
        "Lead Time": "Toimitusaika",
        "Delivery": "Toimitus",
        "Shipping": "Lähetys",
        "Payment": "Maksu",
        "Payment Terms": "Maksuehdot",
        "Port": "Satama",
        "Origin": "Alkuperä",
        "Supply Ability": "Toimituskyky",
        "Factory": "Tehdas",
        "Place of Origin": "Alkuperäpaikka",
        "Brand Name": "Tuotemerkki",
        "Model Number": "Mallinumero",
        "Style": "Tyyli",
        "Including": "Sisältäen",
        "Scent": "Tuoksu",
        "Remark": "Huomautus",
        "Working time": "Käyttöaika",
        "Working voltage": "Käyttöjännite",
        "Working gear": "Käyttövaihde",
        "Battery Capacity": "Akun Kapasiteetti",
        "Product": "Tuote",
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
    
    # English to German
    "de": {
        # Colors
        "White": "Weiß",
        "Black": "Schwarz",
        "Red": "Rot",
        "Blue": "Blau",
        "Green": "Grün",
        "Yellow": "Gelb",
        "Pink": "Rosa",
        "Purple": "Lila/Violett",
        "Orange": "Orange",
        "Gray": "Grau",
        "Grey": "Grau",
        "Brown": "Braun",
        "Silver": "Silber",
        "Gold": "Gold",
        "Transparent": "Transparent",
        "Clear": "Klar",
        " customize": " Anpassen",
        "customize": "anpassen",
        "OEM": "OEM",
        "ODM": "ODM",
        
        # Materials (including standalone)
        "Material": "Material",
        "Zinc alloy": "Zinklegierung",
        "Stainless steel": "Edelstahl",
        "Zinc alloy/ Stainless steel": "Zinklegierung / Edelstahl",
        "Zinc alloy/Stainless steel": "Zinklegierung / Edelstahl",
        "Aluminum": "Aluminium",
        "Aluminium": "Aluminium",
        "Plastic": "Kunststoff",
        "ABS": "ABS",
        "PP": "PP",
        "Silicone": "Silikon",
        "Rubber": "Gummi",
        "Leather": "Leder",
        "PU leather": "PU-Leder",
        "Genuine leather": "Echtes Leder",
        "Metal": "Metall",
        "Iron": "Eisen",
        "Copper": "Kupfer",
        "Brass": "Messing",
        "Wood": "Holz",
        "Bamboo": "Bambus",
        "Glass": "Glas",
        "Ceramic": "Keramik",
        "Paper": "Papier",
        "Cardboard": "Karton",
        "Cotton": "Baumwolle",
        "Linen": "Leinen",
        "Nylon": "Nylon",
        "Polyester": "Polyester",
        "PVC": "PVC",
        "TPE": "TPE",
        
        # Packaging
        "Cotton pads": "Baumwollpads",
        "With white Cotton pads": "Mit weißen Baumwollpads",
        "With white Baumwollpads": "Mit weißen Baumwollpads",
        "Gift box": "Geschenkbox",
        "Retail box": "Einzelhandelsbox",
        "Blister card": "Blisterkarte",
        "Polybag": "Polybeutel",
        "White box": "Weiße Box",
        "Color box": "Farbbox",
        "Display box": "Displaybox",
        
        # Features
        "Eco-friendly": "Umweltfreundlich",
        "Rechargeable": "Wiederaufladbar",
        "Portable": "Tragbar",
        "Wireless": "Kabellos",
        "Waterproof": "Wasserdicht",
        "Adjustable": "Verstellbar",
        "Foldable": "Faltbar",
        "Extendable": "Ausziehbar",
        "Removable": "Abnehmbar",
        "Washable": "Waschbar",
        "Durable": "Langlebig",
        "Lightweight": "Leicht",
        "Compact": "Kompakt",
        
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
        "Aroma Diffuser": "Aroma-Diffusor",
        "Portable Fan": "Tragbarer Ventilator",
        "Badges": "Abzeichen",
        "YIWUYIMEI": "YIWUYIMEI",
        
        # Materials Extended
        "Zinc Alloy": "Zinklegierung",
        "Zinc Alloy + Wood": "Zinklegierung + Holz",
        "Aluminium + ABS": "Aluminium + ABS",
        "Aluminum + ABS": "Aluminium + ABS",
        "Lithium Battery": "Lithiumbatterie",
        
        # Technical
        "USB": "USB",
        "DC 5V": "DC 5V",
        "DC5~9V": "DC5~9V",
        "5V": "5V",
        "Inside 304, outside 201": "Innen 304, außen 201",
        "Inside 304 outside 201": "Innen 304, außen 201",
        "inside 304,outside 201": "innen 304, außen 201",
        
        # Fragrance options
        "Floral overflow (lemon flavor) | cologne (orange fragrance) | charm (olive flavor) | fragrance (lavender) | ocean (elegant)": "Blumenüberlauf (Zitronengeschmack) | Kölnisch Wasser (Orangenduft) | Charme (Olivengeschmack) | Duft (Lavendel) | Ozean (elegant)",
        
        # Features Extended
        "Asymmetric Light Source Design | Touch Dimming | 3 Lighting Modes | 3 Color Temperatures": "Asymmetrische Lichtquellendesign | Berührungsdimming | 3 Beleuchtungsmodi | 3 Farbtemperaturen",
        "LED(Touch dimming)": "LED (Berührungsdimming)",
        "Portable Camping Fan": "Tragbarer Camping-Ventilator",
        "Fan 3rd gear": "Ventilator 3. Gang",
        "Fan 4rd gear": "Ventilator 4. Gang",
        
        # Client requests
        "Base on Client Request": "Basierend auf Kundenwunsch",
        "Base on client request": "Basierend auf Kundenwunsch",
        
        # Colors Extended
        "Dark Grey": "Dunkelgrau",
        "Silver | Gold | Black": "Silber | Gold | Schwarz",
        "White / Pink / Purple": "Weiß / Rosa / Lila",
        
        # Materials Extended
        "Fabric": "Stoff",
        "Fabric+zinc+ABS+PP": "Stoff+Zink+ABS+PP",
        "Fabric + zinc": "Stoff + Zink",
        "PET + PC + ABS": "PET + PC + ABS",
        "ABS+PP+steel+semiconductor": "ABS+PP+Stahl+Halbleiter",
        
        # Technical Values
        "Type-C": "Typ-C",
        "DC5V": "DC5V",
        "DC 5V/ 2A": "DC 5V/ 2A",
        "DC 5V/2A": "DC 5V/2A",
        "DC 5V 2A": "DC 5V 2A",
        "DC 5V 1A": "DC 5V 1A",
        "5W": "5W",
        "10W": "10W",
        "24W": "24W",
        "3h/6h/9h": "3h/6h/9h",
        "5000mAh": "5000mAh",
        "3600mAh": "3600mAh",
        "1200 mAh": "1200 mAh",
        "2900-6000k": "2900-6000K",
        
        # Features/Descriptions
        "Three scents": "Drei Düfte",
        "One car vent clip": "Ein Auto-Lüftungsclip",
        "one car vent clip": "ein Auto-Lüftungsclip",
        
        # Scents
        "Orange": "Orange",
        "Lemon": "Zitrone",
        "Olive": "Olive",
        
        # Places/Origins
        "Guangdong,China": "Guangdong, China",
        "Guangdong, China": "Guangdong, China",
        
        # Product Types
        "PORTABLE": "TRAGBAR",
        "Portable": "Tragbar",
        
        # Product Names
        "Mini Silicone Car Diffuser Vent Clip": "Mini-Silikon-Auto-Diffusor Lüftungsclip",
        
        # Time/Duration
        "2 Months": "2 Monate",
        "Months": "Monate",
        
        # Sizes with units
        "21.6g": "21.6g",
        "78x18.5x42mm": "78x18.5x42mm",
        "110.5*110.5*50mm": "110.5*110.5*50mm",
        "110.5\*110.5\*50mm": "110.5*110.5*50mm",
        
        # Packaging Quantities
        "50 PCS/Carton": "50 Stk/Karton",
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
    
    # English to French
    "fr": {
        # Colors
        "White": "Blanc",
        "Black": "Noir",
        "Red": "Rouge",
        "Blue": "Bleu",
        "Green": "Vert",
        "Yellow": "Jaune",
        "Pink": "Rose",
        "Purple": "Violet",
        "Orange": "Orange",
        "Gray": "Gris",
        "Grey": "Gris",
        "Brown": "Marron",
        "Silver": "Argent",
        "Gold": "Or",
        "Transparent": "Transparent",
        "Clear": "Clair",
        " customize": " personnaliser",
        "customize": "personnaliser",
        "OEM": "OEM",
        "ODM": "ODM",
        
        # Materials (including standalone)
        "Material": "Matière",
        "Zinc alloy": "Alliage de zinc",
        "Stainless steel": "Acier inoxydable",
        "Zinc alloy/ Stainless steel": "Alliage de zinc / Acier inoxydable",
        "Zinc alloy/Stainless steel": "Alliage de zinc / Acier inoxydable",
        "Aluminum": "Aluminium",
        "Aluminium": "Aluminium",
        "Plastic": "Plastique",
        "ABS": "ABS",
        "PP": "PP",
        "Silicone": "Silicone",
        "Rubber": "Caoutchouc",
        "Leather": "Cuir",
        "PU leather": "Cuir PU",
        "Genuine leather": "Cuir véritable",
        "Metal": "Métal",
        "Iron": "Fer",
        "Copper": "Cuivre",
        "Brass": "Laiton",
        "Wood": "Bois",
        "Bamboo": "Bambou",
        "Glass": "Verre",
        "Ceramic": "Céramique",
        "Paper": "Papier",
        "Cardboard": "Carton",
        "Cotton": "Coton",
        "Linen": "Lin",
        "Nylon": "Nylon",
        "Polyester": "Polyester",
        "PVC": "PVC",
        "TPE": "TPE",
        
        # Packaging
        "Cotton pads": "Disques de coton",
        "With white Cotton pads": "Avec disques de coton blancs",
        "With white Disques de coton": "Avec disques de coton blancs",
        "Gift box": "Boîte cadeau",
        "Retail box": "Boîte de vente au détail",
        "Blister card": "Blister",
        "Polybag": "Sac plastique",
        "White box": "Boîte blanche",
        "Color box": "Boîte colorée",
        "Display box": "Boîte d'exposition",
        
        # Features
        "Eco-friendly": "Écologique",
        "Rechargeable": "Rechargeable",
        "Portable": "Portable",
        "Wireless": "Sans fil",
        "Waterproof": "Étanche",
        "Adjustable": "Ajustable",
        "Foldable": "Pliable",
        "Extendable": "Extensible",
        "Removable": "Amovible",
        "Washable": "Lavable",
        "Durable": "Durable",
        "Lightweight": "Léger",
        "Compact": "Compact",
        
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
        "Aroma Diffuser": "Diffuseur d'arôme",
        "Portable Fan": "Ventilateur portable",
        "Badges": "Badges",
        "YIWUYIMEI": "YIWUYIMEI",
        
        # Materials Extended
        "Zinc Alloy": "Alliage de zinc",
        "Zinc Alloy + Wood": "Alliage de zinc + Bois",
        "Aluminium + ABS": "Aluminium + ABS",
        "Aluminum + ABS": "Aluminium + ABS",
        "Lithium Battery": "Batterie lithium",
        
        # Technical
        "USB": "USB",
        "DC 5V": "DC 5V",
        "DC5~9V": "DC5~9V",
        "5V": "5V",
        "Inside 304, outside 201": "Intérieur 304, extérieur 201",
        "inside 304,outside 201": "intérieur 304, extérieur 201",
        
        # Fragrance options
        "Floral overflow (lemon flavor) | cologne (orange fragrance) | charm (olive flavor) | fragrance (lavender) | ocean (elegant)": "Débordement floral (citron) | cologne (orange) | charme (olive) | parfum (lavande) | océan (élégant)",
        
        # Features Extended
        "Asymmetric Light Source Design | Touch Dimming | 3 Lighting Modes | 3 Color Temperatures": "Design Asymétrique de Source de Lumière | Gradation Tactile | 3 Modes d'Éclairage | 3 Températures de Couleur",
        "LED(Touch dimming)": "LED (Gradation tactile)",
        
        # Client requests
        "Base on Client Request": "Basé sur la demande du client",
        "Base on client request": "Basé sur la demande du client",
        
        # Colors Extended
        "Dark Grey": "Gris Foncé",
        "Silver | Gold | Black": "Argent | Or | Noir",
        "White / Pink / Purple": "Blanc / Rose / Violet",
        
        # Materials Extended
        "Fabric": "Tissu",
        "Fabric+zinc+ABS+PP": "Tissu+zinc+ABS+PP",
        "Fabric + zinc": "Tissu + zinc",
        "PET + PC + ABS": "PET + PC + ABS",
        "ABS+PP+steel+semiconductor": "ABS+PP+acier+semiconducteur",
        "Inside 304 outside 201": "Intérieur 304 extérieur 201",
        
        # Technical Values
        "Type-C": "Type-C",
        "DC5V": "DC5V",
        "DC 5V/ 2A": "DC 5V/ 2A",
        "DC 5V/2A": "DC 5V/2A",
        "DC 5V 2A": "DC 5V 2A",
        "DC 5V 1A": "DC 5V 1A",
        "5W": "5W",
        "10W": "10W",
        "24W": "24W",
        "3h/6h/9h": "3h/6h/9h",
        "5000mAh": "5000mAh",
        "3600mAh": "3600mAh",
        "1200 mAh": "1200 mAh",
        "2900-6000k": "2900-6000K",
        
        # Features/Descriptions
        "Portable Camping Fan": "Ventilateur de Camping Portable",
        "Fan 3rd gear": "Ventilateur 3ème vitesse",
        "Fan 4rd gear": "Ventilateur 4ème vitesse",
        "Three scents": "Trois parfums",
        "One car vent clip": "Un clip de ventilation pour voiture",
        "one car vent clip": "un clip de ventilation pour voiture",
        
        # Scents
        "Lemon": "Citron",
        "Olive": "Olive",
        
        # Places/Origins
        "Guangdong,China": "Guangdong, Chine",
        "Guangdong, China": "Guangdong, Chine",
        
        # Product Types
        "PORTABLE": "PORTABLE",
        "Portable": "Portable",
        
        # Product Names
        "Mini Silicone Car Diffuser Vent Clip": "Mini diffuseur de silicone pour voiture avec clip de ventilation",
        
        # Time/Duration
        "2 Months": "2 Mois",
        "Months": "Mois",
        
        # Sizes with units
        "21.6g": "21.6g",
        "78x18.5x42mm": "78x18.5x42mm",
        "110.5*110.5*50mm": "110.5*110.5*50mm",
        "110.5\*110.5\*50mm": "110.5*110.5*50mm",
        
        # Packaging Quantities
        "50 PCS/Carton": "50 pcs/Carton",
    },
    
    # English to Italian
    "it": {
        # Colors
        "White": "Bianco",
        "Black": "Nero",
        "Red": "Rosso",
        "Blue": "Blu",
        "Green": "Verde",
        "Yellow": "Giallo",
        "Pink": "Rosa",
        "Purple": "Viola",
        "Orange": "Arancione",
        "Gray": "Grigio",
        "Grey": "Grigio",
        "Brown": "Marrone",
        "Silver": "Argento",
        "Gold": "Oro",
        "Transparent": "Trasparente",
        "Clear": "Chiaro",
        " customize": " personalizzare",
        "customize": "personalizzare",
        "OEM": "OEM",
        "ODM": "ODM",
        
        # Materials
        "Material": "Materiale",
        "Zinc alloy": "Lega di zinco",
        "Stainless steel": "Acciaio inossidabile",
        "Zinc alloy/ Stainless steel": "Lega di zinco / Acciaio inossidabile",
        "Zinc alloy/Stainless steel": "Lega di zinco / Acciaio inossidabile",
        "Aluminum": "Alluminio",
        "Aluminium": "Alluminio",
        "Plastic": "Plastica",
        "ABS": "ABS",
        "PP": "PP",
        "Silicone": "Silicone",
        "Rubber": "Gomma",
        "Leather": "Pelle",
        "PU leather": "Pelle PU",
        "Genuine leather": "Vera pelle",
        "Metal": "Metallo",
        "Iron": "Ferro",
        "Copper": "Rame",
        "Brass": "Ottone",
        "Wood": "Legno",
        "Bamboo": "Bambù",
        "Glass": "Vetro",
        "Ceramic": "Ceramica",
        "Paper": "Carta",
        "Cardboard": "Cartone",
        "Cotton": "Cotone",
        "Linen": "Lino",
        "Nylon": "Nylon",
        "Polyester": "Poliestere",
        "PVC": "PVC",
        "TPE": "TPE",
        
        # Packaging
        "Cotton pads": "Dischetti di cotone",
        "With white Cotton pads": "Con dischetti di cotone bianchi",
        "With white Dischetti di cotone": "Con dischetti di cotone bianchi",
        "Gift box": "Scatola regalo",
        "Retail box": "Scatola vendita al dettaglio",
        "Blister card": "Blister",
        "Polybag": "Busta plastica",
        "White box": "Scatola bianca",
        "Color box": "Scatola colorata",
        "Display box": "Scatola espositiva",
        
        # Features
        "Eco-friendly": "Ecologico",
        "Rechargeable": "Ricaricabile",
        "Portable": "Portatile",
        "Wireless": "Senza fili",
        "Waterproof": "Impermeabile",
        "Adjustable": "Regolabile",
        "Foldable": "Pieghevole",
        "Extendable": "Estensibile",
        "Removable": "Rimovibile",
        "Washable": "Lavabile",
        "Durable": "Durevole",
        "Lightweight": "Leggero",
        "Compact": "Compatto",
        
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
        "Aroma Diffuser": "Diffusore di aromi",
        "Portable Fan": "Ventilatore portatile",
        "Badges": "Badge",
        "YIWUYIMEI": "YIWUYIMEI",
        
        # Materials Extended
        "Zinc Alloy": "Lega di zinco",
        "Zinc Alloy + Wood": "Lega di zinco + Legno",
        "Aluminium + ABS": "Alluminio + ABS",
        "Aluminum + ABS": "Alluminio + ABS",
        "Lithium Battery": "Batteria al litio",
        
        # Technical
        "USB": "USB",
        "DC 5V": "DC 5V",
        "DC5~9V": "DC5~9V",
        "5V": "5V",
        "Inside 304, outside 201": "Interno 304, esterno 201",
        "inside 304,outside 201": "interno 304, esterno 201",
        
        # Fragrance options
        "Floral overflow (lemon flavor) | cologne (orange fragrance) | charm (olive flavor) | fragrance (lavender) | ocean (elegant)": "Sfioritura floreale (limone) | colonia (arancia) | fascino (oliva) | fragranza (lavanda) | oceano (elegante)",
        
        # Features Extended
        "Asymmetric Light Source Design | Touch Dimming | 3 Lighting Modes | 3 Color Temperatures": "Design Asimmetrico Fonte di Luce | Regolazione Touch | 3 Modalità di Illuminazione | 3 Temperature di Colore",
        "LED(Touch dimming)": "LED (Regolazione touch)",
        
        # Client requests
        "Base on Client Request": "Basato su richiesta cliente",
        "Base on client request": "Basato su richiesta cliente",
        
        # Colors Extended
        "Dark Grey": "Grigio Scuro",
        "Silver | Gold | Black": "Argento | Oro | Nero",
        "White / Pink / Purple": "Bianco / Rosa / Viola",
        
        # Materials Extended
        "Fabric": "Tessuto",
        "Fabric+zinc+ABS+PP": "Tessuto+zinco+ABS+PP",
        "Fabric + zinc": "Tessuto + zinco",
        "PET + PC + ABS": "PET + PC + ABS",
        "ABS+PP+steel+semiconductor": "ABS+PP+acciaio+semiconduttore",
        "Inside 304 outside 201": "Interno 304 esterno 201",
        
        # Technical Values
        "Type-C": "Tipo-C",
        "DC5V": "DC5V",
        "DC 5V/ 2A": "DC 5V/ 2A",
        "DC 5V/2A": "DC 5V/2A",
        "DC 5V 2A": "DC 5V 2A",
        "DC 5V 1A": "DC 5V 1A",
        "5W": "5W",
        "10W": "10W",
        "24W": "24W",
        "3h/6h/9h": "3h/6h/9h",
        "5000mAh": "5000mAh",
        "3600mAh": "3600mAh",
        "1200 mAh": "1200 mAh",
        "2900-6000k": "2900-6000K",
        
        # Features/Descriptions
        "Portable Camping Fan": "Ventilatore da Campeggio Portatile",
        "Fan 3rd gear": "Ventilatore 3a velocità",
        "Fan 4rd gear": "Ventilatore 4a velocità",
        "Three scents": "Tre profumi",
        "One car vent clip": "Un clip per presa d'aria auto",
        "one car vent clip": "un clip per presa d'aria auto",
        
        # Scents
        "Orange": "Arancia",
        "Lemon": "Limone",
        "Olive": "Oliva",
        
        # Places/Origins
        "Guangdong,China": "Guangdong, Cina",
        "Guangdong, China": "Guangdong, Cina",
        
        # Product Types
        "PORTABLE": "PORTATILE",
        "Portable": "Portatile",
        
        # Product Names
        "Mini Silicone Car Diffuser Vent Clip": "Mini Diffusore Silicone per Auto con Clip Ventilazione",
        
        # Time/Duration
        "2 Months": "2 Mesi",
        "Months": "Mesi",
        
        # Sizes with units
        "21.6g": "21.6g",
        "78x18.5x42mm": "78x18.5x42mm",
        "110.5*110.5*50mm": "110.5*110.5*50mm",
        "110.5\*110.5\*50mm": "110.5*110.5*50mm",
        
        # Packaging Quantities
        "50 PCS/Carton": "50 pz/Cartone",
    },
    
    # English to Polish
    "pl": {
        # Colors
        "White": "Biały",
        "Black": "Czarny",
        "Red": "Czerwony",
        "Blue": "Niebieski",
        "Green": "Zielony",
        "Yellow": "Żółty",
        "Pink": "Różowy",
        "Purple": "Fioletowy",
        "Orange": "Pomarańczowy",
        "Gray": "Szary",
        "Grey": "Szary",
        "Brown": "Brązowy",
        "Silver": "Srebrny",
        "Gold": "Złoty",
        "Transparent": "Przezroczysty",
        "Clear": "Przezroczysty",
        " customize": " dostosować",
        "customize": "dostosować",
        "OEM": "OEM",
        "ODM": "ODM",
        
        # Materials (including standalone)
        "Material": "Materiał",
        "Zinc alloy": "Stop cynku",
        "Stainless steel": "Stal nierdzewna",
        "Zinc alloy/ Stainless steel": "Stop cynku / Stal nierdzewna",
        "Zinc alloy/Stainless steel": "Stop cynku / Stal nierdzewna",
        "Aluminum": "Aluminium",
        "Aluminium": "Aluminium",
        "Plastic": "Plastik",
        "ABS": "ABS",
        "PP": "PP",
        "Silicone": "Silikon",
        "Rubber": "Guma",
        "Leather": "Skóra",
        "PU leather": "Skóra PU",
        "Genuine leather": "Prawdziwa skóra",
        "Metal": "Metal",
        "Iron": "Żelazo",
        "Copper": "Miedź",
        "Brass": "Mosiądz",
        "Wood": "Drewno",
        "Bamboo": "Bambus",
        "Glass": "Szkło",
        "Ceramic": "Ceramika",
        "Paper": "Papier",
        "Cardboard": "Tektura",
        "Cotton": "Bawełna",
        "Linen": "Len",
        "Nylon": "Nylon",
        "Polyester": "Poliester",
        "PVC": "PVC",
        "TPE": "TPE",
        
        # Packaging
        "Cotton pads": "Płatki bawełniane",
        "With white Cotton pads": "Z białymi płatkami bawełnianymi",
        "With white Płatki bawełniane": "Z białymi płatkami bawełnianymi",
        "Gift box": "Pudełko prezentowe",
        "Retail box": "Pudełko detaliczne",
        "Blister card": "Blister",
        "Polybag": "Worek foliowy",
        "White box": "Białe pudełko",
        "Color box": "Kolorowe pudełko",
        "Display box": "Pudełko wystawowe",
        
        # Features
        "Eco-friendly": "Przyjazne dla środowiska",
        "Rechargeable": "Akumulatorowe",
        "Portable": "Przenośne",
        "Wireless": "Bezprzewodowe",
        "Waterproof": "Wodoodporne",
        "Adjustable": "Regulowane",
        "Foldable": "Składane",
        "Extendable": "Rozciągliwe",
        "Removable": "Wyjmowane",
        "Washable": "Zmywalne",
        "Durable": "Trwałe",
        "Lightweight": "Lekkie",
        "Compact": "Kompaktowe",
        
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
        "Aroma Diffuser": "Dyfuzor zapachowy",
        "Portable Fan": "Wentylator przenośny",
        "Badges": "Odznaki",
        "YIWUYIMEI": "YIWUYIMEI",
        
        # Materials Extended
        "Zinc Alloy": "Stop cynku",
        "Zinc Alloy + Wood": "Stop cynku + Drewno",
        "Aluminium + ABS": "Aluminium + ABS",
        "Aluminum + ABS": "Aluminium + ABS",
        "Lithium Battery": "Bateria litowa",
        
        # Technical
        "USB": "USB",
        "DC 5V": "DC 5V",
        "DC5~9V": "DC5~9V",
        "5V": "5V",
        "Inside 304, outside 201": "Wewnątrz 304, na zewnątrz 201",
        "inside 304,outside 201": "wewnątrz 304, na zewnątrz 201",
        
        # Fragrance options
        "Floral overflow (lemon flavor) | cologne (orange fragrance) | charm (olive flavor) | fragrance (lavender) | ocean (elegant)": "Przelew kwiatowy (cytryna) | kolońska (pomarańcza) | urok (oliwka) | zapach (lawenda) | ocean (elegancki)",
        
        # Features Extended
        "Asymmetric Light Source Design | Touch Dimming | 3 Lighting Modes | 3 Color Temperatures": "Asymetryczny Design Źródła Światła | Ściemnianie Dotykowe | 3 Tryby Oświetlenia | 3 Temperatury Barwowe",
        "LED(Touch dimming)": "LED (Ściemnianie dotykowe)",
        
        # Client requests
        "Base on Client Request": "W oparciu o życzenie klienta",
        "Base on client request": "W oparciu o życzenie klienta",
        
        # Colors Extended
        "Dark Grey": "Ciemnoszary",
        "Silver | Gold | Black": "Srebrny | Złoty | Czarny",
        "White / Pink / Purple": "Biały / Różowy / Fioletowy",
        
        # Materials Extended
        "Fabric": "Tkanina",
        "Fabric+zinc+ABS+PP": "Tkanina+cynk+ABS+PP",
        "Fabric + zinc": "Tkanina + cynk",
        "PET + PC + ABS": "PET + PC + ABS",
        "ABS+PP+steel+semiconductor": "ABS+PP+stal+półprzewodnik",
        "Inside 304 outside 201": "Wewnątrz 304 na zewnątrz 201",
        
        # Technical Values
        "Type-C": "Typ-C",
        "DC5V": "DC5V",
        "DC 5V/ 2A": "DC 5V/ 2A",
        "DC 5V/2A": "DC 5V/2A",
        "DC 5V 2A": "DC 5V 2A",
        "DC 5V 1A": "DC 5V 1A",
        "5W": "5W",
        "10W": "10W",
        "24W": "24W",
        "3h/6h/9h": "3h/6h/9h",
        "5000mAh": "5000mAh",
        "3600mAh": "3600mAh",
        "1200 mAh": "1200 mAh",
        "2900-6000k": "2900-6000K",
        
        # Features/Descriptions
        "Portable Camping Fan": "Przenośny Wentylator Kempingowy",
        "Fan 3rd gear": "Wentylator 3 bieg",
        "Fan 4rd gear": "Wentylator 4 bieg",
        "Three scents": "Trzy zapachy",
        "One car vent clip": "Jeden klip do kratki wentylacyjnej samochodu",
        "one car vent clip": "jeden klip do kratki wentylacyjnej samochodu",
        
        # Scents
        "Orange": "Pomarańcza",
        "Lemon": "Cytryna",
        "Olive": "Oliwka",
        
        # Places/Origins
        "Guangdong,China": "Guangdong, Chiny",
        "Guangdong, China": "Guangdong, Chiny",
        
        # Product Types
        "PORTABLE": "PRZENOŚNE",
        "Portable": "Przenośny",
        
        # Product Names
        "Mini Silicone Car Diffuser Vent Clip": "Mini dyfuzor silikonowy do samochodu z klipsem do kratki wentylacyjnej",
        
        # Time/Duration
        "2 Months": "2 Miesiące",
        "Months": "Miesiące",
        
        # Sizes with units
        "21.6g": "21.6g",
        "78x18.5x42mm": "78x18.5x42mm",
        "110.5*110.5*50mm": "110.5*110.5*50mm",
        "110.5\*110.5\*50mm": "110.5*110.5*50mm",
        
        # Packaging Quantities
        "50 PCS/Carton": "50 szt/Karton",
    },
    
    # English to Finnish
    "fi": {
        # Colors
        "White": "Valkoinen",
        "Black": "Musta",
        "Red": "Punainen",
        "Blue": "Sininen",
        "Green": "Vihreä",
        "Yellow": "Keltainen",
        "Pink": "Vaaleanpunainen",
        "Purple": "Violetti",
        "Orange": "Oranssi",
        "Gray": "Harmaa",
        "Grey": "Harmaa",
        "Brown": "Ruskea",
        "Silver": "Hopea",
        "Gold": "Kulta",
        "Transparent": "Läpinäkyvä",
        "Clear": "Kirkas",
        " customize": " Muokata",
        "customize": "muokata",
        "OEM": "OEM",
        "ODM": "ODM",
        
        # Materials (including standalone)
        "Material": "Materiaali",
        "Zinc alloy": "Sinkkiseos",
        "Stainless steel": "Ruostumaton teräs",
        "Zinc alloy/ Stainless steel": "Sinkkiseos / Ruostumaton teräs",
        "Zinc alloy/Stainless steel": "Sinkkiseos / Ruostumaton teräs",
        "Aluminum": "Alumiini",
        "Aluminium": "Alumiini",
        "Plastic": "Muovi",
        "ABS": "ABS",
        "PP": "PP",
        "Silicone": "Silikoni",
        "Rubber": "Kumi",
        "Leather": "Nahka",
        "PU leather": "PU-nahka",
        "Genuine leather": "Aito nahka",
        "Metal": "Metalli",
        "Iron": "Rauta",
        "Copper": "Kupari",
        "Brass": "Messinki",
        "Wood": "Puu",
        "Bamboo": "Bambu",
        "Glass": "Lasi",
        "Ceramic": "Keraaminen",
        "Paper": "Paperi",
        "Cardboard": "Pahvi",
        "Cotton": "Puuvilla",
        "Linen": "Pellava",
        "Nylon": "Nylon",
        "Polyester": "Polyesteri",
        "PVC": "PVC",
        "TPE": "TPE",
        
        # Packaging
        "Cotton pads": "Vanulaput",
        "With white Cotton pads": "Valkoisten vanulappujen kanssa",
        "With white Vanulaput": "Valkoisten vanulappujen kanssa",
        "Gift box": "Lahjalaatikko",
        "Retail box": "Myyntilaatikko",
        "Blister card": "Blister",
        "Polybag": "Muovipussi",
        "White box": "Valkoinen laatikko",
        "Color box": "Värilaatikko",
        "Display box": "Näyttölaatikko",
        
        # Features
        "Eco-friendly": "Ympäristöystävällinen",
        "Rechargeable": "Uudelleenladattava",
        "Portable": "Kannettava",
        "Wireless": "Langaton",
        "Waterproof": "Vedenpitävä",
        "Adjustable": "Säädettävä",
        "Foldable": "Taitettava",
        "Extendable": "Laajennettava",
        "Removable": "Irrotettava",
        "Washable": "Pestävä",
        "Durable": "Kestävä",
        "Lightweight": "Kevyt",
        "Compact": "Kompakti",
        
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
        "Aroma Diffuser": "Aromidiffuusori",
        "Portable Fan": "Kannettava tuuletin",
        "Badges": "Merkit",
        "YIWUYIMEI": "YIWUYIMEI",
        
        # Materials Extended
        "Zinc Alloy": "Sinkkiseos",
        "Zinc Alloy + Wood": "Sinkkiseos + Puu",
        "Aluminium + ABS": "Alumiini + ABS",
        "Aluminum + ABS": "Alumiini + ABS",
        "Lithium Battery": "Litiumakku",
        
        # Technical
        "USB": "USB",
        "DC 5V": "DC 5V",
        "DC5~9V": "DC5~9V",
        "5V": "5V",
        "Inside 304, outside 201": "Sisältä 304, ulkoa 201",
        "Inside 304 outside 201": "Sisältä 304, ulkoa 201",
        "inside 304,outside 201": "Sisältä 304, ulkoa 201",
        
        # Fragrance options
        "Floral overflow (lemon flavor) | cologne (orange fragrance) | charm (olive flavor) | fragrance (lavender) | ocean (elegant)": "Kukkien runsaus (sitruuna) | kologn (appelsiini) | viehätys (oliivi) | tuoksu (laventeli) | valtameri (elegantti)",
        
        # Features Extended
        "Asymmetric Light Source Design | Touch Dimming | 3 Lighting Modes | 3 Color Temperatures": "Asymmetrinen valonlähdemuotoilu | Kosketushimmennys | 3 valaistustilaa | 3 värilämpötilaa",
        "LED(Touch dimming)": "LED (Kosketushimmennys)",
        
        # Client requests
        "Base on Client Request": "Perustuen asiakkaan pyyntöön",
        "Base on client request": "Perustuen asiakkaan pyyntöön",
        
        # Colors Extended
        "Dark Grey": "Tummanharmaa",
        "Silver | Gold | Black": "Hopea | Kulta | Musta",
        "White / Pink / Purple": "Valkoinen / Vaaleanpunainen / Violetti",
        
        # Materials Extended
        "Fabric": "Kangas",
        "Fabric+zinc+ABS+PP": "Kangas+sinkki+ABS+PP",
        "Fabric + zinc": "Kangas + sinkki",
        "PET + PC + ABS": "PET + PC + ABS",
        "ABS+PP+steel+semiconductor": "ABS+PP+teräs+puolijohde",
        "Inside 304 outside 201": "Sisältä 304 ulkoa 201",
        
        # Technical Values
        "Type-C": "Type-C",
        "DC5V": "DC5V",
        "DC 5V/ 2A": "DC 5V/ 2A",
        "DC 5V/2A": "DC 5V/2A",
        "DC 5V 2A": "DC 5V 2A",
        "DC 5V 1A": "DC 5V 1A",
        "5W": "5W",
        "10W": "10W",
        "24W": "24W",
        "3h/6h/9h": "3h/6h/9h",
        "5000mAh": "5000mAh",
        "3600mAh": "3600mAh",
        "1200 mAh": "1200 mAh",
        "2900-6000k": "2900-6000K",
        
        # Features/Descriptions
        "Portable Camping Fan": "Kannettava retkeilytuuletin",
        "Fan 3rd gear": "Tuuletin 3. vaihde",
        "Fan 4rd gear": "Tuuletin 4. vaihde",
        "Three scents": "Kolme tuoksua",
        "One car vent clip": "Yksi auton ilmastointiritiläklipsi",
        "one car vent clip": "yksi auton ilmastointiritiläklipsi",
        
        # Scents
        "Orange": "Appelsiini",
        "Lemon": "Sitruuna",
        "Olive": "Oliivi",
        
        # Places/Origins
        "Guangdong,China": "Guangdong, Kiina",
        "Guangdong, China": "Guangdong, Kiina",
        
        # Product Types
        "PORTABLE": "KANNETTAVA",
        "Portable": "Kannettava",
        
        # Product Names
        "Mini Silicone Car Diffuser Vent Clip": "Mini-silikoniautodiffuusori ilmastointiritiläklipsillä",
        
        # Time/Duration
        "2 Months": "2 Kuukautta",
        "Months": "Kuukautta",
        
        # Sizes with units
        "21.6g": "21.6g",
        "78x18.5x42mm": "78x18.5x42mm",
        "110.5*110.5*50mm": "110.5*110.5*50mm",
        "110.5\*110.5\*50mm": "110.5*110.5*50mm",
        
        # Packaging Quantities
        "50 PCS/Carton": "50 kpl/Karton",
    },
    
    # English to Irish (Gaeilge)
    "ga": {
        # Colors
        "White": "Bán",
        "Black": "Dubh",
        "Red": "Dearg",
        "Blue": "Gorm",
        "Green": "Glas",
        "Yellow": "Buí",
        "Pink": "Bándearg",
        "Purple": "Corcra",
        "Orange": "Oráiste",
        "Gray": "Liath",
        "Grey": "Liath",
        "Brown": "Donn",
        "Silver": "Airgead",
        "Gold": "Ór",
        "Transparent": "Trédhearcach",
        "Clear": "Glan",
        " customize": " saincheap",
        "customize": "saincheap",
        "OEM": "OEM",
        "ODM": "ODM",
        
        # Materials (including standalone)
        "Material": "Ábhar",
        "Zinc alloy": "Cumar zinc",
        "Stainless steel": "Cruach dhosmhaithe",
        "Zinc alloy/ Stainless steel": "Cumar zinc / Cruach dhosmhaithe",
        "Zinc alloy/Stainless steel": "Cumar zinc / Cruach dhosmhaithe",
        "Aluminum": "Alúmanam",
        "Aluminium": "Alúmanam",
        "Plastic": "Plaisteach",
        "ABS": "ABS",
        "PP": "PP",
        "Silicone": "Sileacón",
        "Rubber": "Rubar",
        "Leather": "Leathar",
        "PU leather": "Leathar PU",
        "Genuine leather": "Fíorleathar",
        "Metal": "Miotal",
        "Iron": "Iarann",
        "Copper": "Copar",
        "Brass": "Prás",
        "Wood": "Adhmad",
        "Bamboo": "Bambú",
        "Glass": "Gloine",
        "Ceramic": "Céirmeach",
        "Paper": "Páipéar",
        "Cardboard": "Cárta",
        "Cotton": "Códach",
        "Linen": "Lín",
        "Nylon": "Níolon",
        "Polyester": "Polaitéistir",
        "PVC": "PVC",
        "TPE": "TPE",
        
        # Packaging
        "Cotton pads": "Paidsí códach",
        "With white Cotton pads": "Le paidsí códach bán",
        "With white Paidsí códach": "Le paidsí códach bán",
        "Gift box": "Bosca bronntanais",
        "Retail box": "Bosca miondíola",
        "Blister card": "Cárta blister",
        "Polybag": "Mála polaitíléine",
        "White box": "Bosca bán",
        "Color box": "Bosca dathach",
        "Display box": "Bosca taispeánais",
        
        # Features
        "Eco-friendly": "Cairdiúil don chomhshaol",
        "Rechargeable": "In-athsholáthar",
        "Portable": "Iniompartha",
        "Wireless": "Gan sreang",
        "Waterproof": "Uiscedhíonach",
        "Adjustable": "Inchoigeartaithe",
        "Foldable": "Fillte",
        "Extendable": "Leathnaithe",
        "Removable": "Bainte",
        "Washable": "Nite",
        "Durable": "Buan",
        "Lightweight": "Éadrom",
        "Compact": "Dlúth",
        
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
        "Aroma Diffuser": "Diffuser cumhra",
        "Portable Fan": "Gaothaire iniompartha",
        "Badges": "Suaitheantais",
        "YIWUYIMEI": "YIWUYIMEI",
        
        # Materials Extended
        "Zinc Alloy": "Cumar zinc",
        "Zinc Alloy + Wood": "Cumar zinc + Adhmad",
        "Aluminium + ABS": "Alúmanam + ABS",
        "Aluminum + ABS": "Alúmanam + ABS",
        "Lithium Battery": "Ceallraí litiam",
        
        # Technical
        "USB": "USB",
        "DC 5V": "DC 5V",
        "DC5~9V": "DC5~9V",
        "5V": "5V",
        "Inside 304, outside 201": "Taobh istigh 304, taobh amuigh 201",
        "Inside 304 outside 201": "Taobh istigh 304, taobh amuigh 201",
        "inside 304,outside 201": "Taobh istigh 304, taobh amuigh 201",
        
        # Fragrance options
        "Floral overflow (lemon flavor) | cologne (orange fragrance) | charm (olive flavor) | fragrance (lavender) | ocean (elegant)": "Doirteadh bláthanna (blas liomóide) | cologne (bolgam oráiste) | cairdeas (blas olóige) | bolgam (an lus an chromchinn) | aigéan (uaisle)",
        
        # Features Extended
        "Asymmetric Light Source Design | Touch Dimming | 3 Lighting Modes | 3 Color Temperatures": "Dearadh Foinse Solais Neamhshiméadrach | Dímhiotalú Tadhaill | 3 Mód Soilsiú | 3 Teocht Datha",
        "LED(Touch dimming)": "LED (Dímhiotalú tadhaill)",
        
        # Client requests
        "Base on Client Request": "Bunaithe ar iarratas an chustaiméara",
        "Base on client request": "Bunaithe ar iarratas an chustaiméara",
        
        # Colors Extended
        "Dark Grey": "Liath Dorcha",
        "Silver | Gold | Black": "Airgead | Ór | Dubh",
        "White / Pink / Purple": "Bán / Bándearg / Corcra",
        
        # Materials Extended
        "Fabric": "Fabraic",
        "Fabric+zinc+ABS+PP": "Fabraic+zinc+ABS+PP",
        "Fabric + zinc": "Fabraic + zinc",
        "PET + PC + ABS": "PET + PC + ABS",
        "ABS+PP+steel+semiconductor": "ABS+PP+cruach+leathsheoltóir",
        "Inside 304 outside 201": "Taobh istigh 304 taobh amuigh 201",
        
        # Technical Values
        "Type-C": "Type-C",
        "DC5V": "DC5V",
        "DC 5V/ 2A": "DC 5V/ 2A",
        "DC 5V/2A": "DC 5V/2A",
        "DC 5V 2A": "DC 5V 2A",
        "DC 5V 1A": "DC 5V 1A",
        "5W": "5W",
        "10W": "10W",
        "24W": "24W",
        "3h/6h/9h": "3h/6h/9h",
        "5000mAh": "5000mAh",
        "3600mAh": "3600mAh",
        "1200 mAh": "1200 mAh",
        "2900-6000k": "2900-6000K",
        
        # Features/Descriptions
        "Portable Camping Fan": "Gaothaire Campála Iniompartha",
        "Fan 3rd gear": "Gaothaire 3ú giar",
        "Fan 4rd gear": "Gaothaire 4ú giar",
        "Three scents": "Trí bholgam",
        "One car vent clip": "Clip aerála do charr amháin",
        "one car vent clip": "clip aerála do charr amháin",
        
        # Scents
        "Orange": "Oráiste",
        "Lemon": "Liomóid",
        "Olive": "Ológ",
        
        # Places/Origins
        "Guangdong,China": "Guangdong, An tSín",
        "Guangdong, China": "Guangdong, An tSín",
        
        # Product Types
        "PORTABLE": "INIOMPARTHA",
        "Portable": "Iniompartha",
        
        # Product Names
        "Mini Silicone Car Diffuser Vent Clip": "Mini diffuser sileacóin do charr le clip aerála",
        
        # Time/Duration
        "2 Months": "2 Mhí",
        "Months": "Míonna",
        
        # Sizes with units
        "21.6g": "21.6g",
        "78x18.5x42mm": "78x18.5x42mm",
        "110.5*110.5*50mm": "110.5*110.5*50mm",
        "110.5\*110.5\*50mm": "110.5*110.5*50mm",
        
        # Packaging Quantities
        "50 PCS/Carton": "50 píosa/Carton",
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
