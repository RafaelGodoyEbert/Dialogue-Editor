import re
from PIL import ImageDraw
from PIL.ImageQt import ImageQt
from PySide6.QtGui import QPixmap

class PageEntry:
    def __init__(self, text, image):
        self.text = text
        self.image = image
        self.pixmap = None        

    def render_text(self, font, color, position):
        """
        Renders text onto the image and returns a QPixmap.
        'color' should be a tuple or string Pil-compatible.
        """
        # Remove as tags específicas do texto antes de renderizar
        cleaned_text = re.sub(r'\{t\d+\}', '', self.text)

        if self.image is None:
            return None

        image_copy = self.image.copy()
        draw = ImageDraw.Draw(image_copy)
        draw.text(position, cleaned_text, font=font, fill=color)
        
        qimage = ImageQt(image_copy)
        self.pixmap = QPixmap.fromImage(qimage)
        return self.pixmap
