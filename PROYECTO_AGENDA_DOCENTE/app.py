from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('agenda_docente.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

# CURSOS
@app.route('/cursos')
def cursos():
    conn = get_db_connection()
    cursos = conn.execute('SELECT * FROM curso').fetchall()
    conn.close()
    return render_template('cursos.html', cursos=cursos)

@app.route('/cursos/agregar', methods=['POST'])
def agregar_curso():
    nombre = request.form['nombre']
    conn = get_db_connection()
    conn.execute('INSERT INTO curso (nombre) VALUES (?)', (nombre,))
    conn.commit()
    conn.close()
    return redirect(url_for('cursos'))

@app.route('/cursos/eliminar/<int:id_curso>')
def eliminar_curso(id_curso):
    conn = get_db_connection()
    conn.execute('DELETE FROM curso WHERE id_curso=?', (id_curso,))
    conn.commit()
    conn.close()
    return redirect(url_for('cursos'))

# ALUMNOS
@app.route('/alumnos')
def alumnos():
    conn = get_db_connection()
    alumnos = conn.execute('''
        SELECT a.id_alumno, a.nombre, a.apellido, c.nombre AS curso
        FROM alumno a
        LEFT JOIN curso c ON a.id_curso = c.id_curso
    ''').fetchall()
    cursos = conn.execute('SELECT * FROM curso').fetchall()
    conn.close()
    return render_template('alumnos.html', alumnos=alumnos, cursos=cursos)

@app.route('/alumnos/agregar', methods=['POST'])
def agregar_alumno():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    id_curso = request.form.get('id_curso') or None
    conn = get_db_connection()
    conn.execute('INSERT INTO alumno (nombre, apellido, id_curso) VALUES (?, ?, ?)',
                 (nombre, apellido, id_curso))
    conn.commit()
    conn.close()
    return redirect(url_for('alumnos'))

@app.route('/alumnos/eliminar/<int:id_alumno>')
def eliminar_alumno(id_alumno):
    conn = get_db_connection()
    conn.execute('DELETE FROM alumno WHERE id_alumno=?', (id_alumno,))
    conn.commit()
    conn.close()
    return redirect(url_for('alumnos'))

# ASISTENCIAS
@app.route('/asistencias')
def asistencias():
    conn = get_db_connection()
    asistencias = conn.execute('''
        SELECT asis.id_asistencia, al.nombre, al.apellido, asis.fecha, asis.estado
        FROM asistencia asis
        JOIN alumno al ON asis.id_alumno = al.id_alumno
        ORDER BY asis.fecha DESC
    ''').fetchall()
    alumnos = conn.execute('SELECT * FROM alumno').fetchall()
    conn.close()
    return render_template('asistencias.html', asistencias=asistencias, alumnos=alumnos)

@app.route('/asistencias/agregar', methods=['POST'])
def agregar_asistencia():
    id_alumno = request.form['id_alumno']
    estado = request.form['estado']
    fecha = request.form.get('fecha') or date.today().strftime("%Y-%m-%d")
    conn = get_db_connection()
    conn.execute('INSERT INTO asistencia (id_alumno, fecha, estado) VALUES (?, ?, ?)',
                 (id_alumno, fecha, estado))
    conn.commit()
    conn.close()
    return redirect(url_for('asistencias'))

@app.route('/asistencias/eliminar/<int:id_asistencia>')
def eliminar_asistencia(id_asistencia):
    conn = get_db_connection()
    conn.execute('DELETE FROM asistencia WHERE id_asistencia=?', (id_asistencia,))
    conn.commit()
    conn.close()
    return redirect(url_for('asistencias'))

if __name__ == '__main__':
    app.run(debug=True)