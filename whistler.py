import globalPluginHandler
import socket
import speech
from speech.commands import BeepCommand, BreakCommand
from characterProcessing import SymbolLevel
import threading
import tones
import time


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q = []
        self.symbol_level = None
        self.t = threading.Thread(target=self.run, daemon=True)
        self.t.start()

    def extract(self, message):
        return message[message.find("{") + 1 : message.find("}")]

    def process_queue(self):
        cmds=[]
        for item in self.q:
            if item.startswith('q'):
                cmds.append(self.extract(item))
            elif item.startswith('t'):
                words = item.split()
                cmds.append(BeepCommand(int(words[1]), int(words[2])))
            elif item.startswith('sh'):
                words = item.split()
                cmds.append(BreakCommand(int(words[1])))
        self.q.clear()
        speech.speak(cmds, symbolLevel = self.symbol_level)

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
            case "q" | "t" | "sh":
                self.q.append(message)
            case "s":
                self.q.clear()
                speech.cancelSpeech()
            case "d":
                self.process_queue()
            case "tts_set_punctuations":
                match words[1]:
                    case "none": self.symbol_level = SymbolLevel.NONE
                    case "some": self.symbol_level = SymbolLevel.SOME
                    case "all": self.symbol_level = SymbolLevel.ALL

