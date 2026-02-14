import re
from googletrans import Translator

class TranslationService:
    def __init__(self):
        self.translator = Translator()

    def translate_line_with_tags(self, line, source_language, target_language):
        parts = re.split(r'(\{.*?\}|\[.*?\]|\<.*?\>)', line)
        translated_parts = []
        for part in parts:
            if re.match(r'\{.*?\}|\[.*?\]|\<.*?\>', part):
                translated_parts.append(part)
            else:
                try:
                    translation = self.translator.translate(part, dest=target_language, src=source_language)
                    translated_text = translation.text if translation else part
                    translated_parts.append(translated_text)
                except Exception as e:
                    print("Erro na tradução:", str(e))
                    translated_parts.append(part)
        return ''.join(translated_parts)

    def translate_text(self, text, source_language, target_language):
        lines = text.split('\n')
        translated_lines = []
        for line in lines:
            translated_line = self.translate_line_with_tags(line, source_language, target_language)
            translated_lines.append(translated_line)
        return '\n'.join(translated_lines)
