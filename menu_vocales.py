from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class MenuVocales(BoxLayout):

  def __init__(self, al_seleccionar_vocal, al_ver_reporte, **kwargs):
    super().__init__(**kwargs)
    self.orientation = 'vertical'
    self.padding = 20
    self.spacing = 15
    self.al_seleccionar_vocal = al_seleccionar_vocal
    self.al_ver_reporte = al_ver_reporte

    self.add_widget(
        Label(text='¡Elige una Vocal!', font_size='24sp', bold=True)
    )

    grid = GridLayout(cols=3, spacing=10, size_hint_y=0.6)
    vocales = ['A', 'E', 'I', 'O', 'U']

    for v in vocales:
      btn = Button(
          text=v, font_size='32sp', background_color=(0.3, 0.7, 0.9, 1)
      )
      btn.bind(
          on_press=lambda inst, vocal=v: self.al_seleccionar_vocal(vocal)
      )
      grid.add_widget(btn)

    self.add_widget(grid)

    btn_reporte = Button(
        text='Ver Reporte del Docente',
        size_hint_y=0.2,
        background_color=(0.2, 0.8, 0.4, 1),
    )
    btn_reporte.bind(on_press=lambda inst: self.al_ver_reporte())
    self.add_widget(btn_reporte)