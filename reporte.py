from gestor_datos import cargar_datos
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class PantallaReporte(BoxLayout):

  def __init__(self, al_volver_callback, **kwargs):
    super().__init__(**kwargs)
    self.orientation = 'vertical'
    self.padding = 20
    self.spacing = 10
    self.al_volver_callback = al_volver_callback
    self.construir_reporte()

  def on_pre_enter(self, *args):
    self.construir_reporte()

  def construir_reporte(self):
    self.clear_widgets()

    datos = cargar_datos() or {}
    perfil = datos.get(
        'perfil_activo',
        {'nombre': 'Sin registro', 'grado': '-', 'numero_lista': 0},
    )

    self.add_widget(
        Label(
            text='Reporte de Progreso', font_size='22sp', bold=True
        )
    )
    self.add_widget(
        Label(
            text=(
                f"Alumno: #{perfil.get('numero_lista')} -"
                f" {perfil.get('nombre')}\nGrupo: {perfil.get('grado')}"
            ),
            halign='center',
        )
    )

    grid = GridLayout(cols=1, spacing=5, size_hint_y=0.6)
    progreso = datos.get('progreso', {})

    for vocal, info in progreso.items():
      estrellas = '⭐' * int(info.get('estrellas', 0)) if info.get('estrellas', 0) > 0 else '☆☆☆'
      texto = (
          f"Vocal [{vocal}]: {estrellas} | Estado: {info.get('estado', 'Pendiente')} | Intentos:"
          f" {info.get('intentos', 0)}"
      )
      grid.add_widget(Label(text=texto, font_size='14sp'))

    self.add_widget(grid)

    btn_volver = Button(
        text='← Volver al Menú',
        size_hint_y=0.15,
        background_color=(0.3, 0.5, 0.8, 1),
    )
    btn_volver.bind(on_press=lambda inst: self.al_volver_callback())
    self.add_widget(btn_volver)