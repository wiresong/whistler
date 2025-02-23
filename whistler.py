import globalPluginHandler
import socket
import speech
import threading
import tones
import time


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q = []
        self.t = threading.Thread(target=self.run, daemon=True)
        self.t.start()

    def extract(self, message):
        return message[message.find("{") + 1 : message.find("}")]

    def process_queue(self):
        for item in self.q:
            if item.startswith('q'):
                speech.speakMessage(self.extract(item))
            elif item.startswith('t'):
                words = item.split()
                tones.beep(int(words[1]), int(words[2]))
            elif item.startswith('sh'):
                words = item.split()
                time.sleep(int(words[1])/1000)
        self.q.clear()

    def run(self):
        buffer = ""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(("0.0.0.0", 5000))
            while True:
                try:
                    data = s.recv(1024).decode("utf-8")
                    buffer += data
                    while "\n" in buffer:
                        message, buffer = buffer.split("\n", 1)
                        self.process(message)
                except:
                    pass

    def process(self, message):
        words = message.split()
        match words[0]:
            case "version":
                speech.speakText("nvda Emacs server")
            case "tts_reset":
                speech.cancelSpeech()
                self.q.clear()
            case "tts_say":
                speech.speakMessage(self.extract(message))
            case "l":
                speech.speakSpelling(self.extract(message))
            case "q" | "t":
                self.q.append(message)
            case "s":
                self.q.clear()
                speech.cancelSpeech()
            case "d":
                self.process_queue()
