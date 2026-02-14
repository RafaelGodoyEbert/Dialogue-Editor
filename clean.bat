@echo off
chcp 65001 >nul

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         DIALOGUE EDITOR - LIMPEZA DE AMBIENTE              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo ⚠️  Este script irá remover o ambiente virtual atual.
echo.
set /p confirm="Deseja continuar? (S/N): "

if /i not "%confirm%"=="S" (
    echo.
    echo ❌ Operação cancelada.
    pause
    exit /b 0
)

echo.
echo 🧹 Limpando ambiente virtual...

if exist "myenv" (
    rmdir /s /q myenv
    echo ✅ Ambiente virtual removido
) else (
    echo ℹ️  Nenhum ambiente virtual encontrado
)

if exist "env" (
    rmdir /s /q env
    echo ✅ Ambiente antigo removido
)

echo.
echo ✅ Limpeza concluída!
echo.
echo Para reinstalar, execute: install.bat
echo.

pause
