from flask import Flask, render_template, request, redirect
import os, json
from datetime import datetime

app = Flask(__name__, template_folder='.', static_folder='.')

POSTS_FILE = 'posts.json'
USER_FILE = 'user.json'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(file, filename):
    os.makedirs('uploads', exist_ok=True)
    file_path = os.path.join('uploads', filename)
    file.save(file_path)
    return filename

# Rotas
@app.route('/')
def index():
    user = load_json(USER_FILE)
    if not user:
        return render_template('create_user.html')
    posts = load_json(POSTS_FILE)
    return render_template('index.html', posts=reversed(posts), user=user)

@app.route('/create_user', methods=['POST'])
def create_user():
    name = request.form.get('name')
    photo_file = request.files.get('photo')
    user_data = {"name": name, "photo": None}

    if photo_file and allowed_file(photo_file.filename):
        filename = f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}_{photo_file.filename}"
        user_data["photo"] = upload_file(photo_file, filename)

    save_json(USER_FILE, user_data)
    return redirect('/')

@app.route('/post', methods=['POST'])
def post():
    user = load_json(USER_FILE)
    if not user:
        return redirect('/')
    text = request.form.get('text')
    image_file = request.files.get('image')
    image_filename = None

    if image_file and allowed_file(image_file.filename):
        filename = f"img_{datetime.now().strftime('%Y%m%d%H%M%S')}_{image_file.filename}"
        image_filename = upload_file(image_file, filename)

    post_data = {
        "text": text,
        "image": image_filename,
        "user": user["name"],
        "user_photo": user["photo"],
        "date": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    posts = load_json(POSTS_FILE)
    posts.append(post_data)
    save_json(POSTS_FILE, posts)
    return redirect('/')

@app.route('/delete_post/<int:post_index>', methods=['POST'])
def delete_post(post_index):
    user = load_json(USER_FILE)
    if not user or user["name"] != "Rian(adm)":
        return redirect('/')
    posts = load_json(POSTS_FILE)
    if 0 <= post_index < len(posts):
        if posts[post_index].get("image"):
            local_path = os.path.join('uploads', posts[post_index]["image"])
            if os.path.exists(local_path):
                os.remove(local_path)
        posts.pop(post_index)
        save_json(POSTS_FILE, posts)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
