# I'll not let you get

English version is coming soon

## Problem

![task](./src/task.png)

[bird](./src/bird.png)

## Solution

Итак, у нас есть файлик, который вроде png, но чёт не открывается. Смотрим в хексы:

![bird_hex](./src/bird_hex.png)

Ага, gimp. Ну давайте откроем через Gimp.

![gimp](./src/gimp.png)

Во, а вот и птичка) Но интересует нас не она, а то, что лежит под ней. А там у нас какой-то текст:

![gimp_code](./src/gimp_code.png)

Нифига не понятно что там написано, но его можно скопировать и вставить в тхт файлик.

![code](./src/code.png)

Так, ну во-первых видим, что это хексы, да не просто хексы, а файлик .class, то есть это байт код Java (заголовок CAFEBABE). Быстренько пишем скрипт, чтобы отрезать первый столбик (это просто адреса, если кто не заметил).

```Python
with open("code.txt", "r") as f:
	text = f.readlines()

new_text = []
for t in text:
	new_text.append("".join(t.split(" ")[1:]))
code = "".join(new_text).replace("\n", "")

with open("code.class", "wb") as f:
	f.write(bytes.fromhex(code))
```

Вроде бы вот оно счастье, декомпилим теперь и получаем...

![decompile_fail](./src/decompile_fail.png)

null, ха, что ж не так-то? Заглянем в хексы класса:

![wrong_class](./src/wrong_class.png)

Так, если посмотреть повнимательней, то видно, что некоторые байтики стоят как бы не на месте. На самом деле они поменялись местами с другими байтами (это хорошо видно на строках).

Здесь мне стало плохо. Вручную переставлять байты там, где они не на месте, это не самое приятное занятие, а как написать скрипт - непонятно. Дальше я предположил, что поменялись местами не отдельные байты, а целые столбцы байтов. Тут уже стало легче.

Так, теперь надо разобраться какие столбцы с какими надо менять местами. Ну вот вместо niti в 3 строке, наверное должно быть init. Значит надо поменять местами 6 с 7 столбцы, и 8 с 9. Анализируя таким образом остальной код стало понятно что надо менять местами 0 с 1, 2 с 3, 4 с 5 и т.д. все столбцы хекса. Только в первой строке первые 4 байта должны остаться на своих местах т.к. это заголовок, и с ним изначально всё ОК.

Скрипт для перестановок выглядит вот так:

```Python
from textwrap import wrap

def swap(l, first, second):
	for i in range(len(l)):
		if len(l[i]) == 6 and max(first, second) > 5:
			continue
		temp = l[i][first]
		l[i][first] = l[i][second]
		l[i][second] = temp
	return l

with open("code.txt", "r") as f:
	text = f.readlines()

new_text = []
for t in text:
	new_text.append("".join(t.split(" ")[1:]))

lines = []
for line in new_text:
	lines.append(wrap((line).replace("\n", ""), 2))

new_lines = swap(lines, 0, 1)
new_lines = swap(new_lines, 2, 3)
new_lines = swap(new_lines, 4, 5)
new_lines = swap(new_lines, 6, 7)
new_lines = swap(new_lines, 8, 9)
new_lines = swap(new_lines, 10, 11)
new_lines = swap(new_lines, 12, 13)
new_lines = swap(new_lines, 14, 15)

new_lines[0][0] = 'ca'
new_lines[0][1] = 'fe'
new_lines[0][2] = 'ba'
new_lines[0][3] = 'be'

new_lines[-1][0]
hex_code = "".join(["".join(i) for i in new_lines])

with open("new_class.class", "wb") as f:
	f.write(bytes.fromhex(hex_code))

```

В итоге получаем такой вот хекс:

![good_class](./src/good_class.png)

Декомпилируем:

![decompile_success](./src/decompile_success.png)

Вот, вычисляем результат работы кода и получаем флаг:

![flag](./src/flag.png)

`b00t2root{893116}`