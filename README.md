# Pessoas Desaparecidas

Site para ajudar famílias a divulgar o desaparecimento de pessoas e facilitar o compartilhamento dos casos nas redes sociais. O projeto também traz um painel de estatísticas, feito com Pandas e Plotly, que mostra a situação dos casos a partir de dados agregados.

> **Status:** projeto em desenvolvimento (MVP), rodando localmente. Ainda não está publicado na internet.

## Funcionalidades

- Lista de casos com busca por nome ou cidade e paginação
- Página de cada caso, com foto, dados e contato da família
- Botão para compartilhar o caso no WhatsApp
- Formulário de cadastro com upload de foto e número do B.O.
- Moderação: todo cadastro novo só aparece no site depois de aprovado no painel administrativo
- Painel de estatísticas com casos por cidade, por mês e por faixa etária, taxa de resolução e tempo médio até a pessoa ser encontrada
- Comando que cria casos fictícios para testar o site

## Tecnologias

- **Python** e **Django** (back end, banco de dados e painel administrativo)
- **SQLite** (banco de dados em desenvolvimento)
- **Pandas** e **Plotly** (análise de dados e gráficos)
- **HTML** e **CSS** (templates do Django)
- **Pillow** (upload de imagens)
- **uv** (gerenciamento de ambiente e dependências)

## Como rodar

Pré-requisitos: Python 3.12 ou superior e o [uv](https://docs.astral.sh/uv/) instalado.

```bash
git clone https://github.com/JonatasF-Alves/desaparecidos.git
cd desaparecidos

uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py popular_exemplos
python manage.py runserver
```

Depois abra:

| Endereço | O que é |
|---|---|
| http://127.0.0.1:8000/ | Lista de casos |
| http://127.0.0.1:8000/cadastrar/ | Cadastro de um caso |
| http://127.0.0.1:8000/painel/ | Estatísticas |
| http://127.0.0.1:8000/admin/ | Moderação (login do superusuário) |

O comando `popular_exemplos` cria 12 casos **fictícios** para você ver o site funcionando. Para apagá-los, use `python manage.py popular_exemplos --limpar`.

## Estrutura do projeto

```
├── config/              # configurações e rotas principais
├── casos/               # cadastro, lista, detalhe e moderação
│   ├── models.py        # modelo Caso
│   ├── views.py         # lógica das páginas
│   ├── forms.py         # formulário de cadastro
│   ├── admin.py         # painel de moderação
│   └── templates/
├── analises/            # painel de estatísticas (Pandas + Plotly)
│   └── views.py
├── templates/base.html  # layout comum e CSS
└── manage.py
```

## Privacidade e moderação

O site lida com informações de pessoas reais, então algumas decisões foram tomadas desde o início:

- Nenhum cadastro é publicado sem aprovação de um moderador.
- O número do B.O. é obrigatório, para ajudar a verificar os casos.
- As estatísticas usam apenas totais, nunca dados de uma pessoa específica.
- O banco de dados e as fotos enviadas ficam fora do repositório (`.gitignore`).
- Os dados de exemplo são todos fictícios. **Não use dados reais para testar.**

## Antes de publicar na internet

Esta versão é para desenvolvimento. Para um deploy real ainda é preciso:

- Definir um `SECRET_KEY` próprio por variável de ambiente e desligar o `DEBUG`
- Configurar `ALLOWED_HOSTS`
- Trocar o SQLite por PostgreSQL
- Guardar as fotos em um serviço externo (por exemplo, AWS S3)
- Escrever uma política de privacidade (LGPD) e definir quem vai moderar os cadastros

## Próximos passos

- [ ] Botão para marcar um caso como encontrado
- [ ] Botão para denunciar um cadastro
- [ ] Mapa de calor com os locais de desaparecimento
- [ ] Contas de usuário, para cada família gerenciar o próprio caso
- [ ] Deploy

## Sobre o desenvolvimento

Este projeto foi desenvolvido com apoio de IA (Claude, da Anthropic) na estrutura e no código inicial. As alterações, os testes e a evolução do projeto são feitos por mim.

## Autor

**Jonatas Fernandes Alves**
Estudante de Engenharia de Software, em busca de estágio na área de análise de dados.
GitHub: [@JonatasF-Alves](https://github.com/JonatasF-Alves)