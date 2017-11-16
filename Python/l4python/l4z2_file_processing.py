import textwrap

def stream_to_paragraphs(stream):
    current_paragraph = ""
    for line in stream:
        if "\t" not in line:
            current_paragraph += line
        else:
            paragraphs = line.split("\t")
            current_paragraph += paragraphs[0]
            if current_paragraph:
                yield current_paragraph.strip()
            for paragraph in paragraphs[1:-1]:
                if paragraph:
                    yield paragraph.strip()
            current_paragraph = paragraphs[-1]
    yield current_paragraph.strip()

def file_paragrapher(file):
    return stream_to_paragraphs(open(file, 'r'))

format_paragraph = textwrap.fill

for paragraph in file_paragrapher('test.txt'):
    print("***************")
    print(format_paragraph(paragraph, 15))
    print("***************")
