from src.index import INDEX, MODES

# Mode types: course, random,  words, texts
class Mode:
    def __init__(self, type="course", layout=None, language=None):
        if type in MODES:
            self.type = type
        else:
            raise ValueError("Invalid mode type")
        if layout in INDEX["layouts"] or language in INDEX["languages"]:
            self.layout = layout
            self.language = language
        else:
            raise ValueError("Incorrect layout or language")
