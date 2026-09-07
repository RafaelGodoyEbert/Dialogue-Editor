# 📦 Guia de Instalação - Dialogue Editor

## 🚀 Instalação Rápida (Recomendado)

### Usando UV (Ultrarrápido!)

1. **Execute o instalador automático:**
   ```bash
   install.bat
   ```

2. **Execute o programa:**
   ```bash
   run_Dialogue_Editor.bat
   ```

Pronto! O instalador UV irá:
- ✅ Instalar UV automaticamente (se necessário)
- ✅ Verificar/instalar Python
- ✅ Criar ambiente virtual
- ✅ Instalar todas as dependências
- ✅ Configurar scripts de execução

---

## 🔧 O que é UV?

**UV** é um gerenciador de pacotes Python extremamente rápido, escrito em Rust. Ele é:
- ⚡ **10-100x mais rápido** que pip tradicional
- 🎯 **Compatível** com pip e requirements.txt
- 🔒 **Confiável** com resolução de dependências determinística
- 🪶 **Leve** e fácil de instalar

### Por que usar UV?

| Característica | pip tradicional | UV |
|---------------|-----------------|-----|
| Velocidade de instalação | ~30-60s | ~3-5s |
| Resolução de conflitos | Básica | Avançada |
| Cache inteligente | Limitado | Completo |
| Instalação de Python | Manual | Automática |

---

## 📋 Requisitos

- **Windows** 7 ou superior
- **Conexão com internet** (apenas para instalação)
- **~100 MB** de espaço em disco

---

## 🛠️ Instalação Manual (Alternativa)

Se preferir instalar manualmente sem UV:

### 1. Instalar Python
- Baixe Python 3.8+ de [python.org](https://www.python.org/downloads/)
- Durante a instalação, marque "Add Python to PATH"

### 2. Criar ambiente virtual
```bash
python -m venv myenv
```

### 3. Ativar ambiente
```bash
myenv\Scripts\activate
```

### 4. Instalar dependências
```bash
pip install -r requirements.txt
```

### 5. Executar
```bash
python Dialogue_Editor.py
```

---

## 🐛 Solução de Problemas

### UV não instala automaticamente

Se o instalador não conseguir instalar UV automaticamente:

1. **Instale manualmente via PowerShell:**
   ```powershell
   irm https://astral.sh/uv/install.ps1 | iex
   ```

2. **Ou baixe o instalador:** [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

3. **Execute install.bat novamente**

### Erro de permissão

Se encontrar erros de permissão:
- Execute o instalador como **Administrador**
- Clique com botão direito em `install.bat` → "Executar como administrador"

### Ambiente virtual corrompido

Se o ambiente virtual apresentar problemas:
```bash
# Delete a pasta myenv
rmdir /s /q myenv

# Execute o instalador novamente
install.bat
```

### Dependências não instalam

Se houver erro ao instalar dependências:
```bash
# Tente atualizar o UV
uv self update

# Execute o instalador novamente
install.bat
```

---

## 📦 Dependências

O projeto usa as seguintes bibliotecas Python:

- **tk** (0.1.0) - Interface gráfica
- **tqdm** (4.66.4) - Barras de progresso
- **googletrans** (4.0.0rc1) - Tradução automática
- **pillow** (10.3.0) - Processamento de imagens
- **six** (1.16.0) - Compatibilidade Python 2/3

---

## 🔄 Atualizando Dependências

Para atualizar as dependências do projeto:

```bash
# Ativar ambiente
call myenv\Scripts\activate

# Atualizar com UV (rápido)
uv pip install -r requirements.txt --upgrade

# Ou com pip tradicional
pip install -r requirements.txt --upgrade
```

---

## 📚 Recursos Adicionais

- **Documentação UV:** [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)
- **Python:** [https://www.python.org/](https://www.python.org/)
- **Dialogue Editor README:** [README.md](README.md)

---

## 💡 Dicas

1. **Primeira instalação:** Use `install.bat` - ele configura tudo automaticamente
2. **Execução diária:** Use `run_Dialogue_Editor.bat` - mais rápido
3. **Problemas:** Delete `myenv` e execute `install.bat` novamente
4. **Atualizações:** Execute `install.bat` para reinstalar com versões mais recentes

---

## ✨ Vantagens do Instalador UV

- 🚀 **Setup em segundos** ao invés de minutos
- 🔄 **Reinstalação rápida** se algo der errado
- 📦 **Gerenciamento automático** de Python e dependências
- 🎯 **Zero configuração** manual necessária
- 💾 **Cache inteligente** para reinstalações instantâneas

---

**Desenvolvido com ❤️ usando UV**
