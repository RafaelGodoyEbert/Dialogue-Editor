@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ============================================
:: Dialogue Editor - Instalador UV
:: ============================================

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         DIALOGUE EDITOR - INSTALADOR AUTOMÁTICO            ║
echo ║                    Powered by UV                           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

:: Verificar se UV está instalado
echo [1/5] Verificando UV...
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  UV não encontrado! Instalando UV...
    echo.
    
    :: Instalar UV usando PowerShell
    powershell -ExecutionPolicy ByPass -Command "irm https://astral.sh/uv/install.ps1 | iex"
    
    if %errorlevel% neq 0 (
        echo.
        echo ❌ Erro ao instalar UV!
        echo Por favor, instale manualmente: https://docs.astral.sh/uv/
        pause
        exit /b 1
    )
    
    :: Adicionar UV ao PATH da sessão atual
    set "PATH=%USERPROFILE%\.cargo\bin;%PATH%"
    
    echo ✅ UV instalado com sucesso!
) else (
    echo ✅ UV já está instalado
)

echo.
echo [2/5] Verificando Python...

:: Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Python não encontrado! Instalando Python 3.11 via UV...
    echo.
    uv python install 3.11
    if %errorlevel% neq 0 (
        echo ❌ Erro ao instalar Python!
        pause
        exit /b 1
    )
    echo ✅ Python 3.11 instalado com sucesso!
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ Python !PYTHON_VERSION! encontrado
)

echo.
echo [3/5] Criando ambiente virtual...

:: Remover ambiente antigo se existir
if exist "myenv" (
    echo ⚠️  Removendo ambiente virtual antigo...
    rmdir /s /q myenv
)

:: Criar ambiente virtual com UV usando Python 3.11
uv venv myenv --python 3.11
if %errorlevel% neq 0 (
    echo ❌ Erro ao criar ambiente virtual!
    pause
    exit /b 1
)
echo ✅ Ambiente virtual criado

echo.
echo [4/5] Instalando dependências...

:: Instalar dependências usando UV (muito mais rápido que pip!)
echo Instalando pacotes Python...
uv pip install -r requirements.txt --python myenv\Scripts\python.exe
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Tentando instalação alternativa com wheels pré-compilados...
    
    :: Tentar com pip tradicional como fallback
    call myenv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    if %errorlevel% neq 0 (
        echo ❌ Erro ao instalar dependências!
        echo.
        echo Possíveis soluções:
        echo 1. Verifique sua conexão com internet
        echo 2. Tente executar como Administrador
        echo 3. Instale Visual C++ Build Tools: https://aka.ms/vs/17/release/vs_BuildTools.exe
        pause
        exit /b 1
    )
)
echo ✅ Dependências instaladas

echo.
echo [5/5] Atualizando script de execução...

:: Criar/atualizar run_Dialogue_Editor.bat
(
echo @echo off
echo.
echo call myenv\Scripts\activate
echo.
echo python Dialogue_Editor.py
echo.
echo pause
) > run_Dialogue_Editor.bat

echo ✅ Script de execução atualizado

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║              ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Para executar o Dialogue Editor, use:
echo   ^> run_Dialogue_Editor.bat
echo.
echo Ou simplesmente clique duas vezes no arquivo run_Dialogue_Editor.bat
echo.

pause
