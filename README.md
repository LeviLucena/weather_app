<p align="center">
  <!-- Linguagem principal -->
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python Badge" />
  </a>
  
  <!-- Framework web -->
  <a href="https://flask.palletsprojects.com/">
    <img src="https://img.shields.io/badge/-Flask-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask Badge" />
  </a>

  <!-- Banco de dados -->
  <a href="https://www.postgresql.org/">
    <img src="https://img.shields.io/badge/-PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL Badge" />
  </a>

  <!-- Biblioteca ORM -->
  <a href="https://www.sqlalchemy.org/">
    <img src="https://img.shields.io/badge/-SQLAlchemy-E44C24?style=flat-square&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy Badge" />
  </a>

  <!-- Agendador de tarefas -->
  <a href="https://apscheduler.readthedocs.io/">
    <img src="https://img.shields.io/badge/-APScheduler-4B8BBE?style=flat-square&logo=python&logoColor=white" alt="APScheduler Badge" />
  </a>

  <!-- Gráficos -->
  <a href="https://matplotlib.org/">
    <img src="https://img.shields.io/badge/-Matplotlib-11557C?style=flat-square&logo=plotly&logoColor=white" alt="Matplotlib Badge" />
  </a>

  <a href="https://plotly.com/">
    <img src="https://img.shields.io/badge/-Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white" alt="Plotly Badge" />
  </a>

  <!-- API de clima -->
  <a href="https://content.meteoblue.com/en/business-solutions/weather-apis">
    <img src="https://img.shields.io/badge/-Meteoblue%20API-0072C6?style=flat-square&logo=cloud&logoColor=white" alt="Meteoblue Badge" />
  </a>

  <!-- Ambiente -->
  <a href="https://pypi.org/project/python-dotenv/">
    <img src="https://img.shields.io/badge/-Dotenv-000000?style=flat-square&logo=python&logoColor=white" alt="Dotenv Badge" />
  </a>

  <!-- Status do projeto -->
  <img src="https://img.shields.io/badge/status-completo-brightgreen?style=flat-square" alt="Status Badge" />
</p>

![Gemini_Generated_Image_voioiivoioiivoio](https://github.com/user-attachments/assets/1f81099b-a0f3-4941-b0bc-e2df904918f7)

Esta é uma aplicação web feita com **Flask** que consome dados da API de clima da **Meteoblue**, armazena em um banco de dados relacional e exibe relatórios interativos com **gráficos** de temperatura, vento e precipitação.



## 🚀 Funcionalidades

- 🔄 Atualização **automática** dos dados meteorológicos a cada 6 horas.
- 📅 Filtro por intervalo de datas.
- 📊 Visualização dos dados em **gráficos** (Matplotlib e Plotly).
- 🗃️ Armazenamento persistente dos dados no banco de dados (PostgreSQL ou SQLite).
- 🌎 Consulta por latitude e longitude.
- ✅ Indicação da **última atualização** bem-sucedida dos dados.

---

## 🛠️ Stack Tecnológica

- 🐍 [Flask](https://flask.palletsprojects.com/) - Microframework web Python
- 🗃️ [SQLAlchemy](https://www.sqlalchemy.org/) - ORM para banco de dados SQL
- ⛅ [Meteoblue API](https://content.meteoblue.com/en/business-solutions/weather-apis) - API de previsão do tempo
- ⏱️ [APScheduler](https://apscheduler.readthedocs.io/) - Agendador de tarefas
- 📊 [Matplotlib](https://matplotlib.org/) - Biblioteca para visualização de dados
- 📈 [Plotly](https://plotly.com/) - Criação de gráficos interativos
- 🔑 [Python Dotenv](https://pypi.org/project/python-dotenv/) - Gerenciamento de variáveis de ambiente

---

## 🧪 Como executar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/weather-forecast-app.git
cd weather-forecast-app
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Crie um arquivo .env na raiz do projeto com o conteúdo:
```bash
METEOBLUE_API_KEY=sua_chave_api_aqui
```
Você pode obter uma chave da API no site da Meteoblue.

### 5. Execute a aplicação
```bash
python app.py
```
Acesse em http://localhost:5000.

## 🗃️ Banco de Dados
Por padrão, a aplicação usa o banco definido em config.py. Pode ser facilmente configurada para usar PostgreSQL, SQLite ou outro banco relacional.

As tabelas são criadas automaticamente na primeira execução.

## 🕒 Atualização Automática
Os dados são atualizados automaticamente a cada 6 horas com o uso do APScheduler.

A data/hora da última atualização bem-sucedida é salva em last_update.txt e exibida na interface do usuário.

## 📁 Estrutura do Projeto
```bash
weather-app/
├── app.py
├── config.py
├── models.py
├── meteoblue_api.py
├── db.py
├── requirements.txt
├── .env
├── templates/
│   └── index.html
├── static/
├── last_update.txt
```

## 📸 Exemplo da Interface
| 🟦 **Imagem 1** 🟦       | 🟦 **Imagem 2** 🟦       | 🟦 **Imagem 3** 🟦       | 🟦 **Imagem 4** 🟦       |
|--------------------------|--------------------------|--------------------------|--------------------------|
| ![Descrição1](https://github.com/user-attachments/assets/3ce68dfe-aba5-4cd1-9c0f-e6a16be99d73) | ![Descrição2](https://github.com/user-attachments/assets/e1f7bec9-2192-42ea-aba3-7051021ff756) | ![Descrição3](https://github.com/user-attachments/assets/475ca998-4a89-44ce-b2a7-4322845fcdcd) | ![Descrição4](https://github.com/user-attachments/assets/71f802b8-5a0a-416d-a74c-517f4aab7ecd) |
| *Tela Inicial*           | *Gráfico Temperatura*              | *Gráfico Interativo*              | *Previsão nos Próximos Dias*              |

## 📄 Licença
Este projeto está licenciado sob a MIT License.

## 🙋‍♂️ Contribuição
Contribuições são bem-vindas! Sinta-se livre para abrir issues ou pull requests.
