import socket
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window

class RemoteKeyboardClient(App):
    def __init__(self, **kwargs):
        super(RemoteKeyboardClient, self).__init__(**kwargs)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('YOUR_IP_ADDRESS', 12345))  # Replace with your IP address and port
    
    def build(self):
        layout = BoxLayout(orientation='vertical')
        for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            btn = Button(text=char, on_press=self.key_press, on_release=self.key_release)
            layout.add_widget(btn)
        return layout
    
    def key_press(self, instance):
        self.client_socket.send(f"PRESS:{instance.text}".encode())
    
    def key_release(self, instance):
        self.client_socket.send(f"RELEASE:{instance.text}".encode())

    def on_stop(self):
        self.client_socket.close()

if __name__ == "__main__":
    RemoteKeyboardClient().run()
