from deep_translator import GoogleTranslator

class Translator:
    async def to_en(self, text: str, src_lang: str) -> str:
        try:
            if not src_lang or src_lang == "en":
                return text
            return GoogleTranslator(source=src_lang, target="en").translate(text)
        except Exception:
            return text

    async def from_en(self, text: str, dst_lang: str) -> str:
        try:
            if not dst_lang or dst_lang == "en":
                return text
            return GoogleTranslator(source="en", target=dst_lang).translate(text)
        except Exception:
            return text
