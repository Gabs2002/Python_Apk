from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.screenmanager import ScreenManager, Screen
from pyModbusTCP.client import ModbusClient
from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)  # Define a cor de fundo para branco
class ConnectionScreen(Screen):
    def __init__(self, **kwargs):
        super(ConnectionScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=[40, 250], size=(360, 640))

        self.ip_input = TextInput(hint_text='IP Address', multiline=False, size_hint_y=None, height=40,
                                  background_normal='', background_color=(1, 1, 1, 0.8))
        self.port_input = TextInput(hint_text='Port', multiline=False, input_type='number', size_hint_y=None, height=40,
                                    background_normal='', background_color=(1, 1, 1, 0.8))
        connect_button = Button(text='Connect', on_press=self.connect_pressed, size_hint_y=None, height=40,
                                background_normal='', background_color=(0.33, 0.66, 1, 1))

        layout.add_widget(self.ip_input)
        layout.add_widget(self.port_input)
        layout.add_widget(connect_button)

        self.add_widget(layout)

    def connect_pressed(self, instance):
        ip = self.ip_input.text
        port = int(self.port_input.text)

        app = App.get_running_app()
        app.modbus_client = ModbusClient(ip, port, auto_open=True)

        if app.modbus_client.open():
            app.sm.current = 'control'

class ControlScreen(Screen):
    def __init__(self, **kwargs):
        super(ControlScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=[40, 180], size=(360, 640))

        button1 = Button(text='Stop', on_press=lambda x: self.send_command(1,slider.value), size_hint_y=None, height=40,
                         background_normal='', background_color=(0.33, 0.66, 1, 1))
        button2 = Button(text='Go Right', on_press=lambda x: self.send_command(2,slider.value), size_hint_y=None, height=40,
                         background_normal='', background_color=(0.33, 0.66, 1, 1))
        button3 = Button(text='Go Left', on_press=lambda x: self.send_command(3,slider.value), size_hint_y=None, height=40,
                         background_normal='', background_color=(0.33, 0.66, 1, 1))
        slider = Slider(min=5, max=10, value=5)

        disconnect_button = Button(text='Disconnect', on_press=self.disconnect_pressed,
                                   size_hint_y=None, height=40, background_normal='', background_color=(1, 0, 0, 1))

        layout.add_widget(button1)
        layout.add_widget(button2)
        layout.add_widget(button3)
        layout.add_widget(slider)
        layout.add_widget(disconnect_button)

        self.add_widget(layout)

    def send_command(self, reg_value,slider_val):
        try:
            # Modifica o registrador de endereço 1
            app = App.get_running_app()
            app.modbus_client.write_single_register(1, reg_value)
            app.modbus_client.write_single_register(2,int(slider_val))
            print(f"Registrador 1 modificado para: {reg_value}")
            print(f'Valor do slider {int(slider_val)}')
        except Exception as e:
            print(f"Erro ao modificar registrador: {e}")

    def disconnect_pressed(self, instance):
        app = App.get_running_app()
        app.modbus_client.close()
        app.sm.current = 'connection'

class MyApp(App):
    def build(self):
        # Screen manager to handle switching between screens
        self.sm = ScreenManager()

        # Create and add screens
        connection_screen = ConnectionScreen(name='connection')
        control_screen = ControlScreen(name='control')

        self.sm.add_widget(connection_screen)
        self.sm.add_widget(control_screen)
        self.title ="Client Control"
        return self.sm

if __name__ == '__main__':
    MyApp().run()
