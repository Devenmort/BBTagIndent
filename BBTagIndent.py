import re
import os,sys
import string

# "Brace stays on initial line", "Separate line for each brace"
OPENING_BRACE_REACTION = "Brace stays on initial line"
# "Newline after", "Don't react"
SEMICOLON_REACTION = "Newline after"


if len(sys.argv) >= 2:
    file_to_process = sys.argv[1]
else:
    print("Enter the name of file for processing")
    driver_dir = input()

try:
    current_file = open(file_to_process,"r", encoding='utf-8')
except:
    print("No such file or file read error")
    sys.exit(1)

splitted_name = file_to_process.split('.')

print(splitted_name[0] + '.' + splitted_name[1] + '_indented.' + splitted_name[2])
current_file_out = open(splitted_name[0] + '.' + splitted_name[1] + '_indented.' + splitted_name[2],"w", encoding='utf-8')

# логика

# можно было бы сделать объект State для всего этого
indent_level = 0
indent_symbol = '\t'
newline_symbol = '\n'
cursor = 0

text_to_indent = current_file.read()
current_file.close()
array_to_output = bytearray()

# нужно учитывать отступы изначального текста! А нужно ли? Можно их игнорить.


def increase_indent():
    global indent_level
    indent_level += 1

def decrease_indent():
    global indent_level
    indent_level -= 1
    if indent_level < 0:
        raise OSError("There is an odd closing bracket")

def output_symbol(symbol):
    global array_to_output
    array_to_output = bytearray().join((array_to_output, symbol.encode()))

def indent(level = 1):
    for i in range(level):
        output_symbol(indent_symbol)

def advance_cursor():
    global cursor
    cursor += 1

def skip_symbol():
    advance_cursor()

def newline():
    output_symbol(newline_symbol)

def opening_brace_action(brace):
    # открывающая скобка
    if OPENING_BRACE_REACTION == "Separate line for each brace":
        # поставить переход на новую строку
        newline()
        # проставить отступы
        indent(indent_level)
        # проставляем скобку
        output_symbol(brace)
        # увеличить уровень отступов
        increase_indent()
        # поставить переход на новую строку
        newline()
        # проставить отступы
        indent(indent_level)
    elif OPENING_BRACE_REACTION == "Brace stays on initial line":
        # проставляем скобку
        output_symbol(brace)
        # поставить переход на новую строку
        newline()
        # увеличить уровень отступов
        increase_indent()
        # проставить отступы
        indent(indent_level)


def closing_brace_action(brace):
    # закрывающая скобка
    # поставить переход на новую строку
    newline()
    # уменьшить уровень отступов
    decrease_indent()
    # проставить отступы
    indent(indent_level)
    # проставляем скобку
    output_symbol(brace)

def semicolon_action(semicolon):
    # точка с запятой
    if SEMICOLON_REACTION == "Don't react":
        # проставляем точку с запятой
        output_symbol(semicolon)
    elif SEMICOLON_REACTION == "Newline after":
        # проставляем точку с запятой
        output_symbol(semicolon)
        # перевод на новую строку
        newline()
        # проставить отступы
        indent(indent_level)

for i in range(len(text_to_indent)):
    if      text_to_indent[i] == '{':
        opening_brace_action('{')
    elif    text_to_indent[i] == '}':
        closing_brace_action('}')
    elif    text_to_indent[i] == ';':
        semicolon_action(';')
    elif    text_to_indent[i] == '\t':
        skip_symbol()
    elif    text_to_indent[i] == ' ':
        output_symbol(text_to_indent[i])
    elif    text_to_indent[i] == newline_symbol:
        skip_symbol()
    else:
        output_symbol(text_to_indent[i])
        advance_cursor()


text_to_output = array_to_output.decode()
# постэффекты (вычищение артефактов преобразований)

text_to_output = re.sub(r"^\s*\n", "", text_to_output, flags = re.MULTILINE)

# вывод в файл
current_file_out.write(text_to_output)
current_file_out.close()


# {
#     set;
#     ~msgidd;
#     {
#         send;
#         {
#             channelid
#         };
#         Вы уверены, что хотите предложить эту роль для голосования?;
#         {
#             embedbuild;
#             title:
#             {
#                 args;
#                 0
#             };
#             description:
#             {
#                 args;
#                 1;
#                 n
#             };
#             color:ea4b00
#         }
#     }
# }

# {
#     set;~msgidd;{
#         send;{
#             channelid
#         };Вы уверены, что хотите предложить эту роль для голосования?;{
#             embedbuild;title:{
#                 args;0
#             };description:{
#                 args;1;n
#             };color:ea4b00
#         }
#     }
# }