def decode_special_character(a_string):
    test_bytes = bytes(a_string, encoding='raw_unicode_escape')
    return test_bytes.decode('unicode-escape')


with open("FOC_fighter_wikipedia_links.txt", "r") as handle:
    data = handle.readlines()
list_element = []
with open("FOC_fighter_wikipedia_links_formatted.txt", "w", encoding="utf-8") as handle:
    for element in data:
        index = 0
        while index < len(element):
            if element[index] == "\\" and element[index + 1] == "u":
                selected_chars = element[index:index + 6]
                decoded_char = decode_special_character(selected_chars)
                element = element.replace(selected_chars, decoded_char)
                index = 0
            index = index + 1
        list_element += element
        print(element)
        handle.write(element[:-1] + "\n")