### Rest api. Перевалирующееся.

[Попробовать API](http://51.250.89.197).

Всё в соответствии с первоначальной спецификацией, за исключением того,
что пустые поля должны быть либо null либо в принципе не входить в запрос.

Изображения кодируются в формате base64. Предполагается, что изображения - в формате jpg.
Это никак не проверяется)

Всё остальное проверяется очень тщательно.

Пример рабочего json запроса можно найти в файле [REST/pereval/test_data.json](REST/pereval/test_data.json)
Тесты запросов лежат в tests.py.

Список записей можно фильтровать через параметры user__email и status.
Например, 
```http://my.domain/submitData/?user__email=test%40test.te&status=new```

* Метод POST ищёт пользователя по email и, в случае успеха обновляет существующей записи в бд все _непустые_ поля.

* Метод POST принимает images в виде строк, закодированых в base64, 
сохраняет их на диск (действуя из предположения, что файлы пришли в формате .jpeg), 
и создаёт ссылку на изображение в базе данных.

* Через PUT/PATCH можно поменять все параметры, кроме пользователя (user) и картинок(images), если "status" отчёта "new".

* Для картинок нужно реализовывать отдельный endpoint, иначе непонятно, как определять, 
хочет ли пользователь изменить существующую картинку, или добавить новую. Можно изменить структуру запроса, 
чтобы пользователь присылал исходное название файла, а не только содержимое - 
так их можно будет хоть как-то дифференцировать. Но endpoint - в любом случае лучше=)

### OPENAPI schema
Лежит [здесь.](openapi-schema.yml)

#### Или json описания, полученные из OPTIONS

##### Для методов POST/GET
```http://my.domain/submitData/``` - POST/GET

```http://my.domain/submitData/<int:pk>/``` - GET
```json
{
    "name": "Pereval List",
    "description": "API endpoint that allows users to view or add perevals.\nUse null for optional fields, or don't include them.\nDo NOT use \"\" as value for optional fields!",
    "renders": [
        "application/json",
        "text/html"
    ],
    "parses": [
        "application/json",
        "application/x-www-form-urlencoded",
        "multipart/form-data"
    ],
    "actions": {
        "POST": {
            "pk": {
                "type": "integer",
                "required": false,
                "read_only": true,
                "label": "ID"
            },
            "status": {
                "type": "choice",
                "required": false,
                "read_only": true,
                "label": "Status"
            },
            "beauty_title": {
                "type": "string",
                "required": false,
                "read_only": false,
                "label": "Beauty title",
                "max_length": 50
            },
            "title": {
                "type": "string",
                "required": true,
                "read_only": false,
                "label": "Title",
                "max_length": 100
            },
            "other_titles": {
                "type": "string",
                "required": false,
                "read_only": false,
                "label": "Other titles",
                "max_length": 100
            },
            "connect": {
                "type": "string",
                "required": false,
                "read_only": false,
                "label": "Connect",
                "max_length": 200
            },
            "add_time": {
                "type": "datetime",
                "required": true,
                "read_only": false,
                "label": "Add time"
            },
            "user": {
                "type": "nested object",
                "required": true,
                "read_only": false,
                "label": "User",
                "children": {
                    "email": {
                        "type": "email",
                        "required": true,
                        "read_only": false,
                        "label": "Email",
                        "max_length": 254
                    },
                    "fam": {
                        "type": "string",
                        "required": false,
                        "read_only": false,
                        "label": "Fam",
                        "max_length": 100
                    },
                    "name": {
                        "type": "string",
                        "required": false,
                        "read_only": false,
                        "label": "Name",
                        "max_length": 100
                    },
                    "otc": {
                        "type": "string",
                        "required": false,
                        "read_only": false,
                        "label": "Otc",
                        "max_length": 100
                    },
                    "phone": {
                        "type": "string",
                        "required": false,
                        "read_only": false,
                        "label": "Phone",
                        "max_length": 25
                    }
                }
            },
            "coords": {
                "type": "nested object",
                "required": true,
                "read_only": false,
                "label": "Coords",
                "children": {
                    "latitude": {
                        "type": "float",
                        "required": true,
                        "read_only": false,
                        "label": "Latitude"
                    },
                    "longitude": {
                        "type": "float",
                        "required": true,
                        "read_only": false,
                        "label": "Longitude"
                    },
                    "height": {
                        "type": "integer",
                        "required": true,
                        "read_only": false,
                        "label": "Height"
                    }
                }
            },
            "level": {
                "type": "nested object",
                "required": true,
                "read_only": false,
                "label": "Level",
                "children": {
                    "winter": {
                        "type": "string",
                        "required": false,
                        "read_only": false,
                        "label": "Winter"
                    },
                    "summer": {
                        "type": "string",
                        "required": false,
                        "read_only": false,
                        "label": "Summer"
                    },
                    "autumn": {
                        "type": "string",
                        "required": false,
                        "read_only": false,
                        "label": "Autumn"
                    },
                    "spring": {
                        "type": "string",
                        "required": false,
                        "read_only": false,
                        "label": "Spring"
                    }
                }
            },
            "images": {
                "type": "field",
                "required": true,
                "read_only": false,
                "label": "Images",
                "child": {
                    "type": "nested object",
                    "required": true,
                    "read_only": false,
                    "children": {
                        "data": {
                            "type": "base64encoded jpeg file",
                            "required": true,
                            "read_only": false,
                            "label": "Data"
                        },
                        "title": {
                            "type": "string",
                            "required": true,
                            "read_only": false,
                            "label": "Title",
                            "max_length": 100
                        }
                    }
                }
            }
        }
    }
}
```

##### Для методов PUT/PATCH не доступны поля user и images

В остальном, структура аналогичная.

```http://my.domain/submitData/<int:pk>/```
```json
{
    "name": "Pereval List",
    "description": "API endpoint that allows users to view or add perevals.\nUse null for optional fields, or don't include them.\nDo NOT use \"\" as value for optional fields!",
    "renders": [
        "application/json",
        "text/html"
    ],
    "parses": [
        "application/json",
        "application/x-www-form-urlencoded",
        "multipart/form-data"
    ],
    "actions": {
        "PATCH": {
            "pk": {
                "type": "integer",
                "required": false,
                "read_only": true,
                "label": "ID"
            },
            "status": {
                "type": "choice",
                "required": false,
                "read_only": true,
                "label": "Status"
            },
            "beauty_title": {
                "type": "string",
                "required": false,
                "read_only": false,
                "label": "Beauty title",
                "max_length": 50
            },
            "title": {
                "type": "string",
                "required": true,
                "read_only": false,
                "label": "Title",
                "max_length": 100
            },
            "other_titles": {
                "type": "string",
                "required": false,
                "read_only": false,
                "label": "Other titles",
                "max_length": 100
            },
            "connect": {
                "type": "string",
                "required": false,
                "read_only": false,
                "label": "Connect",
                "max_length": 200
            },
            "add_time": {
                "type": "datetime",
                "required": true,
                "read_only": false,
                "label": "Add time"
            },
            "coords": {
                "type": "nested object",
                "required": true,
                "read_only": false,
                "label": "Coords",
                "children": {
                    "latitude": {
                        "type": "float",
                        "required": true,
                        "read_only": false,
                        "label": "Latitude"
                    },
                    "longitude": {
                        "type": "float",
                        "required": true,
                        "read_only": false,
                        "label": "Longitude"
                    },
                    "height": {
                        "type": "integer",
                        "required": true,
                        "read_only": false,
                        "label": "Height"
                    }
                }
            },
            "level": {
                "type": "nested object",
                "required": true,
                "read_only": false,
                "label": "Level",
                "children": {
                    "winter": {
                        "type": "string",
                        "required": false,
                        "read_only": false,
                        "label": "Winter"
                    },
                    "summer": {
                        "type": "string",
                        "required": false,
                        "read_only": false,
                        "label": "Summer"
                    },
                    "autumn": {
                        "type": "string",
                        "required": false,
                        "read_only": false,
                        "label": "Autumn"
                    },
                    "spring": {
                        "type": "string",
                        "required": false,
                        "read_only": false,
                        "label": "Spring"
                    }
                }
            }            
        }
    }
}
```



