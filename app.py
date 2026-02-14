from flask import Flask, render_template, request, g, redirect, session, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

app.secret_key = 'tr4b4lh0_d3_b4nc0_d3_d4d02' 

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
    cursor_post = cnx.cursor(dictionary=True)
    cursor_get_cliente = cnx.cursor(dictionary=True)

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
            cursor_post.execute(sql, valores)
            cnx.commit()
        except Error as err:
            return f"Erro ao cadastrar o pet: {err}", 500
        finally:
            cursor_post.close()

######### FAZER PARA O VETERINARIO ADICIONAR O CLIENTE PELO NOME ESCOLHENDO EM UMA CAIXA
    cursor_get_cliente.execute("SELECT ID, Nome, CPF FROM Cliente ORDER BY Nome")
    clientes = cursor_get_cliente.fetchall()
    cursor_get_cliente.close()

    return render_template("cadastro_pet.html", clientes=clientes)

@app.route('/consultas/novo', methods=('POST','GET'))
def cadastrar_consulta():

    cnx = get_db()
    cursor_post = cnx.cursor(dictionary=True)
    cursor_get_pet = cnx.cursor(dictionary=True)
    cursor_get_vet = cnx.cursor(dictionary=True)
    
    if request.method == 'POST':
        data_consulta = request.form.get('data_consulta')
        horas = request.form.get('horas')
        id_pet = request.form.get('id_pet')
        crmv = request.form.get('crmv')
        status = request.form.get('status')
        valor = request.form.get('valor') or 0.0
        observacoes = request.form.get('observacoes')

        if not data_consulta:
            flash('A Data da Consulta é Obrigatoria!', 'danger')
            return redirect(url_for('cadastro_consulta'))
        if not horas:
            flash('A hora é Obrigatoria!', 'danger')
            return redirect(url_for('cadastro_consulta'))
        if not id_pet:
            flash('O Pet é Obrigatorio!', 'danger')
            return redirect(url_for('cadastro_consulta'))
        if not crmv:
            flash('O CRMV é Obrigatorio!', 'danger')
            return redirect(url_for('cadastro_consulta'))
        if not status:
            flash('O Status é Obrigatorio!', 'danger')
            return redirect(url_for('cadastro_consulta'))
        if not valor:
            flash('O valor é Obrigatorio!', 'danger')
            return redirect(url_for('cadastro_consulta'))
        if not observacoes:
            flash('A Observação é Obrigatoria!', 'danger')
            return redirect(url_for('cadastro_consulta'))

        sql = "INSERT INTO Consulta (Data_Consulta, Horas, Observacoes, Valor, Status_Consulta, ID_Pet, CRMV) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        
        valores = (data_consulta, horas, observacoes, valor, status, id_pet, crmv)

        try:
            cursor_post.execute(sql, valores)
            cnx.commit()
        except Error as err:
            return f"Erro ao cadastrar o pet: {err}", 500
        finally:
            cursor_post.close()
    # METODO GET PARA PEGAR OS PETS E OS VETERINARIOS NO BVANCO DE DADOS PARA ADICIONAR NA LISTA DE ESCOLHAS
    cursor_get_pet.execute("SELECT Pet.ID, Pet.Nome, Cliente.Nome as dono_nome FROM Pet JOIN Cliente ON Pet.ID_Cliente = Cliente.ID ORDER BY Pet.Nome")
    pet_select = cursor_get_pet.fetchall()
    cursor_get_pet.close()

    cursor_get_vet.execute("SELECT CRMV, Nome, Especialidade FROM Veterinario ORDER BY Nome")
    veterinario_select = cursor_get_vet.fetchall()
    cursor_get_vet.close()

    return render_template("cadastro_consulta.html", pets=pet_select, veterinarios=veterinario_select)

if __name__ == "__main__":
    app.run(debug=True) # debug=True ativa o recarregamento automático