import os 
import pandas as pd
import kaleido

def baixar_imagem(figure, tipo, nome, imagem):
        if tipo == "html":
            figure.write_html(f"static/{nome.replace(' ', '_')}.html")
            print("Gráfico gerado com sucesso")
            imagem = f"{nome.replace(' ', '_')}.html"
        elif tipo == "image":
            figure.write_image(f"static/{nome.replace(' ', '_')}.png", engine="kaleido")
            print("Gráfico gerado com sucesso")
            imagem = f"{nome.replace(' ', '_')}.png"
        else:
            raise ValueError('O parâmetro "imagem" deve ser "html" ou "png".')

def verificar_extensao_csv(file_path):
        if not file_path.endswith('.csv'):
                raise ValueError("A base de dados não é um arquivo CSV.")

def retirar_amostragem(dataset, amostragem):
        dataset_completo = pd.read_csv(dataset, delimiter=",")
        valor_amostragem = int(len(dataset_completo) * amostragem)
        amostra = dataset_completo.sample(n=valor_amostragem, random_state=42)
        amostra.to_csv('datasets/amostragem.csv', index=False)

def excluir_arquivo_amostragem():
        os.remove('datasets/amostragem.csv')

def verificar_parametros(nome, base_dados, amostragem, features, target, tipo_imagem):
        if nome == None:
                raise ValueError(f'Faltou informar o parâmetro "nome"')
        if base_dados == None:
                raise ValueError(f'Faltou informar o parâmetro "base_dados"')
        if amostragem == None:
                raise ValueError(f'Faltou informar o parâmetro "amostragem"')
        if features == None:
                raise ValueError(f'Faltou informar o parâmetro "features"')
        if target == None:
                raise ValueError(f'Faltou informar o parâmetro "target"')
        if tipo_imagem == None:
                raise ValueError(f'Faltou informar o parâmetro "tipo_imagem"')