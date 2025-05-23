# Generated by Django 5.2.1 on 2025-05-16 19:03

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comunidad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('region', models.CharField(blank=True, max_length=100, null=True)),
                ('pais', models.CharField(max_length=50)),
                ('idioma_principal', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Comunidad',
                'verbose_name_plural': 'Comunidades',
                'db_table': 'raiz.comunidades',
            },
        ),
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('clave', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('valor', models.TextField()),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('tipo', models.CharField(choices=[('texto', 'Texto'), ('numero', 'Número'), ('boolean', 'Booleano'), ('json', 'JSON'), ('email', 'Email')], max_length=50)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Configuración',
                'verbose_name_plural': 'Configuraciones',
                'db_table': 'raiz.configuracion',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('pagado', 'Pagado'), ('procesando', 'Procesando'), ('enviado', 'Enviado'), ('entregado', 'Entregado'), ('cancelado', 'Cancelado')], default='pendiente', max_length=50)),
                ('direccion_envio', models.TextField()),
                ('ciudad_envio', models.CharField(max_length=100)),
                ('pais_envio', models.CharField(max_length=100)),
                ('codigo_postal', models.CharField(blank=True, max_length=20, null=True)),
                ('telefono_contacto', models.CharField(max_length=20)),
                ('email_contacto', models.EmailField(max_length=100)),
                ('metodo_pago', models.CharField(max_length=50)),
                ('referencia_pago', models.CharField(blank=True, max_length=100, null=True)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=12)),
                ('costo_envio', models.DecimalField(decimal_places=2, max_digits=12)),
                ('impuestos', models.DecimalField(decimal_places=2, max_digits=12)),
                ('descuento_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, max_digits=12)),
                ('notas', models.TextField(blank=True, null=True)),
                ('codigo_seguimiento', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_entrega', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'db_table': 'raiz.pedidos',
            },
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Rol',
                'verbose_name_plural': 'Roles',
                'db_table': 'raiz.roles',
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('icono', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('orden', models.IntegerField(blank=True, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('categoria_padre', models.ForeignKey(blank=True, db_column='categoria_padre_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.categoria')),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
                'db_table': 'raiz.categorias',
            },
        ),
        migrations.CreateModel(
            name='EtiquetaCultural',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('id_comunidad', models.ForeignKey(blank=True, db_column='id_comunidad', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.comunidad')),
            ],
            options={
                'verbose_name': 'Etiqueta cultural',
                'verbose_name_plural': 'Etiquetas culturales',
                'db_table': 'raiz.etiquetas_culturales',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('historia_cultural', models.TextField(blank=True, null=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=12)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('stock', models.IntegerField()),
                ('unidad_medida', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('aprobado', models.BooleanField(default=False)),
                ('fecha_aprobacion', models.DateTimeField(blank=True, null=True)),
                ('destacado', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('vistas', models.IntegerField(default=0)),
                ('activo', models.BooleanField(default=True)),
                ('tecnica_elaboracion', models.TextField(blank=True, null=True)),
                ('tiempo_elaboracion', models.CharField(blank=True, max_length=100, null=True)),
                ('materiales', models.TextField(blank=True, null=True)),
                ('id_categoria', models.ForeignKey(db_column='id_categoria', on_delete=django.db.models.deletion.CASCADE, to='core.categoria')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'db_table': 'raiz.productos',
            },
        ),
        migrations.CreateModel(
            name='PedidoItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=12)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=12)),
                ('id_pedido', models.ForeignKey(db_column='id_pedido', on_delete=django.db.models.deletion.CASCADE, to='core.pedido')),
                ('id_producto', models.ForeignKey(db_column='id_producto', on_delete=django.db.models.deletion.CASCADE, to='core.producto')),
            ],
            options={
                'verbose_name': 'Item de pedido',
                'verbose_name_plural': 'Items de pedidos',
                'db_table': 'raiz.pedido_items',
            },
        ),
        migrations.CreateModel(
            name='ProductoImagen',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('es_principal', models.BooleanField(default=False)),
                ('orden', models.IntegerField(default=0)),
                ('id_producto', models.ForeignKey(db_column='id_producto', on_delete=django.db.models.deletion.CASCADE, to='core.producto')),
            ],
            options={
                'verbose_name': 'Imagen de producto',
                'verbose_name_plural': 'Imágenes de productos',
                'db_table': 'raiz.producto_imagenes',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('biografia', models.TextField(blank=True, null=True)),
                ('foto_perfil', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('ultimo_login', models.DateTimeField(blank=True, null=True)),
                ('verificado', models.BooleanField(default=False)),
                ('activo', models.BooleanField(default=True)),
                ('token_recuperacion', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_token', models.DateTimeField(blank=True, null=True)),
                ('id_comunidad', models.ForeignKey(blank=True, db_column='id_comunidad', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.comunidad')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'db_table': 'raiz.usuarios',
            },
        ),
        migrations.AddField(
            model_name='producto',
            name='id_admin_aprobador',
            field=models.ForeignKey(blank=True, db_column='id_admin_aprobador', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productos_aprobados', to='core.usuario'),
        ),
        migrations.AddField(
            model_name='producto',
            name='id_vendedor',
            field=models.ForeignKey(db_column='id_vendedor', on_delete=django.db.models.deletion.CASCADE, to='core.usuario'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='id_usuario',
            field=models.ForeignKey(db_column='id_usuario', on_delete=django.db.models.deletion.CASCADE, to='core.usuario'),
        ),
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=200)),
                ('resumen', models.TextField(blank=True, null=True)),
                ('contenido', models.TextField()),
                ('imagen_portada', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_publicacion', models.DateTimeField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('estado', models.CharField(choices=[('borrador', 'Borrador'), ('publicado', 'Publicado'), ('archivado', 'Archivado')], default='borrador', max_length=50)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('vistas', models.IntegerField(default=0)),
                ('destacado', models.BooleanField(default=False)),
                ('id_comunidad', models.ForeignKey(blank=True, db_column='id_comunidad', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.comunidad')),
                ('id_autor', models.ForeignKey(db_column='id_autor', on_delete=django.db.models.deletion.CASCADE, to='core.usuario')),
            ],
            options={
                'verbose_name': 'Noticia',
                'verbose_name_plural': 'Noticias',
                'db_table': 'raiz.noticias',
                'ordering': ['-fecha_publicacion'],
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('accion', models.CharField(max_length=100)),
                ('tabla_afectada', models.CharField(blank=True, max_length=100, null=True)),
                ('id_registro', models.CharField(blank=True, max_length=100, null=True)),
                ('detalles', models.TextField(blank=True, null=True)),
                ('ip', models.CharField(blank=True, max_length=45, null=True)),
                ('user_agent', models.TextField(blank=True, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('id_usuario', models.ForeignKey(blank=True, db_column='id_usuario', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.usuario')),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Logs',
                'db_table': 'raiz.logs',
            },
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('ubicacion', models.TextField(blank=True, null=True)),
                ('coordenadas_gps', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('imagen', models.CharField(blank=True, max_length=255, null=True)),
                ('enlace_virtual', models.CharField(blank=True, max_length=255, null=True)),
                ('es_virtual', models.BooleanField(default=False)),
                ('capacidad', models.IntegerField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('programado', 'Programado'), ('en_curso', 'En curso'), ('finalizado', 'Finalizado'), ('cancelado', 'Cancelado')], default='programado', max_length=50)),
                ('id_comunidad', models.ForeignKey(blank=True, db_column='id_comunidad', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.comunidad')),
                ('id_organizador', models.ForeignKey(db_column='id_organizador', on_delete=django.db.models.deletion.CASCADE, to='core.usuario')),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
                'db_table': 'raiz.eventos',
                'ordering': ['fecha_inicio'],
            },
        ),
        migrations.CreateModel(
            name='ProductoEtiqueta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_etiqueta', models.ForeignKey(db_column='id_etiqueta', on_delete=django.db.models.deletion.CASCADE, to='core.etiquetacultural')),
                ('id_producto', models.ForeignKey(db_column='id_producto', on_delete=django.db.models.deletion.CASCADE, to='core.producto')),
            ],
            options={
                'verbose_name': 'Etiqueta de producto',
                'verbose_name_plural': 'Etiquetas de productos',
                'db_table': 'raiz.producto_etiquetas',
                'unique_together': {('id_producto', 'id_etiqueta')},
            },
        ),
        migrations.CreateModel(
            name='Resena',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('calificacion', models.IntegerField()),
                ('comentario', models.TextField(blank=True, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('aprobado', models.BooleanField(default=True)),
                ('id_producto', models.ForeignKey(db_column='id_producto', on_delete=django.db.models.deletion.CASCADE, to='core.producto')),
                ('id_usuario', models.ForeignKey(db_column='id_usuario', on_delete=django.db.models.deletion.CASCADE, to='core.usuario')),
            ],
            options={
                'verbose_name': 'Reseña',
                'verbose_name_plural': 'Reseñas',
                'db_table': 'raiz.resenas',
                'unique_together': {('id_producto', 'id_usuario')},
            },
        ),
        migrations.CreateModel(
            name='EventoAsistente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('asistio', models.BooleanField(default=False)),
                ('id_evento', models.ForeignKey(db_column='id_evento', on_delete=django.db.models.deletion.CASCADE, to='core.evento')),
                ('id_usuario', models.ForeignKey(db_column='id_usuario', on_delete=django.db.models.deletion.CASCADE, to='core.usuario')),
            ],
            options={
                'verbose_name': 'Asistente a evento',
                'verbose_name_plural': 'Asistentes a eventos',
                'db_table': 'raiz.evento_asistentes',
                'unique_together': {('id_evento', 'id_usuario')},
            },
        ),
        migrations.CreateModel(
            name='UsuarioRol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_asignacion', models.DateTimeField(auto_now_add=True)),
                ('id_rol', models.ForeignKey(db_column='id_rol', on_delete=django.db.models.deletion.CASCADE, to='core.rol')),
                ('id_usuario', models.ForeignKey(db_column='id_usuario', on_delete=django.db.models.deletion.CASCADE, to='core.usuario')),
            ],
            options={
                'verbose_name': 'Rol de usuario',
                'verbose_name_plural': 'Roles de usuarios',
                'db_table': 'raiz.usuarios_roles',
                'unique_together': {('id_usuario', 'id_rol')},
            },
        ),
    ]
