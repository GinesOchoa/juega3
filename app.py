from flask import Flask, render_template, request, jsonify, redirect, session, url_for, flash
from controladores.producto_dao import ProductoDAO
from controladores.usuarios_dao import UsuariosDAO
from modelos.producto import JuegoCompra, JuegoAlquiler
from controladores.carrito_dao import CarritoDAO
from controladores.carrito_dao import carrito
from controladores.venta_dao import VentaDAO
from controladores.mesa_dao import MesaDAO
from modelos.venta import Venta
from modelos.mesa import Mesa
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

usuarios_dao = UsuariosDAO('usuarios.json')
carrito_dao = CarritoDAO('juegos_de_compra.json')
venta_dao = VentaDAO('ventas.json')
producto_dao_compra = ProductoDAO('juegos_de_compra.json')
producto_dao_alquiler = ProductoDAO('juegos_de_alquiler.json')
mesa_dao = MesaDAO('mesa.json')

app.permanent_session_lifetime = timedelta(days=1)

from flask import request, session, flash, redirect, url_for

@app.route('/reservamesa', methods=['GET', 'POST'])
def reservar_mesa():
    if request.method == 'POST':
        mesa_id = int(request.form['mesa'])
        if mesa_dao.reservar_mesa(mesa_id):
            flash("Mesa reservada con éxito.", "success")
        else:
            flash("La mesa seleccionada está ocupada. Por favor, seleccione otra mesa.", "error")
        return redirect(url_for('reservar_mesa'))
    else:
        return render_template('reservamesa.html')


@app.route('/venta')
def venta():
    return render_template('venta.html')

@app.route('/venta', methods=['GET'])
def listar_ventas():
    ventas = venta_dao.cargar_ventas()
    return jsonify(ventas)

@app.route('/venta', methods=['POST'])
def agregar_venta():
    data = request.json
    venta_id = venta_dao.generar_id_venta()
    venta = Venta(venta_id, data['usuario'], data['productos'], data['precio_total'])
    venta_dao.guardar_venta(venta)
    return jsonify({"mensaje": "Venta agregada exitosamente"})

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

@app.route('/venta', methods=['DELETE'])
def eliminar_venta():
    data = request.json
    venta_id = data['id']
    venta_dao.eliminar_venta(venta_id)
    return jsonify({"mensaje": "Venta eliminada exitosamente"})

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

@app.route('/carrito')
def mostrar_pagina():
    total = carrito_dao.calcular_total()
    mensaje = carrito_dao.mensaje_carrito()
    return render_template('carrito.html', juegos_de_compra=producto_dao_compra.listar_juegos(), carrito=carrito, mensaje=mensaje, total=total)

@app.route('/carrito/agregar', methods=['POST'])
def agregar_producto_carrito():
    producto = request.form['idProducto']
    carrito_dao.agregar_al_carrito(producto)
    return redirect("/carrito")

@app.route('/carrito/eliminar', methods=['POST'])
def eliminar_producto_carrito():
    producto_index = request.form['index']
    carrito_dao.eliminar_del_carrito(producto_index)
    return redirect("/carrito")

@app.route('/carrito/limpiar', methods=['POST'])
def limpiar_carrito():
    carrito_dao.eliminar_todo_carrito()
    return redirect("/carrito")

@app.route('/carrito/descuento', methods=['POST'])
def descuento():
    mensaje = carrito_dao.mensaje_carrito()
    total_sin_descuento = carrito_dao.calcular_total()
    descuento = request.form['descuento']
    total_con_descuento = carrito_dao.aplicar_descuento(total_sin_descuento, descuento)
    session['total_con_descuento'] = total_con_descuento
    return render_template('carrito.html', juegos_de_compra=producto_dao_compra.listar_juegos(), carrito=carrito, total=total_con_descuento, mensaje=mensaje)

@app.route('/admin')
def admin_panel():
    if 'usuario' in session and session['usuario'] == 'admin':
        return render_template('admin_panel.html')
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = usuarios_dao.obtener_usuario_por_credenciales(username, password)
        if usuario:
            session['usuario'] = usuario['username']
            if usuario['admin']:
                return redirect('/admin')
            else:
                return redirect('/usuarios')
        else:
            return render_template('login.html', error="Credenciales incorrectas. Inténtalo de nuevo.")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)  
    return jsonify({"mensaje": "Sesión cerrada exitosamente"})  

@app.route('/usuarios')
def usuario_panel():
    if 'usuario' in session:
        return render_template('usuario_panel.html')
    else:
        return redirect('/login')

@app.route('/')
def display_page():
    lista_compra = producto_dao_compra.listar_juegos()
    lista_alquiler = producto_dao_alquiler.listar_juegos()
    return render_template('index.html', lista_compra=lista_compra, lista_alquiler=lista_alquiler)

@app.route('/productos/compra', methods=['GET'], endpoint='listar_productos_compra')
def listar_productos_compra():
    productos = producto_dao_compra.listar_juegos()
    return jsonify(productos)

@app.route('/productos/compra', methods=['POST'])
def agregar_producto_compra():
    data = request.json
    juego_compra = JuegoCompra(data['idProducto'], data['nombre'], data['precio'], data['descripcion'], data['stock'])
    producto_dao_compra.agregar_juego(juego_compra)
    return jsonify({"mensaje": "Producto de compra agregado exitosamente"})

@app.route('/productos/compra', methods=['PUT'])
def actualizar_producto_compra():
    data = request.json
    idProducto = data['idProducto'] 
    juego_compra_actualizado = JuegoCompra(idProducto, data['nombre'], data['precio'], data['descripcion'], data['stock'])
    producto_dao_compra.actualizar_juego(juego_compra_actualizado)
    return jsonify({"mensaje": "Producto de compra actualizado exitosamente"})

@app.route('/productos/compra', methods=['DELETE'], endpoint='eliminar_producto_compra')
def eliminar_producto_compra():
    data = request.json
    idProducto = data['idProducto']
    producto_dao_compra.eliminar_juego(idProducto)
    return jsonify({"mensaje": "Producto de compra eliminado exitosamente"})

@app.route('/productos/alquiler', methods=['GET'], endpoint='listar_productos_alquiler')
def listar_productos_alquiler():
    productos = producto_dao_alquiler.listar_juegos()
    return jsonify(productos)

@app.route('/productos/alquiler', methods=['POST'])
def agregar_juego_alquiler():
    data = request.json
    juego_alquiler = JuegoAlquiler(data['idProducto'], data['nombre'], data['precio_por_hora'], data['descripcion'], data['disponible_para_alquilar'])
    producto_dao_alquiler.agregar_juego(juego_alquiler)
    return jsonify({"mensaje": "Juego de alquiler agregado exitosamente"})

@app.route('/productos/alquiler', methods=['PUT'])
def actualizar_juego_alquiler():
    data = request.json
    idProducto = request.form.get('idProducto')
    juego_alquiler_actualizado = JuegoAlquiler(idProducto, data['nombre'], data['precio_por_hora'], data['descripcion'], data['disponible_para_alquilar'])
    producto_dao_alquiler.actualizar_juego(idProducto, juego_alquiler_actualizado)
    return jsonify({"mensaje": "Juego de alquiler actualizado exitosamente"})

@app.route('/productos/alquiler', methods=['DELETE'])
def eliminar_juego_alquiler():
    idProducto = request.form.get('idProducto')
    producto_dao_alquiler.eliminar_juego(idProducto)
    return jsonify({"mensaje": "Juego de alquiler eliminado exitosamente"})

if __name__ == '__main__':
    app.run(host='www.juega3.com', port=80, debug=True)
