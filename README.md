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
