from flask import Flask, render_template, request, redirect, url_for, session
from src.models.estudantes import Estudante, EstudanteDAO
import base64, os, sys

HOST = "localhost"
PORT = 4000
DEBUG = True

# Inclui o diretório do projeto no sys.path
# project_root = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, project_root)

# Define o caminho completo para os diretórios templates e static
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'static')

app = Flask(__name__)
app.secret_key = "unbavalia"

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'pwd123456',
    'database': 'unbavalia',
}

# Define os diretórios para o Flask
app.template_folder = template_dir
app.static_folder = static_dir
app.static_url_path = '/static'

estudante_dao = EstudanteDAO(db_config)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Verificar as credenciais no banco de dados
        estudante_id = estudante_dao.validar_credenciais(email, senha)
        if estudante_id:
            # Se as credenciais forem válidas, armazene o ID do estudante na sessão
            # e redirecione-o para a página inicial
            session['estudante_id'] = estudante_id
            return redirect(url_for('index'))
        else:
            # Se as credenciais estiverem incorretas, renderize o template de login com uma mensagem de erro
            return render_template('login.html', error="Email ou senha incorretos")
    else:
        # Se for uma requisição GET, renderize o template do formulário de login
        return render_template('login.html')
    
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        matricula = request.form['matricula_estudante']
        nome = request.form['nome_estudante']
        curso = request.form['curso_estudante']
        email = request.form['email_estudante']
        senha = request.form['senha_estudante']
        foto = request.files['foto_estudante']

        # Codifica a foto em base64 antes de salvar no banco de dados
        foto_base64 = base64.b64encode(foto.read()).decode('utf-8')

        # Cria o objeto Estudante com os dados do formulário
        estudante = Estudante(None, matricula, nome, curso, email, senha, "Comum", foto_base64)

        # Salva o estudante no banco de dados
        if estudante_dao.save(estudante):
            # Se o cadastro foi bem-sucedido, redireciona para a página de login
            return redirect(url_for('login'))
        else:
            # Se ocorreu algum erro no cadastro, exibe uma mensagem de erro no template
            return render_template('cadastro.html', error="Erro ao cadastrar o usuário")

    else:
        # Se for uma requisição GET, renderiza o template do formulário de cadastro
        return render_template('cadastro.html')

@app.route('/')
def index():
    # Verifica se o estudante está logado antes de exibir a página inicial
    if 'estudante_id' in session:
        estudante_id = session['estudante_id']
        # Verifique se o ID do estudante existe no banco de dados
        estudante = estudante_dao.get_by_id(estudante_id)
        if estudante:
            # Redireciona para a página indexAdmin.html se o cargo for "Admin"
            if estudante.cargo_estudante == "Admin":
                return render_template('indexAdmin.html')
            else:
                # Caso contrário, exibe a página index.html padrão
                return render_template('index.html')
    
    # Se o estudante não estiver logado ou se o ID não existir no banco de dados, redirecione-o novamente para a página de login
    return redirect(url_for('login'))

if (__name__ == "__main__"):
    app.run(HOST, PORT, DEBUG)