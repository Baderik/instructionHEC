import json

close_open_index = 1


def convert_to_html(element, class_index=3):
    global close_open_index

    mb = 5 - class_index
    mb = f"mb-{mb}" if mb > 0 else ""
    element_html = ''

    if element["type"] == "list":
        element_html += f'''<div class="col-12 lvl{class_index} {mb}">
                <span class="openBlock lvl{class_index}" id="{close_open_index}">+ {element["name"]}</span></div>
                <div class="col-1"></div><div class="col-11 block lvl{class_index}" id="{close_open_index}">
                <div class="row">'''

        close_open_index += 1

        if element["content"]:
            for next_element in element["content"]:
                element_html += convert_to_html(next_element, class_index + 1)

        element_html += '</div></div>'

    elif element["type"] == "html":
        element_html += element["name"].replace('>', f' class="col-12 lvl{class_index} {mb}">', 1)

    else:
        element_html += f'<span class="col-12 lvl{class_index} {mb}">{element["name"]}</span>'

    return element_html


def convert_in_block_to_html(in_block):
    in_block_html = f'''<div class="col-12 2"><h3><a href="{in_block["href"]}">{in_block["name"]}</a></h3></div>
    <div class="col-1"></div><div class="col-9"><div class="row">'''
    content = in_block["content"]

    if content:
        for element in content:
            in_block_html += convert_to_html(element)

    in_block_html += f'''</div></div><a href = {in_block["href"]} class="col-2">
    <img src="{in_block["img"]}" alt=""></a>'''

    return in_block_html


def convert_block_to_html(block):
    block_html = f'''<div class="row justify-content-center">
    <div class="col-12"><h2 class="1">{block["name"]}</h2></div></div>'''

    content = block["content"]

    if content:
        block_html += '<div class="row my-3">'

        for in_block in content:
            block_html += convert_in_block_to_html(in_block)

        block_html += '</div>'

    return block_html


def generate(file_in="static/data.json", file_out="templates/index.html"):
    main = '''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Инструкции</title>
    <link rel="shortcut icon" href="https://i.ibb.co/PjSGjpG/2.png" type="image/png">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <link rel="stylesheet" href="{{ url_for('static', filename='stylesheet/index.css') }}">
    </head><body><div class="container">'''

    with open(file_in) as data:
        data = json.loads(data.read())

    for block in data:
        main += convert_block_to_html(block)

    main += '''</div></body>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="{{ url_for('static', filename='javascript/index.js') }}"></script></html>'''

    if file_out:
        with open(file_out, "w") as out:
            print(main, file=out)

    else:
        return main


if __name__ == '__main__':
    generate()
