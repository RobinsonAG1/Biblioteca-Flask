from flask import Blueprint, render_template, request, redirect, url_for
from app.models.publicacion import Publicacion
from app.models.users import User
from app.models.etiqueta import Etiqueta
from app import db

bp = Blueprint('publicacion', __name__, url_prefix='/Publicacion')

@bp.route('/')
def index():
    publicaciones = Publicacion.query.all()
    return render_template('publicacion/index.html', data=publicaciones)

@bp.route('/detail/<int:id>')
def detail(id):
    publicacion = Publicacion.query.get_or_404(id)
    return render_template('publicacion/detail.html', publicacion=publicacion)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    users = User.query.all()
    etiquetas = Etiqueta.query.all()
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        user_id = request.form['user_id']
        etiqueta_ids = request.form.getlist('etiquetas')
        new_publicacion = Publicacion(titulo=titulo, contenido=contenido, user_id=int(user_id))
        if etiqueta_ids:
            selected_etiquetas = Etiqueta.query.filter(Etiqueta.id.in_(etiqueta_ids)).all()
            new_publicacion.etiquetas = selected_etiquetas
        db.session.add(new_publicacion)
        db.session.commit()
        return redirect(url_for('publicacion.index'))

    return render_template('publicacion/add.html', users=users, etiquetas=etiquetas)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    publicacion = Publicacion.query.get_or_404(id)
    users = User.query.all()
    etiquetas = Etiqueta.query.all()
    if request.method == 'POST':
        publicacion.titulo = request.form['titulo']
        publicacion.contenido = request.form['contenido']
        publicacion.user_id = int(request.form['user_id'])
        etiqueta_ids = request.form.getlist('etiquetas')
        if etiqueta_ids:
            selected_etiquetas = Etiqueta.query.filter(Etiqueta.id.in_(etiqueta_ids)).all()
            publicacion.etiquetas = selected_etiquetas
        else:
            publicacion.etiquetas = []
        db.session.commit()
        return redirect(url_for('publicacion.index'))

    return render_template('publicacion/edit.html', publicacion=publicacion, users=users, etiquetas=etiquetas)

@bp.route('/delete/<int:id>')
def delete(id):
    publicacion = Publicacion.query.get_or_404(id)
    db.session.delete(publicacion)
    db.session.commit()
    return redirect(url_for('publicacion.index'))
