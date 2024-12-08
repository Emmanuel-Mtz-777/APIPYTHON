from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Configuración para subir imágenes
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Datos en memoria (simulación de base de datos)
usuarios = []
grupos = []
miembros_grupo = []
mensajes_grupo = []
mensajes_er = []
eventos = []
encuestas = []
preguntas = []
opciones = []
respuestas = []

# Ruta para agregar usuario
@app.route('/usuarios', methods=['POST'])
def agregar_usuario():
    data = request.json
    nuevo_usuario = {
        "idUsuario": len(usuarios) + 1,
        "nombre": data['nombre'],
        "apellido": data['apellido'],
        "correo": data['correo'],
        "contrasena": data['contrasena']
    }
    usuarios.append(nuevo_usuario)
    return jsonify({"message": "Usuario creado correctamente", "usuario": nuevo_usuario}), 201

# Ruta para consultar usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify({"usuarios": usuarios}), 200

# Ruta para actualizar usuario
@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    data = request.json
    usuario = next((u for u in usuarios if u['idUsuario'] == id_usuario), None)
    if usuario:
        usuario['nombre'] = data.get('nombre', usuario['nombre'])
        usuario['apellido'] = data.get('apellido', usuario['apellido'])
        usuario['correo'] = data.get('correo', usuario['correo'])
        usuario['contrasena'] = data.get('contrasena', usuario['contrasena'])
        return jsonify({"message": "Usuario actualizado correctamente", "usuario": usuario}), 200
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404

# Ruta para eliminar usuario
@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    global usuarios
    usuario = next((u for u in usuarios if u['idUsuario'] == id_usuario), None)
    if usuario:
        usuarios = [u for u in usuarios if u['idUsuario'] != id_usuario]
        return jsonify({"message": "Usuario eliminado correctamente"}), 200
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404

# Ruta para agregar grupo
@app.route('/grupos', methods=['POST'])
def agregar_grupo():
    data = request.json
    # Obtener el archivo de imagen de la solicitud
    image = request.files.get('image')
    
    # Si hay una imagen y es de un tipo permitido
    if image and allowed_file(image.filename):
        # Guardar el archivo en la carpeta configurada
        filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(filename)
        image_url = f'/static/images/{image.filename}'  # La URL de la imagen
    else:
        image_url = None
    
    nuevo_grupo = {
        "idGrupo": len(grupos) + 1,
        "nombre": data['nombre'],
        "descripcion": data['descripcion'],
        "image": image_url  # La URL de la imagen se guarda en la base de datos
    }
    grupos.append(nuevo_grupo)
    return jsonify({"message": "Grupo creado correctamente", "grupo": nuevo_grupo}), 201

# Ruta para consultar grupos
@app.route('/grupos', methods=['GET'])
def obtener_grupos():
    return jsonify({"grupos": grupos}), 200

# Ruta para consultar grupo por id
@app.route('/grupos/<int:id_grupo>', methods=['GET'])
def obtener_grupo(id_grupo):
    grupo = next((g for g in grupos if g['idGrupo'] == id_grupo), None)
    if grupo:
        return jsonify({"grupo": grupo}), 200
    else:
        return jsonify({"message": "Grupo no encontrado"}), 404

# Ruta para actualizar grupo
@app.route('/grupos/<int:id_grupo>', methods=['PUT'])
def actualizar_grupo(id_grupo):
    data = request.json
    grupo = next((g for g in grupos if g['idGrupo'] == id_grupo), None)
    
    if grupo:
        grupo['nombre'] = data.get('nombre', grupo['nombre'])
        grupo['descripcion'] = data.get('descripcion', grupo['descripcion'])
        
        # Si se manda una nueva imagen, actualizarla
        image = request.files.get('image')
        if image and allowed_file(image.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(filename)
            grupo['image'] = f'/static/images/{image.filename}'  # Actualizamos la URL de la imagen
        
        return jsonify({"message": "Grupo actualizado correctamente", "grupo": grupo}), 200
    else:
        return jsonify({"message": "Grupo no encontrado"}), 404

# Ruta para eliminar grupo
@app.route('/grupos/<int:id_grupo>', methods=['DELETE'])
def eliminar_grupo(id_grupo):
    global grupos
    grupo = next((g for g in grupos if g['idGrupo'] == id_grupo), None)
    if grupo:
        grupos = [g for g in grupos if g['idGrupo'] != id_grupo]
        return jsonify({"message": "Grupo eliminado correctamente"}), 200
    else:
        return jsonify({"message": "Grupo no encontrado"}), 404

# Rutas para agregar miembro a un grupo
@app.route('/miembros_grupo', methods=['POST'])
def agregar_miembro_grupo():
    data = request.json
    nuevo_miembro = {
        "idMiembros": len(miembros_grupo) + 1,
        "idUsuario": data['idUsuario'],
        "idGrupo": data['idGrupo'],
        "fechaIngreso": data['fechaIngreso']
    }
    miembros_grupo.append(nuevo_miembro)
    return jsonify({"message": "Miembro agregado al grupo correctamente", "miembro": nuevo_miembro}), 201

# Ruta para agregar mensaje en grupo
@app.route('/mensajes_grupo', methods=['POST'])
def agregar_mensaje_grupo():
    data = request.json
    nuevo_mensaje = {
        "idMensajeG": len(mensajes_grupo) + 1,
        "idUsuario": data['idUsuario'],
        "idGrupo": data['idGrupo'],
        "mensaje": data['mensaje'],
        "fechaHora": data['fechaHora']
    }
    mensajes_grupo.append(nuevo_mensaje)
    return jsonify({"message": "Mensaje en grupo agregado correctamente", "mensaje": nuevo_mensaje}), 201

# Rutas para mensajes entre usuarios
@app.route('/mensajes_er', methods=['POST'])
def agregar_mensaje_er():
    data = request.json
    nuevo_mensaje_er = {
        "idMensajeER": len(mensajes_er) + 1,
        "emisorUsuarioId": data['emisorUsuarioId'],
        "receptorUsuarioId": data['receptorUsuarioId'],
        "mensaje": data['mensaje'],
        "fechaHora": data['fechaHora']
    }
    mensajes_er.append(nuevo_mensaje_er)
    return jsonify({"message": "Mensaje entre usuarios agregado correctamente", "mensaje": nuevo_mensaje_er}), 201

# Rutas para eventos
@app.route('/eventos', methods=['POST'])
def agregar_evento():
    data = request.json
    nuevo_evento = {
        "idEvento": len(eventos) + 1,
        "nombre": data['nombre'],
        "lugar": data['lugar'],
        "fecha": data['fecha'],
        "idUsuario": data['idUsuario']
    }
    eventos.append(nuevo_evento)
    return jsonify({"message": "Evento creado correctamente", "evento": nuevo_evento}), 201

# Rutas para encuestas
@app.route('/encuestas', methods=['POST'])
def agregar_encuesta():
    data = request.json
    nueva_encuesta = {
        "idEncuesta": len(encuestas) + 1,
        "titulo": data['titulo'],
        "descripcion": data['descripcion'],
        "fechaCreacion": data['fechaCreacion'],
        "idUsuario": data['idUsuario']
    }
    encuestas.append(nueva_encuesta)
    return jsonify({"message": "Encuesta creada correctamente", "encuesta": nueva_encuesta}), 201

# Rutas para preguntas
@app.route('/preguntas', methods=['POST'])
def agregar_pregunta():
    data = request.json
    nueva_pregunta = {
        "idPregunta": len(preguntas) + 1,
        "idEncuesta": data['idEncuesta'],
        "textoPregunta": data['textoPregunta']
    }
    preguntas.append(nueva_pregunta)
    return jsonify({"message": "Pregunta agregada correctamente", "pregunta": nueva_pregunta}), 201

# Rutas para opciones de preguntas
@app.route('/opciones', methods=['POST'])
def agregar_opcion():
    data = request.json
    nueva_opcion = {
        "idOpcion": len(opciones) + 1,
        "idPregunta": data['idPregunta'],
        "textoOpcion": data['textoOpcion']
    }
    opciones.append(nueva_opcion)
    return jsonify({"message": "Opción agregada correctamente", "opcion": nueva_opcion}), 201

# Rutas para respuestas
@app.route('/respuestas', methods=['POST'])
def agregar_respuesta():
    data = request.json
    nueva_respuesta = {
        "idRespuesta": len(respuestas) + 1,
        "idUsuario": data['idUsuario'],
        "idOpcion": data['idOpcion']
    }
    respuestas.append(nueva_respuesta)
    return jsonify({"message": "Respuesta agregada correctamente", "respuesta": nueva_respuesta}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
