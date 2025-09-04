import os
import requests
import dash

def fix_dash_issues():
    """Corrige todos os problemas do Dash de uma vez"""
    try:
        # 1. Corrige arquivos React faltantes
        dash_path = os.path.dirname(dash.__file__)
        deps_path = os.path.join(dash_path, 'deps')
        os.makedirs(deps_path, exist_ok=True)
        
        react_files = {
            "react@18.3.1.js": "https://unpkg.com/react@18.3.1/umd/react.production.min.js",
            "react-dom@18.3.1.js": "https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js"
        }
        
        for filename, url in react_files.items():
            filepath = os.path.join(deps_path, filename)
            if not os.path.exists(filepath):
                print(f"Baixando {filename}...")
                response = requests.get(url)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"✓ {filename} baixado")
                
        # 2. Corrige compatibilidade Flask
        try:
            import flask
            print(f"Versão do Flask: {flask.__version__}")
        except Exception as e:
            print(f"Erro no Flask: {e}")
            
    except Exception as e:
        print(f"Erro durante correção: {e}")

if __name__ == "__main__":
    fix_dash_issues()   