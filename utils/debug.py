# utils/_debug.py

def _debug(*data):
    sep = '─' * 40
    print(f'\n{sep}\n')
    for item in data:
        tipo = type(item).__name__
        print(f'[{tipo}]\n{repr(item)}')
        print(f'\n{sep}\n')