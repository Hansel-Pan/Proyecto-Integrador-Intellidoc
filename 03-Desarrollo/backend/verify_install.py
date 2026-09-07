#!/usr/bin/env python
"""Script de verificación de instalación - IntelliDoc Backend"""
import sys
import shutil
import subprocess

def run(cmd, description):
    print(f"\n[TEST] {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("  OK")
            return True
        else:
            print(f"  FALLO: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print("  TIMEOUT")
        return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def test_import(module, description):
    print(f"\n[TEST] Import {module} ({description})...")
    try:
        __import__(module)
        print("  OK")
        return True
    except Exception as e:
        print(f"  FALLO: {e}")
        return False

def main():
    print("=" * 50)
    print("  Verificación de instalación - IntelliDoc")
    print("=" * 50)

    if sys.version_info[:2] not in ((3, 11), (3, 12)):
        print("\n[ERROR] Este backend requiere Python 3.11 o 3.12.")
        return 1
    
    all_ok = True
    
    # 1. Verificar Python y pip
    all_ok &= run([sys.executable, "--version"], "Python version")
    all_ok &= run([sys.executable, "-m", "pip", "--version"], "Pip version")
    
    # 2. Verificar imports críticos
    critical_imports = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("sqlalchemy", "SQLAlchemy"),
        ("pydantic", "Pydantic"),
        ("pydantic_settings", "Pydantic Settings"),
        ("jose", "Python-JOSE"),
        ("passlib", "Passlib"),
        ("pymysql", "PyMySQL"),
        ("alembic", "Alembic"),
        ("pdfplumber", "PDFPlumber"),
        ("docx", "Python-DOCX"),
        ("sentence_transformers", "Sentence Transformers"),
        ("chromadb", "ChromaDB"),
        ("httpx", "HTTPX"),
        ("google.generativeai", "Google Generative AI"),
        ("aiofiles", "Aiofiles"),
        ("numpy", "NumPy"),
        ("scipy", "SciPy"),
    ]
    
    for module, desc in critical_imports:
        all_ok &= test_import(module, desc)
    
    # 3. Verificar ChromaDB persistente
    print("\n[TEST] ChromaDB PersistentClient...")
    try:
        import chromadb
        from chromadb.config import Settings as ChromaSettings
        from pathlib import Path
        verify_path = Path(".verify_chroma")
        client = chromadb.PersistentClient(path=str(verify_path), settings=ChromaSettings(anonymized_telemetry=False))
        collection = client.get_or_create_collection("test_verify")
        collection.add(ids=["1"], documents=["test"], embeddings=[[0.1]*384])
        results = collection.query(query_embeddings=[[0.1]*384], n_results=1)
        assert len(results["ids"][0]) == 1
        client.delete_collection("test_verify")
        shutil.rmtree(verify_path, ignore_errors=True)
        print("  OK - PersistentClient funcional")
    except Exception as e:
        print(f"  FALLO: {e}")
        all_ok = False
    
    # 4. Verificar app.main
    print("\n[TEST] App FastAPI import...")
    try:
        from app.main import app
        print("  OK")
    except Exception as e:
        print(f"  FALLO: {e}")
        all_ok = False
    
    # 5. Verificar rutas
    print("\n[TEST] Rutas API registradas...")
    try:
        from app.main import app
        routes = [r.path for r in app.routes if r.path.startswith("/api")]
        print(f"  OK - {len(routes)} endpoints registrados")
        for r in sorted(routes):
            print(f"    - {r}")
    except Exception as e:
        print(f"  FALLO: {e}")
        all_ok = False
    
    # Resumen
    print("\n" + "=" * 50)
    if all_ok:
        print("  TODAS LAS PRUEBAS PASARON")
        print("  El backend está listo para ejecutarse:")
        print("    uvicorn app.main:app --reload --port 8000")
    else:
        print("  ALGUNAS PRUEBAS FALLARON")
        print("  Revisa los errores arriba")
    print("=" * 50)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())