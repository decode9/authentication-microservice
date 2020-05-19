from pynput import keyboard

class hotKeys():

    def __init__(self, COMBINATIONS, callback, *callParams):
        self.callback = callback
        self.callParams = callParams
        self.COMBINATIONS = COMBINATIONS
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def execute(self, key):
        self.callParams and self.callback(key, self.callParams) or self.callback(key)
        
    def on_press(self, key):
        if key in self.COMBINATIONS:
            self.execute(key)
