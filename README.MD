SISSUP Nefron - Sistema de Suporte ao Faturamento para Clínicas de Nefrologia
📜 Sobre o Projeto

O SISSUP Nefron é uma aplicação web projetada para modernizar e otimizar o processo de faturamento de sessões de diálise, com um foco inicial no fluxo de auditoria do SUS. O objetivo principal é eliminar o manuseio de papel, agilizar as aprovações, reduzir glosas e garantir a conformidade jurídica e contábil através de um fluxo de trabalho 100% digital.

Este projeto foi construído utilizando uma arquitetura moderna e containerizada com Docker, garantindo um ambiente de desenvolvimento robusto, replicável e pronto para a produção.
✨ Funcionalidades (MVP - Etapa 1)

    Dossiê de Faturamento Digital: Centralização de todos os documentos necessários (Laudo APAC, documentos do paciente, folhas de sessão) em um repositório digital por paciente/mês.

    Digitalização na Recepção: Permite que a equipe da recepção digitalize e anexe documentos diretamente ao dossiê correspondente.

    Portal de Auditoria Remoto: Uma interface web segura para que as auditoras acessem, revisem e aprovem os dossiês de faturamento de qualquer lugar.

    Assinatura Eletrônica de Auditoria: Registro da aprovação da auditora com validade jurídica (Assinatura Eletrônica Simples), incluindo trilha de auditoria completa (quem, o quê, quando, onde).

    Gestão de Convênios Flexível: O sistema permite a configuração de diferentes convênios (SUS, privados) e seus respectivos checklists de documentos obrigatórios.

    Armazenamento Seguro: Utilização do MinIO, um servidor de objetos compatível com S3, para o armazenamento seguro e de longo prazo dos documentos digitalizados.

🚀 Roadmap (Visão de Futuro - Etapa 2)

Após a validação do MVP, o projeto evoluirá para um Sistema de Registro Eletrônico em Saúde (S-RES) completo:

    Prontuário 100% Digital: Substituição das folhas de sessão em papel por registros nato-digitais.

    Assinatura Digital Qualificada (ICP-Brasil): Integração para que médicos e enfermeiros assinem os registros clínicos com validade jurídica plena.

    Autenticação Biométrica do Paciente: Utilização de reconhecimento facial para o check-in do paciente e assinatura de termos de consentimento (TCLE).

🛠️ Tech Stack

    Backend: Python 3.11, Django

    Frontend: HTML, CSS, JavaScript (com a abordagem de renderização no servidor usando HTMX + Alpine.js + Bootstrap 5)

    Banco de Dados: PostgreSQL 16

    Armazenamento de Arquivos: MinIO (S3 Compatible)

    Containerização e Orquestração: Docker & Docker Compose

    Ambiente de Desenvolvimento Principal: Linux (Pop!_OS)

⚙️ Primeiros Passos (Configuração do Ambiente de Desenvolvimento)

Siga estes passos para configurar e rodar o projeto localmente.
Pré-requisitos

    Sistema Operacional: Um ambiente Linux (Ubuntu, Pop!_OS, etc.) é recomendado.

    Docker: Versão mais recente instalada.

    Docker Compose: Versão 1.29 ou superior.

    Git: Para clonar o repositório.

    VS Code: Editor de código recomendado.