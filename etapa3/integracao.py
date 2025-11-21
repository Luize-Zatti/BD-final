import os
from collections import defaultdict
import xml.etree.ElementTree as ET

import psycopg2
from dotenv import load_dotenv


load_dotenv()

DB_NAME = os.getenv("PG_DB", "trabalho_bd2")
DB_USER = os.getenv("PG_USER", "postgres")
DB_PASSWORD = os.getenv("PG_PASSWORD", "")
DB_HOST = os.getenv("PG_HOST", "localhost")
DB_PORT = os.getenv("PG_PORT", "5432")

XML_FORNECIMENTO = os.getenv("FORNECIMENTO_XML", "fornecimento.xml")



def carregar_pecas_pg():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )
    cur = conn.cursor()
    cur.execute(
        """
        SELECT cod_peca, pnome, cor, peso, cidade, preco
        FROM peca
        ORDER BY cod_peca;
        """
    )

    pecas = []
    for row in cur.fetchall():
        pecas.append(
            {
                "cod_peca": row[0],
                "pnome": row[1],
                "cor": row[2],
                "peso": float(row[3]),
                "cidade": row[4],
                "preco": float(row[5]),
            }
        )

    cur.close()
    conn.close()
    return pecas


def carregar_fornecimentos_xml(caminho_xml: str = XML_FORNECIMENTO):
    if not os.path.exists(caminho_xml):
        raise FileNotFoundError(f"Arquivo XML não encontrado: {caminho_xml}")

    tree = ET.parse(caminho_xml)
    root = tree.getroot()

    fornecimentos_por_peca = defaultdict(list)

    for f in root.findall("fornecimento"):
        cod_fornec = f.findtext("Cod_Fornec")
        cod_peca = f.findtext("Cod_Peca")
        cod_proj = f.findtext("Cod_Proj")
        qtd_text = f.findtext("Quantidade")

        try:
            quantidade = int(qtd_text)
        except (TypeError, ValueError):
            quantidade = 0

        fornecimentos_por_peca[cod_peca].append(
            {
                "cod_fornec": cod_fornec,
                "cod_proj": cod_proj,
                "quantidade": quantidade,
            }
        )

    return fornecimentos_por_peca

def integrar_dados():
    pecas = carregar_pecas_pg()
    fornecimentos_por_peca = carregar_fornecimentos_xml()

    for p in pecas:
        cod = p["cod_peca"]
        print("=" * 60)
        print(f"Peça {cod} - {p['pnome']}")
        print(
            f"Cor: {p['cor']} | Cidade: {p['cidade']} "
            f"| Preço: {p['preco']:.2f}"
        )
        print("Fornecimentos relacionados:")

        fornecs = fornecimentos_por_peca.get(cod, [])

        if not fornecs:
            print("  (nenhum fornecimento encontrado no XML)")
        else:
            for f in fornecs:
                print(
                    f"  Fornecedor: {f['cod_fornec']} | "
                    f"Projeto: {f['cod_proj']} | "
                    f"Quantidade: {f['quantidade']}"
                )


if __name__ == "__main__":
    print("=== Integração PECA (PostgreSQL + .env) + fornecimento.xml ===")
    integrar_dados()
