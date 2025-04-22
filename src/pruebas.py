from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.graphics import Rectangle
from kivy.core.image import Image as CoreImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import NumericProperty
from math import cos, sin, radians

class PieChart(Widget):
     porcentaje = 0   # Propiedad para el porcentaje del gráfico de torta

     def __init__(self, **kwargs):
        super(PieChart, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (200, 200)  # Tamaño del widget de la torta (ajusta según necesites)
        self.draw()  # Dibujar inicialmente el gráfico de torta

     def set_porcentaje(self, porcentaje):
        self.porcentaje = porcentaje
        self.draw()  # Llamar a draw para actualizar el gráfico de torta

     def draw(self):
        # Limpiar el canvas existente
        self.canvas.clear()

        # Determinar el radio y el centro del círculo
        radio = min(self.width, self.height) / 2.0
        centro_x = self.x + self.width / 2.0  # Centro sobre el eje x
        centro_y = self.y + self.height / 2.0  # Centro sobre el eje y

        # Ángulo inicial y final del sector
        start_angle = 0
        end_angle =self.porcentaje * 3.6  # Convertir porcentaje a ángulo
        with self.canvas:
            Color(1, 0.1647, 0.1647)
            Ellipse(pos=(centro_x - radio, centro_y - radio), size=(radio * 2, radio * 2))
        # Dibujar el sector de la torta
        with self.canvas:
             Color(0.1843, 1, 0.1647)  # Color azul (puedes ajustar los valores RGB según tu preferencia)
             Line(circle=(centro_x, centro_y, radio, start_angle, end_angle))

            # Dibujar líneas desde el borde del círculo hacia el centro
             for angle in range(int(start_angle), int(end_angle)):
                # Calcular coordenadas del borde del círculo
                x1 = centro_x + radio * cos(radians(angle))
                y1 = centro_y + radio * sin(radians(angle))
                # Dibujar línea desde el borde hasta el centro
                Line(points=[x1, y1, centro_x, centro_y])
                         

class BackgroundLabel(Label):
    def __init__(self, background_image, **kwargs):
        super(BackgroundLabel, self).__init__(**kwargs)
        with self.canvas.before:
            self.rect_bg = Rectangle(source=background_image, size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect_bg.size = instance.size
        self.rect_bg.pos = instance.pos

class TaskApp(App):
    def build(self):
        Window.size = (350, 600)
        self.diseño_sup = BoxLayout(orientation='vertical')
        box = BoxLayout()
        with box.canvas:
            Color(0.4, 0.7, 0.5, 1)  # Color RGB: R=0.4, G=0.7, B=0.5, opacidad=1
            self.rect = Rectangle(size=box.size, pos=box.pos)

        # Agregar un botón dentro del BoxLayout coloreado
        button = Button(text="¡Hola, Kivy!", size_hint=(0.5, 0.5))
        box.add_widget(button)

        # Agregar el BoxLayout coloreado al layout principal
        self.diseño_sup.add_widget(box)


        # Crear el layout principal
        self.layout = BoxLayout(orientation='vertical')

      
        # Crear la página de inicio
        self.page_inicio = BoxLayout(orientation='vertical')
        self.page_inicio_content = self.create_inicio_content()
        self.page_inicio.add_widget(self.page_inicio_content)
        with  self.page_inicio.canvas.before:
            Color(1, 1, 1, 1)  # Color en formato RGBA (verde claro)
            self.rect = Rectangle(size= (10000,10000), pos= self.page_inicio_content.pos)
        

        # Guardar el contenido de la página de inicio
        self.saved_content = self.page_inicio_content

        # Mostrar la página de inicio por defecto
        self.layout.add_widget(self.page_inicio)

        # Agregar la barra de navegación
        self.nav_bar = self.create_nav_bar()
        self.layout.add_widget(self.nav_bar)

        return self.layout

    def create_inicio_content(self):
        # Crear el contenido de la página de inicio
        self.tasks = []  # Lista para almacenar las tareas
        self.historial = []  # Lista para almacenar el historial de las tareas
        self.historialcomp = []
        # Crear un ScrollView para contener la lista de tareas
        scrollview = ScrollView()

        # Crear un layout para las tareas dentro del ScrollView
        self.task_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5, padding=(5, 5))
        self.task_list.bind(minimum_height=self.task_list.setter('height'))  # Ajustar la altura del layout según el contenido

        # Crear el layout principal
        inicio_content_layout = BoxLayout(orientation='vertical', padding=[0, 0, 0, 0])

        # Barra superior de bienvenida
        welcome_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.4))
        welcome_label = BackgroundLabel(background_image='fondosup.png', text="Hola \n¡Bienvenido a tu lista de tareas!", font_size=20)
        welcome_bar.add_widget(welcome_label)

        # Agregar la barra superior al layout principal
        inicio_content_layout.add_widget(welcome_bar)

        # Crear un layout horizontal para el input de texto y el botón
        input_button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)

        # Campo de entrada de texto para agregar nuevas tareas
        self.task_input = TextInput(size_hint=(0.7, 0.8), hint_text="Ingrese una nueva tarea",
                                    background_normal='fondinput.png', border=(5, 5, 5, 5))
        input_button_layout.add_widget(self.task_input)

        # Botón para agregar tareas
        add_button = Button(size_hint=(0.1, 0.7), background_normal='add.png', border=(5, 5, 5, 5))
        add_button.bind(on_press=self.add_task)
        input_button_layout.add_widget(add_button)

        # Agregar el layout horizontal al layout principal
        inicio_content_layout.add_widget(input_button_layout)

        # Agregar el layout de tareas al ScrollView
        scrollview.add_widget(self.task_list)
        inicio_content_layout.add_widget(scrollview)

        return inicio_content_layout

#FUNCION DE AÑADIR TAREA 
    def add_task(self, instance):
        task_text = self.task_input.text.strip()
        if task_text:
            task_label = BackgroundLabel(
                text=task_text,
                size_hint=(1, None),
                height=40,
                font_size=16,
                color=(0, 0, 0, 1),
                background_image='bordelist.png'
            )
            tarea = str(task_label.text)

            # Inicializar flag como False para indicar que la tarea no está completa
            flag = False

            delete_button = Button(
                background_normal='eliminar.png',
                size_hint=(None, None),
                size=(60, 60),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            delete_button.bind(on_press=self.delete_task)

            complete_button = Button(
                background_normal='completar.png',
                size_hint=(None, None),
                size=(60, 60),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            complete_button.bind(on_press=self.complete_task)

            task_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
            task_layout.add_widget(task_label)

            # Añadir un espacio flexible entre el label y los botones
            task_layout.add_widget(Widget(size_hint=(0.1, None), width=20))

            task_layout.add_widget(delete_button)
            task_layout.add_widget(complete_button)

            self.task_list.add_widget(task_layout, index=0)  # Agregar en la parte superior de la lista
            self.tasks.insert(0, task_layout)  # Insertar en la parte superior de la lista
            self.task_input.text = ""

            # Leer el archivo para contar las tareas existentes
            file_name = "historial.txt"
            try:
                with open(file_name, "r") as file:
                    lines = file.readlines()
                task_number = len(lines) + 1  # Obtener el siguiente número de orden
            except FileNotFoundError:
                task_number = 1  # Si el archivo no existe, empezar con el número 1

            # Guardar la tarea con número de orden en el archivo de historial
            with open(file_name, "a") as file:
                file.write(f"Pendiente: {tarea}\n")


    def delete_task(self, instance):
        task_layout = instance.parent
        self.task_list.remove_widget(task_layout)
        self.tasks.remove(task_layout)


    def complete_task(self, instance):
        print("complete_task method called")  # Comprobación inicial

        task_layout = instance.parent
        print("Children of task_layout:", task_layout.children)  # Imprimir todos los hijos del layout

        # Buscar el BackgroundLabel en los hijos del layout
        task_label = None
        for child in task_layout.children:
            if isinstance(child, BackgroundLabel):
                task_label = child
                break

        # Verificar si hemos encontrado el task_label
        if task_label is None:
            print("Error: BackgroundLabel not found in task_layout children.")
            return

        # Imprimir información de depuración
        print(f"Task label before completion: {task_label.text}")

        task_label.background_image = "completar.png"
        instance.disabled = True

        # Cambiar la imagen del botón a una nueva imagen
        instance.background_disabled_normal = 'completed.png'

        self.historialcomp.append(task_layout)

        tarea = str(task_label.text)
        print("Tarea: " + tarea)
        file_name = "historial.txt"

        # Leer todas las líneas del archivo de historial
        with open(file_name, "r") as file:
            lines = file.readlines()

        # Buscar y eliminar la tarea completada de las líneas
        with open(file_name, "w") as file:
            for line in lines:
                if tarea not in line:
                    file.write(line)
                else:
                    print(f"Removed task from file: {line.strip()}")

        file_nameCompl = "histcompletadas.txt"
        # Agregar la tarea completada al archivo de historial como completada
        with open(file_nameCompl, "a") as file:
            file.write("Completada:" + tarea + "\n")

        # Imprimir información de depuración al final
        print(f"Task label after completion: {task_label.text}")
        print("Task marked as completed and written to file.")


    def create_nav_bar(self):
        
        # Crear la barra de navegación
        nav_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=45)

        # Agregar botones a la barra de navegación
        self.button_inicio = Button( background_normal='inicio.png')
        self.button_inicio.bind(on_press=self.show_inicio)

        self.button_historial = Button(background_normal='historial.png')
        self.button_historial.bind(on_press=self.show_historial)

        self.button_productividad = Button(background_normal='productividad.png')
        self.button_productividad.bind(on_press=self.show_productividad)

        
        nav_bar.add_widget(self.button_inicio)
        nav_bar.add_widget(self.button_historial)
        nav_bar.add_widget(self.button_productividad)

       
        return nav_bar

    def show_inicio(self, instance):
        # Cambiar el estilo del botón de inicio
        self.button_inicio.background_color = (0.5, 0.5, 0.5, 1)

        # Restaurar el estilo de los otros botones
        self.button_historial.background_color = (1, 1, 1, 1)
        self.button_productividad.background_color = (1, 1, 1, 1)

        # Mostrar la página de inicio y restaurar su contenido guardado
        self.layout.clear_widgets()
        self.layout.add_widget(self.page_inicio)
        self.layout.add_widget(self.nav_bar)

    def show_historial(self, instance):
        # Guardar el contenido actual antes de cambiar de página
        self.saved_content = self.layout.children[0]

        # Mostrar la nueva página
        self.layout.clear_widgets()
        self.layout.add_widget(self.create_historial_content())
        self.layout.add_widget(self.nav_bar)

        # Restaurar el estilo de los botones
        self.button_inicio.background_color = (1, 1, 1, 1)
        self.button_historial.background_color = (0.5, 0.5, 0.5, 1)
        self.button_productividad.background_color = (1, 1, 1, 1)

    def show_productividad(self, instance):
        # Guardar el contenido actual antes de cambiar de página
        self.saved_content = self.layout.children[0]

        # Mostrar la nueva página
        self.layout.clear_widgets()
        self.layout.add_widget(self.create_productividad_content())
        self.layout.add_widget(self.nav_bar)

        # Restaurar el estilo de los botones
        self.button_inicio.background_color = (1, 1, 1, 1)
        self.button_historial.background_color = (1, 1, 1, 1)
        self.button_productividad.background_color = (0.5, 0.5, 0.5, 1)

    
    def create_historial_content(self):
        # Crear el layout principal
    layout = BoxLayout(orientation='vertical')

    # Agregar un fondo blanco
    with layout.canvas.before:
        Color(1, 1, 1, 1)  # Color blanco
        self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

    # Barra superior de bienvenida
    welcome_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.4))
    welcome_label = BackgroundLabel(background_image='fondosup.png', text="HISTORIAL", font_size=20)
    welcome_bar.add_widget(welcome_label)
    layout.add_widget(welcome_bar)

    # Crear el ScrollView y la tabla para las tareas pendientes
    scrollview_pen = ScrollView(size_hint=(1, 0.45))
    tabla_pen = BoxLayout(orientation='vertical', spacing=5, padding=10, size_hint_y=None)
    tabla_pen.bind(minimum_height=tabla_pen.setter('height'))

    # Encabezado de la tabla pendientes
    encabezado_pen = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
    estado_pen = Label(text='PENDIENTES', bold=True, size_hint_x=0.5, color=(0, 0, 0, 1))
    encabezado_pen.add_widget(estado_pen)
    encabezado_pen.add_widget(Label(text='TAREA', bold=True, size_hint_x=0.5, color=(0, 0, 0, 1)))
    encabezado_pen.add_widget(Label(text='', bold=True, size_hint_x=0.2, color=(0, 0, 0, 1)))  # Espacio para el botón
    tabla_pen.add_widget(encabezado_pen)

    # Leer datos desde el archivo historial.txt
    file_name_pen = "historial.txt"
    with open(file_name_pen, "r") as file:
        lines_pen = file.readlines()

    # Agregar filas de datos a la tabla pendientes
    for line in lines_pen:
        parts = line.strip().split(":")
        if len(parts) == 2:
            estado = parts[0]
            tarea = parts[1]
            fila_pen = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
            fila_pen.add_widget(Label(text=estado, size_hint_x=0.5, color=(0, 0, 0, 1)))
            fila_pen.add_widget(Label(text=tarea, size_hint_x=0.5, color=(0, 0, 0, 1)))

            # Agregar botón para completar la tarea
            boton_completar = Button(text='Completar', size_hint_x=0.2)
            boton_completar.bind(on_press=self.completar_tarea)  # Asignar función de callback
            fila_pen.add_widget(boton_completar)

            tabla_pen.add_widget(fila_pen)

    scrollview_pen.add_widget(tabla_pen)
    layout.add_widget(scrollview_pen)

    # Crear el ScrollView y la tabla para las tareas completadas
    scrollview_comp = ScrollView(size_hint=(1, 0.45))
    tabla_comp = BoxLayout(orientation='vertical', spacing=5, padding=10, size_hint_y=None)
    tabla_comp.bind(minimum_height=tabla_comp.setter('height'))

    # Encabezado de la tabla completadas
    encabezado_comp = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
    estado_comp = Label(text='COMPLETADAS', bold=True, size_hint_x=0.5, color=(0, 0, 0, 1))
    encabezado_comp.add_widget(estado_comp)
    encabezado_comp.add_widget(Label(text='TAREA', bold=True, size_hint_x=0.5, color=(0, 0, 0, 1)))
    tabla_comp.add_widget(encabezado_comp)

    # Leer datos desde el archivo histcompletadas.txt
    file_name_comp = "histcompletadas.txt"
    with open(file_name_comp, "r") as file:
        lines_comp = file.readlines()

    # Agregar filas de datos a la tabla completadas
    for line in lines_comp:
        parts = line.strip().split(":")
        if len(parts) == 2:
            estado = parts[0]
            tarea = parts[1]
            fila_comp = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
            fila_comp.add_widget(Label(text=estado, size_hint_x=0.5, color=(0, 0, 0, 1)))
            fila_comp.add_widget(Label(text=tarea, size_hint_x=0.5, color=(0, 0, 0, 1)))
            tabla_comp.add_widget(fila_comp)

    scrollview_comp.add_widget(tabla_comp)
    layout.add_widget(scrollview_comp)

    return layout
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
                
#PANTALLA DE PRODUCTIVIDAD
    def create_productividad_content(self):
        # Crear el layout principal
        layout = BoxLayout(orientation='vertical')

        # Agregar un fondo blanco
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # Color blanco
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

        # Barra superior de bienvenida
        welcome_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=150)  # Aumentar la altura
        welcome_label = BackgroundLabel(background_image='fondosup.png', text="PRODUCTIVIDAD", font_size=20)
        welcome_bar.add_widget(welcome_label)
        layout.add_widget(welcome_bar)

        # Crear un ScrollView para el contenido
        scrollview = ScrollView(size_hint=(1, 1))
        contenido = BoxLayout(orientation='vertical', size_hint_y=None, padding=[0, 20, 0, 0], spacing=20)  # Añadir padding superior y spacing
        contenido.bind(minimum_height=contenido.setter('height'))

        file_name_comp = "histcompletadas.txt"
        with open(file_name_comp, "r") as file:
            taskcomp = file.readlines()
            lines_comp = len(taskcomp)
            print(lines_comp)

        file_name = "historial.txt"
        with open(file_name, "r") as file:
            taskpen = file.readlines()
            lines_pen = len(taskpen)
            print(lines_pen)

        if lines_pen>0 or lines_comp>0:
            totaltasks = lines_comp + lines_pen
            porc_comp = (lines_comp*100)/totaltasks
            porc_pen = (lines_pen*100)/totaltasks
            strtotaltask = str(totaltasks)
        else: 
            totaltasks=0
            porc_comp=0
            porc_pen=0
            strtotaltask = str(totaltasks)

        # Crear el widget de gráfico de torta y ajustar su tamaño
        rojo_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40, padding=[50, 0])  # Añadir padding horizontal
        rojo = BackgroundLabel(background_image='indicadorrojo.png', size_hint=(None, None), size=(30, 30))  # Hacer más pequeño
        rojotext = Label(text="Tareas pendientes (%"+f"{porc_pen:.2f}"+")", color=(0, 0, 0, 1), bold=True)

        rojo_layout.add_widget(rojo)
        rojo_layout.add_widget(rojotext)

        verde_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40, padding=[50, 0])  # Añadir padding horizontal
        verde = BackgroundLabel(background_image='indicadorverde.png', size_hint=(None, None), size=(30, 30))  # Hacer más pequeño
        verdetext = Label(text="Tareas completadas (%"+f"{porc_comp:.2f}"+")", color=(0, 0, 0, 1), bold=True)

        verde_layout.add_widget(verde)
        verde_layout.add_widget(verdetext)

        contenido.add_widget(rojo_layout)
        contenido.add_widget(verde_layout)

        totalTareas = Label(text="TOTAL de TAREAS: " + strtotaltask, color=(0, 0, 0, 1), bold=True)
        contenido.add_widget(totalTareas)

        # Crear el widget de gráfico de torta y ajustar su tamaño y posición manualmente
        pie_chart = PieChart(pos=(60,0))  # Tamaño ajustado a ser más pequeño
        pie_chart.set_porcentaje(porc_comp)  # Establecer el porcentaje del gráfico de torta

      
        # Agregar el PieChart al contenido
        contenido.add_widget(pie_chart)

        # Agregar el contenido al ScrollView
        scrollview.add_widget(contenido)

        # Agregar el ScrollView al layout principal
        layout.add_widget(scrollview)

        return layout




    
if __name__ == '__main__':
    TaskApp().run()
