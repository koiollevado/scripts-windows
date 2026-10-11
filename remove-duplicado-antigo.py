import os
import hashlib
from collections import defaultdict

def get_file_hash(file_path):
    """Calcula o hash de um arquivo."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicates(directory):
    """Encontra arquivos duplicados em um diretório."""
    files_by_hash = defaultdict(list)
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_hash = get_file_hash(file_path)
            files_by_hash[file_hash].append(file_path)
    return {hash_value: file_paths for hash_value, file_paths in files_by_hash.items() if len(file_paths) > 1}

def remove_oldest_duplicates(directory):
    """Remove os arquivos duplicados mais antigos."""
    duplicates = find_duplicates(directory)
    for duplicate_list in duplicates.values():
        oldest_file = min(duplicate_list, key=os.path.getmtime)
        for file_path in duplicate_list:
            if file_path != oldest_file:
                os.remove(file_path)
                print(f"Arquivo duplicado removido: {file_path}")

# Diretório onde os arquivos duplicados devem ser procurados
diretorio = './'

# Remover arquivos duplicados mais antigos
remove_oldest_duplicates(diretorio)
