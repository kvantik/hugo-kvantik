# hugo-kvantik
Source and content for the site of the mаgazine "Kvantik".

Это исходный код будущего сайта журнала для любознательных «Квантик».


Сайт создан с помощью генератора [Hugo](http://gohugo.io), собирается автоматически с помощью [Netlify](http://netlify.com), редактирование сайта онлайн возможно с помощью [NetlifyCMS](http://netlifycms.org) по адресу http://kvantik.com/admin

Подробнее смотрите в [вики](https://github.com/aperep/hugo-kvantik/wiki).

Обложки для экранов Retina можно перегенерировать из первых страниц PDF
(нужны Python 3.9+ и `pdftoppm` из Poppler):

```sh
python3 scripts/retina-covers.py static/issue/pdf/2026-??_sample.pdf
```

Скрипт создаёт `static/issue/cover/YYYY-MM@2x.jpg` размером 630×804,
вдвое больше обычных обложек 315×402. Общий шаблон карточки автоматически
добавляет существующий файл в `srcset` с плотностью `2x`; экранный размер
по-прежнему задаётся прежними стилями. Обычные JPEG остаются в `src`.

Остальные обложки архива генерируются командой
`python3 scripts/retina-related.py` из `static-old/articles/files/pdf/`
(также нужен ImageMagick). Размер каждого нового JPEG вдвое больше исходного;
пропорции PDF сохраняются, свободное место заполняется белым.
Шорткод `related` автоматически подключает существующие варианты `@2x`.

Для альманаха №26 и четырёх книг библиотечки использованы изображения МЦНМО;
их адреса сохранены в `scripts/retina-related-web.json`. Для повторной
генерации скачайте эти файлы в отдельный каталог и передайте его:
`python3 scripts/retina-related.py --web-source-dir /path/to/downloads`.

Без вариантов 2× пока остаются альманах №1 (в PDF нет обложки, на МЦНМО
только 300×351) и три комплекта плакатов (на МЦНМО изображения шириной 200 px).
