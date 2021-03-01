import turtle
import re


# список функций для управления параметаризированными командами
# у всех функций будет префикс cmd_ и первый параметр t - черепашка
def cmd_turtle_fd(t, length, *args):
    t.pensize(args[1])
    t.fd(length*args[0])

def cmd_turtle_left(t, angle, *args):
    t.left(angle * args[0])

def cmd_turtle_right(t, angle, *args):
    t.right(angle * args[0])

class LSystem2D:
    def __init__(self, t, axiom, width, length, angle):
        self.axiom = axiom      # инициатор
        self.state = axiom      # строка с набором команд для фрактала (вначале это инициатор)
        self.width = width      # толщина линии рисования
        self.length = length    # длина одного линейного сегмента кривой
        self.angle = angle      # фиксированный угол поворота
        self.t = t              # сама черепашка
        self.rules = {}  # словарь для хранения правил формирования кривых
        self.t.pensize(self.width)
        self.function_key = None
        self.key_re_list = []  # список шаблонов команд
        self.cmd_functions = {}  # словарь связей параметаризованных команд и функций

    def add_rules(self, *rules):
        for key, value in rules:
            key_re = ""                     # шаблон регулярного выражения для выделения ключа
            if not isinstance(value, str):  # ключ с параметрами
                key_re = key.replace("(", r"\(")
                key_re = key_re.replace(")", r"\)")
                key_re = key_re.replace("+", r"\+")
                key_re = key_re.replace("-", r"\-")
                key_re = re.sub(r"([a-z]+)([, ]*)", lambda m: r"([-+]?\b\d+(?:\.\d+)?\b)" + m.group(2), key_re)
                self.key_re_list.append(key_re)

            self.rules[key] = (value, key_re)

    def update_param_cmd(self, m):
        if not self.function_key:
            return ""

        args = list(map(float, m.groups()))
        return self.function_key(*args).lower()

    def generate_path(self, n_iter):
        for n in range(n_iter):
            for key, values in self.rules.items():
                if isinstance(values[0], str):
                    self.state = self.state.replace(key, values[0].lower())
                else:   # команда с параметром
                    self.function_key = values[0]   # ссылка на лямбда-функцию
                    self.state = re.sub(values[1], self.update_param_cmd, self.state)
                    self.function_key = None

            self.state = self.state.upper()


    def set_turtle(self, my_tuple):
        self.t.up()
        self.t.goto(my_tuple[0], my_tuple[1])
        self.t.seth(my_tuple[2])
        self.t.down()

    def add_rules_move(self, *moves):
        for key, func in moves:
            self.cmd_functions[key] = func

    def draw_turtle(self, start_pos, start_angle):
            # ***************
            turtle.tracer(1, 0)  # форсажный режим для черепашки
            self.t.up()  # черепашка воспаряет над поверхностью (чтобы не было следа)
            self.t.setpos(start_pos)  # начальная стартовая позиция
            self.t.seth(start_angle)  # начальный угол поворота
            self.t.down()  # черепашка опускается на "грешную землю"
            turtle_stack = []
            key_list_re = "|".join(self.key_re_list)
            # ***************
            # for move in self.state:
            for values in re.finditer(r"(" + key_list_re + r"|.)", self.state):
                cmd = values.group(0)
                args = [float(x) for x in values.groups()[1:] if x]

                if 'F' in cmd:
                    if len(args) > 0 and self.cmd_functions.get('F'):
                        self.cmd_functions['F'](t, self.length, *args)
                    else:
                        self.t.fd(self.length)
                elif 'S' in cmd:
                    if len(args) > 0 and self.cmd_functions.get('S'):
                        self.cmd_functions['S'](t, self.length, *args)
                    else:
                        self.t.up()
                        self.t.forward(self.length)
                        self.t.down()
                elif '+' in cmd:
                    if len(args) > 0 and self.cmd_functions.get('+'):
                        self.cmd_functions['+'](t, self.angle, *args)
                    else:
                        self.t.left(self.angle)
                elif '-' in cmd:
                    if len(args) > 0 and self.cmd_functions.get('-'):
                        self.cmd_functions['-'](t, self.angle, *args)
                    else:
                        self.t.right(self.angle)
                elif "[" in cmd:
                    turtle_stack.append((self.t.xcor(), self.t.ycor(), self.t.heading(), self.t.pensize()))
                elif "]" in cmd:
                    xcor, ycor, head, w = turtle_stack.pop()
                    self.set_turtle((xcor, ycor, head))
                    self.width = w
                    self.t.pensize(self.width)

            turtle.done()        # чтобы окно не закрывалось после отрисовки


# ************** чтобы окно появлялось в левом верхнем углу с размерами 1200x600
width = 1200
height = 600
screen = turtle.Screen()
screen.setup(width, height, 0, 0)
# **************

t = turtle.Turtle()
t.ht()          # скрываем черепашку

pen_width = 2   # толщина линии рисования (в пикселах)
f_len = 20      # длина одного сегмента прямой (в пикселах)
angle = 33

axiom = "A"

l_sys = LSystem2D(t, axiom, pen_width, f_len, angle)

l_sys.add_rules(("A", "F(1, 1)[+(1)A][-(1)A]"),
                ("F(x, y)", lambda x, y: f"F({1.5*x}, {1.7*y})"),
                ("+(x)", lambda x: f"+({1.1*x})"),
                ("-(x)", lambda x: f"-({1.1*x})"),
                )

l_sys.add_rules_move(("F", cmd_turtle_fd), ("+", cmd_turtle_left), ("-", cmd_turtle_right))
l_sys.generate_path(5)
print(l_sys.state)
l_sys.draw_turtle( (0, -200), 90)

