from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid
from django.utils import timezone

class Comunidad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    pais = models.CharField(max_length=50)
    idioma_principal = models.CharField(max_length=50, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'raiz.comunidades'
        verbose_name = 'Comunidad'
        verbose_name_plural = 'Comunidades'


class Usuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    id_comunidad = models.ForeignKey(Comunidad, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_comunidad')
    telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)
    biografia = models.TextField(null=True, blank=True)
    foto_perfil = models.CharField(max_length=255, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultimo_login = models.DateTimeField(null=True, blank=True)
    verificado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    token_recuperacion = models.CharField(max_length=255, null=True, blank=True)
    fecha_token = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.username})"

    class Meta:
        db_table = 'raiz.usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'raiz.roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'


class UsuarioRol(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_column='id_rol')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'raiz.usuarios_roles'
        unique_together = (('id_usuario', 'id_rol'),)
        verbose_name = 'Rol de usuario'
        verbose_name_plural = 'Roles de usuarios'


class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    icono = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    categoria_padre = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, db_column='categoria_padre_id')
    orden = models.IntegerField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'raiz.categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'


class EtiquetaCultural(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    id_comunidad = models.ForeignKey(Comunidad, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_comunidad')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'raiz.etiquetas_culturales'
        verbose_name = 'Etiqueta cultural'
        verbose_name_plural = 'Etiquetas culturales'


class Producto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_vendedor')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    historia_cultural = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    stock = models.IntegerField()
    unidad_medida = models.CharField(max_length=50, null=True, blank=True)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='id_categoria')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    aprobado = models.BooleanField(default=False)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    id_admin_aprobador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_aprobados', db_column='id_admin_aprobador')
    destacado = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True)
    vistas = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    tecnica_elaboracion = models.TextField(null=True, blank=True)
    tiempo_elaboracion = models.CharField(max_length=100, null=True, blank=True)
    materiales = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
            # Verificar si ya existe un producto con el mismo slug
            exists = Producto.objects.filter(slug=self.slug).exists()
            count = 1
            original_slug = self.slug
            while exists:
                self.slug = f"{original_slug}-{count}"
                count += 1
                exists = Producto.objects.filter(slug=self.slug).exists()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'raiz.productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


class ProductoImagen(models.Model):
    id = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto')
    url = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    es_principal = models.BooleanField(default=False)
    orden = models.IntegerField(default=0)

    def __str__(self):
        return f"Imagen de {self.id_producto.nombre}"

    class Meta:
        db_table = 'raiz.producto_imagenes'
        verbose_name = 'Imagen de producto'
        verbose_name_plural = 'Imágenes de productos'


class ProductoEtiqueta(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto')
    id_etiqueta = models.ForeignKey(EtiquetaCultural, on_delete=models.CASCADE, db_column='id_etiqueta')

    class Meta:
        db_table = 'raiz.producto_etiquetas'
        unique_together = (('id_producto', 'id_etiqueta'),)
        verbose_name = 'Etiqueta de producto'
        verbose_name_plural = 'Etiquetas de productos'


class Noticia(models.Model):
    ESTADOS = (
        ('borrador', 'Borrador'),
        ('publicado', 'Publicado'),
        ('archivado', 'Archivado'),
    )

    id = models.AutoField(primary_key=True)
    id_autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_autor')
    titulo = models.CharField(max_length=200)
    resumen = models.TextField(null=True, blank=True)
    contenido = models.TextField()
    imagen_portada = models.CharField(max_length=255, null=True, blank=True)
    fecha_publicacion = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=50, choices=ESTADOS, default='borrador')
    slug = models.SlugField(max_length=255, unique=True)
    vistas = models.IntegerField(default=0)
    destacado = models.BooleanField(default=False)
    id_comunidad = models.ForeignKey(Comunidad, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_comunidad')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
            # Verificar si ya existe una noticia con el mismo slug
            exists = Noticia.objects.filter(slug=self.slug).exists()
            count = 1
            original_slug = self.slug
            while exists:
                self.slug = f"{original_slug}-{count}"
                count += 1
                exists = Noticia.objects.filter(slug=self.slug).exists()

        # Si se está publicando y no tiene fecha de publicación, establecerla ahora
        if self.estado == 'publicado' and not self.fecha_publicacion:
            self.fecha_publicacion = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'raiz.noticias'
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['-fecha_publicacion']


class Evento(models.Model):
    ESTADOS = (
        ('programado', 'Programado'),
        ('en_curso', 'En curso'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    )

    id = models.AutoField(primary_key=True)
    id_organizador = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_organizador')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    ubicacion = models.TextField(null=True, blank=True)
    coordenadas_gps = models.CharField(max_length=100, null=True, blank=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    imagen = models.CharField(max_length=255, null=True, blank=True)
    enlace_virtual = models.CharField(max_length=255, null=True, blank=True)
    es_virtual = models.BooleanField(default=False)
    capacidad = models.IntegerField(null=True, blank=True)
    id_comunidad = models.ForeignKey(Comunidad, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_comunidad')
    estado = models.CharField(max_length=50, choices=ESTADOS, default='programado')

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'raiz.eventos'
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['fecha_inicio']


class EventoAsistente(models.Model):
    id_evento = models.ForeignKey(Evento, on_delete=models.CASCADE, db_column='id_evento')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    asistio = models.BooleanField(default=False)

    class Meta:
        db_table = 'raiz.evento_asistentes'
        unique_together = (('id_evento', 'id_usuario'),)
        verbose_name = 'Asistente a evento'
        verbose_name_plural = 'Asistentes a eventos'


class Pedido(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('procesando', 'Procesando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=ESTADOS, default='pendiente')
    direccion_envio = models.TextField()
    ciudad_envio = models.CharField(max_length=100)
    pais_envio = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20, null=True, blank=True)
    telefono_contacto = models.CharField(max_length=20)
    email_contacto = models.EmailField(max_length=100)
    metodo_pago = models.CharField(max_length=50)
    referencia_pago = models.CharField(max_length=100, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    costo_envio = models.DecimalField(max_digits=12, decimal_places=2)
    impuestos = models.DecimalField(max_digits=12, decimal_places=2)
    descuento_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    notas = models.TextField(null=True, blank=True)
    codigo_seguimiento = models.CharField(max_length=100, null=True, blank=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.id_usuario.nombre} {self.id_usuario.apellido}"

    class Meta:
        db_table = 'raiz.pedidos'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'


class PedidoItem(models.Model):
    id = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, db_column='id_pedido')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Item de pedido {self.id_pedido.id} - {self.id_producto.nombre}"

    class Meta:
        db_table = 'raiz.pedido_items'
        verbose_name = 'Item de pedido'
        verbose_name_plural = 'Items de pedidos'


class Resena(models.Model):
    id = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    calificacion = models.IntegerField()
    comentario = models.TextField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=True)

    def __str__(self):
        return f"Reseña de {self.id_usuario.nombre} para {self.id_producto.nombre}"

    class Meta:
        db_table = 'raiz.resenas'
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'
        unique_together = (('id_producto', 'id_usuario'),)


class Configuracion(models.Model):
    TIPOS = (
        ('texto', 'Texto'),
        ('numero', 'Número'),
        ('boolean', 'Booleano'),
        ('json', 'JSON'),
        ('email', 'Email'),
    )

    clave = models.CharField(max_length=100, primary_key=True)
    valor = models.TextField()
    descripcion = models.TextField(null=True, blank=True)
    tipo = models.CharField(max_length=50, choices=TIPOS)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.clave

    class Meta:
        db_table = 'raiz.configuracion'
        verbose_name = 'Configuración'
        verbose_name_plural = 'Configuraciones'


class Log(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_usuario')
    accion = models.CharField(max_length=100)
    tabla_afectada = models.CharField(max_length=100, null=True, blank=True)
    id_registro = models.CharField(max_length=100, null=True, blank=True)
    detalles = models.TextField(null=True, blank=True)
    ip = models.CharField(max_length=45, null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.accion} - {self.fecha}"

    class Meta:
        db_table = 'raiz.logs'
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'