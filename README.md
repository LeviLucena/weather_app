# 🌤️ Weather Forecast App

Esta é uma aplicação web feita com **Flask** que consome dados da API de clima da **Meteoblue**, armazena em um banco de dados relacional e exibe relatórios interativos com **gráficos** de temperatura, vento e precipitação.

![image](https://github.com/user-attachments/assets/3ce68dfe-aba5-4cd1-9c0f-e6a16be99d73)

## 🚀 Funcionalidades

- 🔄 Atualização **automática** dos dados meteorológicos a cada 6 horas.
- 📅 Filtro por intervalo de datas.
- 📊 Visualização dos dados em **gráficos** (Matplotlib e Plotly).
- 🗃️ Armazenamento persistente dos dados no banco de dados (PostgreSQL ou SQLite).
- 🌎 Consulta por latitude e longitude.
- ✅ Indicação da **última atualização** bem-sucedida dos dados.

---

## 🛠️ Tecnologias Utilizadas

- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Meteoblue API](https://content.meteoblue.com/en/business-solutions/weather-apis)
- [APScheduler](https://apscheduler.readthedocs.io/)
- [Matplotlib](https://matplotlib.org/)
- [Plotly](https://plotly.com/)
- [Python Dotenv](https://pypi.org/project/python-dotenv/)

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
| 🟦 **Imagem 1** 🟦       | 🟦 **Imagem 2** 🟦       | 🟦 **Imagem 3** 🟦       |
|--------------------------|--------------------------|--------------------------|
| ![Descrição1](https://github.com/user-attachments/assets/e1f7bec9-2192-42ea-aba3-7051021ff756) | ![Descrição2](https://github.com/user-attachments/assets/475ca998-4a89-44ce-b2a7-4322845fcdcd) | ![Descrição3](https://github.com/user-attachments/assets/71f802b8-5a0a-416d-a74c-517f4aab7ecd) |
| *Gráfico Temperatura*              | *Gráfico Interativo*              | *Previsão nos Próximos Dias*              |

## 📄 Licença
Este projeto está licenciado sob a MIT License.

## 🙋‍♂️ Contribuição
Contribuições são bem-vindas! Sinta-se livre para abrir issues ou pull requests.
