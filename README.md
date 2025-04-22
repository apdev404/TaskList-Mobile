# 📱 TaskList-Mobile

¡Bienvenido a **TaskList-Mobile**!  
Una app mobile de gestión de tareas hecha en Python y Kivy.  

---

## 🧠 Descripción

**TaskList-Mobile** es una aplicación sencilla e intuitiva que te permite:

- ✅ Agregar nuevas tareas
- ❌ Eliminar tareas
- 🟢 Marcar tareas como completadas
- 📊 Visualizar el progreso en un gráfico de torta que muestra:
  - Porcentaje de tareas completadas
  - Porcentaje de tareas pendientes

Todo almacenado de forma local en un archivo `.txt` (lo ideal seria actualizarlo a una Base de datos mas solida🤓).

---

## 🛠️ Tecnologías usadas

- 🐍 **Python 3**
- 🧱 **Kivy**: framework para desarrollo mobile multiplataforma
- 📄 Almacenamiento en archivo `.txt` local (implementación básica)

---

## 📸 Capturas de pantalla

> 📷 ¡Acá irían tus screenshots de la app en funcionamiento!

<p align="center">
  <img src="screenshots/main_screen.png" width="250"/>
  <img src="screenshots/pie_chart.png" width="250"/>
</p>

---

## 🧪 Cómo probar la app

### 🔹 Ejecutar localmente (modo desarrollo)

1. Cloná el repo:
   ```bash
   git clone https://github.com/tu_usuario/TaskList-Mobile.git
   cd TaskList-Mobile/src

2. Instalá las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
   
3. Ejecutá la app:
   ```bash
   python main.py
   ```

## 📦 Empaquetar para Android con Buildozer
### ⚠️ Solo funciona en Linux (o WSL en Windows)

1. Instalá buildozer en tu entorno Linux:

  ```bash
  pip install buildozer
  sudo apt install -y build-essential git python3 python3-pip unzip openjdk-17-jdk
  ```

2. Inicializá el archivo de configuración:
  
  ```bash
  buildozer init
  ```

3. Editá el archivo buildozer.spec generado y asegurate de configurar:
  
  ```bash
  source.include_exts = py,txt
  requirements = python3,kivy
  orientation = portrait
  ```

4. Empaquetá la app:
  ```bash
  buildozer -v android debug
  ```

5. Instalá el APK en tu dispositivo (conectado por USB y con depuración activada):
  ```bash
  buildozer android deploy run
  ```
