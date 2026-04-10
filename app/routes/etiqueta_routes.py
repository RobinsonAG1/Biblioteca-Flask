from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.etiqueta import Etiqueta
from app import db

etiqueta_bp = Blueprint('etiqueta', __name__, url_prefix='/etiquetas')


@etiqueta_bp.route('/')
@login_required
def lista_etiquetas():
    etiquetas = Etiqueta.query.all()
    return render_template('etiqueta/lista.html', etiquetas=etiquetas)


@etiqueta_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva_etiqueta():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        slug = request.form.get('slug')
        
        etiqueta = Etiqueta(nombre=nombre, slug=slug)
        db.session.add(etiqueta)
        db.session.commit()
        flash('Etiqueta creada exitosamente', 'success')
        return redirect(url_for('etiqueta.lista_etiquetas'))
    
    return render_template('etiqueta/formulario.html', etiqueta=None)


@etiqueta_bp.route('/<int:id>')
@login_required
def ver_etiqueta(id):
    etiqueta = Etiqueta.query.get_or_404(id)
    return render_template('etiqueta/ver.html', etiqueta=etiqueta)


@etiqueta_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_etiqueta(id):
    etiqueta = Etiqueta.query.get_or_404(id)
    
    if request.method == 'POST':
        etiqueta.nombre = request.form.get('nombre')
        etiqueta.slug = request.form.get('slug')
        db.session.commit()
        flash('Etiqueta actualizada exitosamente', 'success')
        return redirect(url_for('etiqueta.lista_etiquetas'))
    
    return render_template('etiqueta/formulario.html', etiqueta=etiqueta)
    
    return render_template('etiqueta/formulario.html', etiqueta=etiqueta)


@etiqueta_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_etiqueta(id):
    etiqueta = Etiqueta.query.get_or_404(id)
    db.session.delete(etiqueta)
    db.session.commit()
    flash('Etiqueta eliminada exitosamente', 'success')
    return redirect(url_for('etiqueta.lista_etiquetas'))