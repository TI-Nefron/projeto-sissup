#!/bin/bash

# Este script coleta informações de diagnóstico para depurar o ambiente Docker.

echo "============================================================"
echo "          INICIANDO COLETA DE DADOS DE DIAGNÓSTICO"
echo "============================================================"
echo ""
echo "AVISO IMPORTANTE: O conteúdo do arquivo .env será exibido."
echo "Revise a saída e REMOVA QUAISQUER SENHAS OU CHAVES SECRETAS"
echo "antes de compartilhar o resultado."
echo ""
sleep 3

echo "==================== 1. VERSÕES DO DOCKER ===================="
docker --version
docker-compose --version
echo ""

echo "==================== 2. STATUS DOS CONTÊINERES ================"
# -a mostra todos os contêineres, incluindo os que pararam
docker ps -a
echo ""

echo "==================== 3. LOGS DO SERVIÇO 'web' ================"
# --no-color para facilitar a leitura em texto puro
docker-compose logs --no-color web
echo ""

echo "==================== 4. ESTRUTURA DE ARQUIVOS ================"
# Verifica se o comando 'tree' está instalado
if ! command -v tree &> /dev/null
then
    echo "'tree' não encontrado. Instalando com 'sudo apt install tree'..."
    echo "Se a instalação falhar, use 'ls -lR' como alternativa."
    sudo apt install tree -y
fi
# Exibe a árvore de arquivos, ignorando pastas que geram muito ruído
tree -I ".venv|__pycache__|.git|.vscode"
echo ""


echo "==================== 5. CONTEÚDO DOS ARQUIVOS DE CONFIGURAÇÃO ================"

echo "-------------------- Conteúdo de: docker-compose.yml --------------------"
cat docker-compose.yml
echo ""

echo "-------------------- Conteúdo de: .env --------------------"
echo "!!! ATENÇÃO: REVISE E REMOVA SEGREDOS DESTE BLOCO !!!"
cat .env
echo ""

# Ajuste o caminho 'djangoapp' se o nome da sua pasta for diferente
PROJECT_APP_DIR="djangoapp"

echo "-------------------- Conteúdo de: ${PROJECT_APP_DIR}/Dockerfile --------------------"
cat "${PROJECT_APP_DIR}/Dockerfile"
echo ""

echo "-------------------- Conteúdo de: ${PROJECT_APP_DIR}/requirements.txt --------------------"
cat "${PROJECT_APP_DIR}/requirements.txt"
echo ""

echo "-------------------- Conteúdo de: ${PROJECT_APP_DIR}/project/settings.py --------------------"
cat "${PROJECT_APP_DIR}/project/settings.py"
echo ""

echo "-------------------- Conteúdo de: ${PROJECT_APP_DIR}/project/urls.py --------------------"
cat "${PROJECT_APP_DIR}/project/urls.py"
echo ""


echo "============================================================"
echo "                   COLETA DE DADOS CONCLUÍDA"
echo "============================================================"
echo "Por favor, copie toda a saída acima, revise o conteúdo do"
echo ".env para remover segredos e compartilhe para análise."
echo ""