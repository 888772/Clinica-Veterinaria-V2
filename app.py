from flask import Flask, render_template, request, g, redirect, session, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

app.secret_key = 'sua_chave_secreta_aqui' 

def connect_database():
    try:
        cnx = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="",
            database="clinica_veterianria"
        )
        return cnx

    except Error as err:
        print(f"Erro ao conectar no MySQL: {err}")
        return None

def get_db():
    if 'db' not in g:
        g.db = connect_database()
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/clientes/novo', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        endereco = request.form.get('endereco')

        cnx = get_db()

        if not nome or not cpf:
            flash('Nome e CPF são obrigatórios!', 'danger')
            return render_template("cadastro_cliente.html")
        if not telefone:
            flash('Telefone é obrigatório!', 'danger')
            return render_template("cadastro_cliente.html")
        if not email:
            flash('Email é obrigatório!', 'danger')
            return render_template("cadastro_cliente.html")
        if not endereco:
            flash('Endereço é obrigatório!', 'danger')
            return render_template("cadastro_cliente.html")

        cursor = cnx.cursor()

        sql = "INSERT INTO Cliente (Nome, Endereco, Telefone, Email, CPF) VALUES (%s, %s, %s, %s, %s)"

        valores = (nome, endereco, telefone, email, cpf)

        try:
            cursor.execute(sql, valores)
            cnx.commit()
        except Error as err:
            return f"Erro ao cadastrar cliente: {err}", 500
        finally:
            cursor.close()
            flash('Cliente cadastrado com sucesso!!', 'success')
        

    return render_template("cadastro_cliente.html")

@app.route('/pets/novo', methods=['POST', 'GET'])
def cadastrar_pet():

    cnx = get_db()
    cursor = cnx.cursor(dictionary=True)

    cursor.execute("SELECT ID, Nome, CPF FROM Cliente ORDER BY Nome")
    clientes = cursor.fetchall()
    cursor.close()

    if request.method == 'POST':
        nome = request.form.get('nome')
        especie = request.form.get('especie')
        data_nascimento = request.form.get('data_nascimento')
        id_cliente = request.form.get('id_cliente')

        if not nome:
            flash('O Nome é Obrigatorio!', 'danger')
            return redirect(url_for('cadastro_pet'))
        if not especie:
            flash('A Espécie é Obrigatoria!', 'danger')
            return redirect(url_for('cadastro_pet'))
        if not id_cliente:
            flash('O ID do cliente/Tutor é Obrigatório!')
            return redirect(url_for('cadastro_pet'))


        sql = "INSERT INTO Pet (Nome, Data_Nascimento, Especie, ID_Cliente) VALUES (%s, %s, %s, %s)"

        valores = (nome, data_nascimento, especie, id_cliente)

        try:
            cursor.execute(sql, valores)
            cnx.commit()
        except Error as err:
            return f"Erro ao cadastrar o pet: {err}", 500
        finally:
            cursor.close()

######### FAZER PARA O VETERINARIO ADICIONAR O CLIENTE PELO NOME ESCOLHENDO EM UMA CAIXA

    return render_template("cadastro_pet.html")

if __name__ == "__main__":
    app.run(debug=True) # debug=True ativa o recarregamento automático