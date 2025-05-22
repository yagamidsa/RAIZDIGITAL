--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	core	configuracion
8	core	eventoasistente
9	core	evento
10	core	productoimagen
11	core	producto
12	core	log
13	core	categoria
14	core	usuariorol
15	core	productoetiqueta
16	core	etiquetacultural
17	core	pedido
18	core	resena
19	core	pedidoitem
20	core	comunidad
21	core	usuario
22	core	rol
23	core	noticia
24	core	noticialike
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add Configuración	7	add_configuracion
26	Can change Configuración	7	change_configuracion
27	Can delete Configuración	7	delete_configuracion
28	Can view Configuración	7	view_configuracion
29	Can add Asistente a evento	8	add_eventoasistente
30	Can change Asistente a evento	8	change_eventoasistente
31	Can delete Asistente a evento	8	delete_eventoasistente
32	Can view Asistente a evento	8	view_eventoasistente
33	Can add Evento	9	add_evento
34	Can change Evento	9	change_evento
35	Can delete Evento	9	delete_evento
36	Can view Evento	9	view_evento
37	Can add Imagen de producto	10	add_productoimagen
38	Can change Imagen de producto	10	change_productoimagen
39	Can delete Imagen de producto	10	delete_productoimagen
40	Can view Imagen de producto	10	view_productoimagen
41	Can add Producto	11	add_producto
42	Can change Producto	11	change_producto
43	Can delete Producto	11	delete_producto
44	Can view Producto	11	view_producto
45	Can add Log	12	add_log
46	Can change Log	12	change_log
47	Can delete Log	12	delete_log
48	Can view Log	12	view_log
49	Can add Categoría	13	add_categoria
50	Can change Categoría	13	change_categoria
51	Can delete Categoría	13	delete_categoria
52	Can view Categoría	13	view_categoria
53	Can add Rol de usuario	14	add_usuariorol
54	Can change Rol de usuario	14	change_usuariorol
55	Can delete Rol de usuario	14	delete_usuariorol
56	Can view Rol de usuario	14	view_usuariorol
57	Can add Etiqueta de producto	15	add_productoetiqueta
58	Can change Etiqueta de producto	15	change_productoetiqueta
59	Can delete Etiqueta de producto	15	delete_productoetiqueta
60	Can view Etiqueta de producto	15	view_productoetiqueta
61	Can add Etiqueta cultural	16	add_etiquetacultural
62	Can change Etiqueta cultural	16	change_etiquetacultural
63	Can delete Etiqueta cultural	16	delete_etiquetacultural
64	Can view Etiqueta cultural	16	view_etiquetacultural
65	Can add Pedido	17	add_pedido
66	Can change Pedido	17	change_pedido
67	Can delete Pedido	17	delete_pedido
68	Can view Pedido	17	view_pedido
69	Can add Reseña	18	add_resena
70	Can change Reseña	18	change_resena
71	Can delete Reseña	18	delete_resena
72	Can view Reseña	18	view_resena
73	Can add Item de pedido	19	add_pedidoitem
74	Can change Item de pedido	19	change_pedidoitem
75	Can delete Item de pedido	19	delete_pedidoitem
76	Can view Item de pedido	19	view_pedidoitem
77	Can add Comunidad	20	add_comunidad
78	Can change Comunidad	20	change_comunidad
79	Can delete Comunidad	20	delete_comunidad
80	Can view Comunidad	20	view_comunidad
81	Can add Usuario	21	add_usuario
82	Can change Usuario	21	change_usuario
83	Can delete Usuario	21	delete_usuario
84	Can view Usuario	21	view_usuario
85	Can add Rol	22	add_rol
86	Can change Rol	22	change_rol
87	Can delete Rol	22	delete_rol
88	Can view Rol	22	view_rol
89	Can add Noticia	23	add_noticia
90	Can change Noticia	23	change_noticia
91	Can delete Noticia	23	delete_noticia
92	Can view Noticia	23	view_noticia
93	Can add Like de noticia	24	add_noticialike
94	Can change Like de noticia	24	change_noticialike
95	Can delete Like de noticia	24	delete_noticialike
96	Can view Like de noticia	24	view_noticialike
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$1000000$EGDvH0FI5d2MfYmeDA4Yfs$m5Glr9g3nZZxSNPDMRRKNINYU4gzftSDoMEHhs92U5Y=	2025-05-16 14:45:05.152524-05	t	yagami			yagamidsa@hotmail.com	t	t	2025-05-16 14:44:48.107462-05
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2025-05-16 00:28:34.428225-05
2	auth	0001_initial	2025-05-16 00:28:34.515483-05
3	admin	0001_initial	2025-05-16 00:28:34.532984-05
4	admin	0002_logentry_remove_auto_add	2025-05-16 00:28:34.539939-05
5	admin	0003_logentry_add_action_flag_choices	2025-05-16 00:28:34.545532-05
6	contenttypes	0002_remove_content_type_name	2025-05-16 00:28:34.548399-05
7	auth	0002_alter_permission_name_max_length	2025-05-16 00:28:34.577944-05
8	auth	0003_alter_user_email_max_length	2025-05-16 00:28:34.583784-05
9	auth	0004_alter_user_username_opts	2025-05-16 00:28:34.588213-05
10	auth	0005_alter_user_last_login_null	2025-05-16 00:28:34.593491-05
11	auth	0006_require_contenttypes_0002	2025-05-16 00:28:34.595508-05
12	auth	0007_alter_validators_add_error_messages	2025-05-16 00:28:34.600905-05
13	auth	0008_alter_user_username_max_length	2025-05-16 00:28:34.611092-05
14	auth	0009_alter_user_last_name_max_length	2025-05-16 00:28:34.618914-05
15	auth	0010_alter_group_name_max_length	2025-05-16 00:28:34.627512-05
16	auth	0011_update_proxy_permissions	2025-05-16 00:28:34.62911-05
17	auth	0012_alter_user_first_name_max_length	2025-05-16 00:28:34.639812-05
18	sessions	0001_initial	2025-05-16 00:28:34.649408-05
19	core	0001_initial	2025-05-16 14:04:12.64184-05
20	core	0002_noticialike	2025-05-19 20:38:40.099053-05
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: raiz.categorias; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."raiz.categorias" (id, nombre, descripcion, icono, slug, orden, activo, categoria_padre_id) FROM stdin;
\.


--
-- Data for Name: raiz.comunidades; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."raiz.comunidades" (id, nombre, descripcion, region, pais, idioma_principal, fecha_registro, activo) FROM stdin;
1	Comunidad Wayúu	Comunidad indígena del norte de Colombia y Venezuela	La Guajira	Colombia	Wayuunaiki	2025-05-16 17:20:58.918806-05	t
\.


--
-- Data for Name: raiz.configuracion; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."raiz.configuracion" (clave, valor, descripcion, tipo, fecha_actualizacion) FROM stdin;
\.


--
-- Data for Name: raiz.etiquetas_culturales; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."raiz.etiquetas_culturales" (id, nombre, descripcion, id_comunidad) FROM stdin;
\.


--
-- Data for Name: raiz.usuarios; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."raiz.usuarios" (id, username, password, email, nombre, apellido, fecha_nacimiento, telefono, direccion, biografia, foto_perfil, fecha_registro, ultimo_login, verificado, activo, token_recuperacion, fecha_token, id_comunidad) FROM stdin;
d2a81182-259b-4d98-9af3-d9cbdb553804	Federman	pbkdf2_sha256$260000$DoxKCWfeXhXTNcYrNN5xdN$KDiq0gfxxaG1nSXNbZAAXgTzQrD6XwNuXfvtb+9djSo=	federman@raizdigital.com	Federman	Usuario	\N	\N	\N	\N	\N	2025-05-16 17:20:58.918806-05	\N	t	t	\N	\N	1
\.


--
-- Data for Name: raiz.eventos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."raiz.eventos" (id, titulo, descripcion, ubicacion, coordenadas_gps, fecha_inicio, fecha_fin, imagen, enlace_virtual, es_virtual, capacidad, estado, id_comunidad, id_organizador) FROM stdin;
\.


--
-- Data for Name: raiz.evento_asistentes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."raiz.evento_asistentes" (id, fecha_registro, asistio, id_evento, id_usuario) FROM stdin;
\.


--
-- Data for Name: raiz.logs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."raiz.logs" (id, accion, tabla_afectada, id_registro, detalles, ip, user_agent, fecha, id_usuario) FROM stdin;
\.


--
-- Data for Name: raiz.noticias; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."raiz.noticias" (id, titulo, resumen, contenido, imagen_portada, fecha_publicacion, fecha_creacion, fecha_actualizacion, estado, slug, vistas, destacado, id_comunidad, id_autor) FROM stdin;
\.


--
-- Data for Name: raiz.noticia_likes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."raiz.noticia_likes" (id, fecha, id_noticia, id_usuario) FROM stdin;
\.


--
-- Data for Name: raiz.pedidos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."raiz.pedidos" (id, fecha_pedido, estado, direccion_envio, ciudad_envio, pais_envio, codigo_postal, telefono_contacto, email_contacto, metodo_pago, referencia_pago, subtotal, costo_envio, impuestos, descuento_total, total, notas, codigo_seguimiento, fecha_entrega, id_usuario) FROM stdin;
\.


--
-- Data for Name: raiz.productos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."raiz.productos" (id, nombre, descripcion, historia_cultural, precio, descuento, stock, unidad_medida, fecha_creacion, fecha_actualizacion, aprobado, fecha_aprobacion, destacado, slug, vistas, activo, tecnica_elaboracion, tiempo_elaboracion, materiales, id_categoria, id_admin_aprobador, id_vendedor) FROM stdin;
\.


--
-- Data for Name: raiz.pedido_items; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."raiz.pedido_items" (id, cantidad, precio_unitario, descuento, subtotal, id_pedido, id_producto) FROM stdin;
\.


--
-- Data for Name: raiz.producto_etiquetas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."raiz.producto_etiquetas" (id, id_etiqueta, id_producto) FROM stdin;
\.


--
-- Data for Name: raiz.producto_imagenes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."raiz.producto_imagenes" (id, url, descripcion, es_principal, orden, id_producto) FROM stdin;
\.


--
-- Data for Name: raiz.resenas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."raiz.resenas" (id, calificacion, comentario, fecha, aprobado, id_producto, id_usuario) FROM stdin;
\.


--
-- Data for Name: raiz.roles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."raiz.roles" (id, nombre, descripcion) FROM stdin;
\.


--
-- Data for Name: raiz.usuarios_roles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."raiz.usuarios_roles" (id, fecha_asignacion, id_rol, id_usuario) FROM stdin;
\.


--
-- Data for Name: categorias; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.categorias (id, nombre, descripcion, icono, slug, categoria_padre_id, orden, activo) FROM stdin;
1	Textiles	Productos tejidos y confeccionados a mano	textile_icon.svg	textiles	\N	1	t
2	Cestería	Canastos y productos elaborados con fibras naturales	basket_icon.svg	cesteria	\N	2	t
3	Joyería	Adornos corporales elaborados con técnicas tradicionales	jewelry_icon.svg	joyeria	\N	3	t
4	Mochilas	Bolsos tejidos utilizando técnicas ancestrales	bag_icon.svg	mochilas	1	1	t
5	Pulseras	Adornos para muñeca elaborados con chaquiras y materiales naturales	bracelet_icon.svg	pulseras	3	1	t
\.


--
-- Data for Name: comunidades; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.comunidades (id, nombre, descripcion, region, pais, idioma_principal, fecha_registro, activo) FROM stdin;
1	Wayúu	Comunidad indígena reconocida por sus tejidos y mochilas tradicionales	La Guajira	Colombia	Wayuunaiki	2025-05-16 13:12:37.384748	t
2	Embera	Conocidos por su artesanía en chaquira y cestería tradicional	Chocó	Colombia	Embera	2025-05-16 13:12:37.384748	t
3	Arhuaco	Tejedores de mochilas con diseños que representan su cosmovisión	Sierra Nevada	Colombia	Ika	2025-05-16 13:12:37.384748	t
\.


--
-- Data for Name: configuracion; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.configuracion (clave, valor, descripcion, tipo, fecha_actualizacion) FROM stdin;
sitio_nombre	Raíz Digital	Nombre del sitio web	texto	2025-05-16 13:12:37.384748
sitio_descripcion	Conectando ancestralidad con el mundo digital	Descripción corta del sitio	texto	2025-05-16 13:12:37.384748
destacados_home	3	Número de productos destacados en la página principal	numero	2025-05-16 13:12:37.384748
envio_minimo	150000	Monto mínimo para envío gratuito	numero	2025-05-16 13:12:37.384748
contacto_email	contacto@raizdigital.com	Email de contacto principal	email	2025-05-16 13:12:37.384748
comision_venta	10	Porcentaje de comisión por venta	numero	2025-05-16 13:12:37.384748
\.


--
-- Data for Name: etiquetas_culturales; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.etiquetas_culturales (id, nombre, descripcion, id_comunidad) FROM stdin;
1	Kanaas	Diseños tradicionales wayúu que representan elementos de la naturaleza	1
2	Okama	Figuras geométricas tradicionales de la comunidad Embera	2
3	Geometría Sagrada	Patrones arhuacos que representan elementos del cosmos	3
4	Chinchorro	Hamaca tradicional de la cultura Wayúu	1
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.usuarios (id, username, password, email, nombre, apellido, fecha_nacimiento, id_comunidad, telefono, direccion, biografia, foto_perfil, fecha_registro, ultimo_login, verificado, activo, token_recuperacion, fecha_token) FROM stdin;
31b4c8f1-eb28-49ec-85a1-d15e5aa75565	ximena	pbkdf2_sha256$260000$1nNeq9gen2LMeseANNyorb$XLLKnTqUcQRk0rs0q8IqSVUI1EoZn0Yj719T8fZeIK8=	maria@wayuu.com	María	Ximena	1985-05-15	1	3101234567	Ranchería El Paso, Riohacha	Tejedora wayúu con más de 20 años de experiencia en mochilas tradicionales	maria_profile.jpg	2025-05-16 13:12:37.384748	2025-05-21 22:52:58.703373	t	t	\N	\N
505cbe90-fa4d-42c5-87ed-b6229ac20c46	david	pbkdf2_sha256$260000$LuDnnnKflKpNVIxgZvnZHb$Ced+MPLTRTDjJcbLLdH9xbxLMmHKsbrfZpWvOJaDbhU=	admin@raizdigital.com	David	Rojas	1990-01-01	2	3001234567	Calle Principal #123, Bogotá	Administrador de la plataforma Raíz Digital	admin_profile.jpg	2025-05-16 13:12:37.384748	2025-05-21 19:14:19.743734	t	t	\N	\N
8af9b5ab-ac4f-48e6-bb90-faf2d9f96b87	tania	pbkdf2_sha256$260000$E8GkizBZ7E47OVBtaMctOV$O3jdp7esywWOkQiKFhIpBuqIcDGXq0jpu8D9c+sl6ak=	usuario@ejemplo.com	Tania	Rojas	1995-10-20	2	3501234567	Calle 45 #23-14, Medellín	Apasionado por las artesanías indígenas colombianas	user_profile.jpg	2025-05-16 13:12:37.384748	2025-05-21 19:16:19.78026	t	t	\N	\N
2a8aee1c-1e0d-4eec-8e5d-fe04fb56462e	federman	pbkdf2_sha256$260000$kPRj8pEZXQNoNBBcH5Tr6U$Crcm8Icjc/TZC+/cM2tytSxluVb97aR2WXt7bmvKbJk=	yagamidsa@hotmail.com	Federman	Correa	1980-09-16	1	3118026851	Sierra Nevada, Santa Marta	Tejedora de mochilas arhuacas con diseños tradicionales que representan nuestra cosmovisión	luisa_profile.jpg	2025-05-16 13:12:37.384748	2025-05-22 03:02:51.421638	t	t	\N	\N
544f2813-1d98-49cc-b34b-b9b25c92a15f	sara	pbkdf2_sha256$260000$QnxWDcuO4p9NG0ylT85doC$6utOguzMMUC1ngV+slEHuURErFtP+M/jtVYCiRBKJlk=	carlos@embera.com	Sara	Rojas	1990-08-10	2	3151234567	Comunidad Embera, Quibdó	Artesano especializado en cestería y joyería con chaquiras	carlos_profile.jpg	2025-05-16 13:12:37.384748	2025-05-21 19:17:15.999383	t	t	\N	\N
\.


--
-- Data for Name: eventos; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.eventos (id, id_organizador, titulo, descripcion, ubicacion, coordenadas_gps, fecha_inicio, fecha_fin, imagen, enlace_virtual, es_virtual, capacidad, id_comunidad, estado) FROM stdin;
1	505cbe90-fa4d-42c5-87ed-b6229ac20c46	Taller de Tejido Wayúu	Aprende las técnicas ancestrales de tejido Wayúu de la mano de artesanas tradicionales	Centro Cultural La Candelaria, Bogotá	4.5981,-74.0758	2025-05-31 13:12:37.384748	2025-05-31 17:12:37.384748	taller_wayuu.jpg	\N	f	20	1	programado
2	544f2813-1d98-49cc-b34b-b9b25c92a15f	Webinar: Simbología Embera en Artesanías	Descubre el significado detrás de los símbolos y colores utilizados en las artesanías Embera	\N	\N	2025-06-05 13:12:37.384748	2025-06-05 15:12:37.384748	webinar_embera.jpg	https://meet.raizdigital.com/embera-simbolos	t	100	2	programado
\.


--
-- Data for Name: evento_asistentes; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.evento_asistentes (id_evento, id_usuario, fecha_registro, asistio) FROM stdin;
1	8af9b5ab-ac4f-48e6-bb90-faf2d9f96b87	2025-05-14 13:12:37.384748	f
2	8af9b5ab-ac4f-48e6-bb90-faf2d9f96b87	2025-05-15 13:12:37.384748	f
2	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	2025-05-13 13:12:37.384748	f
\.


--
-- Data for Name: logs; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.logs (id, id_usuario, accion, tabla_afectada, id_registro, detalles, ip, user_agent, fecha) FROM stdin;
1	505cbe90-fa4d-42c5-87ed-b6229ac20c46	crear	productos	c4d501e5-ffda-4f53-bd4b-866dd5b4ca4e	Creación de nuevo producto	192.168.1.100	\N	2025-04-16 13:12:37.384748
2	8af9b5ab-ac4f-48e6-bb90-faf2d9f96b87	comprar	pedidos	345b6f8e-5831-4264-9549-0ec3c73ed993	Realización de pedido	186.28.45.67	\N	2025-04-26 13:12:37.384748
3	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	logout	usuarios	\N	Cierre de sesión	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0	2025-05-22 03:51:54.666255
4	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	logout	usuarios	\N	Cierre de sesión	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0	2025-05-22 03:56:40.063844
5	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	logout	usuarios	\N	Cierre de sesión	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0	2025-05-22 03:56:40.06705
6	2a8aee1c-1e0d-4eec-8e5d-fe04fb56462e	logout	usuarios	\N	Cierre de sesión	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0	2025-05-22 04:02:55.975089
7	2a8aee1c-1e0d-4eec-8e5d-fe04fb56462e	logout	usuarios	\N	Cierre de sesión	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0	2025-05-22 04:54:17.211161
8	2a8aee1c-1e0d-4eec-8e5d-fe04fb56462e	logout	usuarios	\N	Cierre de sesión	127.0.0.1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0	2025-05-22 08:03:00.80926
\.


--
-- Data for Name: noticia_likes; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.noticia_likes (id, id_noticia, id_usuario, fecha_like) FROM stdin;
7	14	2a8aee1c-1e0d-4eec-8e5d-fe04fb56462e	2025-05-20 01:41:41.472425
10	25	505cbe90-fa4d-42c5-87ed-b6229ac20c46	2025-05-20 01:47:07.4326
13	20	505cbe90-fa4d-42c5-87ed-b6229ac20c46	2025-05-20 03:08:02.334853
14	26	505cbe90-fa4d-42c5-87ed-b6229ac20c46	2025-05-20 03:08:09.302946
15	15	2a8aee1c-1e0d-4eec-8e5d-fe04fb56462e	2025-05-20 03:29:00.757039
16	16	2a8aee1c-1e0d-4eec-8e5d-fe04fb56462e	2025-05-20 03:47:25.958286
17	17	505cbe90-fa4d-42c5-87ed-b6229ac20c46	2025-05-21 20:51:36.599279
18	17	8af9b5ab-ac4f-48e6-bb90-faf2d9f96b87	2025-05-22 00:16:52.822278
20	26	544f2813-1d98-49cc-b34b-b9b25c92a15f	2025-05-22 00:17:35.885486
21	18	544f2813-1d98-49cc-b34b-b9b25c92a15f	2025-05-22 00:17:47.397616
22	19	544f2813-1d98-49cc-b34b-b9b25c92a15f	2025-05-22 00:17:58.950455
23	17	544f2813-1d98-49cc-b34b-b9b25c92a15f	2025-05-22 00:18:47.854863
24	13	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	2025-05-22 00:37:32.686083
25	14	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	2025-05-22 00:37:40.773233
26	15	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	2025-05-22 00:37:47.894
27	16	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	2025-05-22 00:37:55.941725
28	13	2a8aee1c-1e0d-4eec-8e5d-fe04fb56462e	2025-05-22 03:59:32.81253
\.


--
-- Data for Name: noticia_vistas; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.noticia_vistas (id, id_noticia, id_usuario, fecha_vista) FROM stdin;
1	17	505cbe90-fa4d-42c5-87ed-b6229ac20c46	2025-05-20 00:17:03.760076
2	18	505cbe90-fa4d-42c5-87ed-b6229ac20c46	2025-05-20 00:17:50.823572
3	19	505cbe90-fa4d-42c5-87ed-b6229ac20c46	2025-05-20 00:50:02.947761
4	20	505cbe90-fa4d-42c5-87ed-b6229ac20c46	2025-05-20 00:51:19.912981
5	14	2a8aee1c-1e0d-4eec-8e5d-fe04fb56462e	2025-05-20 01:13:41.097021
6	13	2a8aee1c-1e0d-4eec-8e5d-fe04fb56462e	2025-05-20 01:15:00.11189
7	16	2a8aee1c-1e0d-4eec-8e5d-fe04fb56462e	2025-05-20 01:16:41.160206
8	25	505cbe90-fa4d-42c5-87ed-b6229ac20c46	2025-05-20 01:47:04.66624
9	26	505cbe90-fa4d-42c5-87ed-b6229ac20c46	2025-05-20 03:08:07.937859
10	15	2a8aee1c-1e0d-4eec-8e5d-fe04fb56462e	2025-05-20 03:28:57.58803
11	17	8af9b5ab-ac4f-48e6-bb90-faf2d9f96b87	2025-05-22 00:16:46.722332
12	17	544f2813-1d98-49cc-b34b-b9b25c92a15f	2025-05-22 00:17:22.179726
13	26	544f2813-1d98-49cc-b34b-b9b25c92a15f	2025-05-22 00:17:33.529133
14	18	544f2813-1d98-49cc-b34b-b9b25c92a15f	2025-05-22 00:17:45.799578
15	19	544f2813-1d98-49cc-b34b-b9b25c92a15f	2025-05-22 00:17:57.235373
16	13	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	2025-05-22 00:37:31.058611
17	14	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	2025-05-22 00:37:39.177791
18	15	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	2025-05-22 00:37:46.034866
19	16	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	2025-05-22 00:37:53.943417
\.


--
-- Data for Name: noticias; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.noticias (id, id_autor, titulo, resumen, contenido, imagen_portada, fecha_publicacion, fecha_creacion, fecha_actualizacion, estado, slug, vistas, destacado, id_comunidad) FROM stdin;
13	8af9b5ab-ac4f-48e6-bb90-faf2d9f96b87	Celebración ancestral en la comunidad Wayúu	Miembros de la comunidad Wayúu se reunieron para celebrar una importante ceremonia ancestral que mantiene vivas nuestras tradiciones.	<p>En un emotivo encuentro que reunió a jóvenes y ancianos por igual, la comunidad Wayúu celebró una ceremonia ancestral este fin de semana.</p>\\n\\n<p>La ceremonia, que tiene raíces que se remontan a cientos de años, representa un momento vital para la transmisión de conocimientos y el fortalecimiento de la identidad cultural.</p>\\n\\n<p>"Estas ceremonias son la forma en que nuestros ancestros nos hablan a través del tiempo. Cada movimiento, cada palabra, cada símbolo tiene un significado profundo que debemos preservar", explicó uno de los ancianos presentes.</p>\\n\\n<p>Los jóvenes participantes demostraron un entusiasmo especial por aprender y conservar estas tradiciones, un signo prometedor para la continuidad cultural de la comunidad.</p>\\n\\n<p>La celebración concluyó con un banquete de alimentos tradicionales y un intercambio de artesanías, reforzando los lazos comerciales y culturales que hacen de Wayúu una comunidad única y vibrante.</p>	celebracion_1.jpg	2025-05-17 18:33:36.384559	2025-05-14 18:33:36.384559	2025-05-22 00:37:31.058611	publicado	celebracion-ancestral-wayuu-20250519	4	t	1
14	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	Nuevo taller artesanal impulsa economía local en Wayúu	Un nuevo centro de producción artesanal abre sus puertas en Wayúu, ofreciendo empleo a más de 15 familias y revitalizando técnicas tradicionales.	<p>La economía local de Wayúu recibe un impulso significativo con la inauguración de un nuevo taller artesanal que emplea técnicas ancestrales combinadas con innovación.</p>\\n\\n<p>El taller, financiado en parte por un programa de desarrollo sostenible, ha contratado a 15 artesanos locales y planea expandirse en los próximos meses.</p>\\n\\n<p>"Este espacio no solo representa una fuente de ingresos, sino una manera de preservar nuestras técnicas tradicionales que estaban en riesgo de perderse", comentó la coordinadora del proyecto.</p>\\n\\n<p>Los productos elaborados incluyen textiles con tintes naturales, cerámica decorativa y utilitaria, y accesorios hechos con materiales sostenibles de la región.</p>\\n\\n<p>El taller también funcionará como centro de capacitación para jóvenes interesados en aprender los oficios tradicionales, asegurando la transmisión de conocimientos entre generaciones.</p>	taller_1.jpg	2025-05-14 18:33:36.384559	2025-05-12 18:33:36.384559	2025-05-22 00:37:39.177791	publicado	taller-artesanal-wayuu-20250519	60	f	1
15	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	Próximo festival cultural reunirá tradiciones de Wayúu	El festival anual de Wayúu se celebrará el próximo mes con exhibiciones de artesanía, gastronomía tradicional y presentaciones culturales.	<p>La comunidad Wayúu se prepara para su festival cultural anual que promete ser un escaparate de las mejores tradiciones y expresiones artísticas de la región.</p>\\n\\n<p>El evento, que se realizará del 15 al 17 del próximo mes, incluirá:</p>\\n\\n<ul>\\n<li>Exposición y venta de artesanías tradicionales</li>\\n<li>Talleres de elaboración artesanal abiertos al público</li>\\n<li>Degustación de gastronomía ancestral</li>\\n<li>Presentaciones de música y danza tradicional</li>\\n<li>Ceremonias rituales abiertas a visitantes</li>\\n</ul>\\n\\n<p>"Este festival es nuestra ventana al mundo. Es la manera en que compartimos quiénes somos y damos a conocer el valor de nuestras tradiciones", explicó el organizador principal.</p>\\n\\n<p>Se espera la asistencia de visitantes de comunidades vecinas y turistas nacionales e internacionales, lo que representa una importante oportunidad económica para los artesanos y comerciantes locales.</p>	festival_1.jpg	2025-05-09 18:33:36.384559	2025-05-07 18:33:36.384559	2025-05-22 00:37:46.034866	publicado	festival-cultural-wayuu-20250519	17	f	1
20	8af9b5ab-ac4f-48e6-bb90-faf2d9f96b87	Artesanía de Embera recibe reconocimiento internacional	La técnica artesanal única de Embera ha sido reconocida por UNESCO como patrimonio cultural inmaterial, destacando su valor y autenticidad.	<p>Una importante noticia para la comunidad Embera: nuestras técnicas artesanales tradicionales han recibido reconocimiento internacional como parte del patrimonio cultural inmaterial de la humanidad.</p>\\n\\n<p>Este reconocimiento destaca la exclusiva técnica de Embera que se ha transmitido de generación en generación por más de cinco siglos.</p>\\n\\n<p>"Este reconocimiento no es solo un honor, sino una responsabilidad para seguir preservando y desarrollando nuestras tradiciones", comentó uno de los maestros artesanos de la comunidad.</p>\\n\\n<p>El certificado aumentará la visibilidad y valor de las creaciones artesanales de la comunidad, representando una oportunidad para la economía local y el turismo cultural.</p>\\n\\n<p>Para celebrar este logro, se organizará una exhibición especial de las piezas más representativas de la artesanía local, junto con demostraciones de los procesos de creación para el público.</p>	reconocimiento_2.jpg	2025-05-04 18:33:36.384559	2025-05-03 18:33:36.384559	2025-05-21 19:59:56.331342	publicado	reconocimiento-artesania-embera-20250519	9	t	2
19	8af9b5ab-ac4f-48e6-bb90-faf2d9f96b87	Próximo festival cultural reunirá tradiciones de Embera	El festival anual de Embera se celebrará el próximo mes con exhibiciones de artesanía, gastronomía tradicional y presentaciones culturales.	<p>La comunidad Embera se prepara para su festival cultural anual que promete ser un escaparate de las mejores tradiciones y expresiones artísticas de la región.</p>\\n\\n<p>El evento, que se realizará del 15 al 17 del próximo mes, incluirá:</p>\\n\\n<ul>\\n<li>Exposición y venta de artesanías tradicionales</li>\\n<li>Talleres de elaboración artesanal abiertos al público</li>\\n<li>Degustación de gastronomía ancestral</li>\\n<li>Presentaciones de música y danza tradicional</li>\\n<li>Ceremonias rituales abiertas a visitantes</li>\\n</ul>\\n\\n<p>"Este festival es nuestra ventana al mundo. Es la manera en que compartimos quiénes somos y damos a conocer el valor de nuestras tradiciones", explicó el organizador principal.</p>\\n\\n<p>Se espera la asistencia de visitantes de comunidades vecinas y turistas nacionales e internacionales, lo que representa una importante oportunidad económica para los artesanos y comerciantes locales.</p>	festival_2.jpg	2025-05-09 18:33:36.384559	2025-05-07 18:33:36.384559	2025-05-22 00:17:57.235373	publicado	festival-cultural-embera-20250519	62	f	2
18	8af9b5ab-ac4f-48e6-bb90-faf2d9f96b87	Nuevo taller artesanal impulsa economía local en Embera	Un nuevo centro de producción artesanal abre sus puertas en Embera, ofreciendo empleo a más de 15 familias y revitalizando técnicas tradicionales.	La economía local de Embera recibe un impulso significativo con la inauguración de un nuevo taller artesanal que emplea técnicas ancestrales combinadas con innovación.\r\nEl taller, financiado en parte por un programa de desarrollo sostenible, ha contratado a 15 artesanos locales y planea expandirse en los próximos meses.\r\n\r\n"Este espacio no solo representa una fuente de ingresos, sino una manera de preservar nuestras técnicas tradicionales que estaban en riesgo de perderse", comentó la coordinadora del proyecto.\r\n\r\nLos productos elaborados incluyen textiles con tintes naturales, cerámica decorativa y utilitaria, y accesorios hechos con materiales sostenibles de la región.\r\n\r\nEl taller también funcionará como centro de capacitación para jóvenes interesados en aprender los oficios tradicionales, asegurando la transmisión de conocimientos entre generaciones.	taller_2.jpg	2025-05-14 18:33:36.384559	2025-05-12 18:33:36.384559	2025-05-22 00:17:45.799578	publicado	taller-artesanal-embera-20250519	5	f	2
16	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	Artesanía de Wayúu recibe reconocimiento internacional	La técnica artesanal única de Wayúu ha sido reconocida por UNESCO como patrimonio cultural inmaterial, destacando su valor y autenticidad.	<p>Una importante noticia para la comunidad Wayúu: nuestras técnicas artesanales tradicionales han recibido reconocimiento internacional como parte del patrimonio cultural inmaterial de la humanidad.</p>\\n\\n<p>Este reconocimiento destaca la exclusiva técnica de Wayúu que se ha transmitido de generación en generación por más de cinco siglos.</p>\\n\\n<p>"Este reconocimiento no es solo un honor, sino una responsabilidad para seguir preservando y desarrollando nuestras tradiciones", comentó uno de los maestros artesanos de la comunidad.</p>\\n\\n<p>El certificado aumentará la visibilidad y valor de las creaciones artesanales de la comunidad, representando una oportunidad para la economía local y el turismo cultural.</p>\\n\\n<p>Para celebrar este logro, se organizará una exhibición especial de las piezas más representativas de la artesanía local, junto con demostraciones de los procesos de creación para el público.</p>	reconocimiento_1.jpg	2025-05-04 18:33:36.384559	2025-05-03 18:33:36.384559	2025-05-22 00:37:53.943417	publicado	reconocimiento-artesania-wayuu-20250519	67	f	1
21	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	Iniciativa Raíz Digital une a artesanos de todo el país	La plataforma Raíz Digital está transformando la forma en que las comunidades artesanales acceden al mercado digital global.	<p>La iniciativa Raíz Digital está creando un puente entre las técnicas ancestrales y el mundo digital, permitiendo que artesanos de diversas comunidades puedan compartir sus creaciones con un público global.</p>\n\n<p>Esta plataforma no solo facilita la comercialización de productos artesanales, sino que también preserva y documenta las técnicas tradicionales, creando un repositorio digital de conocimiento cultural.</p>\n\n<p>"La brecha digital ha sido un obstáculo para muchas comunidades artesanales. Raíz Digital busca eliminar esa barrera y crear oportunidades equitativas", explicó el director del proyecto.</p>\n\n<p>Hasta la fecha, más de 50 comunidades se han unido a la plataforma, con resultados prometedores en términos de visibilidad y ventas de sus productos artesanales.</p>	raiz_digital_global.jpg	2025-05-18 18:33:36.384559	2025-05-16 18:33:36.384559	2025-05-19 18:34:29.123273	publicado	iniciativa-raiz-digital-une-artesanos-pais-20250519	188	t	3
22	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	Feria Nacional de Artesanías Tradicionales anuncia fecha	La feria más importante de artesanías del país se celebrará el próximo mes con participación de comunidades de todas las regiones.	<p>La Feria Nacional de Artesanías Tradicionales ha anunciado su próxima edición, que reunirá a artesanos de todas las regiones del país en un espacio dedicado a la celebración de nuestra riqueza cultural.</p>\n\n<p>Este año, la feria contará con pabellones especializados por tipo de artesanía y región, facilitando a los visitantes la exploración de la diversidad artesanal del país.</p>\n\n<p>Además de la exhibición y venta de artesanías, el programa incluye:</p>\n\n<ul>\n<li>Conferencias sobre comercio justo y desarrollo sostenible</li>\n<li>Talleres prácticos de técnicas artesanales para todos los públicos</li>\n<li>Concursos de innovación manteniendo la esencia tradicional</li>\n<li>Encuentros entre artesanos y diseñadores para colaboraciones creativas</li>\n</ul>\n\n<p>Los organizadores esperan superar los 100,000 visitantes de la edición anterior, consolidando este evento como un referente en la valorización de la artesanía tradicional.</p>	feria_nacional.jpg	2025-05-11 18:33:36.384559	2025-05-09 18:33:36.384559	2025-05-19 18:34:29.123273	publicado	feria-nacional-artesanias-tradicionales-20250519	113	f	3
23	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	Nuevas políticas de apoyo al sector artesanal tradicional	El gobierno ha anunciado un paquete de medidas para fortalecer el sector artesanal, incluyendo créditos especiales y programas de capacitación.	<p>Un importante anuncio para el sector artesanal: el gobierno ha revelado un paquete integral de políticas diseñadas para fortalecer y desarrollar la artesanía tradicional en todo el país.</p>\n\n<p>Entre las medidas más destacadas se encuentran:</p>\n\n<ul>\n<li>Créditos especiales con tasas preferenciales para artesanos registrados</li>\n<li>Programas de capacitación en marketing digital y comercio electrónico</li>\n<li>Subsidios para la participación en ferias internacionales</li>\n<li>Reconocimiento legal de técnicas artesanales como patrimonio cultural</li>\n<li>Integración de la enseñanza de artesanías tradicionales en el currículo escolar de regiones artesanales</li>\n</ul>\n\n<p>"Estas políticas responden a las necesidades expresadas por el propio sector artesanal durante años de diálogo. Estamos comprometidos con la preservación de nuestras tradiciones culturales y con el bienestar económico de quienes las mantienen vivas", señaló el ministro responsable.</p>\n\n<p>Las diferentes comunidades artesanales han recibido con optimismo estas medidas, que comenzarán a implementarse a partir del próximo trimestre.</p>	politicas_artesanal.jpg	2025-05-08 18:33:36.384559	2025-05-06 18:33:36.384559	2025-05-19 18:34:29.123273	publicado	politicas-apoyo-sector-artesanal-20250519	49	f	3
24	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	Estudio revela aumento en demanda global de artesanías tradicionales	Un reciente estudio de mercado muestra que la demanda de artesanías auténticas y tradicionales ha aumentado un 35% en el último año.	<p>La artesanía tradicional está experimentando un renacimiento global, según revela un reciente estudio de mercado que muestra un aumento del 35% en la demanda de piezas artesanales auténticas durante el último año.</p>\n\n<p>Esta tendencia se atribuye a varios factores:</p>\n\n<ul>\n<li>Creciente interés por productos sostenibles y con historia</li>\n<li>Rechazo a la producción masiva y preferencia por lo único y personalizado</li>\n<li>Mayor conciencia sobre el comercio justo y el apoyo a comunidades tradicionales</li>\n<li>Influencia de redes sociales en la visibilización de artesanías antes desconocidas</li>\n</ul>\n\n<p>"Estamos viendo un cambio paradigmático en los patrones de consumo. Las nuevas generaciones valoran la autenticidad, la sostenibilidad y la conexión cultural que ofrecen las artesanías tradicionales", explica el director del estudio.</p>\n\n<p>El informe también destaca que los compradores están dispuestos a pagar más por productos que incluyan información sobre su origen, la comunidad que los elabora y las técnicas empleadas.</p>\n\n<p>Esta tendencia representa una oportunidad sin precedentes para las comunidades artesanales que logren combinar sus técnicas tradicionales con estrategias efectivas de acceso al mercado global.</p>	estudio_artesanias.jpg	2025-05-01 18:33:36.384559	2025-04-29 18:33:36.384559	2025-05-19 18:34:29.123273	publicado	aumento-demanda-artesanias-tradicionales-20250519	59	f	3
26	505cbe90-fa4d-42c5-87ed-b6229ac20c46	sad	asdasd	asdasd	sad.jpg	2025-05-20 03:07:47.589699	2025-05-20 03:07:47.589699	2025-05-22 00:17:33.529133	publicado	sad	2	f	2
25	505cbe90-fa4d-42c5-87ed-b6229ac20c46	sdfsdf	sdfsdfsdf	sdfsdfsd	sdfsdf.jpg	2025-05-20 01:46:54.775906	2025-05-20 01:46:54.775906	2025-05-20 02:56:31.786083	archivado	sdfsdf	1	t	2
17	8af9b5ab-ac4f-48e6-bb90-faf2d9f96b87	Celebración ancestral en la comunidad Embera	Miembros de la comunidad Embera se reunieron para celebrar una importante ceremonia ancestral que mantiene vivas nuestras tradiciones.	<p>En un emotivo encuentro que reunió a jóvenes y ancianos por igual, la comunidad Embera celebró una ceremonia ancestral este fin de semana.</p>\\n\\n<p>La ceremonia, que tiene raíces que se remontan a cientos de años, representa un momento vital para la transmisión de conocimientos y el fortalecimiento de la identidad cultural.</p>\\n\\n<p>"Estas ceremonias son la forma en que nuestros ancestros nos hablan a través del tiempo. Cada movimiento, cada palabra, cada símbolo tiene un significado profundo que debemos preservar", explicó uno de los ancianos presentes.</p>\\n\\n<p>Los jóvenes participantes demostraron un entusiasmo especial por aprender y conservar estas tradiciones, un signo prometedor para la continuidad cultural de la comunidad.</p>\\n\\n<p>La celebración concluyó con un banquete de alimentos tradicionales y un intercambio de artesanías, reforzando los lazos comerciales y culturales que hacen de Embera una comunidad única y vibrante.</p>	celebracion-ancestral-embera-20250519.jpg	2025-05-17 18:33:36.384559	2025-05-14 18:33:36.384559	2025-05-22 00:17:22.179726	publicado	celebracion-ancestral-embera-20250519	54	t	2
\.


--
-- Data for Name: pedidos; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.pedidos (id, id_usuario, fecha_pedido, estado, direccion_envio, ciudad_envio, pais_envio, codigo_postal, telefono_contacto, email_contacto, metodo_pago, referencia_pago, subtotal, costo_envio, impuestos, descuento_total, total, notas, codigo_seguimiento, fecha_entrega) FROM stdin;
345b6f8e-5831-4264-9549-0ec3c73ed993	8af9b5ab-ac4f-48e6-bb90-faf2d9f96b87	2025-04-26 13:12:37.384748	entregado	Calle 45 #23-14	Medellín	Colombia	050001	3501234567	usuario@ejemplo.com	transferencia	REF123456789	195000.00	15000.00	0.00	0.00	210000.00	Entregar en portería	\N	\N
6f371efe-5515-44ac-ac6f-1b45397619ab	8af9b5ab-ac4f-48e6-bb90-faf2d9f96b87	2025-05-11 13:12:37.384748	enviado	Calle 45 #23-14	Medellín	Colombia	050001	3501234567	usuario@ejemplo.com	tarjeta	PAY987654321	450000.00	20000.00	0.00	45000.00	425000.00	Llamar antes de entregar	\N	\N
\.


--
-- Data for Name: productos; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.productos (id, id_vendedor, nombre, descripcion, historia_cultural, precio, descuento, stock, unidad_medida, id_categoria, fecha_creacion, fecha_actualizacion, aprobado, fecha_aprobacion, id_admin_aprobador, destacado, slug, vistas, activo, tecnica_elaboracion, tiempo_elaboracion, materiales) FROM stdin;
c4d501e5-ffda-4f53-bd4b-866dd5b4ca4e	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	Mochila Wayúu Tradicional	Mochila tejida a mano con diseños tradicionales wayúu	Las mochilas wayúu o "susu" son parte fundamental de nuestra identidad. Cada diseño representa elementos de nuestra cosmovisión y se transmiten de generación en generación.	150000.00	0.00	10	unidad	4	2025-05-16 13:12:37.384748	\N	t	\N	\N	t	mochila-wayuu-tradicional	0	t	Tejido a mano con técnica de crochet single	3 semanas	Hilo acrílico de alta calidad, tirante en cuero con borlas decorativas
094a63e5-282d-4233-92da-463aa737d4d3	31b4c8f1-eb28-49ec-85a1-d15e5aa75565	Chinchorro Wayúu Familiar	Hamaca tradicional wayúu para 2-3 personas, tejida con técnicas ancestrales	El chinchorro es fundamental en la vida cotidiana wayúu. Es un espacio de descanso, socialización y representa el vientre materno en nuestra cultura.	450000.00	10.00	5	unidad	1	2025-05-16 13:12:37.384748	\N	t	\N	\N	f	chinchorro-wayuu-familiar	0	t	Tejido manual con técnica de urdimbre y entrelazado	2 meses	Hilo de algodón procesado manualmente, tintes naturales
b59fea40-3406-4c42-ab2c-4ea9860a2bec	544f2813-1d98-49cc-b34b-b9b25c92a15f	Canasto Embera Multicolor	Canasto tradicional elaborado con fibras naturales y tintes de origen vegetal	Estos canastos son utilizados para almacenar alimentos y objetos importantes. Los diseños representan el territorio y la conexión con los espíritus de la naturaleza.	85000.00	0.00	8	unidad	2	2025-05-16 13:12:37.384748	\N	t	\N	\N	t	canasto-embera-multicolor	0	t	Tejido en espiral con técnica de enrollado	2 semanas	Fibra de caña flecha, tintes naturales extraídos de plantas de la región
2d70ee6c-d96d-4068-8c4f-32d82bdb7478	544f2813-1d98-49cc-b34b-b9b25c92a15f	Pulsera Okama Embera	Pulsera elaborada con chaquiras en diseño tradicional Okama	Las pulseras representan protección espiritual y conexión con los ancestros. Los colores y diseños tienen significados específicos relacionados con nuestra cosmogonía.	45000.00	5.00	15	unidad	5	2025-05-16 13:12:37.384748	\N	t	\N	\N	f	pulsera-okama-embera	0	t	Tejido con aguja e hilo, técnica de puntada en cruz	3 días	Chaquiras checas de vidrio, hilo de nylon
\.


--
-- Data for Name: pedido_items; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.pedido_items (id, id_pedido, id_producto, cantidad, precio_unitario, descuento, subtotal) FROM stdin;
1	345b6f8e-5831-4264-9549-0ec3c73ed993	c4d501e5-ffda-4f53-bd4b-866dd5b4ca4e	1	150000.00	0.00	150000.00
2	345b6f8e-5831-4264-9549-0ec3c73ed993	2d70ee6c-d96d-4068-8c4f-32d82bdb7478	1	45000.00	0.00	45000.00
3	6f371efe-5515-44ac-ac6f-1b45397619ab	094a63e5-282d-4233-92da-463aa737d4d3	1	450000.00	45000.00	405000.00
\.


--
-- Data for Name: producto_etiquetas; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.producto_etiquetas (id_producto, id_etiqueta) FROM stdin;
c4d501e5-ffda-4f53-bd4b-866dd5b4ca4e	1
094a63e5-282d-4233-92da-463aa737d4d3	4
b59fea40-3406-4c42-ab2c-4ea9860a2bec	2
2d70ee6c-d96d-4068-8c4f-32d82bdb7478	2
\.


--
-- Data for Name: producto_imagenes; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.producto_imagenes (id, id_producto, url, descripcion, es_principal, orden) FROM stdin;
1	c4d501e5-ffda-4f53-bd4b-866dd5b4ca4e	mochila_wayuu_1.jpg	Vista frontal de la mochila	t	1
2	c4d501e5-ffda-4f53-bd4b-866dd5b4ca4e	mochila_wayuu_2.jpg	Detalle del diseño Kanaas	f	2
3	094a63e5-282d-4233-92da-463aa737d4d3	chinchorro_wayuu_1.jpg	Chinchorro extendido	t	1
4	094a63e5-282d-4233-92da-463aa737d4d3	chinchorro_wayuu_2.jpg	Detalle de los bordes tejidos	f	2
5	b59fea40-3406-4c42-ab2c-4ea9860a2bec	canasto_embera_1.jpg	Vista superior del canasto	t	1
6	b59fea40-3406-4c42-ab2c-4ea9860a2bec	canasto_embera_2.jpg	Detalle del patrón tejido	f	2
7	2d70ee6c-d96d-4068-8c4f-32d82bdb7478	pulsera_embera_1.jpg	Pulsera completa	t	1
8	2d70ee6c-d96d-4068-8c4f-32d82bdb7478	pulsera_embera_2.jpg	Pulsera en muñeca	f	2
\.


--
-- Data for Name: resenas; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.resenas (id, id_producto, id_usuario, calificacion, comentario, fecha, aprobado) FROM stdin;
1	c4d501e5-ffda-4f53-bd4b-866dd5b4ca4e	8af9b5ab-ac4f-48e6-bb90-faf2d9f96b87	5	Excelente calidad y bellísimos diseños. Se nota el trabajo artesanal auténtico.	2025-05-06 13:12:37.384748	t
2	b59fea40-3406-4c42-ab2c-4ea9860a2bec	8af9b5ab-ac4f-48e6-bb90-faf2d9f96b87	4	Muy bonito el canasto, los colores son vibrantes y la calidad es muy buena.	2025-05-01 13:12:37.384748	t
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.roles (id, nombre, descripcion) FROM stdin;
1	administrador	Administrador del sistema con acceso completo
2	usuario	Usuario regular con acceso limitado
3	vendedor	Usuario con permisos para vender productos
\.


--
-- Data for Name: usuarios_roles; Type: TABLE DATA; Schema: raiz; Owner: -
--

COPY raiz.usuarios_roles (id_usuario, id_rol, fecha_asignacion) FROM stdin;
505cbe90-fa4d-42c5-87ed-b6229ac20c46	1	2025-05-16 13:12:37.384748
544f2813-1d98-49cc-b34b-b9b25c92a15f	3	2025-05-16 13:12:37.384748
8af9b5ab-ac4f-48e6-bb90-faf2d9f96b87	2	2025-05-16 13:12:37.384748
31b4c8f1-eb28-49ec-85a1-d15e5aa75565	1	2025-05-16 13:12:37.384748
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 96, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 24, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 20, true);


--
-- Name: raiz.categorias_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."raiz.categorias_id_seq"', 1, false);


--
-- Name: raiz.comunidades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."raiz.comunidades_id_seq"', 1, true);


--
-- Name: raiz.etiquetas_culturales_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."raiz.etiquetas_culturales_id_seq"', 1, false);


--
-- Name: raiz.evento_asistentes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."raiz.evento_asistentes_id_seq"', 1, false);


--
-- Name: raiz.eventos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."raiz.eventos_id_seq"', 1, false);


--
-- Name: raiz.logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."raiz.logs_id_seq"', 1, false);


--
-- Name: raiz.noticia_likes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."raiz.noticia_likes_id_seq"', 1, false);


--
-- Name: raiz.noticias_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."raiz.noticias_id_seq"', 5, true);


--
-- Name: raiz.pedido_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."raiz.pedido_items_id_seq"', 1, false);


--
-- Name: raiz.producto_etiquetas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."raiz.producto_etiquetas_id_seq"', 1, false);


--
-- Name: raiz.producto_imagenes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."raiz.producto_imagenes_id_seq"', 1, false);


--
-- Name: raiz.resenas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."raiz.resenas_id_seq"', 1, false);


--
-- Name: raiz.roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."raiz.roles_id_seq"', 1, false);


--
-- Name: raiz.usuarios_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."raiz.usuarios_roles_id_seq"', 1, false);


--
-- Name: categorias_id_seq; Type: SEQUENCE SET; Schema: raiz; Owner: -
--

SELECT pg_catalog.setval('raiz.categorias_id_seq', 5, true);


--
-- Name: comunidades_id_seq; Type: SEQUENCE SET; Schema: raiz; Owner: -
--

SELECT pg_catalog.setval('raiz.comunidades_id_seq', 3, true);


--
-- Name: etiquetas_culturales_id_seq; Type: SEQUENCE SET; Schema: raiz; Owner: -
--

SELECT pg_catalog.setval('raiz.etiquetas_culturales_id_seq', 4, true);


--
-- Name: eventos_id_seq; Type: SEQUENCE SET; Schema: raiz; Owner: -
--

SELECT pg_catalog.setval('raiz.eventos_id_seq', 2, true);


--
-- Name: logs_id_seq; Type: SEQUENCE SET; Schema: raiz; Owner: -
--

SELECT pg_catalog.setval('raiz.logs_id_seq', 8, true);


--
-- Name: noticia_likes_id_seq; Type: SEQUENCE SET; Schema: raiz; Owner: -
--

SELECT pg_catalog.setval('raiz.noticia_likes_id_seq', 28, true);


--
-- Name: noticia_vistas_id_seq; Type: SEQUENCE SET; Schema: raiz; Owner: -
--

SELECT pg_catalog.setval('raiz.noticia_vistas_id_seq', 19, true);


--
-- Name: noticias_id_seq; Type: SEQUENCE SET; Schema: raiz; Owner: -
--

SELECT pg_catalog.setval('raiz.noticias_id_seq', 26, true);


--
-- Name: pedido_items_id_seq; Type: SEQUENCE SET; Schema: raiz; Owner: -
--

SELECT pg_catalog.setval('raiz.pedido_items_id_seq', 3, true);


--
-- Name: producto_imagenes_id_seq; Type: SEQUENCE SET; Schema: raiz; Owner: -
--

SELECT pg_catalog.setval('raiz.producto_imagenes_id_seq', 10, true);


--
-- Name: resenas_id_seq; Type: SEQUENCE SET; Schema: raiz; Owner: -
--

SELECT pg_catalog.setval('raiz.resenas_id_seq', 3, true);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: raiz; Owner: -
--

SELECT pg_catalog.setval('raiz.roles_id_seq', 6, true);


--
-- PostgreSQL database dump complete
--

