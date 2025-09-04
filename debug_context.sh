#!/bin/bash

echo "============================================================"
echo "          INICIANDO COLETA DE DADOS DE DIAGNÓSTICO"
echo "============================================================"
echo ""
echo "AVISO: O conteúdo do .env será exibido. Revise antes de compartilhar."
echo ""
sleep 2

echo "==================== 1. VERSÕES DO DOCKER ===================="
docker --version
docker-compose --version
echo ""

echo "==================== 2. STATUS DOS CONTÊINERES ================"
docker ps -a
echo ""

echo "==================== 3. LOGS DO SERVIÇO 'web' ================"
docker-compose logs --no-color web
echo ""

echo "==================== 4. ESTRUTURA DE ARQUIVOS ================"
if ! command -v tree &> /dev/null
then
    echo "'tree' não encontrado. Usando 'ls -lR' como alternativa."
    ls -lR
else
    tree -I ".venv|__pycache__|.git|.vscode|frontend/node_modules"
fi
echo ""


echo "==================== 5. ARQUIVOS DE CONFIGURAÇÃO ================"

echo "-------------------- docker-compose.yml --------------------"
cat docker-compose.yml
echo ""

echo "-------------------- .env --------------------"
echo "!!! ATENÇÃO: REVISE E REMOVA SEGREDOS DESTE BLOCO !!!"
cat .env
echo ""

PROJECT_APP_DIR="backend"

echo "-------------------- ${PROJECT_APP_DIR}/Dockerfile --------------------"
cat "${PROJECT_APP_DIR}/Dockerfile"
echo ""

echo "-------------------- ${PROJECT_APP_DIR}/requirements.txt --------------------"
cat "${PROJECT_APP_DIR}/requirements.txt"
echo ""

echo "-------------------- ${PROJECT_APP_DIR}/project/settings.py --------------------"
cat "${PROJECT_APP_DIR}/project/settings.py"
echo ""

echo "-------------------- ${PROJECT_APP_DIR}/project/urls.py --------------------"
cat "${PROJECT_APP_DIR}/project/urls.py"
echo ""


echo "============================================================"
echo "                   COLETA DE DADOS CONCLUÍDA"
echo "============================================================"
echo ""