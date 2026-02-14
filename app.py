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


##### BACKEND DO SITE ##### 

@app.route("/")
def home():

    cnx = get_db()
    cursor_view = cnx.cursor(dictionary=True)

    if cnx is None:
        flash('Erro de conexão com o banco.', 'danger')
        return redirect(url_for('home'))

    sql = """SELECT 
            c.ID, 
            c.Data_Consulta, 
            c.Horas, 
            c.Status_Consulta,
            p.Nome AS pet_nome,
            cli.Nome AS dono_nome,
            v.Nome AS vet_nome
        FROM Consulta c
        JOIN Pet p ON c.ID_Pet = p.ID
        JOIN Cliente cli ON p.ID_Cliente = cli.ID
        LEFT JOIN Veterinario v ON c.CRMV = v.CRMV
        ORDER BY c.Data_Consulta DESC, c.Horas ASC
        LIMIT 10
        """

    cursor_view.execute(sql)
    consultas_view = cursor_view.fetchall()
    cursor_view.close()

    return render_template("index.html", consultas=consultas_view)

##### BARRA DE NAVEGAÇÃO #####

@app.route('/clientes', methods=['GET'])
def clientes():
    cnx = get_db()
    cursor = cnx.cursor(dictionary=True)

    sql = "SELECT * FROM Cliente ORDER BY Nome ASC"

    cursor.execute(sql)
    clientes = cursor.fetchall()
    cursor.close()
    
    return render_template('clientes.html', clientes=clientes)

@app.route('/pets')
def pets():

    cnx = get_db()
    cursor = cnx.cursor(dictionary=True)

    sql = """
        SELECT p.ID, p.Nome, p.Especie, p.Data_Nascimento, c.Nome as dono_nome
        FROM Pet p
        LEFT JOIN Cliente c ON p.ID_Cliente = c.ID
        ORDER BY p.ID ASC
    """

    cursor.execute(sql)
    pets_views = cursor.fetchall()
    cursor.close()

    return render_template('pets.html', pets=pets_views)

@app.route('/veterinarios', methods=['GET', 'POST'])
def veterinarios():
    cnx = get_db()
    cursor = cnx.cursor(dictionary=True)
    sql = "SELECT * FROM Veterinario ORDER BY Nome ASC"
    cursor.execute(sql)
    veterinarios = cursor.fetchall()
    cnx.close()
    return render_template('veterinarios.html', veterinarios=veterinarios)

@app.route('/vacinas', methods=['GET', 'POST'])
def gerenciar_vacinas():
    cnx = get_db()
    cursor_view = cnx.cursor(dictionary=True)
    cursor_get_pet = cnx.cursor(dictionary=True)

    cursor_get_pet.execute("SELECT Pet.ID, Pet.Nome, Cliente.Nome as dono_nome FROM Pet JOIN Cliente ON Pet.ID_Cliente = Cliente.ID ORDER BY Pet.Nome")
    pet_select = cursor_get_pet.fetchall()
    cursor_get_pet.close()

    cursor_view.execute("SELECT v.ID, v.Tipo, v.Marca, p.Nome as pet_nome, p.Especie as especie,c.Nome as dono_nome FROM Vacina v JOIN Pet p ON v.ID_Pet = p.ID JOIN Cliente c ON p.ID_Cliente = c.ID ORDER BY v.ID DESC")
    vacinas_view = cursor_view.fetchall()
    cursor_view.close()
    
    return render_template("gerenciar_vacinas.html", pets=pet_select, vacinas=vacinas_view)

##### (CADASTROS) #####

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
            flash('Pet cadastrado com sucesso!!', 'success')

######### FAZER PARA O VETERINARIO ADICIONAR O CLIENTE PELO NOME ESCOLHENDO EM UMA CAIXA
    cursor_get_cliente.execute("SELECT ID, Nome, CPF FROM Cliente ORDER BY Nome")
    clientes = cursor_get_cliente.fetchall()
    cursor_get_cliente.close()

    return render_template("cadastro_pet.html", clientes=clientes)

@app.route('/consultas/novo', methods=['POST','GET'])
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
            flash('Consulta cadastrada com sucesso!!', 'success')

    # METODO GET PARA PEGAR OS PETS E OS VETERINARIOS NO BVANCO DE DADOS PARA ADICIONAR NA LISTA DE ESCOLHAS
    cursor_get_pet.execute("SELECT Pet.ID, Pet.Nome, Cliente.Nome as dono_nome FROM Pet JOIN Cliente ON Pet.ID_Cliente = Cliente.ID ORDER BY Pet.Nome")
    pet_select = cursor_get_pet.fetchall()
    cursor_get_pet.close()

    cursor_get_vet.execute("SELECT CRMV, Nome, Especialidade FROM Veterinario ORDER BY Nome")
    veterinario_select = cursor_get_vet.fetchall()
    cursor_get_vet.close()

    return render_template("cadastro_consulta.html", pets=pet_select, veterinarios=veterinario_select)

@app.route('/veterinario/novo', methods=['GET', 'POST'])
def cadastrar_veterinario():

    cnx = get_db()
    cursor = cnx.cursor(dictionary=True)

    if request.method == 'POST':
        crmv = request.form.get('crmv')
        nome = request.form.get('nome')
        especialidade = request.form.get('especialidade')
        telefone = request.form.get('telefone')
        email = request.form.get('email')

        try:
            sql = "INSERT INTO Veterinario (CRMV, Nome, Especialidade, Telefone, Email) VALUES (%s, %s, %s, %s, %s)"
            
            valores = (crmv, nome, especialidade, telefone, email)
            
            cursor.execute(sql, valores)
            cnx.commit()
            flash('Veterinário cadastrado com sucesso!', 'success')
            return redirect(url_for('veterinarios'))
        except Exception as e:
            cnx.rollback()
            if "Duplicate entry" in str(e):
                flash('Este CRMV já está cadastrado!', 'danger')
            else:
                flash(f'Erro: {str(e)}', 'danger')

    return render_template('cadastro_veterinario.html')

@app.route('/vacinas/cadastrar', methods=['POST'])
def cadastrar_vacina():
    id_pet = request.form.get('id_pet')
    tipo = request.form.get('tipo')
    marca = request.form.get('marca')

    cnx = get_db()
    cursor = cnx.cursor()

    sql = "INSERT INTO Vacina (Marca, Tipo, ID_Pet) VALUES (%s, %s, %s)"

    valores = (marca, tipo, id_pet)

    try:
        cursor.execute(sql, valores)
        cnx.commit()
    except Error as err:
        return f"Erro ao cadastrar o pet: {err}", 500
    finally:
        cursor.close()
        flash('Vacina cadastrada com sucesso!!', 'success')
    return redirect(url_for('gerenciar_vacinas'))

#### EXCLUSÃO (VACINAS) ####

@app.route('/vacinas/excluir/<int:id>', methods=['POST'])
def excluir_vacina(id):
    cnx = get_db()
    cursor = cnx.cursor()
    try:
        sql = "DELETE FROM Vacina WHERE ID = %s LIMIT 1"
        cursor.execute(sql, (id,))
        cnx.commit()
        flash('Registro de vacina removido.', 'warning')
    except Exception as e:
        cnx.rollback()
        flash('Erro ao excluir.', 'danger')
    
    return redirect(url_for('gerenciar_vacinas'))

#### EDIÇÃO/EXCLUSÃO (CLIENTES) ####

@app.route('/clientes/excluir/<int:id>', methods=['POST'])
def excluir_cliente(id):
    cnx = get_db()
    cursor = cnx.cursor()
    try:
        sql = "DELETE FROM Cliente WHERE ID = %s LIMIT 1"
        cursor.execute(sql, (id,))
        cnx.commit()
        flash('Cliente excluído com sucesso. Os pets vinculados agora estão sem dono.', 'success')
    except Exception as e:
        cnx.rollback()
        flash('Erro ao excluir.', 'danger')
    return redirect(url_for('clientes'))

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):

    cnx = get_db()
    cursor = cnx.cursor(dictionary=True)

    if request.method == 'POST':
        # 1. Captura os novos dados
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        endereco = request.form.get('endereco')

        try:
            # 2. Executa o UPDATE
            sql = "UPDATE Cliente SET Nome = %s, Telefone = %s, Email = %s, Endereco = %s WHERE ID = %s"

            valores = (nome, telefone, email, endereco, id)

            cursor.execute(sql, valores)
            cnx.commit()
            flash('Cliente atualizado com sucesso!', 'success')
            return redirect(url_for('clientes'))
        
        except Exception as e:
            cnx.rollback()
            flash(f'Erro ao atualizar: {str(e)}', 'danger')
            return redirect(url_for('clientes'))

    # GET → carregar cliente
    cursor.execute("SELECT * FROM Cliente WHERE ID = %s", (id,))
    cliente = cursor.fetchone()
    cursor.close()

    if not cliente:
        flash('Cliente não encontrado!', 'danger')
        return redirect(url_for('clientes'))
        
    return render_template('editar_cliente.html', cliente=cliente)

#### EDIÇÃO/EXCLUSÃO (PETS) ####

@app.route('/pets/excluir/<int:id>', methods=['POST'])
def excluir_pet(id):

    cnx = get_db()
    cursor = cnx.cursor()

    try:
        sql = "DELETE FROM Pet WHERE ID = %s"
        cursor.execute(sql, (id,))
        cnx.commit()
        flash('Registo do pet removido com sucesso.', 'success')
    except Exception as e:
        cnx.rollback()
        # Caso exista uma restrição nas Vacinas ou Consultas associadas ao Pet
        flash(f'Erro ao excluir: {str(e)}', 'danger')
        
    return redirect(url_for('pets'))

@app.route('/pets/editar/<int:id>', methods=['GET', 'POST'])
def editar_pet(id):

    cnx = get_db()
    cursor = cnx.cursor(dictionary=True)
    cursor_cliente = cnx.cursor(dictionary=True)

    if request.method == 'POST':
        nome = request.form.get('nome')
        especie = request.form.get('especie')
        data_nascimento = request.form.get('data_nascimento')
        id_cliente = request.form.get('id_cliente')
        
        # Se o utilizador selecionar a opção "Sem proprietário" (valor vazio)
        if not id_cliente:
            id_cliente = None

        try:
            sql = "UPDATE Pet SET Nome = %s, Especie = %s, Data_Nascimento = %s, ID_Cliente = %s WHERE ID = %s"

            valores = (nome, especie, data_nascimento, id_cliente, id)

            cursor.execute(sql, valores)
            cnx.commit()
            flash('Pet atualizado com sucesso!', 'success')
            return redirect(url_for('pets'))
        
        except Exception as e:
            cursor.rollback()
            flash(f'Erro ao atualizar pet: {str(e)}', 'danger')
            return redirect(url_for('pets'))

    # Se for GET: Buscar dados do Pet selecionado
    cursor.execute("SELECT * FROM Pet WHERE ID = %s", (id,))
    pet = cursor.fetchone()
    cursor.close()
    
    if not pet:
        flash('Pet não encontrado!', 'danger')
        return redirect(url_for('pets'))
        
    # Buscar lista de clientes para preencher o <select> do HTML
    cursor_cliente.execute("SELECT ID, Nome, CPF FROM Cliente ORDER BY Nome ASC")
    clientes = cursor_cliente.fetchall()
    cursor_cliente.close()

    if not clientes:
        flash('Clientes não encontrado!', 'danger')
        return redirect(url_for('pets'))
    
    return render_template('editar_pet.html', pet=pet, clientes=clientes)

#### EDIÇÃO/EXCLUSÃO (VETERINARIOS) ####

@app.route('/veterinario/editar/<int:id>', methods=['GET', 'POST'])
def editar_veterinario(id):

    cnx = get_db()
    cursor = cnx.cursor(dictionary=True)

    if request.method == 'POST':
        crmv = request.form.get('crmv')
        nome = request.form.get('nome')
        especialidade = request.form.get('especialidade')
        telefone = request.form.get('telefone')
        email = request.form.get('email')

        try:
            # O MySQL fará o CASCADE do CRMV para a tabela Consultas automaticamente!
            sql = """
                UPDATE Veterinario 
                SET CRMV = %s, Nome = %s, Especialidade = %s, 
                    Telefone = %s, Email = %s 
                WHERE ID = %s
            """

            valores = (crmv, nome, especialidade, telefone, email, id)

            cursor.execute(sql, valores)
            cnx.commit()
            flash('Dados do veterinário atualizados!', 'success')
            return redirect(url_for('veterinarios'))
        except Exception as e:
            cnx.rollback()
            if "Duplicate entry" in str(e):
                flash('O CRMV inserido já pertence a outro profissional.', 'danger')
            else:
                flash(f'Erro ao atualizar: {str(e)}', 'danger')
            return redirect(url_for('veterinarios'))
    cursor.execute("SELECT * FROM Veterinario WHERE ID = %s", (id,))
    vet = cursor.fetchone()
    cnx.close()
    if not vet:
        flash('Veterinário não encontrado!', 'danger')
        return redirect(url_for('veterinarios'))
        
    return render_template('editar_veterinario.html', vet=vet)

# 4. EXCLUIR VETERINÁRIO
@app.route('/veterinarios/excluir/<int:id>', methods=['POST'])
def excluir_veterinario(id):

    cnx = get_db()
    cursor = cnx.cursor(dictionary=True)

    try:
        sql = "DELETE FROM Veterinario WHERE ID = %s"
        cursor.execute(sql, (id,))
        cnx.commit()
        flash('Veterinário removido. Consultas associadas agora estão sem médico (NULL).', 'warning')
    except Exception as e:
        cnx.rollback()
        flash(f'Erro ao excluir: {str(e)}', 'danger')
        
    return redirect(url_for('veterinarios'))

if __name__ == "__main__":
    app.run(debug=True) # debug=True ativa o recarregamento automático