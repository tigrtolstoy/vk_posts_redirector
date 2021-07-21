# vk_posts_redirector
## Цель проекта
Я не люблю ВКонтакте, но у меня появилась необходимость просматривать посты из нескольких групп. Поэтому я решил разработать небольшое приложение, которые будет пересылать новые записи из интересующих меня пабликов мне в телеграм.


## Необходимые файлы
Для работы приложения необходимо два дополнительных файла:
- `.env`
- `groups_ids.json`

Файл `.env` имеет вид:
```
VK_ACCESS_TOKEN = "***"
TG_ACCESS_TOKEN = "***"
TG_CHANEL_ID = "***"
```
`VK_ACCESS_TOKEN` - токен для работ с API VK 
`TG_ACCESS_TOKEN` - токен для работ с telegram-ботом
`TG_CHANEL_ID` - id канала, куда telegram-бот будет пересылать сообщения


Файл `groups_ids.json` имеет вид:
```
{
    "groups_ids": [
        "***",
        "***",
        "***"
    ]
}
```
В списке `groups_ids` находятся id групп, посты из которых пользователь хочет пересылать в telegram-канал.


## Особенности работы
В файл `groups_ids` можно дабавить любое количество id групп ВК.<br>
Если до этого ни один пост со стены группы не был отправлен в телеграм канал, приложение осущесвит пересылку всех постов со стены сообщества за последние 3 дня.<br>
Данные о последнем пересланом посте сохраняются в базе данных (sqlite3). Таким образом, при перезагрузке программы, не произойдет повторная отправка постов из ВК в Telegram.
*Для того, что бы telegram-бот мог отправлять сообщения в канал, его нужно сделать администратором!*


## Зависимости
Для работы программы необходимы библиотеки, перечень которых представлен в файле `requirements.txt`.
Для установки зависимостей можно воспользоваться командой:<br>
`pip install -r requirements.txt`
Кроме того, на устройтсве должна быть установлена СУБД sqlite3.

## Запуск
Запуск программы осуществляется командой `python3 main.py`