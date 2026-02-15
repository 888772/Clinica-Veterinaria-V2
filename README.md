# 🐾 VetClinic Manager

O **VetClinic Manager** é um sistema web robusto para a gestão de clínicas veterinárias. O projeto centraliza o controle de proprietários, animais, corpo clínico, agendamentos e registros de imunização em uma interface intuitiva e responsiva.

---

## 📝 Sobre o Desenvolvimento

Este software foi desenvolvido como um projeto prático unindo lógica de backend personalizada e interface moderna.
* **Backend:** A lógica de servidor e as rotas em Python/Flask foram construídas pelo desenvolvedor, utilizando como base a estrutura lógica fornecida pela IA **Gemini**.
* **Banco de Dados:** O sistema utiliza **Raw SQL (MySQL)** para manipulação de dados, sem o uso de ORMs (como Flask-SQLAlchemy), garantindo máxima performance e controle sobre as queries.
* **Frontend:** A interface visual e todos os templates HTML foram gerados pela IA **Gemini**, utilizando as tecnologias HTML5, Bootstrap 5 e ícones do FontAwesome.

---

## 🚀 Tecnologias Utilizadas

* **Linguagem:** [Python 3.x](https://www.python.org/)
* **Framework Web:** [Flask](https://flask.palletsprojects.com/)
* **Banco de Dados:** [MySQL](https://www.mysql.com/) (Consultas SQL puras).
* **Interface:** [Bootstrap 5.3](https://getbootstrap.com/) & [FontAwesome](https://fontawesome.com/).

---

## 📊 Estrutura do Banco de Dados

A arquitetura do banco foi desenhada para garantir a segurança dos dados e a persistência do histórico clínico:


* **Cliente:** Dados dos proprietários com integridade via CPF.
* **Pet:** Registro dos animais com vínculo `ON DELETE SET NULL` para o dono.
* **Veterinário:** Identificação via CRMV com `ON UPDATE CASCADE`.
* **Consulta:** Gestão de status (Reservada, Em Andamento, Concluída) e prontuário.
* **Vacina:** Histórico de imunização vinculado a cada Pet.

---

## 📂 Estrutura de Arquivos (Templates)

A organização dos arquivos de interface segue o padrão de visualização, cadastro e edição para cada módulo:

```text
templates/
├── index.html                  # Dashboard e Página Inicial
│
├── clientes.html               # Listagem de Clientes
├── cadastro_cliente.html       # Formulário de novo Cliente
├── editar_cliente.html         # Atualização de dados de Cliente
│
├── pets.html                   # Listagem de Pets
├── cadastro_pet.html           # Formulário de novo Pet
├── editar_pet.html             # Atualização de dados de Pet
│
├── veterinarios.html           # Listagem do Corpo Clínico
├── cadastro_veterinario.html   # Formulário de novo Veterinário
├── editar_veterinario.html     # Atualização de dados de Veterinário
│
├── consultas.html              # Painel de Agendamentos
├── cadastro_consulta.html      # Formulário de novo Agendamento
├── editar_consulta.html        # Atualização de Status e Prontuário
│
├── gerenciar_vacinas.html      # Histórico Geral de Vacinação
└── cadastro_vacinas.html       # Registro de aplicação de Vacina 
```
## 🛠️ Como Executar o Projeto
**Clone o repositório:**

Bash
git clone [https://github.com/seu-usuario/vetclinic-manager.git](https://github.com/seu-usuario/vetclinic-manager.git)

**Instale as dependências necessárias:**

Bash
pip install flask mysql-connector-python

**Configuração do Banco:**

Crie o banco de dados clinica_veterinaria no seu MySQL.

Execute os scripts DDL para criação das tabelas.

Certifique-se de que a string de conexão no app.py está correta.

**Rode a aplicação:**

Bash
python app.py ou flask run

Desenvolvido por José Guilherme Lima Ferreira
Design e Templates fornecidos por Gemini AI
