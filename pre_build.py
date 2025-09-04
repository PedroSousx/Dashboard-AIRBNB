import os
import requests
import subprocess
import sys

def fix_dash_deps():
    """Corrige as dependências faltantes do Dash"""
    try:
        # Instala o dash primeiro
        subprocess.check_call([sys.executable, "-m", "pip", "install", "dash==2.6.1"])
        
        import dash
        dash_path = os.path.dirname(dash.__file__)
        deps_path = os.path.join(dash_path, 'deps')
        
        # Cria diretório se não existir
        os.makedirs(deps_path, exist_ok=True)
        
        # URLs dos arquivos necessários
        files_to_download = {
            "react@18.3.1.js": "https://unpkg.com/react@18.3.1/umd/react.production.min.js",
            "react-dom@18.3.1.js": "https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js"
        }
        
        for filename, url in files_to_download.items():
            filepath = os.path.join(deps_path, filename)
            if not os.path.exists(filepath):
                print(f"Baixando {filename}...")
                response = requests.get(url)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"{filename} baixado com sucesso!")
                
    except Exception as e:
        print(f"Erro ao corrigir dependências: {e}")

if __name__ == "__main__":
    fix_dash_deps()