from gestor_datos import guardar_perfil
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput


class PantallaFormulario(BoxLayout):

  def __init__(self, al_completar_callback, **kwargs):
    super().__init__(**kwargs)
    self.orientation = 'vertical'
    self.padding = 20
    self.spacing = 10
    self.al_completar_callback = al_completar_callback

    self.add_widget(
        Label(text='Registro del Estudiante', font_size='22sp', bold=True)
    )

    self.add_widget(Label(text='Nombre completo del alumno:'))
    self.txt_nombre = TextInput(
        multiline=False, hint_text='Ej. Karla Sánchez'
    )
    self.add_widget(self.txt_nombre)

    self.add_widget(Label(text='Grado / Sección:'))
    self.spn_grado = Spinner(
        text='Primero A', values=('Primero A', 'Primero B', 'Primero C')
    )
    self.add_widget(self.spn_grado)

    self.add_widget(Label(text='Número en lista:'))
    self.txt_numero = TextInput(
        multiline=False, input_filter='int', hint_text='Ej. 1'
    )
    self.add_widget(self.txt_numero)

    btn_guardar = Button(
        text='Guardar e Iniciar',
        size_hint_y=0.3,
        background_color=(0.2, 0.6, 0.9, 1),
    )
    btn_guardar.bind(on_press=self.procesar_guardado)
    self.add_widget(btn_guardar)

  def procesar_guardado(self, instance):
    nombre = self.txt_nombre.text.strip() or 'Estudiante'
    grado = self.spn_grado.text
    numero = int(self.txt_numero.text.strip() or 1)

    datos = guardar_perfil(nombre, grado, numero)
    self.al_completar_callback(datos)