import subprocess

# Caminho para o seu arquivo requirements.txt
requirements_path = 'requirements.txt'

# Ler os pacotes do requirements.txt
with open(requirements_path, 'r') as f:
    packages = f.readlines()

# Atualizar cada pacote
for package in packages:
    package_name = package.strip().split('==')[0]  # Extrair o nome do pacote
    if package_name:  # Verificar se não é uma linha em branco
        subprocess.run(f'pip install --upgrade {package_name}', shell=True)

# Gerar novo requirements.txt com versões atualizadas
updated_packages = subprocess.check_output(['pip', 'freeze']).decode('utf-8')

with open(requirements_path, 'w') as f:
    f.write(updated_packages)
