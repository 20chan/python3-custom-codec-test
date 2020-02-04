import codecs, io, encodings
from encodings import utf_8

def transform(lines):
    lines[3] = lines[3].replace("hello", "wow")
    return "".join(lines)

def wow_transform(stream):
    output = transform(stream.readlines())
    return output.rstrip()

def wow_transform_string(input):
    stream = io.StringIO(bytes(input).decode("utf-8"))
    return wow_transform(stream)

def wow_decodde(input, errors="strict"):
    return wow_transform_string(input), len(input)

class WowIncrementalDecoder(utf_8.IncrementalDecoder):
    def decode(self, input, final=False):
        self.buffer += input
        if final:
            buff = self.buffer
            self.buffer = b""
            return super(WowIncrementalDecoder, self).decode(
                wow_transform_string(buff).encode("utf-8"), final=True
            )
        else:
            return ""

class WowStreamReader(utf_8.StreamReader):
    def __init__(self, *args, **kwargs):
        codecs.StreamReader.__init__(self, *args, **kwargs)
        self.stream = io.StringIO(wow_transform(self.stream))

def search_function(encoding):
    if encoding != "wow":
        return None
    utf8 = encodings.search_function("utf8")
    return codecs.CodecInfo(
        name="wow",
        encode=utf8.encode,
        decode=wow_decodde,
        incrementalencoder=utf8.incrementalencoder,
        incrementaldecoder=WowIncrementalDecoder,
        streamreader=WowStreamReader,
        streamwriter=utf8.streamwriter,
    )

codecs.register(search_function)
