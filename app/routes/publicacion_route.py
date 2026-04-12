from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.publicacion import Publicacion
from app.models.users import User
from app.models.etiqueta import Etiqueta
from app import db

bp = Blueprint('publicacion', __name__, url_prefix='/Publicacion')

@bp.route('/')
@login_required
def index():
    # Mostrar todas las publicaciones
    publicaciones = Publicacion.query.all()
    return render_template('publicacion/index.html', data=publicaciones)

@bp.route('/etiqueta/<int:etiqueta_id>')
@login_required
def publicaciones_por_etiqueta(etiqueta_id):
    etiqueta = Etiqueta.query.get_or_404(etiqueta_id)
    publicaciones = Publicacion.query.filter(Publicacion.etiquetas.any(id=etiqueta_id)).all()
    return render_template('publicacion/index.html', data=publicaciones, etiqueta=etiqueta)

@bp.route('/detail/<int:id>')
@login_required
def detail(id):
    publicacion = Publicacion.query.get_or_404(id)
    # Permitir ver cualquier publicación
    return render_template('publicacion/detail.html', publicacion=publicacion)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    etiquetas = Etiqueta.query.all()
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        # Usar el ID del usuario actual en lugar de permitir selección
        new_publicacion = Publicacion(titulo=titulo, contenido=contenido, user_id=current_user.idUser)
        etiqueta_ids = request.form.getlist('etiquetas')
        if etiqueta_ids:
            selected_etiquetas = Etiqueta.query.filter(Etiqueta.id.in_(etiqueta_ids)).all()
            new_publicacion.etiquetas = selected_etiquetas
        db.session.add(new_publicacion)
        db.session.commit()
        flash('Publicación creada exitosamente.', 'success')
        return redirect(url_for('publicacion.index'))

    return render_template('publicacion/add.html', etiquetas=etiquetas)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    publicacion = Publicacion.query.get_or_404(id)
    # Verificar que la publicación pertenece al usuario actual
    if publicacion.user_id != current_user.idUser:
        flash('No tienes permiso para editar esta publicación.', 'danger')
        return redirect(url_for('publicacion.index'))

    etiquetas = Etiqueta.query.all()
    if request.method == 'POST':
        publicacion.titulo = request.form['titulo']
        publicacion.contenido = request.form['contenido']
        # No permitir cambiar el user_id
        etiqueta_ids = request.form.getlist('etiquetas')
        if etiqueta_ids:
            selected_etiquetas = Etiqueta.query.filter(Etiqueta.id.in_(etiqueta_ids)).all()
            publicacion.etiquetas = selected_etiquetas
        else:
            publicacion.etiquetas = []
        db.session.commit()
        flash('Publicación actualizada exitosamente.', 'success')
        return redirect(url_for('publicacion.index'))

    return render_template('publicacion/edit.html', publicacion=publicacion, etiquetas=etiquetas)

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    publicacion = Publicacion.query.get_or_404(id)
    # Verificar que la publicación pertenece al usuario actual
    if publicacion.user_id != current_user.idUser:
        flash('No tienes permiso para eliminar esta publicación.', 'danger')
        return redirect(url_for('publicacion.index'))

    db.session.delete(publicacion)
    db.session.commit()
    flash('Publicación eliminada exitosamente.', 'success')
    return redirect(url_for('publicacion.index'))
