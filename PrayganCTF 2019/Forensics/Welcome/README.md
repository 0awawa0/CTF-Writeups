# Welcome

## Таска

Do you think this is a normal image? No! Dig deeper to find out more.....

![welcome](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/welcome.jpeg)

## Решение

Такс, ну понятное дело, первым делом я загнал картинку в Stegsolve, но там ничего интересного не обнаружилось. Поэтому я решил взглянуть на неё в хексе. Вот там уже картинка повеселее:

![hexview](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/hexview.png)

Видим заголовок .zip архива. Аккуратно вырезаем архив и сохраняем в новом файлике. Распаковываем, а там еще один архив, ха. Распаковываем его тоже. А в нём... опять архив, но еще и secret.bmp.

![secret](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/secret.png)

Ну мы уж и не смотрим на секрет, а рвёмся распаковывать zip. А не тут-то было, архивчик-то запаролен:

![password](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/password.png)

Ну ладно, смотрим чё там в картинке:

![fail](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/fail.png)

Ой. Ясненько, смотрим хексы:

![what](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/what.png)

А это вообще не файл, каша какая-то. Но в конце есть кусочек подозрительно похожий на Base64. Декодируем, и:

![decode1](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/decode1.png)

Чё за... Так, спокойствие, а если убрать "==" с конца:

![decode2](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/decode2.png)

Во, а вот и пароль. Распаковываем архив и видим картинку:

![a](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/a.png)

Пихаем её сразу в Stegsolve и вуаля:

![HACKERMAN](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/HACKERMAN.png)
