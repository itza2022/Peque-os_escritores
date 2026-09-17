from formulario import PantallaFormulario
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from menu_vocales import MenuVocales
from reporte import PantallaReporte


class PequeñosEscritoresApp(App):

  def build(self):
    self.sm = ScreenManager()

    # Pantalla 1: Formulario
    pantalla_form = Screen(name='formulario')
    pantalla_form.add_widget(
        PantallaFormulario(al_completar_callback=self.ir_a_menu)
    )
    self.sm.add_widget(pantalla_form)

    return self.sm

  def ir_a_menu(self):
    # Transición al menú de vocales
    if not self.sm.has_screen('menu'):
      pantalla_menu = Screen(name='menu')
      pantalla_menu.add_widget(
          MenuVocales(
              al_seleccionar_vocal=self.ir_a_lienzo,
              al_ver_reporte=self.ir_a_reporte,
          )
      )
      self.sm.add_widget(pantalla_menu)
    self.sm.current = 'menu'

  def ir_a_lienzo(self, vocal):
    # La pantalla del lienzo trazado se cargará dinámicamente según la vocal
    pass

  def ir_a_reporte(self):
    pass


if __name__ == '__main__':
  PequeñosEscritoresApp().run()