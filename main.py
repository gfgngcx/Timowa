import firebase_admin
from firebase_admin import credentials, firestore
import threading
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock

Window.clearcolor = 1, 1, 1, 1

# JSON-Daten
json_data = {
    "type": "service_account",
    "project_id": "testchat-c3abe",
    "private_key_id": "ba45c5f61a45aa35591fd911f378edc9f9ab7ccf",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC+mYa8LQfPKkz5\nRltS4xbB2r3XdcnNhAbGxgzIlDTux8YheGAqrLicRvc1fa2NYQmQoEKrPla6vxk4\ntmN4vkn6gATTIv7icLHTT9/jlZ3DwQMe7NrauNLP3PD/r+52SnhH9BV8FPqjUeeB\nvhXo28q5ff2Av7Ouz7qs1X2Sk+vYp9sllmILT3iSrIhDeakIC1W0OUJOs1L8Hv1Q\n4m/KsfBh7sulDcqcn+WgTQKWjJqS3vChQIajTxzu2bH7w2YUXIhhYIkHYgQzzUwt\nRFT37EdWUfZ9E249uP+GeqTGr/Za65SM6ivBKkPn2KKREEO5lTAM/vZqqwPy7xOr\ncu2/tOr9AgMBAAECggEAGcOxFeDUbGmgbBXZpHO0ENJb1TND6zcMn3QIKFj4asqw\nerfF8B7W+bESG7X4buMOIvG28WUE3kuUwjjNa3X1lBoYDN5vK/bl4tWqQx5nbB28\nKUMFNonDXXvVTArhJjZc2gUhnltLoiYhMEWcupRza+2fBfdj95528oQNbHH4cJnM\nERgMut2vAMpsO2xn60d0szdX2De04oNiE+y6Rby0g7BCeRcOHwcjy+uwItx/nEhv\nE4cXDnQrAyXEB5L2oKw8Mpa66SGozYZNaanuTFLtZ/ux/1k2KynvmqPz61bq55oh\n+ziuPCQMmKJDQ+I1jLINrD8ELhn1YtpDNHGr6NjsFQKBgQD2I12kWGYwzVv2MP/7\nbjupI0VxOBeikVPUQcfmK2L0Y2Izy5MUBcZm+cS4icsRPvTwOMlctrgn1yfqYCNf\ndhKTYnp49Rh39SFeDxRb+v66hynKHIs4ykWpVBcaHjmBeBSBbp0EwS6kACKK7A+8\nQQRPgkOTzMn2R4rL+g653DAPnwKBgQDGPID9MDnvpku3GAi1joBo5gZAWue28QrG\nXcRyfbsNb9UmNzxCpsOutGr8YyPjhax4GesNrQnPZsrberYgWOknvoSUBRf9t/qX\nDT5ktZMF5BNWy/6dS+qLUnLXSO7zYgP2yfXXP7jLB2L8reOBADEZ7Ew8Abb+cjbh\nhWJ1aZtP4wKBgH6nZhkaL8Nu+KIvRplfeK2o66O9xFOvyl4PV0h2DN5KgY67czw7\nWINGhNacePSv26P85IijsRE3Il/1Bl6pyBc09mZlYCjh50CaK9TEy+y5fmR02aLo\nWn4uOhEDen3Hh22uuHdo3JIhS6UGoXYyUoCDPDjCiS4EVERvsMIsrkJrAoGBAK9c\n4KKZofbdPkeXDEVH7VJeghM2F5sfOm/mjRzXGry1PHKVFErF6X9H/QiNzza7jqmk\nC+pKM850WWm08R5GaOMOx4uFwgZhVV2AirxeX9QrQexbgz605KQg6JSH4VIOWAFe\nAYtLxHZeb3OlhAcfG1CaV4oR3kbS1LfF3iaNqKYPAoGATRSyO7dWIbOGyovBH6Dl\nMJsDbPpjp8leOisCQtUqxDvKDOtG4TwxAEhUUnq7d/PPdBuA60bbiFXHNebdn45Z\n2GF28fZrKgk7zKr/b4QDdb9z1y+LxImnJA9ZZ5EDYRAWa0ATzdZsDDU54m8jb9Be\ngIZzn1xn9/diZjnhdt3FnCg=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-ikt8o@testchat-c3abe.iam.gserviceaccount.com",
    "client_id": "107349512788397650706",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ikt8o%40testchat-c3abe.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# Initialisiere Firebase-App mit den Anmeldedaten
cred = credentials.Certificate(json_data)
firebase_admin.initialize_app(cred)

# Initialisiere Firestore-Datenbank
db = firestore.client()

class Background(Widget):
    pass

class ChatApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = None
        self.chat_messages = []

    def build(self):
        layout = BoxLayout(orientation='vertical')

        background = Background()
        layout.add_widget(background)

        with background.canvas.before:
            Color(1, 1, 1, 1)  # Weißer Hintergrund
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

        self.chat_display = ScrollView()
        self.chat_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.chat_display.add_widget(self.chat_layout)
        layout.add_widget(self.chat_display)

        self.message_entry = TextInput(size_hint_y=None, height=60, multiline=False, font_size=20)
        self.message_entry.bind(on_text_validate=self.send_message)
        layout.add_widget(self.message_entry)

        button_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)

        self.send_button = Button(text="Senden", size_hint_x=None, width=100, font_size=20)
        self.send_button.bind(on_press=self.send_message)
        button_layout.add_widget(self.send_button)

        self.username_entry = TextInput(hint_text='Benutzername', multiline=False, font_size=20)
        self.username_entry.bind(on_text_validate=self.set_username)
        button_layout.add_widget(self.username_entry)

        layout.add_widget(button_layout)

        # Starte den Thread für das Empfangen von Nachrichten
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        return layout

    def set_username(self, *args):
        self.username = self.username_entry.text
        self.username_entry.disabled = True
        self.message_entry.focus = True

    def send_message(self, *args):
        message_text = self.message_entry.text
        if message_text and self.username:
            message_data = {
                'username': self.username,
                'message_text': message_text,
                'timestamp': firestore.SERVER_TIMESTAMP
            }
            db.collection('messages').add(message_data)
            self.message_entry.text = ''

    def receive_messages(self):
        messages_ref = db.collection('messages').order_by('timestamp')
        while True:
            docs = messages_ref.stream()
            messages = [doc.to_dict() for doc in docs if 'username' in doc.to_dict() and 'message_text' in doc.to_dict()]
            self.chat_messages = messages
            Clock.schedule_once(lambda dt: self.on_chat_messages(self, self.chat_messages))
            time.sleep(1)  # Überprüfe alle Sekunde auf neue Nachrichten

    def on_chat_messages(self, instance, value):
        self.display_chat()

    def display_chat(self):
        self.chat_layout.clear_widgets()
        for message in self.chat_messages:
            label = Label(text=f"{message['username']}: {message['message_text']}", size_hint_y=None, height=40,
                          font_size=18, color=(0, 0, 0, 1))  # Schwarzer Text
            self.chat_layout.add_widget(label)

    def on_stop(self):
        self.receive_thread.join()

def delete_all_messages():
    messages_ref = db.collection('messages')
    docs = messages_ref.stream()
    for doc in docs:
        doc.reference.delete()

def main():
    # Lösche alle Nachrichten beim Start des Scripts
    delete_all_messages()
    time.sleep(1)  # Kurze Pause, um sicherzustellen, dass das Löschen abgeschlossen ist

    app = ChatApp()
    app.run()

if __name__ == "__main__":
    main()
