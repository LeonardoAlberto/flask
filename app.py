from criandopix import criar_pix
from flask import Flask, render_template, request, redirect, session, jsonify, flash
from conexao import add_user
import mysql.connector
from datetime import timedelta, datetime
import datetime
import requests
import base64
import bcrypt
from teste import aumentar, validar_data_hora

# CustomerFlow

db_creditos = {
    'user': 'admin',
    'password': 'Ladas2015',
    'host': 'database-1.crpptqrdm74l.us-east-1.rds.amazonaws.com',
    'database': 'creditos'
}
db_database = {
    'user': 'admin',
    'password': 'Ladas2015',
    'host': 'database-1.crpptqrdm74l.us-east-1.rds.amazonaws.com',
    'database': 'database'
}
db_console = {
    'user': 'admin',
    'password': 'Ladas2015',
    'host': 'database-1.crpptqrdm74l.us-east-1.rds.amazonaws.com',
    'database': 'console'
}

app = Flask(__name__)

app.secret_key = "@sd2¨21%d2$#rd1ed12&21@"
app.permanent_session_lifetime = timedelta(minutes=120)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        banco_creditos = mysql.connector.connect(**db_creditos)
        cursor_creditos = banco_creditos.cursor()

        sql = 'SELECT senha FROM creditos WHERE usuario = %s'
        val = usuario,
        cursor_creditos.execute(sql, val)
        senha_bd = cursor_creditos.fetchall()

        banco_creditos.commit()
        cursor_creditos.close()

        try:
            if senha_bd:
                if bcrypt.checkpw(senha.encode('utf-8'), senha_bd[0][0].encode('utf-8')):
                    session["user"] = usuario.lower()
                    return redirect("/painel")
                else:
                    flash(u'A senha inserida esta invalida.', 'error')
            else:
                flash(u'Usuario não foi encontrado no Banco de dados.', 'error')
        except:
            print('Erro no login')

    return render_template("login.html", erro="")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        senha_confirm = request.form['senha_confirm']
        numero = request.form['numero']

        if senha == senha_confirm:
            if len(senha) > 5:
                if len(numero) == 15:
                    if len(usuario) > 5:
                        if not any(char.isspace() for char in usuario) and not any(
                                char.isspace() for char in senha_confirm):

                            if any(c.isalpha() for c in usuario):
                                try:
                                    banco_database = mysql.connector.connect(**db_database)
                                    cursor_database = banco_database.cursor()

                                    banco_console = mysql.connector.connect(**db_console)
                                    cursor_console = banco_console.cursor()

                                    banco_creditos = mysql.connector.connect(**db_creditos)
                                    cursor_creditos = banco_creditos.cursor()

                                    sql = "CREATE TABLE IF NOT EXISTS {} (nome  VARCHAR(255),vencimento VARCHAR(255) UNIQUE, numero VARCHAR(255),valor int, plano VARCHAR(255),id VARCHAR(255),adicionado VARCHAR(255) )".format(
                                        usuario.lower())
                                    cursor_database.execute(sql)

                                    sql = "CREATE TABLE IF NOT EXISTS {} (nome  VARCHAR(255),horario VARCHAR(255), numero VARCHAR(255), descricao VARCHAR(255),status VARCHAR(255) )".format(
                                        usuario.lower())
                                    cursor_console.execute(sql)

                                    numero_correto = numero.replace("(", "").replace(
                                        ")", "").replace("-", "").replace(" ", "")

                                    senha_bytes = senha.encode('utf-8')
                                    salt = bcrypt.gensalt()
                                    hash_senha = bcrypt.hashpw(senha_bytes, salt)

                                    sql = 'INSERT INTO creditos Values(%s,%s,%s,%s)'
                                    val = (usuario, hash_senha, 0, numero_correto)
                                    cursor_creditos.execute(sql, val)

                                    sql = 'INSERT INTO imagens Values(%s,"","offline")'
                                    val = (usuario,)
                                    cursor_creditos.execute(sql, val)

                                    banco_database.commit()
                                    banco_creditos.commit()
                                    banco_console.commit()
                                    cursor_database.close()
                                    cursor_console.close()
                                    cursor_creditos.close()
                                    flash(u'Usuario criado com sucesso volte a pagina de login!', 'success')
                                except:
                                    flash(u'Usuario ja existente.', 'error')
                            else:
                                flash(u'O nome de usuario precisa conter alguma letra.', 'warn')
                        else:
                            flash(u'Os dados abaixo nao podem conter espaços.', 'warn')
                    else:
                        flash(u'O nome de usuario precisa conter no minimo 6 caracteres.', 'error')
                else:
                    flash(u'Verifique se esta correto seu numero.', 'warn')
            else:
                flash(u'A senha deve conter no minimo 6 caracteres.', 'warn')
        else:
            flash(u'A senhas devem ser iguais.', 'error')

    return render_template("register.html", erro="")


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if "user" in session:
        user = session["user"]
        if request.method == 'POST':
            usuario = user
            senha_atual = request.form['senha_atual']
            senha_nova = request.form['senha_nova']
            senha_confirm = request.form['senha_confirm']

            banco_creditos = mysql.connector.connect(**db_creditos)
            cursor_creditos = banco_creditos.cursor()

            sql = 'SELECT senha FROM creditos WHERE usuario = %s'
            val = usuario,
            cursor_creditos.execute(sql, val)
            hash_armazenado = cursor_creditos.fetchall()[0][0]
            hash_bytes = hash_armazenado.encode('utf-8')
            if not any(char.isspace() for char in senha_nova):
                if bcrypt.checkpw(senha_atual.encode('utf-8'), hash_bytes):
                    if senha_nova == senha_confirm:
                        if not senha_atual.encode('utf-8') == senha_nova.encode('utf-8'):
                            if len(senha_nova) > 5:

                                senha_bytes = senha_confirm.encode('utf-8')
                                salt = bcrypt.gensalt()
                                hash_senha = bcrypt.hashpw(senha_bytes, salt)

                                sql = 'UPDATE creditos SET senha = %s WHERE usuario = %s'
                                val = (hash_senha, usuario)
                                cursor_creditos.execute(sql, val)

                                banco_creditos.commit()
                                cursor_creditos.close()
                                flash(u'Senha alterada com sucesso!', 'success')
                            else:
                                flash(u'A nova senha deve ter no minimo 6 caracteres.', 'warn')
                        else:
                            flash(u'A nova senha deve ser diferente da antiga.', 'warn')
                    else:
                        flash(u'As senhas devem ser iguais.', 'warn')
                else:
                    flash(u'A sua senha esta incorreta.', 'error')
            else:
                flash(u'A sua senha nao pode conter espaço.', 'error')

        return render_template("profile.html", user=user)
    else:
        return redirect('/')


@app.route('/painel', methods=['GET', 'POST'])
def painel():
    if "user" in session:
        user = session["user"]

        banco_creditos = mysql.connector.connect(**db_creditos)
        cursor_creditos = banco_creditos.cursor()

        sql = 'SELECT creditos FROM creditos WHERE usuario = %s'
        val = (user,)
        cursor_creditos.execute(sql, val)

        creditos_total = cursor_creditos.fetchall()
        cursor_creditos.close()

        return render_template("painel.html", user=user, creditos_total=creditos_total[0][0])
    else:
        return redirect('/')


@app.route('/status_creditos', methods=['GET', 'POST'])
def status_creditos():
    if "user" in session:
        user = session["user"]

        banco_creditos = mysql.connector.connect(**db_creditos)
        cursor_creditos = banco_creditos.cursor()

        sql = 'SELECT creditos FROM creditos WHERE usuario = %s'
        val = (user,)
        cursor_creditos.execute(sql, val)
        creditos_total = cursor_creditos.fetchall()[0][0]
        cursor_creditos.close()
        return jsonify(creditos_total)


@app.route('/conectar', methods=['GET', 'POST'])
def conectar():
    if "user" in session:
        user = session["user"]
        banco_creditos = mysql.connector.connect(**db_creditos)
        cursor_creditos = banco_creditos.cursor()
        sql = 'SELECT * FROM imagens WHERE usuario = %s'
        val = (user,)
        cursor_creditos.execute(sql, val)
        dados = cursor_creditos.fetchall()

        imagem = dados[0][1]
        imagem_codificada = base64.b64encode(imagem).decode('utf-8')

        return render_template("connectar.html", user=user, status=dados[0][2], imagem=imagem_codificada)
    else:
        return redirect('/')


@app.route('/status', methods=['GET', 'POST'])
def status():
    if "user" in session:
        user = session["user"]
        banco_creditos = mysql.connector.connect(**db_creditos)
        cursor_creditos = banco_creditos.cursor()

        sql = 'SELECT status FROM imagens WHERE usuario = %s'
        val = (user,)
        cursor_creditos.execute(sql, val)

        return jsonify(cursor_creditos.fetchall()[0][0])
    else:
        return redirect('/')


@app.route('/imagem', methods=['GET', 'POST'])
def imagem():
    if "user" in session:
        user = session["user"]
        banco_creditos = mysql.connector.connect(**db_creditos)
        cursor_creditos = banco_creditos.cursor()

        sql = 'SELECT * FROM imagens WHERE usuario = %s'
        val = (user,)
        cursor_creditos.execute(sql, val)

        dados = cursor_creditos.fetchall()

        imagem = dados[0][1]
        imagem_codificada = base64.b64encode(imagem).decode('utf-8')
        return jsonify(imagem_codificada)


@app.route('/habilitar/<usuario>', methods=['GET', 'POST'])
def habilitar(usuario):
    if "user" in session:
        user = session["user"]
        if user == usuario:
            banco_creditos = mysql.connector.connect(**db_creditos)
            cursor_creditos = banco_creditos.cursor()

            sql = 'SELECT * FROM creditos WHERE usuario = %s'
            val = (user,)
            cursor_creditos.execute(sql, val)

            creditos_atual = cursor_creditos.fetchall()[0][2]
            if creditos_atual > 0:
                sql = 'SELECT status FROM imagens WHERE usuario = %s'
                val = (user,)
                cursor_creditos.execute(sql, val)

                status_atual = cursor_creditos.fetchall()[0][0]
                if status_atual == "offline":

                    sql = 'UPDATE imagens SET status = "ativo" WHERE usuario = %s'
                    val = (user,)
                    cursor_creditos.execute(sql, val)

                    sql = 'UPDATE imagens SET imagem = "" WHERE usuario = %s'
                    val = (user,)
                    cursor_creditos.execute(sql, val)

                    banco_creditos.commit()
                    cursor_creditos.close()
                    return redirect('/conectar')
                else:
                    flash(u'Voce ja contem uma instancia online.', 'error')
                    return redirect('/conectar')
            else:
                flash(u'Voce precisa ter pelo menos 1 credito para ativar uma instancia.', 'warn')
                return redirect('/conectar')
        else:
            flash(u'Voce não tem permissao para isso.', 'error')
            return redirect('/conectar')
    else:
        return redirect("/")


@app.route('/desabilitar/<usuario>', methods=['GET', 'POST'])
def desabilitar(usuario):
    if "user" in session:
        user = session["user"]
        if user == usuario:
            banco_creditos = mysql.connector.connect(**db_creditos)
            cursor_creditos = banco_creditos.cursor()

            sql = 'SELECT status FROM imagens WHERE usuario = %s'
            val = (user,)
            cursor_creditos.execute(sql, val)
            status_atual = cursor_creditos.fetchall()[0][0]

            if status_atual == "online":
                sql = 'UPDATE imagens SET status = "desabilitar" WHERE usuario = %s'
                val = (user,)
                cursor_creditos.execute(sql, val)

                banco_creditos.commit()
                cursor_creditos.close()
                flash(u'Desabilitando com sucesso...', 'success')
                return redirect("/conectar")
            else:
                flash(u"Você não possui nenhuma instância online.", "warn")
                return redirect("/conectar")
        else:
            flash(u'Voce não tem permissao para isso.', 'error')
            return redirect("/conectar")
    else:
        return redirect('/')


@app.route('/criar', methods=['GET', 'POST'])
def criar():
    if "user" in session:
        user = session["user"]
        if request.method == 'POST':
            nome = request.form['cliente']
            vencimento = request.form['vencimento'].replace(
                "-", "/").replace("T", "-")
            numero = request.form['numero']
            valor = request.form['valor']
            plano = request.form['plano']

            if len(vencimento) == 16:
                if validar_data_hora(vencimento):
                    numero_1 = f"+55{numero.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')}"

                    status = add_user(nome=nome, vencimento=vencimento,
                                      numero=numero_1, valor=valor, plano=plano, user=user)

                    if status:
                        return redirect("/painel")
                    else:
                        flash(u'Não pode haver dois logins com o mesmo horario de vencimento, Altere o minuto.', 'warn')
                else:
                    flash(u'Data invalida.', 'error')
            else:
                flash(u'Verifique se esta correto a data de vencimento.', 'error')
        return render_template("criar.html")
    else:
        return redirect('/')


@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    if "user" in session:
        user = session["user"]

        banco_database = mysql.connector.connect(**db_database)
        cursor_database = banco_database.cursor()
        banco_database.commit()

        banco_database.commit()
        sql = 'SELECT * FROM {} ORDER BY adicionado DESC'.format(user)
        cursor_database.execute(sql)

        clientes = cursor_database.fetchall()
        banco_database.commit()
        cursor_database.close()
        return render_template("usuarios.html", len=len(clientes), clientes=clientes)
    else:
        return redirect('/')


@app.route('/historico', methods=['GET', 'POST'])
def historico():
    if "user" in session:
        user = session["user"]

        banco_console = mysql.connector.connect(**db_console)
        cursor_console = banco_console.cursor()

        banco_console.commit()

        sql = "SELECT * FROM {} ORDER BY horario DESC".format(user)
        cursor_console.execute(sql)

        clientes = cursor_console.fetchall()

        banco_console.commit()
        cursor_console.close()
        return render_template("console.html", len=len(clientes), clientes=clientes)
    else:
        return redirect('/')


@app.route('/usuarios/<categoria>/<pesquisa>', methods=['GET', 'POST'])
def pesquisar_usuarios(categoria, pesquisa):
    if "user" in session:
        user = session["user"]

        categorias_aceitas = ['id', 'nome', 'adicionado', 'vencimento', 'numero', 'valor', 'plano']

        if not categoria in categorias_aceitas:
            return 'Categoria incorreta.'

        banco_database = mysql.connector.connect(**db_database)
        cursor_database = banco_database.cursor()

        banco_database.commit()

        sql = "SELECT * FROM {} WHERE {} LIKE %s".format(user, categoria)
        val = ('%' + pesquisa + '%',)
        cursor_database.execute(sql, val)

        clientes = cursor_database.fetchall()

        banco_database.commit()
        cursor_database.close()
        return render_template("usuarios.html", len=len(clientes), clientes=clientes)
    else:
        return redirect('/')


@app.route('/usuarios/ordenar/<categoria>', methods=['GET', 'POST'])
def ordenar_usuarios(categoria):
    if "user" in session:
        user = session["user"]

        categorias_aceitas = ['id', 'nome', 'adicionado', 'vencimento', 'numero', 'valor', 'plano']

        if not categoria in categorias_aceitas:
            return 'Categoria incorreta.'

        banco_database = mysql.connector.connect(**db_database)
        cursor_database = banco_database.cursor()

        if session.get('sort_order') == 'asc':
            sort_order = 'DESC'
            session['sort_order'] = 'desc'
        else:
            sort_order = 'ASC'
            session['sort_order'] = 'asc'

        sql = "SELECT * FROM {} ORDER BY {} {}".format(user, categoria, sort_order)
        cursor_database.execute(sql)

        clientes = cursor_database.fetchall()

        cursor_database.close()
        return render_template("usuarios.html", len=len(clientes), clientes=clientes)
    else:
        return redirect('/')


@app.route('/usuarios/<id>', methods=['GET', 'POST'])
def usuarios_select(id):
    if "user" in session:
        user = session["user"]

        banco_database = mysql.connector.connect(**db_database)
        cursor_database = banco_database.cursor()

        sql = "SELECT * FROM {} WHERE id = %s".format(user)
        val = (id,)
        cursor_database.execute(sql, val)

        cliente = cursor_database.fetchall()[0]

        data_hora = datetime.datetime.strptime(cliente[1], "%Y/%m/%d-%H:%M")
        data_hora_iso = data_hora.isoformat()

        banco_database.commit()
        if request.method == 'POST':
            nome = request.form['cliente']
            vencimento = request.form['vencimento'].replace(
                "-", "/").replace("T", "-")
            numero = request.form['numero']
            valor = request.form['valor']
            plano = request.form['plano']

            if len(vencimento) == 16:
                sql = "UPDATE {} SET nome = %s WHERE id = %s".format(user)
                val = (nome, cliente[5])
                cursor_database.execute(sql, val)
                try:
                    sql = "UPDATE {} SET vencimento = %s WHERE id = %s".format(user)
                    val = (vencimento, cliente[5])
                    cursor_database.execute(sql, val)
                except:
                    flash(u'Não pode haver dois logins com o mesmo horario de vencimento, Altere o minuto.', 'warn')
                    return render_template("editar_usuario.html",
                                           nome_cliente=cliente[0], vencimento=data_hora_iso, numero=cliente[2],
                                           valor=cliente[3], plano=cliente[4], usuarios_select=usuarios_select,
                                           id=cliente[5])

                if not numero == cliente[2]:
                    numero_1 = f"+55{numero.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')}"
                    sql = "UPDATE {} SET numero = %s WHERE id = %s".format(user)
                    val = (numero_1, cliente[5])
                    cursor_database.execute(sql, val)

                sql = "UPDATE {} SET valor = %s WHERE id = %s".format(user)
                val = (str(valor), cliente[5])
                cursor_database.execute(sql, val)

                sql = "UPDATE {} SET plano = %s WHERE id = %s".format(user)
                val = (plano, cliente[5])
                cursor_database.execute(sql, val)

                banco_database.commit()
                cursor_database.close()
                return redirect("/usuarios")
            else:
                flash(u'Verifique se esta correta a data de vencimento.', 'warn')
                return render_template("editar_usuario.html",
                                       nome_cliente=cliente[0], vencimento=data_hora_iso, numero=cliente[2],
                                       valor=cliente[3], plano=cliente[4], usuarios_select=usuarios_select,
                                       id=cliente[5])

        return render_template("editar_usuario.html", nome_cliente=cliente[0], vencimento=data_hora_iso,
                               numero=cliente[2],
                               valor=cliente[3], plano=cliente[4], usuarios_select=usuarios_select, id=cliente[5])
    else:
        return redirect('/')


@app.route('/usuarios/deletar/<id>', methods=['GET', 'POST'])
def usuario_delete(id):
    if "user" in session:
        user = session["user"]

        banco_database = mysql.connector.connect(**db_database)
        cursor_database = banco_database.cursor()

        sql = "SELECT * FROM {} WHERE id = %s".format(user)
        val = (id,)
        cursor_database.execute(sql, val)

        cliente = cursor_database.fetchall()[0][0]
        cursor_database.close()

        return render_template("deletar.html", id=id, cliente=cliente)


@app.route('/usuarios/deletar/confirm/<id>', methods=['GET', 'POST'])
def usuario_delete_confirm(id):
    if "user" in session:
        user = session["user"]

        banco_database = mysql.connector.connect(**db_database)
        cursor_database = banco_database.cursor()

        sql = "DELETE FROM {} WHERE id = %s".format(user)
        val = (id,)
        cursor_database.execute(sql, val)

        banco_database.commit()
        cursor_database.close()
        return redirect("/usuarios")


@app.route('/usuarios/renovar/<id>', methods=['GET', 'POST'])
def usuario_renovar(id):
    if "user" in session:
        user = session["user"]

        banco_database = mysql.connector.connect(**db_database)
        cursor_database = banco_database.cursor()

        sql = "SELECT * FROM {} WHERE id = %s".format(user)
        val = (id,)
        cursor_database.execute(sql, val)

        cliente = cursor_database.fetchall()[0][0]
        cursor_database.close()

        return render_template("add_mes.html", id=id, cliente=cliente)


@app.route('/renovar/<id>/<meses>', methods=['GET', 'POST'])
def usuario_renovar_confirm(id, meses):
    if "user" in session:
        user = session["user"]

        if not meses.isnumeric():
            return 'Adicione numeros em meses!'

        try:
            banco_database = mysql.connector.connect(**db_database)
            cursor_database = banco_database.cursor()

            sql = 'SELECT vencimento FROM {} WHERE id = %s'.format(user)
            val = (id,)
            cursor_database.execute(sql, val)

            data_atual = cursor_database.fetchall()[0][0]
            data_atual_formatada = data_atual[0:10].replace('/', '-')
            horario_atual = data_atual[11:16]

            nova_data = aumentar(int(meses), data_atual_formatada)
            nova_data_formatada = str(nova_data).replace('-', '/')[0:10]
            data_final = f'{nova_data_formatada}-{horario_atual}'

            sql = 'UPDATE {} SET vencimento = %s WHERE id = %s'.format(user)
            val = (data_final, id)
            cursor_database.execute(sql, val)

            return redirect("/usuarios")
        except:
            flash(u'Falha na renovaçao, Realize manualmente', 'warn')
            return redirect("/usuarios")
        finally:
            banco_database.commit()
            cursor_database.close()
    else:
        return 'Sem permissao.'


@app.route('/pagamento/<id>', methods=['GET', 'POST'])
def exibir_pagamento(id):
    try:

        access_token = "APP_USR-4552254824501886-022223-187f28fb2384d920b7248e90fa71896d-472313762"
        url = f"https://api.mercadopago.com/v1/payments/{id}?access_token={access_token}"
        response = requests.get(url)
        payment_info = response.json()

        image_qr = payment_info["point_of_interaction"]["transaction_data"]['qr_code_base64']
        code_qr = payment_info["point_of_interaction"]["transaction_data"]['qr_code']
        descricao = payment_info['description']
        expira = payment_info['date_of_expiration']
        valor = payment_info['transaction_amount']

        return render_template("pagamento.html", image_qr=image_qr, descricao=descricao, expira=expira[0:10],
                               valor=valor, code_qr=code_qr)
    except:
        flash(u'Não encontramos o id de pagamento.', 'error')
        return render_template("pagamento.html")


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if "user" in session:
        user = session["user"]
        if request.method == 'POST':
            banco_creditos = mysql.connector.connect(**db_creditos)
            cursor_creditos = banco_creditos.cursor()

            data_atual = datetime.date.today()
            data_futura = data_atual + datetime.timedelta(days=2)

            numero = request.form['numero']
            creditos = request.form['creditos']
            dados = criar_pix(descricao=f"{creditos} Creditos para o painel do usuario {user}.",
                              preco=int(creditos) * 0.90)

            sql = "INSERT INTO pagamentos Values(%s,%s,%s,%s,%s,%s) "
            val = (user, numero, creditos, dados['status'], str(dados['id']), str(data_futura))
            cursor_creditos.execute(sql, val)

            banco_creditos.commit()
            cursor_creditos.close()
            return redirect('/pagamento/' + str(dados['id']) + "")

        return render_template("payment.html", user=user)
    else:
        return redirect('/')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/logout')
def logout():
    try:
        session.pop('user', None)
        return redirect('/')
    except:
        print('erro')


app.register_error_handler(404, page_not_found)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
