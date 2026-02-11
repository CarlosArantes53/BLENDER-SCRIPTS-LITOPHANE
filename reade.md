## 📂 Como Instalar o Add-on

Como o projeto está dividido em vários arquivos Python, a maneira correta de instalar é como um pacote (pasta):

1. **Prepare a pasta**: Crie uma pasta chamada `lithophane_maker` no seu computador. | ou simplesmente baixe esse repositório do github zipado e pule para o passo "4".
2. **Mova os arquivos**: Coloque os seguintes arquivos dentro dessa pasta:
* `__init__.py`
* `properties.py`
* `ui.py`
* `operators.py`
* `geometry.py`


3. **Crie um arquivo ZIP**: Compacte a pasta `lithophane_maker` para gerar um arquivo `lithophane_maker.zip`.
4. **No Blender**:
* Vá em **Edit > Preferences** (Editar > Preferências).
* Selecione a aba **Add-ons**.
* Clique em **Install...** e selecione o arquivo `.zip` que você criou.
* Pesquise por "Gerador de Lithophane Pro Modular" na lista e marque a caixa de seleção para ativá-lo.



---

## 🛠️ Como Usar

Após a ativação, o painel do add-on aparecerá na **Sidebar** (barra lateral) da **3D Viewport**:

1. Pressione a tecla **N** no teclado para abrir a barra lateral.
2. Clique na aba **Lithophane**.
3. **Configuração**:
* **Imagem Base**: Selecione o caminho do arquivo de imagem (JPG/PNG) que deseja converter.
* **Geometria**: Escolha entre os formatos *Plano*, *Curva Externa*, *Curva Interna*, *Cilindro* ou *Domo*.
* **Detalhes**: Ajuste a espessura mínima (partes claras) e a profundidade de cor (partes escuras).
* **Qualidade**: Defina o nível de resolução (subdivisões da malha) e as iterações de suavização para remover o aspecto "pixelado".


4. **Finalização**:
* **Fundo Plano**: Ative para criar uma base reta, ideal para impressão 3D vertical.
* **Aplicar Modificadores**: Se marcado, o Blender converterá os modificadores em malha real automaticamente após a geração.


5. Clique em **Gerar Lithophane 3D**.

---

## 📋 Requisitos

* **Blender**: Versão 4.0.0 ou superior.
* **Unidades**: O script configura automaticamente o sistema para Milímetros para facilitar a exportação para fatiadores de impressão 3D.