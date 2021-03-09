"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 12345
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def index():
    """ Redirects to the users page """

    return redirect('/users')

@app.route('/users')
def list_users():
    """ Shows all users """

    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """ Shows detail page of a specific user """
    
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user, posts=user.posts)

@app.route('/users/new')
def show_add_user():
    """ Shows the add a new user form """

    return render_template('add-user.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    """ Adds new user to database then redirects to all users page """

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form.get('image_url')
    image_url = image_url.strip() if image_url else None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """ Shows the edit page for a user with a specific id """

    user = User.query.get_or_404(user_id)
    return render_template('edit-user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """ Edits an already existing user then updates the DB """

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form.get('image_url')
    image_url = image_url.strip() if image_url else None

    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """ Deletes an existing user then removes from the DB """

    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def show_add_post(user_id):
    """ Shows the add a new post form """

    tags = Tag.query.all()
    user = User.query.get_or_404(user_id)
    return render_template('add-post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """ Adds new post to database then redirects to the user details page """

    title = request.form['title']
    content = request.form.get('content')

    tag_ids = request.form.getlist('tag')
    int_tag_ids = tuple(int(id) for id in tag_ids)
    tags = Tag.query.filter(Tag.id.in_(int_tag_ids)).all()

    post = Post(title=title, content=content, user_id=user_id, tags=tags)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """ Shows the post details page for a specific post """

    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post(post_id):
    """ Shows the edit post page """

    all_tags = Tag.query.all()
    post = Post.query.get_or_404(post_id)
    post_tag_ids = tuple(tag.id for tag in post.tags)
    return render_template('edit-post.html', post=post, all_tags=all_tags, post_tag_ids=post_tag_ids)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """ Edits an already existing post then updates the DB """

    post = Post.query.get_or_404(post_id)
    new_title = request.form['title']
    new_content = request.form.get('content')
    tag_ids = request.form.getlist('tag')
    int_tag_ids = tuple(int(id) for id in tag_ids)
    tags = Tag.query.filter(Tag.id.in_(int_tag_ids)).all()

    post.title = new_title
    post.content = new_content
    post.tags = tags

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """ Deletes an existing post then removes it from the DB """
    
    user_id = Post.query.get_or_404(post_id).user_id
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/tags')
def list_tags():
    """ Shows all tags """

    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """ Shows details page for a specific tag """

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template('tag.html', posts=posts, tag=tag)

@app.route('/tags/new')
def show_add_tag():
    """ Shows the add a new tag form """
    return render_template('add-tag.html')

@app.route('/tags/new', methods=["POST"])
def add_tag():
    """ Adds a new tag to the DB then redirects to  """

    name = request.form['name']
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag(tag_id):
    """ Shows the edit form for an existing tag """

    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit-tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    """ Edits an existing tag then updates the DB """

    tag = Tag.query.get_or_404(tag_id)
    name = request.form['name']
    tag.name = name
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """ Removes an existing tag then deletes it from DB """

    PostTag.query.filter_by(tag_id=tag_id).delete()
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()
    return redirect('/tags')