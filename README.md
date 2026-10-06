# duplicate-finder-python

Encontra arquivos duplicados em diretório por tamanho + SHA-1. Saída JSON,
sem biblioteca externa. Limites de tamanho, ignora symlink e arquivo
perdido por erro de leitura.

## Uso

    python3 dupfinder.py --root /caminho --out dup-report.json
    python3 dupfinder.py --root /caminho --min-size 1024

## Saída

JSON com grupos, tamanho, sha1 e lista de caminhos. Total de duplicados no fim.

## Segurança

Somente leitura. Ignora symlink. Limita MAX_FILE 256 MB. Erros de acesso
são pulados, não abortam a varredura. SHA-1 é usado como id, não como
criptografia de segurança.

## Limitações

SHA-1 não é oficial para encontrar duplicatas com cinflito garantido; para
máxima segurança use SHA-256. Sem interface gráfica, sem exclusão por padrão.

## Próximos passos

Modo dry-run com remoção segura, suporte a SHA-256, exclusão por glob.

## Autor

Rafael Nunes — [@Rafaelnunes-alt2](https://github.com/Rafaelnunes-alt2)
