# Desaparecidos

Plataforma web para divulgar casos de pessoas desaparecidas, com moderação, denúncia de abuso e um painel de análise de dados agregados.

> **Projeto de portfólio.** Os casos exibidos na demonstração são **fictícios**. O site não está aberto a casos reais.

**Demonstração:** https://desaparecidos-xtff.onrender.com *(hospedagem gratuita: a primeira visita pode demorar alguns segundos enquanto o serviço acorda)*

## O problema

Divulgar um desaparecimento rápido ajuda, mas um site aberto a qualquer pessoa também atrai abuso: casos falsos, spam e exposição indevida de dados. O objetivo do projeto foi construir algo útil **e** defensável, pensando em segurança, moderação e privacidade desde o início, e não depois.

## Funcionalidades

- Cadastro de casos com foto, descrição, local, data e contato
- Lista, página de detalhe e busca
- Contas de usuário com verificação de e-mail obrigatória e área "Meus casos"
- **Moderação:** todo caso só aparece depois de aprovado por um administrador, e o número do B.O. é obrigatório
- Botão "marcar como encontrado" (somente o dono do caso)
- **Denúncia** de casos: uma por pessoa, e o caso sai do ar automaticamente ao atingir um limite
- **Painel de análises** (`/painel/`) com Pandas e Plotly, usando apenas dados agregados

## Decisões de segurança

Em linhas gerais, sem detalhes que facilitem ataque:

- CAPTCHA (Cloudflare Turnstile) no cadastro, no envio de casos e nas denúncias
- Limites de uso por conta e por endereço IP, com o IP real do visitante lido do cabeçalho confiável da Cloudflare (e não do `X-Forwarded-For`, que pode ser forjado)
- Contagem dos limites em cache no banco de dados, para não se perder a cada reinício do serviço
- Validação de upload no servidor: tamanho máximo e formatos de imagem permitidos
- Segredos somente em variáveis de ambiente, nunca no código nem no Git
- Fotos e banco de dados de desenvolvimento fora do controle de versão

## Stack

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.12, Django 6.1 |
| Autenticação | django-allauth |
| Frontend | Templates Django (HTML e CSS) |
| Análises | Pandas, Plotly |
| Banco | SQLite (local) e PostgreSQL no Neon (produção) |
| Fotos | Cloudinary (via django-cloudinary-storage) |
| E-mail | Brevo, pela API (django-anymail) |
| Deploy | Render (gunicorn + WhiteNoise) |
| Ambiente | uv |

## Decisões técnicas e aprendizados

- **Armazenamento de fotos:** descartei serviços com cobrança incerta ou exigência de cartão e escolhi o Cloudinary no plano gratuito. O bloco de configuração só é ativado se as variáveis existirem, então o projeto roda localmente com o disco.
- **Checagem de existência da foto:** testei `storage.exists()` por foto, mas com armazenamento na nuvem cada chamada vira uma requisição de rede, o que deixa listas lentas. A lista usa apenas a verificação do campo e mostra um quadro "Foto indisponível".
- **E-mail em produção:** o SMTP do Brevo deu *timeout* no Render, que bloqueia as portas SMTP no plano gratuito. Troquei para a API do Brevo, que usa HTTPS.
- **IP do cliente atrás de proxy:** sem configuração, o allauth enxergava o IP interno do proxy, e todos os visitantes dividiam o mesmo contador de limite. Validei com uma página de depuração temporária, depois removida.
- **Dois bancos separados:** o banco local (SQLite) e o de produção (Neon) são independentes. Um caso criado localmente não existe no site no ar.

## Rodando localmente

Requisitos: Python 3.12 e [uv](https://docs.astral.sh/uv/).

```bash
git clone <url-do-repositorio>
cd desaparecidos
uv venv
uv pip install -r requirements.txt
cp .env.example .env   # preencha com os seus valores
uv run python manage.py migrate
uv run python manage.py createcachetable
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

Variáveis de ambiente usadas (valores nunca vão para o Git):

`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_HTTPS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, `DATABASE_URL` (opcional, usa SQLite se ausente), `TURNSTILE_SITE_KEY`, `TURNSTILE_SECRET_KEY`, `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`, `BREVO_API_KEY`, `DEFAULT_FROM_EMAIL`, `ALLAUTH_TRUSTED_CLIENT_IP_HEADER`.

## Estrutura

```
config/    configurações do projeto e rotas
casos/     cadastro, lista, detalhe, busca, moderação, denúncia
analises/  painel de análises (Pandas + Plotly)
templates/ páginas HTML
build.sh   script de build do Render
```

## Próximos passos

- Testes automatizados (os arquivos de teste ainda estão vazios)
- Mapa de calor com Folium e mais métricas no painel
- Backups do banco e moderação que escale
- Domínio próprio com autenticação de e-mail (SPF/DKIM/DMARC), para melhorar a entrega
- Antes de qualquer uso com casos reais: termos de uso, política de privacidade e adequação à LGPD, com revisão jurídica (envolve dados de menores)

## Autor

**Jonatas Fernandes Alves**: estudante de Engenharia de Software, em busca de estágio em Análise de Dados.
GitHub: [@JonatasF-Alves](https://github.com/JonatasF-Alves)