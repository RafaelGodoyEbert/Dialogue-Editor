# Dialogue Editor by RafaGodoy & Krisp
[English](https://github.com/RafaelGodoyEbert/Dialogue-Editor/blob/main/README.md) [Português](https://github.com/RafaelGodoyEbert/Dialogue-Editor/blob/main/README_portuguese.md)

![image](https://github.com/RafaelGodoyEbert/Dialogue-Editor/assets/78083427/ce9991bb-788a-453c-a244-d16e296927d7)

## Sobre o Projeto

O **Dialogue Editor** é uma ferramenta de edição de diálogos interativos, criada por Rafael Godoy & Krisp. Esta aplicação permite carregar diálogos de arquivos de texto, exibi-los e editá-los diretamente em uma interface gráfica. Além disso, você pode traduzir os diálogos para diferentes idiomas e sobrepor texto em imagens.

## Funcionalidades

- **Carregar e Salvar Diálogos**: Abra e salve arquivos de texto contendo diálogos.
- **Edição de Texto**: Edite os diálogos diretamente na interface gráfica.
- **Filtro de Pesquisa**: Pesquise diálogos específicos.
- **Tradução**: Traduza os diálogos usando o Google Translate.
- **Sobreposição de Texto em Imagens**: Carregue uma imagem e sobreponha texto nela.
- **Navegação entre Páginas**: Navegue entre diferentes páginas de diálogo.
- **Escolha de Fonte e Cor do Texto**: Personalize a fonte e a cor do texto.

## Como Usar

### Requisitos

- Python 3.x
- Bibliotecas:
  - `tkinter`
  - `Pillow`
  - `googletrans`
  - `tqdm`
  - `i18n`

### Instalação

1. Clone o repositório:

```bash
git clone https://github.com/RafaelGodoyEbert/Dialogue-Editor
cd dialogue-editor
```

2. Instale as dependências:

```bash
python -m venv myenv
myenv\Scripts\activate

pip install -r requirements.txt
```

### Executando o Aplicativo

Para iniciar o aplicativo, execute o seguinte comando:

```bash
python dialogue_editor.py
```

### Uso da Interface

1. **Carregar Diálogos**: Vá até o menu `Arquivo` e selecione `Carregar Dialogos` para carregar um arquivo de texto contendo diálogos.
2. **Carregar Imagem**: Vá até o menu `Arquivo` e selecione `Carregar Imagem` para carregar uma imagem.
3. **Carregar Fonte**: Vá até o menu `Arquivo` e selecione `Carregar Fonte` para carregar uma fonte personalizada.
4. **Salvar Diálogos**: Use as opções `Salvar` ou `Salvar como...` no menu `Arquivo` para salvar as edições feitas nos diálogos.
5. **Tradução**: Selecione os idiomas de origem e destino nas comboboxes e clique em `Traduzir arquivo` para traduzir o arquivo inteiro ou `Traduzir linha` para traduzir uma linha específica.
6. **Navegação**: Use os botões `Página anterior` e `Próxima Página` para navegar entre as páginas de diálogo. (Se for aplicável)
7. **Personalização**: Utilize as entradas de `Tamanho da fonte` e `Posição do texto` para ajustar a aparência do texto sobreposto na imagem.

## Créditos

Criado por: Rafael Godoy & Krisp

- **GitHub**: [RafaelGodoyEbert](https://github.com/RafaelGodoyEbert)
- **X (Twitter)**: [GodoyEbert](https://twitter.com/GodoyEbert)
- **YouTube**: [Godoyy](https://youtube.com/@Godoyy)
- **E-mail**: rafaelgodebert@gmail.com

**Apoie o projeto:**

- **PIX**: rafaelgodebert@gmail.com
- **PayPal**: [Clique aqui](https://www.paypal.com/donate?hosted_button_id=XXXXX)

## Licença

Este projeto está licenciado sob os termos da licença GPL. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
