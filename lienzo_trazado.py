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
    self.puntos_trazo = []

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
      self.puntos_trazo = [(touch.x, touch.y)]
      return True

  def on_touch_move(self, touch):
    if 'linea' in touch.ud and self.collide_point(*touch.pos):
      touch.ud['linea'].points += [touch.x, touch.y]
      self.puntos_trazo.append((touch.x, touch.y))
      return True

  def on_touch_up(self, touch):
    if 'linea' in touch.ud:
      self.puntos_trazo.append((touch.x, touch.y))
      return True

  def evaluar_trazo(self):
    """Evalúa si el trazo es un intento válido para la vocal."""
    puntos = self.puntos_trazo
    if len(puntos) < 8:
      return 0

    xs = [p[0] for p in puntos]
    ys = [p[1] for p in puntos]
    ancho = max(xs) - min(xs)
    alto = max(ys) - min(ys)
    distancia = 0
    for i in range(1, len(puntos)):
      x1, y1 = puntos[i - 1]
      x2, y2 = puntos[i]
      distancia += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    if len(puntos) >= 25 and ancho > 50 and alto > 30 and distancia > 120:
      return 3
    if len(puntos) >= 12 and ancho > 20 and alto > 15 and distancia > 40:
      return 2
    if len(puntos) >= 8 and ancho > 10 and alto > 10:
      return 1
    return 0


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
    self.lienzo.puntos_trazo = []
    self.lienzo.dibujar_rieles()

  def guardar_y_volver(self, instance):
    estrellas = self.lienzo.evaluar_trazo()
    actualizar_progreso(self.vocal, estrellas=estrellas)
    self.al_volver_callback()