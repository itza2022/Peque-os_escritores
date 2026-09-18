from formulario import PantallaFormulario
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from lienzo_trazado import PantallaLienzo
from menu_vocales import MenuVocales
from reporte import PantallaReporte


class PequeñosEscritoresApp(App):

  def build(self):
    self.title = 'Pequeños Escritores'
    self.sm = ScreenManager(transition=SlideTransition())

    # 1. Pantalla Inicial: Formulario de Registro
    pantalla_form = Screen(name='formulario')
    pantalla_form.add_widget(
        PantallaFormulario(al_completar_callback=self.ir_a_menu)
    )
    self.sm.add_widget(pantalla_form)

    return self.sm

  def ir_a_menu(self, datos=None):
    """Navega hacia el Menú de Selección de Vocales."""
    if not self.sm.has_screen('menu'):
      pantalla_menu = Screen(name='menu')
      pantalla_menu.add_widget(
          MenuVocales(
              al_seleccionar_vocal=self.ir_a_lienzo,
              al_ver_reporte=self.ir_a_reporte,
          )
      )
      self.sm.add_widget(pantalla_menu)

    self.sm.transition.direction = 'left'
    self.sm.current = 'menu'

  def ir_a_lienzo(self, vocal):
    """Crea o actualiza la pantalla del lienzo con la vocal elegida."""
    nombre_pantalla = f'lienzo_{vocal}'

    if not self.sm.has_screen(nombre_pantalla):
      pantalla_lienzo = Screen(name=nombre_pantalla)
      vista_lienzo = PantallaLienzo(
          vocal=vocal, al_volver_callback=self.volver_al_menu
      )
      pantalla_lienzo.add_widget(vista_lienzo)
      self.sm.add_widget(pantalla_lienzo)

    self.sm.transition.direction = 'left'
    self.sm.current = nombre_pantalla

  def ir_a_reporte(self):
    """Abre la pantalla del reporte general de progreso."""
    if not self.sm.has_screen('reporte'):
      pantalla_rep = Screen(name='reporte')
      vista_rep = PantallaReporte(al_volver_callback=self.volver_al_menu)
      pantalla_rep.add_widget(vista_rep)
      self.sm.add_widget(pantalla_rep)

    self.sm.transition.direction = 'left'
    self.sm.current = 'reporte'

  def volver_al_menu(self):
    """Regresa al menú principal con una transición hacia la derecha."""
    self.sm.transition.direction = 'right'
    self.sm.current = 'menu'


if __name__ == '__main__':
  PequeñosEscritoresApp().run()