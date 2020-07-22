import kivy
from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.label  import Label
from kivy.lang  import Builder
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.uix.button import Button
from jnius import autoclass

Builder.load_string("""
<AudioTool>
    orientation: 'vertical'
    Label:
        id: display_label
        text: '00:00'

    BoxLayout:
        size_hint: 1, .2
        TextInput:
            id:user_input
            text: '5'
            disabled: duration_switch.active == False
            on_text: root.enforce_numeric()

        Switch:
            id: duration_switch

    BoxLayout:
        Button:
            id: start_button
            text: 'Start recording'
            on_release: root.startRecording_clock()

        Button:
            id: stop_button
            text: 'Stop recording'
            on_release: root.stopRecording()
            disabled: True
""")

class MyRecorder:
    def __init__(self):
        self.MediaRecorder = autoclass('android.media.MediaRecorder')
        self.AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
        self.OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
        self.AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')

        #create a recorder
        self.mRecorder = self.MediaRecorder()
        self.mRecorder.setAudioSource(self.AudioSource.MIC)
        self.mRecorder.setOutputFormat(self.OutputFormat.)
        self.mRecorder.setOutputFile('/sdcard/kivy/robin/rb.wav')
        self.mRecorder.setAudioEncoder(self.AudioEncoder.AMR_NB)
        self.mRecorder.prepare()



class TestApp(App):
    def build(self):
        return AudioTool()

class AudioTool(BoxLayout):
    def __init__(self, **kwargs):
        super(AudioTool, self).__init__(**kwargs)
        self.start_button = self.ids['start_button']
        self.stop_button = self.ids['stop_button']
        self.display_label = self.ids['display_label']
        self.switch = self.ids['duration_switch']
        self.user_input = self.ids['user_input']


    def enforce_numeric(self):
        if self.user_input.text.isdigit() == False:
            digit_list = [num for num in self.user_input.text if num.isdigit()]
            self.user_input.text = "".join(digit_list)

    def startRecording_clock(self):
        self.mins = 0
        self.zero = 1
        self.duration = int(self.user_input.text)
        Clock.schedule_interval(self.updateDisplay, 1)
        self.start_button.disabled = True
        self.stop_button.disabled = False
        self.switch.disabled = True
        Clock.schedule_once(self.startRecording)

    def startRecording(self, dt):
        self.r = MyRecorder()
        self.r.mRecorder.start()

    def stopRecording(self):
        Clock.unschedule(self.updateDisplay)
        self.r.mRecorder.stop()
        self.r.mRecorder.release()
        Clock.unschedule(self.startRecording)
        self.display_label.text = 'Finished Recording'
        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.switch.disabled = False


    def updateDisplay(self, dt):
        if self.switch.active == False:
            if self.zero < 60 and len(str(self.zero)) == 1:
                self.display_label.text = '0' + str(self.mins) + ':0' + str(self.zero)
                self.zero += 1

            elif self.zero < 60 and len(str(self.zero)) == 2:
                self.display_label.text = '0' + str(self.mins) + ':' + str(self.zero)
                self.zero += 1
            elif self.zero == 60:
                self.mins += 1
                self.display_label.text = '0' + str(self.mins) + ':00' + str(self.zero)
                self.zero += 1
        elif self.switch.active == True:
                if self.duration == 0:
                    self.display_label.text = 'Recording finished'
                    self.stopRecording()
                elif self.duration > 0 and len(str(self.duration)) == 1:
                    self.display_label.text = '00' + ':0' + str(self.duration)
                    self.duration -= 1
                elif self.duration > 0 and self.duration < 60 and len(str(self.duration)) == 2:
                    self.display_label.text = '00' + ':' + str(self.duration)
                    self.duration -= 1
                elif self.duration >= 60 and len(str(self.duration % 60)) == 1:
                    self.mins = self.duration / 60
                    self.display_label.text = '0' + ':0' + str(self.duration)
                    self.duration -= 1
                elif self.duration >= 60 and len(str(self.duration % 60)) == 2:
                    self.mins = self.duration / 60
                    self.display_label.text = '0' + ':' + str(self.duration)
                    self.duration -= 1

if __name__ == '__main__':
    TestApp().run()
