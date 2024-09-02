# Trabalho Segurança Computacional

## Integrantes

- Gustavo Vieira de Araújo - Matrícula: 211068440;
- Luiz Henrique Figueiredo Soares - Matrícula: 212007162;

***
!!! Observação: Os relatorios de cada parte estão na respectivas pastas de cada parte !!!
***

## Como rodar os testes da cifra/decifra de bloco e modo de operação CTR (AES-128) ?

1. Clonar projeto:

```bash
git clone https://github.com/GustavoVieiraDeAraujo/Trabalho-Seguranca-Computacional.git
```

2. Entrar na pasta `parte_1_211068440`:

```bash
cd ./Projeto-Seguranca-Computacional/parte_1_211068440
```

3. Baixar bibliotecas necessarias:

```bash
pip install numpy pycryptodome
```

4. Executar os testes:

```bash
 python3 ./testes.py
```

## Como rodar os testes do gerador/verificador de Assinaturas ?

1. Clonar projeto:

```bash
git clone https://github.com/GustavoVieiraDeAraujo/Trabalho-Seguranca-Computacional.git
```

2. Entrar na pasta `parte_2_211068403`:

```bash
cd ./Projeto-Seguranca-Computacional/parte_2_211068403
```

3. Baixar bibliotecas necessarias:

```bash
pip install numpy
pip install haslib
```

4. Executar o codigo:

```bash
 python3 ./RSA-OEAP.py
```