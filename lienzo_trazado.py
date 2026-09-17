from gestor_datos import actualizar_progreso
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class RielesLienzo(Widget):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.bind(size=self.dibujar_rieles, pos=self.dibujar_rieles)

  def dibujar_rieles(self, *args):
    self.canvas.before.clear()
    ancho, alto = self.size
    x, y = self.pos
    alto_franja = alto / 3

    with self.canvas.before:
      # Cielo (Azul claro)
      Color(0.7, 0.85, 1, 1)
      Rectangle(pos=(x, y + alto_franja * 2), size=(ancho, alto_franja))

      # Pasto (Verde claro)
      Color(0.7, 0.9, 0.7, 1)
      Rectangle(pos=(x, y + alto_franja), size=(ancho, alto_franja))

      # Tierra (Marrón suave)
      Color(0.85, 0.75, 0.65, 1)
      Rectangle(pos=(x, y), size=(ancho, alto_franja))

  def on_touch_down(self, touch):
    if self.collide_point(*touch.pos):
      with self.canvas:
        Color(0.1, 0.1, 0.1, 1)  # Color del trazo (Negro)
        touch.ud['linea'] = Line(points=(touch.x, touch.y), width=6)

  def on_touch_move(self, touch):
    if 'linea' in touch.ud and self.collide_point(*touch.pos):
      touch.ud['linea'].points += [touch.x, touch.y]


class PantallaLienzo(BoxLayout):

  def __init__(self, vocal, al_volver_callback, **kwargs):
    super().__init__(**kwargs)
    self.orientation = 'vertical'
    self.vocal = vocal
    self.al_volver_callback = al_volver_callback

    # Encabezado
    self.add_widget(
        Label(
            text=f'Traza la vocal: {self.vocal}',
            font_size='22sp',
            size_hint_y=0.1,
        )
    )

    # Area de dibujo táctil
    self.lienzo = RielesLienzo(size_hint_y=0.75)
    self.add_widget(self.lienzo)

    # Botones inferiores
    panel_btns = BoxLayout(size_hint_y=0.15, spacing=10, padding=5)

    btn_limpiar = Button(
        text='Borrar', background_color=(0.9, 0.4, 0.4, 1)
    )
    btn_limpiar.bind(on_press=self.limpiar)

    btn_completar = Button(
        text='¡Listo! ⭐⭐⭐', background_color=(0.2, 0.7, 0.3, 1)
    )
    btn_completar.bind(on_press=self.guardar_y_volver)

    panel_btns.add_widget(btn_limpiar)
    panel_btns.add_widget(btn_completar)
    self.add_widget(panel_btns)

  def limpiar(self, instance):
    self.lienzo.canvas.clear()
    self.lienzo.dibujar_rieles()

  def guardar_y_volver(self, instance):
    actualizar_progreso(self.vocal, estrellas=3)
    self.al_volver_callback()