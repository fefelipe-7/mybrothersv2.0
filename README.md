# 💬 my brothers - rede social simples

uma rede social minimalista desenvolvida em python flask com sistema de login/logout, posts com texto e imagens, e controle de administração.

## 🚀 funcionalidades

### sistema de usuários
- **login/logout** com sessões persistentes
- **registro** de novos usuários com validação
- **upload de foto** de perfil (opcional)
- **sistema de administração** para moderar conteúdo

### posts e interação
- **criar posts** com texto e imagens
- **feed** com posts em ordem cronológica (mais recentes primeiro)
- **upload de imagens** nos posts (png, jpg, jpeg, gif)
- **deletar posts** (apenas administradores)

### interface
- **design responsivo** com fundo de imagem
- **interface moderna** com efeitos de transparência
- **navegação intuitiva** entre páginas
- **mensagens de erro** amigáveis

## 🛠️ tecnologias utilizadas

- **python 3.x** - linguagem principal
- **flask** - framework web
- **flask-session** - gerenciamento de sessões
- **html5** - estrutura das páginas
- **css3** - estilização e layout
- **json** - armazenamento de dados

## 📁 estrutura do projeto

```
mybrothersv2.0/
├── app.py                 # aplicação principal flask
├── requirements.txt       # dependências do projeto
├── users.json            # dados dos usuários
├── posts.json            # dados dos posts
├── index.html            # página principal (feed)
├── login.html            # página de login
├── register.html         # página de cadastro
├── create_user.html      # página antiga (não usada)
├── style.css             # estilos css
└── uploads/              # diretório de imagens (criado automaticamente)
```

## 🔧 instalação e execução

### 1. instalar dependências
```bash
pip install -r requirements.txt
```

### 2. executar aplicação
```bash
python app.py
```

### 3. acessar aplicação
abra o navegador e acesse: `http://127.0.0.1:5000`

## 👤 usuários padrão

### administrador
- **username:** `rian_adm`
- **senha:** `admin123`
- **permissões:** pode deletar qualquer post

### criar novo usuário
- acesse a página de login
- clique em "cadastre-se aqui"
- preencha os dados solicitados
- faça upload de foto (opcional)

## 📝 como usar

### 1. fazer login
- acesse a aplicação
- digite username e senha
- clique em "entrar"

### 2. criar post
- digite o texto no campo "o que você está pensando?"
- selecione uma imagem (opcional)
- clique em "postar"

### 3. gerenciar posts (admin)
- faça login como administrador
- clique no botão "apagar" em qualquer post
- confirme a exclusão

### 4. fazer logout
- clique no botão "sair" no canto superior direito

## 🔒 sistema de segurança

### autenticação
- **sessões seguras** com chave secreta
- **verificação de login** em todas as rotas protegidas
- **redirecionamento automático** para login quando não autenticado

### validação de dados
- **verificação de arquivos** (apenas imagens permitidas)
- **validação de username** único
- **sanitização de entrada** nos formulários

### controle de acesso
- **sistema de administração** baseado em flag `is_admin`
- **proteção de rotas** sensíveis
- **verificação de permissões** antes de ações administrativas

## 🎨 personalização

### alterar fundo
- substitua o arquivo `fundo.jpeg` na raiz do projeto
- mantenha o mesmo nome do arquivo

### modificar cores
- edite o arquivo `style.css`
- altere as variáveis de cor conforme necessário

### adicionar funcionalidades
- edite `app.py` para novas rotas
- crie novos templates html
- atualize `style.css` para novos estilos

## 🐛 resolução de problemas

### erro de importação
- verifique se todas as dependências estão instaladas
- execute: `pip install -r requirements.txt`

### erro de permissão
- verifique se o diretório `uploads/` existe
- garanta permissões de escrita no diretório

### posts não aparecem
- verifique se o arquivo `posts.json` existe
- confirme se há dados válidos no arquivo

### login não funciona
- verifique se o arquivo `users.json` existe
- confirme se há usuários cadastrados

## 📊 estrutura de dados

### usuário (users.json)
```json
{
  "users": [
    {
      "id": 1,
      "username": "rian_adm",
      "name": "rian(adm)",
      "password": "admin123",
      "photo": "foto.jpg",
      "is_admin": true,
      "created_at": "2024-01-01 10:00:00"
    }
  ],
  "next_id": 2
}
```

### post (posts.json)
```json
[
  {
    "text": "conteúdo do post",
    "image": "imagem.jpg",
    "user": "nome do usuário",
    "user_photo": "foto_usuario.jpg",
    "user_id": 1,
    "date": "01/01/2024 10:00"
  }
]
```

## 🚀 próximas funcionalidades

- [ ] sistema de likes nos posts
- [ ] comentários nos posts
- [ ] busca e filtros
- [ ] sistema de notificações
- [ ] chat entre usuários
- [ ] upload de vídeos
- [ ] sistema de hashtags
- [ ] modo escuro/claro

## 📄 licença

este projeto é de código aberto e pode ser usado livremente para fins educacionais e pessoais.

## 👨‍💻 desenvolvimento

desenvolvido com ❤️ usando python flask e muito café ☕

---

**versão:** 2.0  
**última atualização:** janeiro 2024  
**status:** em desenvolvimento ativo
