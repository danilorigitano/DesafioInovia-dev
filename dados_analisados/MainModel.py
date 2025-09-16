"""
MainModel.py - Executa pipeline de processamento de silhuetas
Ordem: processar_BBox_CSV.py → processar_silhueta_CSV.py → Relevante.py → DadosRelevantes.py
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def run_script(script_name):
    """Executa um script Python e retorna sucesso/falha."""
    print(f"🚀 Executando {script_name}...")
    
    script_path = Path(__file__).parent / script_name
    if not script_path.exists():
        print(f"❌ Arquivo não encontrado: {script_name}")
        return False
    
    try:
        # Ensure child Python runs in UTF-8 mode so prints with emojis don't crash
        env = os.environ.copy()
        env.setdefault("PYTHONUTF8", "1")
        env.setdefault("PYTHONIOENCODING", "utf-8")

        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )
        
        if result.returncode == 0:
            print(f"✅ {script_name} - Sucesso")
            if result.stdout.strip():
                try:
                    print(result.stdout)
                except UnicodeEncodeError:
                    # Fallback: print a safe representation
                    print(result.stdout.encode("utf-8", errors="replace").decode("utf-8", errors="replace"))
            return True
        else:
            print(f"❌ {script_name} - Erro (código {result.returncode})")
            if result.stderr:
                try:
                    print(f"Erro: {result.stderr}")
                except UnicodeEncodeError:
                    print(f"Erro: ", end="")
                    print(result.stderr.encode("utf-8", errors="replace").decode("utf-8", errors="replace"))
            return False
            
    except Exception as e:
        print(f"❌ {script_name} - Exceção: {e}")
        return False

def main():
    """Executa o pipeline completo."""
    print("🎯 PIPELINE DE PROCESSAMENTO DE SILHUETAS")
    print("=" * 50)
    
    scripts = [
        'processar_BBox_CSV.py',
        'processar_silhueta_CSV.py', 
        'Relevante.py',
        'DadosRelevantes.py'
    ]
    
    start_time = time.time()
    success_count = 0
    
    for script in scripts:
        if run_script(script):
            success_count += 1
        print("-" * 30)
    
    total_time = time.time() - start_time
    
    print(f"📊 RESULTADO: {success_count}/{len(scripts)} scripts executados")
    print(f"⏱️  Tempo total: {total_time:.1f}s")
    
    if success_count == len(scripts):
        print("🎉 Pipeline completo!")
        return 0
    else:
        print("⚠️  Pipeline incompleto")
        return 1

if __name__ == "__main__":
    # Reconfigure stdout to UTF-8 where supported to avoid encoding errors
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n🛑 Interrompido pelo usuário")
        sys.exit(130)