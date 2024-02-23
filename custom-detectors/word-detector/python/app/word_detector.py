from google.cloud import vision

WORD_SEPARATORS = "`~!@#$%^&*()-_=+[{]}\|;:'\",.<>/?"


class WordDetector:
    def __init__(self):
        self._client = vision.ImageAnnotatorClient()
    
    def _iterate_words(self, pages: list[vision.Page]) -> list[str]:
        for page in pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        yield word

    def _include_separator(self, word_text: str) -> bool:
        return any(s in word_text for s in WORD_SEPARATORS)
    
    def detect(self, content: str) -> list[float]:
        """Detect words in an image.
        Word means sequential letters without any sperator like space or comma.
        For example, words of abc.def are "abc" and "def".

        Args:
            content (str): image enceded in base64

        Returns:
            list[list[float]]:
                list of bounding boxes of words.
                Each box is represented as [min_x, min_y, max_x, max_y], and each value is normalized from 0 to 1.
        """
        image = vision.Image(content=content)
        response = self._client.text_detection(image=image)
        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(
                    response.error.message
                )
            )
        pages = response.full_text_annotation.pages
        width = pages[0].width
        height = pages[0].height
        boxes = []
        for word in self._iterate_words(pages):
            word_text = "".join([symbol.text for symbol in word.symbols])
            if not self._include_separator(word_text):
                min_x = 1
                min_y = 1
                max_x = 0
                max_y = 0
                for vertex in word.bounding_box.vertices:
                    normalized_x = vertex.x / width
                    normalized_y = vertex.y / height
                    min_x = min(min_x, normalized_x)
                    min_y = min(min_y, normalized_y)
                    max_x = max(max_x, normalized_x)
                    max_y = max(max_y, normalized_y)
                box = [min_x, min_y, max_x, max_y]
                boxes.append(box)
                continue

            min_y = 1
            max_y = 0
            for vertex in word.bounding_box.vertices:
                normalized_y = vertex.y / height
                min_y = min(min_y, normalized_y)
                max_y = max(max_y, normalized_y)
            is_continuous_word = False
            sub_word_min_x = 1
            sub_word_max_x = 0
            for symbol in word.symbols:
                symbol_x_min = 1
                symbol_x_max = 0
                for vertex in symbol.bounding_box.vertices:
                    normalized_x = vertex.x / width
                    symbol_x_min = min(symbol_x_min, normalized_x)
                    symbol_x_max = max(symbol_x_max, normalized_x)
                if symbol.text in WORD_SEPARATORS:
                    if is_continuous_word:
                        # append sub_word
                        box = [sub_word_min_x, min_y, sub_word_max_x, max_y]
                        boxes.append(box)
                        is_continuous_word = False
                        continue
                else:
                    if is_continuous_word:
                        sub_word_max_x = symbol_x_max
                    else:
                        # start sub_word
                        sub_word_min_x = symbol_x_min
                        sub_word_max_x = symbol_x_max
                        is_continuous_word = True
                        continue
            if is_continuous_word:
                box = [sub_word_min_x, min_y, sub_word_max_x, max_y]
                boxes.append(box)

        return boxes
