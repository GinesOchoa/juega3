from flask import Flask, render_template, request, jsonify, redirect, session, url_for, flash, json
from controladores.producto_dao import ProductoDAO
from controladores.usuarios_dao import UsuariosDAO
from modelos.producto import JuegoCompra, JuegoAlquiler
from controladores.carrito_dao import CarritoDAO
from controladores.carrito_dao import carrito
from controladores.venta_dao import VentaDAO
from controladores.mesa_dao import MesaDAO
from modelos.venta import Venta
from datetime import timedelta, datetime
from modelos.usuarios import ClienteFisico, ClienteOnline

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

usuarios_dao = UsuariosDAO('usuarios.json')
carrito_dao = CarritoDAO('juegos_de_compra.json')
venta_dao = VentaDAO('ventas.json')
producto_dao_compra = ProductoDAO('juegos_de_compra.json')
producto_dao_alquiler = ProductoDAO('juegos_de_alquiler.json')
mesa_dao = MesaDAO("mesa.json", "eventos.json")

app.permanent_session_lifetime = timedelta(days=1)

@app.route('/alquiler', methods=['GET'])
def mostrar_formulario_alquiler():
    juegos_disponibles = producto_dao_alquiler.listar_juegos()
    return render_template('formulario_alquiler.html', juegos_disponibles=juegos_disponibles)

@app.route('/alquilar_juego', methods=['POST'])
def alquilar_juego():
    usuario = session.get('usuario')
    if usuario:
        id_juego = int(request.form['juego'])
        fecha_alquiler = request.form['fecha_alquiler']
        hora_alquiler = request.form['hora_alquiler']
        fecha_devolucion = request.form['fecha_devolucion']
        hora_devolucion = request.form['hora_devolucion']
        
        juego = producto_dao_alquiler.obtener_juego_por_id(id_juego)
        
        if not juego:
            flash('El juego seleccionado no existe.', 'error')
            return redirect(url_for('mostrar_formulario_alquiler'))
    
        if not juego.disponible_para_alquilar:
            flash('El juego seleccionado no está disponible para alquilar.', 'error')
            return redirect(url_for('mostrar_formulario_alquiler'))

        precio_por_hora = juego.precio_por_hora
        precio_total = producto_dao_alquiler.calcular_precio_total(precio_por_hora, fecha_alquiler, hora_alquiler, fecha_devolucion, hora_devolucion)
        
        recibo = {
            'id_juego': id_juego,
            'fecha_alquiler': fecha_alquiler,
            'hora_alquiler': hora_alquiler,
            'fecha_devolucion': fecha_devolucion,
            'hora_devolucion': hora_devolucion,
            'precio_total': precio_total,
            'usuario': usuario
        }

        producto_dao_alquiler.guardar_recibo_alquiler(recibo)
        producto_dao_alquiler.actualizar_disponibilidad_juegos()

        flash(f'Juego alquilado por {precio_total} euros.', 'success')
        return redirect(url_for('mostrar_formulario_alquiler'))
    else:
        flash('Debes iniciar sesión para realizar una compra', 'error')
        return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        email = request.form['email']
        telefono = request.form['telefono']
        tipo = request.form['tipo']
        direccion_envio = request.form.get('direccion_envio', '')
        provincia = request.form.get('provincia', '')
        localidad = request.form.get('localidad', '')
        nacionalidad = request.form.get('nacionalidad', '')
        codigo_postal = request.form.get('codigo_postal', '')

        # Validar contraseñas
        if not usuarios_dao.validar_contrasena(password):
            flash('La contraseña no cumple con los requisitos mínimos.', 'error')
            return redirect(url_for('registro'))
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return redirect(url_for('registro'))

        # Validar correo electrónico
        if not usuarios_dao.validar_correo(email):
            flash('El correo electrónico no es válido.', 'error')
            return redirect(url_for('registro'))

        # Validar formato del teléfono
        if not usuarios_dao.validar_telefono(telefono):
            flash('El formato del teléfono no es válido.', 'error')
            return redirect(url_for('registro'))

        # Validar formato del código postal
        if tipo == 'Online' and not usuarios_dao.validar_codigo_postal(codigo_postal):
            flash('El formato del código postal no es válido.', 'error')
            return redirect(url_for('registro'))

        # Verificar si el nombre de usuario ya está en uso
        if usuarios_dao.obtener_usuario_por_username(username):
            flash('El nombre de usuario ya está en uso.', 'error')
            return redirect(url_for('registro'))

        # Crear usuario y agregarlo a la base de datos
        if tipo == 'Fisico':
            nuevo_usuario = ClienteFisico(None, username, password, nombre, apellidos, email, telefono)
        else:
            nuevo_usuario = ClienteOnline(None, username, password, nombre, apellidos, email, telefono,
                                           direccion_envio, provincia, localidad, nacionalidad, codigo_postal)

        usuarios_dao.agregar_usuario(nuevo_usuario)
        flash('Usuario registrado correctamente.', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('registro.html')

#usuario
@app.route('/calendario')
def calendario():
    with open('eventos.json') as f:
        eventos = json.load(f)
    return render_template('calendario.html', eventos=eventos)

#usuario
@app.route('/reservamesa', methods=['GET', 'POST'])
def reservar_mesa():
    if request.method == 'POST':
        mesa_id = int(request.form['mesa'])
        mesa = mesa_dao.obtener_mesa_por_id(mesa_id)  # Obtener la mesa con el ID
        if mesa and mesa_dao.guardar_reserva(mesa):  # Verificar si la mesa existe y guardar la reserva
            flash("Mesa reservada con éxito.", "success")
        else:
            flash("La mesa seleccionada está ocupada. Por favor, seleccione otra mesa.", "error")
        return redirect(url_for('reservar_mesa'))
    else:
        return render_template('reservamesa.html')

#Admin
@app.route('/venta')
def venta():
    return render_template('venta.html')
#Admin
@app.route('/venta', methods=['GET'])
def listar_ventas():
    ventas = venta_dao.cargar_ventas()
    return jsonify(ventas)
#Admin
@app.route('/venta', methods=['POST'])
def agregar_venta():
    data = request.json
    venta_id = venta_dao.generar_id_venta()
    venta = Venta(venta_id, data['usuario'], data['productos'], data['precio_total'])
    venta_dao.guardar_venta(venta)
    return jsonify({"mensaje": "Venta agregada exitosamente"})

#Admin
@app.route('/venta', methods=['PUT']) 
def actualizar_venta():
    data = request.json
    venta_id = data['id']
    nuevos_datos = {
        "usuario": data['usuario'],
        "productos": data['productos'],
        "precio_total": data['precio_total']
    }
    venta_dao.actualizar_venta(venta_id, nuevos_datos)
    return jsonify({"mensaje": "Venta actualizada exitosamente"})
#Admin
@app.route('/venta', methods=['DELETE'])
def eliminar_venta():
    data = request.json
    venta_id = data['id']
    venta_dao.eliminar_venta(venta_id)
    return jsonify({"mensaje": "Venta eliminada exitosamente"})
#usuario
@app.route('/carrito/procesar_venta', methods=['POST'])
def procesar_venta():
    usuario = session.get('usuario')
    
    if usuario:
        compra = []
        
        if 'total_con_descuento' in session:
            total = session.pop('total_con_descuento')
        else:
            total = carrito_dao.calcular_total()
            
        carrito_dao.nueva_lista(carrito, compra)
        carrito_dao.eliminar_todo_carrito()
        
        for item in carrito:
            compra.append(item[1])
        
        carrito.clear()
        venta_id = venta_dao.generar_id_venta()
        venta = Venta(venta_id, usuario, compra, total)
        venta_dao.guardar_venta(venta)
        return render_template('recibo.html', total=total, carrito=compra, juegos_de_compra=producto_dao_compra.listar_juegos())
    else:
        flash('Debes iniciar sesión para realizar una compra', 'error')
        return redirect(url_for('login'))
#usuario
@app.route('/carrito')
def mostrar_pagina():
    total = carrito_dao.calcular_total()
    mensaje = carrito_dao.mensaje_carrito()
    return render_template('carrito.html', juegos_de_compra=producto_dao_compra.listar_juegos(), carrito=carrito, mensaje=mensaje, total=total)
#usuario
@app.route('/carrito/agregar', methods=['POST'])
def agregar_producto_carrito():
    producto = request.form['idProducto']
    carrito_dao.agregar_al_carrito(producto)
    return redirect("/carrito")
#usuario
@app.route('/carrito/eliminar', methods=['POST'])
def eliminar_producto_carrito():
    producto_index = request.form['index']
    carrito_dao.eliminar_del_carrito(producto_index)
    return redirect("/carrito")
#usuario
@app.route('/carrito/limpiar', methods=['POST'])
def limpiar_carrito():
    carrito_dao.eliminar_todo_carrito()
    return redirect("/carrito")
#usuario
@app.route('/carrito/descuento', methods=['POST'])
def descuento():
    mensaje = carrito_dao.mensaje_carrito()
    total_sin_descuento = carrito_dao.calcular_total()
    descuento = request.form['descuento']
    total_con_descuento = carrito_dao.aplicar_descuento(total_sin_descuento, descuento)
    session['total_con_descuento'] = total_con_descuento
    return render_template('carrito.html', juegos_de_compra=producto_dao_compra.listar_juegos(), carrito=carrito, total=total_con_descuento, mensaje=mensaje)
#Admin
@app.route('/admin')
def admin_panel():
    if 'usuario' in session and session['usuario'] == 'admin':
        return render_template('admin_panel.html')
    else:
        return redirect('/login')
#usuario
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = usuarios_dao.obtener_usuario_por_credenciales(username, password)
        if usuario:
            session['usuario'] = usuario
            if usuario['admin']:
                return redirect('/admin')
            else:
                return redirect('/usuarios')
        else:
            return render_template('login.html', error="Credenciales incorrectas. Inténtalo de nuevo.")

    return render_template('login.html')
#usuario
@app.route('/logout')
def logout():
    session.pop('usuario', None)  
    return jsonify({"mensaje": "Sesión cerrada exitosamente"})  
#usuario
@app.route('/usuarios')
def usuario_panel():
    if 'usuario' in session:
        username = session['usuario']
        
        # Cargar los datos de las ventas desde el archivo JSON
        with open('ventas.json', 'r') as file:
            ventas = json.load(file)
        
        # Encontrar la última compra del usuario actual
        ultima_compra = None
        for venta in ventas[::-1]:  # Iterar en reversa para encontrar la última compra
            if venta['usuario'] == username:
                ultima_compra = venta
                break
        
        # Cargar alquileres y reservas
        alquileres = producto_dao_alquiler.cargar_alquileres()
        reservas = mesa_dao.cargar_reservas()

        # Determinar alquileres activos
        alquileres_activos = []
        fecha_actual = datetime.now().date()
        for alquiler in alquileres:
            fecha_devolucion = datetime.strptime(alquiler['fecha_devolucion'], '%Y-%m-%d').date()
            if fecha_actual <= fecha_devolucion:
                alquileres_activos.append(alquiler)

        # Determinar reservas activas
        reservas_activas = []
        for mesa in reservas['mesas']:
            for reserva in mesa['reservas']:
                fecha_liberacion = datetime.strptime(reserva['fecha_liberacion'], '%Y-%m-%d').date()
                if fecha_actual <= fecha_liberacion:
                    reservas_activas.append(reserva)
        
        # Si se encontró una última compra, se pasa al template
        if ultima_compra:
            nombre_usuario = session['usuario']['username']
            if session['usuario']['premium']:
                tipo_usuario = "Premium"
            else:
                tipo_usuario = "Normal"
            return render_template('usuario_panel.html', 
                                   nombre_usuario=nombre_usuario, 
                                   tipo_usuario=tipo_usuario, 
                                   ultima_compra=ultima_compra,
                                   alquileres_activos=alquileres_activos,
                                   reservas_activas=reservas_activas)
        else:
            return render_template('usuario_panel.html', mensaje="No se encontraron compras.")
    else:
        return redirect('/login')

@app.route('/cambiar_contrasena', methods=['POST'])
def cambiar_contrasena():
    usuario = session.get('usuario')
    if usuario:
        contrasena_actual = request.form['contrasena_actual']
        nueva_contrasena = request.form['nueva_contrasena']
        
        if usuario['password'] == contrasena_actual:
            usuario['password'] = nueva_contrasena
            session['usuario'] = usuario
            usuarios_dao.actualizar_usuario(usuario)
            return "Contraseña actualizada exitosamente"
        else:
            return "La contraseña actual ingresada no es correcta"
    else:
        return redirect('/login')


@app.route('/cambiar_email', methods=['POST'])
def cambiar_email():
    usuario = session.get('usuario')
    if 'usuario' in session:
        usuario = session['usuario']
        nuevo_email = request.form['nuevo_email']

        if usuarios_dao.validar_correo(nuevo_email):
            usuario['email'] = nuevo_email
            usuarios_dao.actualizar_usuario(usuario)
            return "Correo electrónico actualizado exitosamente"
        else:
            return "El formato del correo electrónico no es válido"
    else:
        return redirect('/login')

#usuario
@app.route('/')
def display_page():
    lista_compra = producto_dao_compra.listar_juegos()
    lista_alquiler = producto_dao_alquiler.listar_juegos()
    return render_template('index.html', lista_compra=lista_compra, lista_alquiler=lista_alquiler)
#Admin
@app.route('/productos/compra', methods=['GET'], endpoint='listar_productos_compra')
def listar_productos_compra():
    productos = producto_dao_compra.listar_juegos()
    return jsonify(productos)
#Admin
@app.route('/productos/compra', methods=['POST'])
def agregar_producto_compra():
    data = request.json
    juego_compra = JuegoCompra(data['idProducto'], data['nombre'], data['precio'], data['descripcion'], data['stock'])
    producto_dao_compra.agregar_juego(juego_compra)
    return jsonify({"mensaje": "Producto de compra agregado exitosamente"})
#Admin
@app.route('/productos/compra', methods=['PUT'])
def actualizar_producto_compra():
    data = request.json
    idProducto = data['idProducto'] 
    juego_compra_actualizado = JuegoCompra(idProducto, data['nombre'], data['precio'], data['descripcion'], data['stock'])
    producto_dao_compra.actualizar_juego(juego_compra_actualizado)
    return jsonify({"mensaje": "Producto de compra actualizado exitosamente"})
#Admin
@app.route('/productos/compra', methods=['DELETE'], endpoint='eliminar_producto_compra')
def eliminar_producto_compra():
    data = request.json
    idProducto = data['idProducto']
    producto_dao_compra.eliminar_juego(idProducto)
    return jsonify({"mensaje": "Producto de compra eliminado exitosamente"})
#Admin
@app.route('/productos/alquiler', methods=['GET'], endpoint='listar_productos_alquiler')
def listar_productos_alquiler():
    productos = producto_dao_alquiler.listar_juegos()
    return jsonify(productos)
#Admin
@app.route('/productos/alquiler', methods=['POST'])
def agregar_juego_alquiler():
    data = request.json
    juego_alquiler = JuegoAlquiler(data['idProducto'], data['nombre'], data['precio_por_hora'], data['descripcion'], data['disponible_para_alquilar'])
    producto_dao_alquiler.agregar_juego(juego_alquiler)
    return jsonify({"mensaje": "Juego de alquiler agregado exitosamente"})
#Admin
@app.route('/productos/alquiler', methods=['PUT'])
def actualizar_juego_alquiler():
    data = request.json
    idProducto = request.form.get('idProducto')
    juego_alquiler_actualizado = JuegoAlquiler(idProducto, data['nombre'], data['precio_por_hora'], data['descripcion'], data['disponible_para_alquilar'])
    producto_dao_alquiler.actualizar_juego(idProducto, juego_alquiler_actualizado)
    return jsonify({"mensaje": "Juego de alquiler actualizado exitosamente"})
#Admin
@app.route('/productos/alquiler', methods=['DELETE'])
def eliminar_juego_alquiler():
    idProducto = request.form.get('idProducto')
    producto_dao_alquiler.eliminar_juego(idProducto)
    return jsonify({"mensaje": "Juego de alquiler eliminado exitosamente"})

if __name__ == '__main__':
    app.run(host='www.juega3.com', port=80, debug=True)
