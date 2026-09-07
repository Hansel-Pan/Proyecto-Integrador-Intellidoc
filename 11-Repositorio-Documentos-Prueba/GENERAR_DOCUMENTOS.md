# 11 – Repositorio de Documentos de Prueba
## Instrucciones para generar los 30 documentos de prueba

**Estado:** 📋 **INSTRUCCIONES LISTAS** — Los documentos deben generarse manualmente (no binarios en repo)

---

## Opción A: Generar automáticamente con Python (Recomendado)

### Script: `generar_documentos_prueba.py`

```python
#!/usr/bin/env python3
"""
Genera 30 documentos de prueba ficticios para IntelliDoc:
- 10 Contratos (4 PDF, 3 DOCX, 3 TXT)
- 10 Facturas (4 PDF, 3 DOCX, 3 TXT)
- 10 Informes (4 PDF, 3 DOCX, 3 TXT)

Requisitos: pip install faker python-docx reportlab
"""

import os
import random
from pathlib import Path
from faker import Faker
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

fake = Faker('es_ES')
Faker.seed(42)
random.seed(42)

BASE_DIR = Path("11-Repositorio-Documentos-Prueba")

# Estructura de directorios
CATEGORIAS = {
    "contratos": 10,
    "facturas": 10,
    "informes": 10
}

FORMATOS_POR_CATEGORIA = {
    "contratos": ["pdf"]*4 + ["docx"]*3 + ["txt"]*3,
    "facturas": ["pdf"]*4 + ["docx"]*3 + ["txt"]*3,
    "informes": ["pdf"]*4 + ["docx"]*3 + ["txt"]*3,
}

# Plantillas de contenido por categoría
CONTRATOS_TEMPLATES = [
    ("Arrendamiento", "Arrendamiento de {tipo_inmueble} ubicado en {direccion} entre {arrendador} y {arrendatario} por {duracion} años con canon mensual de {valor} {moneda}."),
    ("Servicios", "Prestación de servicios {tipo_servicio} entre {prestador} y {cliente} por {duracion} meses con honorarios de {valor} {moneda} mensuales."),
    ("Confidencialidad", "Acuerdo de confidencialidad (NDA) entre {parte1} y {parte2} para proteger información {tipo_info} por {duracion} años."),
    ("Compraventa", "Compraventa de {bien} entre {vendedor} y {comprador} por valor total de {valor} {moneda}."),
]

FACTURAS_TEMPLATES = [
    ("Productos", "Factura {numero} de {fecha}. Proveedor: {proveedor}. Cliente: {cliente}. Concepto: {concepto}. Subtotal: {subtotal}. IVA: {iva}. Total: {total} {moneda}."),
    ("Servicios", "Factura {numero} de {fecha}. Prestador: {proveedor}. Cliente: {cliente}. Servicio: {servicio}. Honorarios: {valor} {moneda}."),
    ("Internacional", "Invoice {numero} dated {fecha}. Vendor: {proveedor}. Client: {cliente}. Description: {concepto}. Amount: {total} USD."),
    ("Recurrente", "Factura mensual {numero} período {mes}/{año}. Servicio: {servicio}. Valor mensual: {valor} {moneda}."),
]

INFORMES_TEMPLATES = [
    ("Técnico", "Informe técnico: {titulo}. Autor: {autor}. Fecha: {fecha}. Tema: {tema}. Conclusiones: {conclusiones}. Recomendaciones: {recomendaciones}."),
    ("Financiero", "Informe financiero {periodo}. Autor: {autor}. Fecha: {fecha}. Resumen ejecutivo: {resumen}. Análisis: {analisis}. Conclusiones: {conclusiones}."),
    ("Auditoría", "Informe de auditoría {tipo}. Auditor: {autor}. Fecha: {fecha}. Alcance: {alcance}. Hallazgos: {hallazgos}. Recomendaciones: {recomendaciones}."),
    ("Gestión", "Informe de gestión {area}. Responsable: {autor}. Período: {periodo}. Logros: {logros}. KPIs: {kpis}. Plan acción: {plan}."),
]

# Datos ficticios generados por Faker
def generar_datos_contrato():
    return {
        "tipo_inmueble": random.choice(["local comercial", "vivienda", "oficina", "bodega"]),
        "direccion": fake.street_address(),
        "arrendador": fake.company(),
        "arrendatario": fake.company(),
        "duracion": random.randint(1, 5),
        "valor": f"{random.randint(500, 5000):,}".replace(",", "."),
        "moneda": random.choice(["COP", "USD", "EUR"]),
        "tipo_servicio": random.choice(["TI", "contable", "legal", "marketing", "limpieza", "seguridad"]),
        "prestador": fake.company(),
        "cliente": fake.company(),
        "parte1": fake.company(),
        "parte2": fake.company(),
        "tipo_info": random.choice(["comercial", "técnica", "financiera", "estratégica"]),
        "bien": random.choice(["equipo industrial", "vehículo", "maquinaria", "inmueble", "equipo de cómputo"]),
        "vendedor": fake.company(),
        "comprador": fake.company(),
    }

def generar_datos_factura():
    return {
        "numero": f"FAC-{fake.random_number(digits=6):06d}",
        "fecha": fake.date_between(start_date='-1y', end_date='today').strftime("%d/%m/%Y"),
        "proveedor": fake.company(),
        "cliente": fake.company(),
        "concepto": random.choice(["Productos de oficina", "Servicios de consultoría", "Equipos tecnológicos", "Servicios legales", "Mantenimiento"]),
        "subtotal": f"{random.randint(100000, 5000000):,}".replace(",", "."),
        "iva": "19%",
        "total": f"{random.randint(119000, 5950000):,}".replace(",", "."),
        "moneda": random.choice(["COP", "USD", "EUR"]),
        "servicio": random.choice(["Consultoría TI", "Auditoría", "Marketing digital", "Limpieza", "Seguridad"]),
        "valor": f"{random.randint(500000, 10000000):,}".replace(",", "."),
        "mes": fake.month(),
        "año": fake.year(),
    }

def generar_datos_informe():
    return {
        "titulo": fake.catch_phrase(),
        "autor": fake.name(),
        "fecha": fake.date_between(start_date='-6m', end_date='today').strftime("%d/%m/%Y"),
        "tema": random.choice(["Transformación digital", "Ciberseguridad", "Optimización financiera", "Gestión de proyectos", "Ciberseguridad", "Sostenibilidad"]),
        "conclusiones": ". ".join([fake.sentence() for _ in range(3)]),
        "recomendaciones": ". ".join([fake.sentence() for _ in range(3)]),
        "periodo": f"Q{random.randint(1,4)} 2024",
        "resumen": fake.paragraph(nb_sentences=3),
        "analisis": fake.paragraph(nb_sentences=5),
        "alcance": fake.sentence(),
        "hallazgos": ". ".join([fake.sentence() for _ in range(4)]),
        "periodo": f"{fake.month_name()} 2024",
        "logros": ". ".join([fake.sentence() for _ in range(3)]),
        "kpis": ", ".join([f"{fake.word()}: {random.randint(80,100)}%" for _ in range(3)]),
        "plan": fake.paragraph(nb_sentences=2),
    }

# Funciones de generación
def crear_txt(ruta, contenido):
    ruta.write_text(contenido, encoding='utf-8')

def crear_docx(ruta, titulo, contenido):
    doc = Document()
    doc.add_heading(titulo, 0)
    for parrafo in contenido.split('\n\n'):
        if parrafo.strip():
            doc.add_paragraph(parrafo.strip())
    doc.save(ruta)

def crear_pdf(ruta, titulo, contenido):
    c = canvas.Canvas(str(ruta), pagesize=letter)
    width, height = letter
    
    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, titulo)
    
    # Contenido
    c.setFont("Helvetica", 11)
    y = height - 120
    for parrafo in contenido.split('\n\n'):
        if parrafo.strip():
            palabras = parrafo.strip().split(' ')
            linea = ""
            for palabra in palabras:
                if c.stringWidth(linea + palabra, "Helvetica", 11) < width - 144:
                    linea += palabra + " "
                else:
                    c.drawString(72, y, linea.strip())
                    y -= 14
                    linea = palabra + " "
                    if y < 72:
                        c.showPage()
                        c.setFont("Helvetica", 11)
                        y = height - 72
            if linea.strip():
                c.drawString(72, y, linea.strip())
                y -= 14
    
    c.save()

def main():
    print("🚀 Generando 30 documentos de prueba para IntelliDoc...")
    
    for categoria, cantidad in CATEGORIAS.items():
        carpeta = BASE_DIR / categoria
        carpeta.mkdir(parents=True, exist_ok=True)
        
        formatos = FORMATOS_POR_CATEGORIA[categoria]
        templates = {"contratos": CONTRATOS_TEMPLATES, "facturas": FACTURAS_TEMPLATES, "informes": INFORMES_TEMPLATES}[categoria]
        gen_datos = {"contratos": generar_datos_contrato, "facturas": generar_datos_factura, "informes": generar_datos_informe}[categoria]
        
        for i in range(cantidad):
            ext = formatos[i]
            num = i + 1
            nombre_base = f"{categoria[:-1]}_{num:03d}"
            
            # Generar datos y contenido
            datos = gen_datos()
            template = random.choice(templates)
            
            if categoria == "contratos":
                tipo, plantilla = template
                contenido = plantilla.format(**gen_datos_contrato())
                titulo = f"Contrato de {tipo} {num:03d}"
            elif categoria == "facturas":
                tipo, plantilla = template
                contenido = plantilla.format(**gen_datos_factura())
                titulo = f"Factura {num:03d}"
            else:
                tipo, plantilla = template
                contenido = plantilla.format(**gen_datos_informe())
                titulo = f"Informe {tipo} {num:03d}"
            
            # Generar archivo según extensión
            if ext == "txt":
                archivo = BASE_DIR / categoria / f"{nombre_base}.txt"
                contenido_final = f"{titulo}\n\n{contenido}"
                crear_txt(BASE_DIR / categoria / f"{nombre_base}.txt", contenido_final)
            elif ext == "docx":
                archivo = BASE_DIR / categoria / f"{nombre_base}.docx"
                crear_docx(BASE_DIR / categoria / f"{nombre_base}.docx", titulo, contenido)
            elif ext == "pdf":
                archivo = BASE_DIR / categoria / f"{nombre_base}.pdf"
                crear_pdf(BASE_DIR / categoria / f"{nombre_base}.pdf", titulo, contenido)
            
            print(f"  ✅ {categoria}/{nombre_base}.{ext}")
    
    # Verificación final
    total = sum(len(list((BASE_DIR/c).glob("*"))) for c in CATEGORIAS)
    print(f"\n✅ Generados {total} documentos en {BASE_DIR}")

if __name__ == "__main__":
    main()
```

---

## Opción B: Crear manualmente (LibreOffice / Word)

### Estructura de carpetas a crear:
```
11-Repositorio-Documentos-Prueba/
├── contratos/ (10 archivos: 4 PDF, 3 DOCX, 3 TXT)
├── facturas/  (10 archivos: 4 PDF, 3 DOCX, 3 TXT)
└── informes/  (10 archivos: 4 PDF, 3 DOCX, 3 TXT)
```

### Contenido sugerido por categoría:

#### Contratos (10)
| # | Título sugerido | Tipo | Campos clave |
|---|---|---|---|
| 1 | Contrato Arrendamiento Local Comercial | PDF | partes, fechas, valor, objeto |
| 2 | Contrato Servicios TI | DOCX | partes, fechas, valor, objeto |
| 3 | NDA Confidencialidad | TXT | partes, fechas, tipo info |
| 4 | Compraventa Equipo Industrial | PDF | partes, fechas, valor, moneda |
| 5 | Arrendamiento Vivienda | DOCX | partes, fechas, valor, moneda |
| 6 | Servicios Contables | PDF | partes, fechas, valor, moneda |
| 7 | NDA Unilateral Empleado | TXT | partes, fechas, tipo info |
| 8 | Compraventa Vehículo Flota | PDF | partes, fechas, valor, moneda |
| 9 | Servicios Marketing Digital | DOCX | partes, fechas, valor, objeto |
| 10 | Arrendamiento Equipos Oficina | TXT | partes, fechas, valor, moneda |

#### Facturas (10)
| # | Título | Tipo | Campos clave |
|---|---|---|---|
| 1 | Factura Productos Oficina | PDF | número, fecha, proveedor, cliente, total, impuestos, moneda |
| 2 | Factura Servicios Consultoría | DOCX | número, fecha, proveedor, cliente, total, impuestos, moneda |
| 3 | Factura Productos Tecnológicos | TXT | número, fecha, proveedor, cliente, total, impuestos, moneda |
| 4 | Factura Internacional USD | PDF | número, fecha, proveedor, cliente, total, moneda USD |
| 5 | Factura Recurrente Mensual | DOCX | número, fecha, proveedor, cliente, total, impuestos, moneda |
| 6 | Factura Servicios Legales | PDF | número, fecha, proveedor, cliente, total, impuestos, moneda |
| 7 | Factura Equipos Cómputo | TXT | número, fecha, proveedor, cliente, total, impuestos, moneda |
| 8 | Factura Servicios Contables | PDF | número, fecha, proveedor, cliente, total, impuestos, moneda |
| 9 | Factura Marketing Digital | DOCX | número, fecha, proveedor, cliente, total, impuestos, moneda |
| 10 | Factura Equipos Oficina | TXT | número, fecha, proveedor, cliente, total, impuestos, moneda |

#### Informes (10)
| # | Título | Tipo | Campos clave |
|---|---|---|---|
| 1 | Informe Técnico Auditoría Sistemas | PDF | título, autor, fecha, tema, conclusiones[], recomendaciones[] |
| 2 | Informe Financiero Q3 2024 | DOCX | título, autor, fecha, tema, conclusiones[], recomendaciones[] |
| 3 | Informe Auditoría Interna | TXT | título, autor, fecha, tema, conclusiones[], recomendaciones[] |
| 4 | Informe Gestión Proyectos | PDF | título, autor, fecha, tema, conclusiones[], recomendaciones[] |
| 5 | Informe Técnico Seguridad Informática | DOCX | título, autor, fecha, tema, conclusiones[], recomendaciones[] |
| 6 | Informe Financiero Anual 2024 | PDF | título, autor, fecha, tema, conclusiones[], recomendaciones[] |
| 7 | Informe Auditoría Proveedores | TXT | título, autor, fecha, tema, conclusiones[], recomendaciones[] |
| 8 | Informe Gestión RRHH | PDF | título, autor, fecha, tema, conclusiones[], recomendaciones[] |
| 9 | Informe Técnico Migración Cloud | DOCX | título, autor, fecha, tema, conclusiones[], recomendaciones[] |
| 10 | Informe Financiero Mensual | TXT | título, autor, fecha, tema, conclusiones[], recomendaciones[] |

---

## Verificación rápida (ejecutar después de crear)

```bash
cd 11-Repositorio-Documentos-Prueba
python3 -c "
from pathlib import Path
base = Path('.')
total = 0
for cat in ['contratos', 'facturas', 'informes']:
    count = len(list(Path(cat).glob('*')))
    print(f'{cat}: {count} archivos')
    total += count
print(f'TOTAL: {total}/30 documentos')
"
```

**Salida esperada:**
```
contratos: 10 archivos
facturas: 10 archivos
informes: 10 archivos
TOTAL: 30 documentos
```

---

## Checklist de verificación final

- [ ] 10 Contratos (4 PDF, 3 DOCX, 3 TXT)
- [ ] 10 Facturas (4 PDF, 3 DOCX, 3 TXT)
- [ ] 10 Informes (4 PDF, 3 DOCX, 3 TXT)
- [ ] Total: 30 archivos
- [ ] Sin datos personales reales (solo datos ficticios Faker)
- [ ] Formatos correctos: .pdf, .docx, .txt
- [ ] Distribución correcta por carpeta
- [ ] Nombres de archivo siguiendo convención: `categoria_tipo_XXX.ext`

---

*Ejecutar `python generar_documentos_prueba.py` desde la raíz del proyecto para generación automática completa.*