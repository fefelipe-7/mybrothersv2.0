# importações necessárias para o funcionamento da aplicação
from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
import os, json
from datetime import datetime

# criação da aplicação flask com configurações de template e arquivos estáticos
app = Flask(__name__, template_folder='.', static_folder='.')

# configuração de sessão para gerenciar login/logout dos usuários
# secret_key é usada para criptografar os dados da sessão
app.config['SECRET_KEY'] = 'mybrothers_secret_key_2024'
# tipo de sessão usando sistema de arquivos (persistente)
app.config['SESSION_TYPE'] = 'filesystem'
# inicialização do sistema de sessões
Session(app)

# constantes para os arquivos de dados
POSTS_FILE = 'posts.json'  # arquivo onde são salvos os posts
USERS_FILE = 'users.json'  # arquivo onde são salvos os usuários
# extensões de imagem permitidas para upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# função para carregar dados de arquivos json
# verifica se o arquivo existe antes de tentar abrir
# retorna lista vazia se arquivo não existir ou tiver erro de formatação
def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# função para salvar dados em arquivos json
# usa encoding utf-8 para suportar caracteres especiais (acentos, emojis)
# ensure_ascii=False permite caracteres não-ascii
# indent=2 formata o json de forma legível
def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# função para verificar se arquivo de imagem é permitido
# verifica se o arquivo tem extensão e se está na lista de permitidas
# converte para minúsculo para evitar problemas de case sensitivity
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# função para fazer upload de arquivos
# cria diretório uploads se não existir
# salva arquivo com nome único baseado em timestamp
# retorna o nome do arquivo salvo
def upload_file(file, filename):
    os.makedirs('uploads', exist_ok=True)
    file_path = os.path.join('uploads', filename)
    file.save(file_path)
    return filename

# função para buscar usuário pelo nome de usuário (username)
# carrega dados de usuários do arquivo json
# percorre lista de usuários procurando pelo username
# retorna dados do usuário se encontrado, senão retorna none
def get_user_by_username(username):
    users_data = load_json(USERS_FILE)
    if isinstance(users_data, dict) and 'users' in users_data:
        for user in users_data['users']:
            if user['username'] == username:
                return user
    return None

# função para buscar usuário pelo id único
# carrega dados de usuários do arquivo json
# percorre lista de usuários procurando pelo id
# retorna dados do usuário se encontrado, senão retorna none
def get_user_by_id(user_id):
    users_data = load_json(USERS_FILE)
    if isinstance(users_data, dict) and 'users' in users_data:
        for user in users_data['users']:
            if user['id'] == user_id:
                return user
    return None

# função para salvar um novo usuário no sistema
# carrega dados existentes ou cria estrutura vazia se necessário
# atribui id único sequencial para o novo usuário
# adiciona usuário na lista e salva no arquivo
# retorna dados do usuário criado
def save_user(user_data):
    users_data = load_json(USERS_FILE)
    if not isinstance(users_data, dict):
        users_data = {'users': [], 'next_id': 1}
    
    user_data['id'] = users_data['next_id']
    users_data['next_id'] += 1
    users_data['users'].append(user_data)
    save_json(USERS_FILE, users_data)
    return user_data

# função para verificar se usuário está logado
# verifica se existe user_id na sessão atual
# retorna true se logado, false se não
def is_logged_in():
    return 'user_id' in session

# função para obter dados do usuário atual da sessão
# verifica se está logado e busca dados completos do usuário
# retorna dados do usuário se logado, senão retorna none
def get_current_user():
    if is_logged_in():
        return get_user_by_id(session['user_id'])
    return None

# ===== ROTAS DA APLICAÇÃO =====

# rota principal - página inicial (feed de posts)
# verifica se usuário está logado, se não redireciona para login
# carrega dados do usuário atual e todos os posts
# exibe posts em ordem reversa (mais recentes primeiro)
@app.route('/')
def index():
    if not is_logged_in():
        return redirect('/login')
    
    user = get_current_user()
    posts = load_json(POSTS_FILE)
    return render_template('index.html', posts=reversed(posts), user=user)

# rota de login - página de autenticação
# get: exibe formulário de login
# post: processa dados de login e autentica usuário
# verifica username e senha, cria sessão se válido
# redireciona para página principal se login bem-sucedido
# exibe erro se credenciais inválidas
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = get_user_by_username(username)
    if user and user['password'] == password:
        session['user_id'] = user['id']
        return redirect('/')
    else:
        return render_template('login.html', error='Usuário ou senha incorretos')

# rota de registro - página de cadastro de novos usuários
# get: exibe formulário de cadastro
# post: processa dados de cadastro e cria novo usuário
# verifica se username já existe antes de criar
# faz upload da foto se fornecida
# cria usuário com dados fornecidos e faz login automático
# redireciona para página principal após cadastro bem-sucedido
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    photo_file = request.files.get('photo')
    
    # verificar se username já existe no sistema
    if get_user_by_username(username):
        return render_template('register.html', error='Nome de usuário já existe')
    
    # criar estrutura de dados do novo usuário
    user_data = {
        'username': username,
        'name': name,
        'password': password,
        'photo': None,
        'is_admin': False,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # fazer upload da foto se fornecida e válida
    if photo_file and allowed_file(photo_file.filename):
        filename = f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}_{photo_file.filename}"
        user_data['photo'] = upload_file(photo_file, filename)
    
    # salvar usuário no sistema e fazer login automático
    user = save_user(user_data)
    session['user_id'] = user['id']
    return redirect('/')

# rota de logout - encerra sessão do usuário
# limpa todos os dados da sessão atual
# redireciona para página de login
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/login')

# rota para criar novo post
# verifica se usuário está logado antes de permitir postagem
# processa texto e imagem do post
# faz upload da imagem se fornecida e válida
# salva post com dados do usuário atual e timestamp
# redireciona para página principal após salvar
@app.route('/post', methods=['POST'])
def post():
    if not is_logged_in():
        return redirect('/login')
    
    user = get_current_user()
    text = request.form.get('text')
    image_file = request.files.get('image')
    image_filename = None

    # fazer upload da imagem se fornecida e válida
    if image_file and allowed_file(image_file.filename):
        filename = f"img_{datetime.now().strftime('%Y%m%d%H%M%S')}_{image_file.filename}"
        image_filename = upload_file(image_file, filename)

    # criar estrutura de dados do post
    post_data = {
        "text": text,
        "image": image_filename,
        "user": user["name"],
        "user_photo": user["photo"],
        "user_id": user["id"],
        "date": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    # salvar post no arquivo de posts
    posts = load_json(POSTS_FILE)
    posts.append(post_data)
    save_json(POSTS_FILE, posts)
    return redirect('/')

# rota para deletar post (apenas administradores)
# verifica se usuário está logado e se é administrador
# remove post da lista e deleta imagem associada se existir
# salva lista atualizada de posts
# redireciona para página principal após deletar
@app.route('/delete_post/<int:post_index>', methods=['POST'])
def delete_post(post_index):
    if not is_logged_in():
        return redirect('/login')
    
    user = get_current_user()
    # verificar se usuário é administrador
    if not user or not user.get("is_admin", False):
        return redirect('/')
    
    posts = load_json(POSTS_FILE)
    # verificar se índice do post é válido
    if 0 <= post_index < len(posts):
        # deletar imagem do post se existir
        if posts[post_index].get("image"):
            local_path = os.path.join('uploads', posts[post_index]["image"])
            if os.path.exists(local_path):
                os.remove(local_path)
        # remover post da lista
        posts.pop(post_index)
        save_json(POSTS_FILE, posts)
    return redirect('/')

# inicialização da aplicação
# executa servidor flask em modo debug para desenvolvimento
if __name__ == '__main__':
    app.run(debug=True)
