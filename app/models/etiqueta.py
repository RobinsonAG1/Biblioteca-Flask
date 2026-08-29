from app import db

#Crear una tabla
publicacion_etiqueta = db.Table(
    'publicacion_etiqueta',
    db.Column('publicacion_id', db.Integer, db.ForeignKey('publicaciones.id'), primary_key=True),
    db.Column('etiqueta_id', db.Integer, db.ForeignKey('etiquetas.id'), primary_key=True)
)

class Etiqueta(db.Model):
    __tablename__ = 'etiquetas'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)

    publicaciones = db.relationship('Publicacion', secondary=publicacion_etiqueta, back_populates='etiquetas')

    def __repr__(self):
        return f'<Etiqueta {self.nombre}>'
