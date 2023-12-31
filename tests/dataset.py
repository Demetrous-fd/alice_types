from contextlib import nullcontext as does_not_raise
from typing import Callable, Any, Optional

import pytest
import orjson

from alice_types import InterfaceType, SlotsType, State, entity, request


class ValueField:
    def __init__(self, obj: dict, json_string: Optional[bytes] = None):
        self.obj = obj
        self.string = orjson.dumps(obj) if json_string is None else json_string


def create_ref() -> Callable:
    objects = dict()

    def wrapper(key: str, obj: Optional[Any] = None) -> Any:
        nonlocal objects
        if obj is not None:
            objects[key] = obj

        elif value := objects.get(key, None):
            obj = value

        return obj

    return wrapper


ref: Callable = create_ref()

ref(
    key="EMPTY",
    obj=ValueField(obj={})
)

ANALYTICS_EVENT = {
    "ERROR": [
        {
            "value": ref(
                key="ANALYTICS_EVENT:ERROR-1",
                obj=ref("EMPTY")
            ),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ref(
                key="ANALYTICS_EVENT:ERROR-2",
                obj=ValueField({"name": "Test", "value": {"1": {"2": {"3": {"4": {"5": {"6": {}}}}}}}})
            ),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
    ],
    "NOT_EMPTY": [
        {
            "value": ref(
                key="ANALYTICS_EVENT:NOT_EMPTY-1",
                obj=ValueField(
                    obj={"name": "Test"},
                    json_string=orjson.dumps({"name": "Test", "value": {}})
                )
            ),
            "expected": ref("ANALYTICS_EVENT:NOT_EMPTY-1").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ANALYTICS_EVENT:NOT_EMPTY-2",
                obj=ValueField({"name": "Test", "value": {}})
            ),
            "expected": ref("ANALYTICS_EVENT:NOT_EMPTY-2").string,
            "raise_handler": does_not_raise()
        },
    ],
}

ANALYTICS = {
    "EMPTY": [
        {
            "value": ref(
                key="ANALYTICS:EMPTY-1",
                obj=ValueField({"events": []})
            ),
            "length": 0,
            "expected": ref("ANALYTICS:EMPTY-1").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ANALYTICS:EMPTY-2",
                obj=ref("EMPTY")
            ),
            "length": 0,
            "expected": ref("ANALYTICS:EMPTY-1").string,
            "raise_handler": does_not_raise()
        },

    ],
    "NOT_EMPTY": [
        {
            "value": ref(
                key="ANALYTICS:NOT_EMPTY-1",
                obj=ValueField(
                    obj={
                        "events": [
                            ref("ANALYTICS_EVENT:NOT_EMPTY-1").obj
                        ]
                    },
                    json_string=f'{{"events":[{ref("ANALYTICS_EVENT:NOT_EMPTY-1").string.decode()}]}}'.encode()
                )
            ),
            "length": 1,
            "expected": ref("ANALYTICS:NOT_EMPTY-1").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ANALYTICS:NOT_EMPTY-2",
                obj=ValueField({
                    "events": [
                        ref("ANALYTICS_EVENT:NOT_EMPTY-2").obj
                    ]
                })
            ),
            "length": 1,
            "expected": ref("ANALYTICS:NOT_EMPTY-2").string,
            "raise_handler": does_not_raise()
        },
    ],
    "ERROR": [
        {
            "value": ref(
                key="ANALYTICS:ERROR-1",
                obj=ValueField({
                    "events": [
                        ref("ANALYTICS_EVENT:ERROR-1").obj
                    ]
                }),
            ),
            "length": None,
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ref(
                key="ANALYTICS:ERROR-2",
                obj=ValueField({
                    "events": [
                        ref("ANALYTICS_EVENT:ERROR-2").obj
                    ]
                }),
            ),
            "length": None,
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        }
    ]
}

INTERFACES = {
    "EMPTY": [
        {
            "value": ref(
                key="INTERFACES:EMPTY-1",
                obj=ref("EMPTY")
            ),
            "expected": [],
            "has": [],
            "raise_handler": does_not_raise()
        },
    ],
    "NOT_EMPTY": [
        {
            "value": ref(
                key="INTERFACES:NOT_EMPTY-1",
                obj=ValueField({"screen": {}, "account_linking": {}, "payments": {}})
            ),
            "expected": [InterfaceType.SCREEN, InterfaceType.ACCOUNT_LINKING, InterfaceType.PAYMENTS],
            "has": [],
            "raise_handler": does_not_raise()
        },
    ],
    "ERROR": [
        {
            "value": ValueField({"screen": {}}),
            "expected": [InterfaceType.SCREEN],
            "has": ["something"],
            "raise_handler": pytest.raises(ValueError)
        },
    ]
}

BUTTON = {
    "NOT_EMPTY": [
        {
            "value": ValueField({"title": "Test"}),
            "expected": orjson.dumps({
                "title": "Test",
                "payload": {},
                "hide": False
            }),
            "raise_handler": does_not_raise()
        },
        {
            "value": ValueField({
                "title": "Test",
                "hide": True
            }),
            "expected": orjson.dumps({
                "title": "Test",
                "payload": {},
                "hide": True
            }),
            "raise_handler": does_not_raise()
        },
        {
            "value": ValueField({
                "title": "Test",
                "url": "https://yandex.ru/dev/dialogs/alice/doc"
            }),
            "expected": orjson.dumps({
                "title": "Test",
                "url": "https://yandex.ru/dev/dialogs/alice/doc",
                "payload": {},
                "hide": False
            }),
            "raise_handler": does_not_raise()
        },
    ],
    "ERROR": [
        {
            "value": ref("EMPTY"),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ValueField({
                "title": "1" * 96
            }),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ValueField({
                "title": "1" * 64,
                "payload": {"data": "1" * 4096}
            }),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ValueField({
                "title": "Test",
                "url": "http://www.reallylong.link/rll/HSH2zA8PLpmIIHX/_H6g_jcTksuXem56AFLr/izklCtmEUz30_EA5CNh4DxwssLIyOfEt7qfc5Fjq6NeJefBnUFm39nPOqEGRYOHiy/S8cY6XaaT45NHwyPjide_VYpYEMUw1H8WaI7LY4pw8AyBog6jtvHeXHKuo1rIjvKCFzzlBoE_vav4vn5Oe41mGaJAvb9hk42KP/E7lH5XJ0xD5_/OPUg3WlccMslaMKQkSMn4cnrHl4FOxeqqQDRc4ODs3RHlueM7ceSa3aqS0MsZhD21AtzzDVlGe5nNzZpIqUMOO8Ak9hypVudLXQqlFmzBvTddBtgiLqBEdHYq/6U7tZxW4hmTOijH25xiLUlBvw2vCjiPbtcFcZ4mrcFbpnd3AqOBu5TEOa6KaOOWv9jSpg_52ThyeuSMyH0H53Bm6Z0rYd/LRHJVgcsWQkMLBmS1pktP8l/UkVcQoNd37n2chl9D5lJLhzBFkgH3erCUrwmLJowiPBHZ89A_g87kvp3oBaTURXwi0Zfxbl67gswnHRwYZBmKa/Nq723DIU3324TmbrWTu_tnpLzLHpPpzVLEJvr3IFHYOtL7AEcmUqrCFPeD6RWrm3vn9/Rv/JaZcK7Y8aHhb9mvOCKURKP4mdpDELS03_AduWFOqoapmcs2RqlgL7Xj0G/KXSiBUnjFYRZFQ6H4KVPybA2hcDmSjItT84qfKfqU_6rOJogx1k6DvOqQI6p0jk5aPfQS2pzYexUBAEvgOd9zGnN_9yYbcqYnJQGVTGGnzxjYRwmGto6DNolxWaoBt6rV1wvwJvjbo7xSxGurIJhCXPajMbcVCeTXdgaJhwqUXOywE/8yEKk5vt5cbimq3ANJEgIk63CHrlbh6jEHcRMIHYhhytjrNEPmXqu7G9yHr6wDgDhtkyiv6GULlyvP6hbzBzYJBU5hRtLY2fifgKkJtzTg8/IMAdvsqMo9WIfrMlPCBZeoznC1mF26DV_T0YQqS9zHhWlm2Xc7uR1jVezA0lSZZec3U1RACozbbsYONVQJT6DAg/qP2ilchdHPOroYnpJ9d9HbOin7srg7esGgSx1cvPNKQymhu_EzuJxw8pBHT5JXSRDesd0oT8n_WAIOy0BgKyJCrWG3Txqsdvaa8ICAP65TCcge3xPNmf2rIlgNGVq6XwS4QyHqYwA/KLIMr5eyUTZ_mgq8nGGER3lYxdLEsGzXjdsHOTISCEw2Gwrsj07ZWE4/89/OBJp9GJVJwZfAOmWzmE20FMvcFLvSTCJiEH8MHdaUFwuxBqnxYKzQLzacoz6ZKXsxHkS/EDH_gahL9P1rckVrlgd5eynBNns2Taa_G8mHz4M0CKmLL2_Mm09esRxveKEHYuL4ZFLsvK/KZbqpEhrZCcVRyW1_NgmDc5hEEbVWAn89K45/K0KppLBTmVQwW/SPz46VLBTI/6Y0KTHXR0C4OsywfYhBOokKajfJV69Sd4ydv6ETRxjmANaA/G5MY7Sklo3b/D2yGjPR5AdZmwJ6XIxMXLgAYfBlVjl_VuncQLbxLmK6AVgoP/VmXnekIoNdni8mq5P9vIlCBIqIMGyToHMZuoBICYb7yXOPnox_jxVQd3nAjF90kebtSUrLc1LZ9MjYLN1JwayHvCLTUc93Z9JaX5oZ3e2iWxHoCfyIpq1kgjPDnArIDuRMGsWnVMct_gtmsT1CKHFvrEI_HpCw3_Q0rFjVhcjKwmjnmptZkpB6zCS146b1D5TkTUndaT8fDejqpyXdyvVr3ADK8_RM_ehn0erjt2vdFYAAb/gO4rZM6W_O4i1M0ECQmJb52iSDUKANKfmIx9WYuBIAgaggQtMDfjZ3ACJ7JqqPA2cDDMk6QlzstIDHNy0CwzUbnGMWL3GYIpwZacsG4aythgEq/e2_kFzHQIQ2t5EWuRlnQUVMI9Kc5UJPgvkXZXfCMpEjIRALdGa_SHxjYA1L97Hizac"
            }),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
    ]
}

MARKUP = {
    "ERROR": [
        {
            "value": ValueField({
                "dangerous_context": False
            }),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        }
    ],
    "EMPTY": [
        {
            "value": ref(
                key="MARKUP:EMPTY-1",
                obj=ValueField({"dangerous_context": None})
            ),
            "expected": ref("MARKUP:EMPTY-1").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="MARKUP:EMPTY-2",
                obj=ref("EMPTY")
            ),
            "expected": ref("MARKUP:EMPTY-1").string,
            "raise_handler": does_not_raise()
        },
    ],
    "NOT_EMPTY": [
        {
            "value": ref(
                key="MARKUP:NOT_EMPTY-1",
                obj=ValueField({"dangerous_context": None})
            ),
            "expected": ref("MARKUP:NOT_EMPTY-1").string,
            "raise_handler": does_not_raise()
        },
    ],
}

INTENTS = {
    "EMPTY": [
        {
            "value": ref(
                key="INTENTS:EMPTY-1",
                obj=ref("EMPTY")
            ),
            "expected": ref("INTENTS:EMPTY-1").string,
            "raise_handler": does_not_raise()
        },
    ],
    "NOT_EMPTY": [
        {
            "value": ref(
                key="INTENTS:NOT_EMPTY-1",
                obj=ValueField({
                    "slots": {
                        "where": {
                            "type": "YANDEX.GEO",
                            "tokens": {
                                "start": 2,
                                "end": 6
                            },
                            "value": {
                                "street": "льва толстого",
                                "house_number": "16"
                            }
                        },
                        "time": {
                            "type": "YANDEX.DATETIME",
                            "tokens": {
                                "start": 6,
                                "end": 9
                            },
                            "value": {
                                "hour": 14,
                                "minute": 0
                            }
                        }
                    }
                })
            ),
            "expected": ref("INTENTS:NOT_EMPTY-1").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="INTENTS:NOT_EMPTY-2",
                obj=ValueField({
                    "slots": {
                        "from": {
                            "type": SlotsType.YANDEX_NUMBER,
                            "value": 1
                        },
                        "to": {
                            "type": SlotsType.YANDEX_NUMBER,
                            "value": 6
                        }
                    }
                })
            ),
            "expected": ref("INTENTS:NOT_EMPTY-2").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="INTENTS:NOT_EMPTY-3",
                obj=ValueField({
                    "slots": {
                        "what": {
                            "type": SlotsType.YANDEX_STRING,
                            "value": "свет"
                        },
                        "where": {
                            "type": SlotsType.YANDEX_STRING,
                            "value": "на кухне"
                        }
                    }
                })
            ),
            "expected": ref("INTENTS:NOT_EMPTY-3").string,
            "raise_handler": does_not_raise()
        },
    ]
}

ENTITY_VALUE = {
    "NOT_EMPTY": [
        {
            "value": ref(
                key="ENTITY_VALUE:NOT_EMPTY:FIO-1",
                obj=ValueField({
                    "first_name": "антон",
                    "patronymic_name": "павлович",
                    "last_name": "чехов"
                })
            ),
            "expected": ref("ENTITY_VALUE:NOT_EMPTY:FIO-1").string,
            "expected_fields": [
                "first_name",
                "patronymic_name",
                "last_name",
            ],
            "type": entity.EntityValueFio,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ENTITY_VALUE:NOT_EMPTY:FIO-2",
                obj=ValueField({
                    "first_name": "лев",
                    "last_name": "толстой"
                })
            ),
            "expected": ref("ENTITY_VALUE:NOT_EMPTY:FIO-2").string,
            "expected_fields": [
                "first_name",
                "last_name",
            ],
            "type": entity.EntityValueFio,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ENTITY_VALUE:NOT_EMPTY:FIO-3",
                obj=ValueField({
                    "first_name": "петька"
                })
            ),
            "expected": ref("ENTITY_VALUE:NOT_EMPTY:FIO-3").string,
            "expected_fields": [
                "first_name",
            ],
            "type": entity.EntityValueFio,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ENTITY_VALUE:NOT_EMPTY:GEO-1",
                obj=ValueField({
                    "country": "россия",
                    "city": "москва",
                    "street": "улица льва толстого",
                    "house_number": "16"
                })
            ),
            "expected": ref("ENTITY_VALUE:NOT_EMPTY:GEO-1").string,
            "expected_fields": [
                "country",
                "city",
                "street",
                "house_number",
            ],
            "type": entity.EntityValueGeo,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ENTITY_VALUE:NOT_EMPTY:GEO-2",
                obj=ValueField({
                    "airport": "аэропорт внуково",
                })
            ),
            "expected": ref("ENTITY_VALUE:NOT_EMPTY:GEO-2").string,
            "expected_fields": [
                "airport"
            ],
            "type": entity.EntityValueGeo,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ENTITY_VALUE:NOT_EMPTY:DATETIME-1",
                obj=ValueField({
                    "day": -1,
                    "day_is_relative": True
                })
            ),
            "expected": ref("ENTITY_VALUE:NOT_EMPTY:DATETIME-1").string,
            "expected_fields": [
                "day",
                "day_is_relative"
            ],
            "type": entity.EntityValueDatetime,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ENTITY_VALUE:NOT_EMPTY:DATETIME-2",
                obj=ValueField({
                    "year": 1982,
                    "month": 9,
                    "day": 15,
                    "hour": 22,
                    "minute": 30,
                })
            ),
            "expected": ref("ENTITY_VALUE:NOT_EMPTY:DATETIME-2").string,
            "expected_fields": [
                "year",
                "month",
                "day",
                "hour",
                "minute"
            ],
            "type": entity.EntityValueDatetime,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ENTITY_VALUE:NOT_EMPTY:NUMBER-1",
                obj=ValueField({
                    "value": 16
                })
            ),
            "expected": ref("ENTITY_VALUE:NOT_EMPTY:NUMBER-1").string,
            "expected_fields": [
                "value"
            ],
            "type": entity.EntityValueNumber,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ENTITY_VALUE:NOT_EMPTY:NUMBER-2",
                obj=ValueField({
                    "value": 3.25
                })
            ),
            "expected": ref("ENTITY_VALUE:NOT_EMPTY:NUMBER-2").string,
            "expected_fields": [
                "value"
            ],
            "type": entity.EntityValueNumber,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ENTITY_VALUE:NOT_EMPTY:DICT",
                obj=ValueField({
                    "text": "Some text 1",
                    "tts": "Some text one"
                })
            ),
            "expected": ref("ENTITY_VALUE:NOT_EMPTY:DICT").string,
            "expected_fields": [
                "text",
                "tts"
            ],
            "type": dict,
            "raise_handler": does_not_raise()
        },
        # TODO: Add custom type check
    ],
}

ENTITY = {
    "NOT_EMPTY": [
        {
            "value": ref(
                key="ENTITY:NOT_EMPTY:FIO-1",
                obj=ValueField({
                    "type": SlotsType.YANDEX_FIO,
                    "tokens": {
                        "start": 3,
                        "end": 6
                    },

                    "value": ref("ENTITY_VALUE:NOT_EMPTY:FIO-1").obj,
                })
            ),
            "expected": ref("ENTITY:NOT_EMPTY:FIO-1").string,
            "type": entity.EntityFio,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ENTITY:NOT_EMPTY:FIO-2",
                obj=ValueField({
                    "type": SlotsType.YANDEX_FIO,
                    "tokens": {
                        "start": 3,
                        "end": 5
                    },
                    "value": ref("ENTITY_VALUE:NOT_EMPTY:FIO-2").obj,
                })
            ),
            "expected": ref("ENTITY:NOT_EMPTY:FIO-2").string,
            "type": entity.EntityFio,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ENTITY:NOT_EMPTY:NUMBER-1",
                obj=ValueField({
                    "type": SlotsType.YANDEX_NUMBER,
                    "tokens": {
                        "start": 5,
                        "end": 6
                    },
                    "value": ref("ENTITY_VALUE:NOT_EMPTY:NUMBER-1").obj,
                })
            ),
            "expected": ref("ENTITY:NOT_EMPTY:NUMBER-1").string,
            "type": entity.EntityNumber,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ENTITY:NOT_EMPTY:NUMBER-2",
                obj=ValueField({
                    "type": SlotsType.YANDEX_NUMBER,
                    "tokens": {
                        "start": 5,
                        "end": 6
                    },
                    "value": ref("ENTITY_VALUE:NOT_EMPTY:NUMBER-2").obj,
                })
            ),
            "expected": ref("ENTITY:NOT_EMPTY:NUMBER-2").string,
            "type": entity.EntityNumber,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ENTITY:NOT_EMPTY:GEO-1",
                obj=ValueField({
                    "type": SlotsType.YANDEX_GEO,
                    "tokens": {
                        "start": 2,
                        "end": 6
                    },
                    "value": ref("ENTITY_VALUE:NOT_EMPTY:GEO-1").obj,
                })
            ),
            "expected": ref("ENTITY:NOT_EMPTY:GEO-1").string,
            "type": entity.EntityGeo,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ENTITY:NOT_EMPTY:GEO-2",
                obj=ValueField({
                    "type": SlotsType.YANDEX_GEO,
                    "tokens": {
                        "start": 1,
                        "end": 3
                    },
                    "value": ref("ENTITY_VALUE:NOT_EMPTY:GEO-2").obj,
                })
            ),
            "expected": ref("ENTITY:NOT_EMPTY:GEO-2").string,
            "type": entity.EntityGeo,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ENTITY:NOT_EMPTY:DATETIME-1",
                obj=ValueField({
                    "type": SlotsType.YANDEX_DATETIME,
                    "tokens": {
                        "start": 6,
                        "end": 8
                    },
                    "value": ref("ENTITY_VALUE:NOT_EMPTY:DATETIME-1").obj,
                })
            ),
            "expected": ref("ENTITY:NOT_EMPTY:DATETIME-1").string,
            "type": entity.EntityDatetime,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ENTITY:NOT_EMPTY:DATETIME-2",
                obj=ValueField({
                    "type": SlotsType.YANDEX_DATETIME,
                    "tokens": {
                        "start": 1,
                        "end": 6
                    },
                    "value": ref("ENTITY_VALUE:NOT_EMPTY:DATETIME-2").obj,
                })
            ),
            "expected": ref("ENTITY:NOT_EMPTY:DATETIME-2").string,
            "type": entity.EntityDatetime,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="ENTITY:NOT_EMPTY:DICT-1",
                obj=ValueField({
                    "type": "TextToSpeech",
                    "tokens": {
                        "start": 0,
                        "end": 13
                    },
                    "value": ref("ENTITY_VALUE:NOT_EMPTY:DICT").obj,
                })
            ),
            "expected": ref("ENTITY:NOT_EMPTY:DICT-1").string,
            "type": entity.EntityBase,
            "raise_handler": does_not_raise()
        },
    ],
    "ERROR": [
        {
            "value": ref("EMPTY"),
            "expected": None,
            "type": entity.EntityBase,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ValueField({
                "type": SlotsType.YANDEX_FIO,
                "tokens": [],
                "value": ref("ENTITY_VALUE:NOT_EMPTY:DATETIME-2").obj
            }),
            "expected": None,
            "type": entity.EntityFio,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ValueField({
                "type": SlotsType.YANDEX_GEO,
                "tokens": {
                    "first": 0,
                    "end": 5
                },
                "value": ref("ENTITY_VALUE:NOT_EMPTY:FIO-1").obj
            }),
            "expected": None,
            "type": entity.EntityGeo,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ValueField({
                "type": SlotsType.YANDEX_NUMBER,
                "tokens": {
                    "start": 0,
                    "last": 5
                },
                "value": ref("ENTITY_VALUE:NOT_EMPTY:DATETIME-1").obj
            }),
            "expected": None,
            "type": entity.EntityNumber,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ValueField({
                "type": SlotsType.YANDEX_GEO,
                "tokens": {
                    "start": 0,
                    "last": 5
                },
                "value": ref("ENTITY_VALUE:NOT_EMPTY:DATETIME-1").obj
            }),
            "expected": None,
            "type": entity.EntityGeo,
            "raise_handler": pytest.raises(ValueError)
        },
    ],
}

META = {
    "NOT_EMPTY": [
        {
            "value": ref(
                key="META:NOT_EMPTY-1",
                obj=ValueField({
                    "locale": "ru-RU",
                    "timezone": "Europe/Moscow",
                    "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
                    "interfaces": ref("INTERFACES:NOT_EMPTY-1").obj,
                    "flags": [],
                })
            ),
            "expected": ref("META:NOT_EMPTY-1").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="META:NOT_EMPTY-2",
                obj=ValueField({
                    "locale": "eu-ES",
                    "timezone": "Europe/Dublin",
                    "client_id": "eu.yandex.searchplugin/7.16 (none none; android 4.4.2)",
                    "interfaces": ref("INTERFACES:NOT_EMPTY-1").obj,
                })
            ),
            "expected": ref("META:NOT_EMPTY-2").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="META:NOT_EMPTY-3",
                obj=ValueField({
                    "locale": "eu",
                    "timezone": "America/New_York",
                    "client_id": "eu.yandex.searchplugin/7.16 (none none; android 4.4.2)",
                    "interfaces": ref("INTERFACES:EMPTY-1").obj,
                })
            ),
            "expected": ref("META:NOT_EMPTY-3").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="META:NOT_EMPTY-4",
                obj=ValueField({
                    "locale": "eu",
                    "timezone": "America/New_York",
                    "client_id": "ru.yandex.quasar.services/1.0 (Yandex Station; android 6.0.1)",
                    "flags": [
                        "no_cards_support"
                    ]
                })
            ),
            "expected": ref("META:NOT_EMPTY-4").string,
            "raise_handler": does_not_raise()
        },
    ],
    "ERROR": [
        {
            "value": ref(
                key="META:ERROR-1",
                obj=ValueField({
                    "locale": "eu" * 33,
                    "timezone": "America" * 10,
                    "client_id": "eu.yandex.searchplugin/7.16 (none none; android 4.4.2)" * 25,
                    "interfaces": ref("INTERFACES:EMPTY-1").obj,
                })
            ),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
    ],
}

NLU = {
    "EMPTY": [
        {
            "value": ref(
                key="NLU:EMPTY-1",
                obj=ValueField({
                    "tokens": [],
                    "entities": [],
                    "intents": {}
                })
            ),
            "expected": ref("NLU:EMPTY-1").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="NLU:EMPTY-2",
                obj=ref("EMPTY")
            ),
            "expected": ref("NLU:EMPTY-1").string,
            "raise_handler": does_not_raise()
        }
    ],
    "NOT_EMPTY": [
        {
            "value": ref(
                key="NLU:NOT_EMPTY-1",
                obj=ValueField({
                    "tokens": [
                        "закажи",
                        "пиццу",
                        "на",
                        "льва",
                        "толстого",
                        "16",
                        "на",
                        "завтра"
                    ],
                    "entities": [
                        ref("ENTITY:NOT_EMPTY:GEO-1").obj,
                        ref("ENTITY:NOT_EMPTY:FIO-2").obj,
                        ref("ENTITY:NOT_EMPTY:NUMBER-1").obj,
                        ref("ENTITY:NOT_EMPTY:DATETIME-1").obj
                    ],
                    "intents": {}
                })
            ),
            "expected": ref("NLU:NOT_EMPTY-1").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="NLU:NOT_EMPTY-2",
                obj=ValueField({
                    "tokens": [],
                    "entities": [],
                    "intents": {
                        "turn.on": ref("INTENTS:NOT_EMPTY-3").obj
                    },
                })
            ),
            "expected": ref("NLU:NOT_EMPTY-2").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="NLU:NOT_EMPTY-3",
                obj=ValueField({
                    "tokens": [
                        "закажи",
                        "такси",
                        "на",
                        "льва",
                        "толстого",
                        "16",
                        "на",
                        "14:00"
                    ],
                    "entities": [],
                    "intents": {
                        "taxi": ref("INTENTS:NOT_EMPTY-1").obj
                    },
                })
            ),
            "expected": ref("NLU:NOT_EMPTY-3").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="NLU:NOT_EMPTY-4",
                obj=ValueField({
                    "tokens": [],
                    "entities": [
                        ref("ENTITY:NOT_EMPTY:DICT-1").obj
                    ],
                    "intents": {},
                })
            ),
            "expected": ref("NLU:NOT_EMPTY-4").string,
            "raise_handler": does_not_raise()
        }
    ],
    "ERROR": [
        {
            "value": ref(
                key="NLU:ERROR-1",
                obj=ValueField({
                    "tokens": [1, 2, 3],
                    "entities": [
                        ref("INTENTS:NOT_EMPTY-3").obj
                    ],
                    "intents": {
                        "turn.on": ref("ENTITY:NOT_EMPTY:DICT-1").obj
                    },
                })
            ),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        }
    ],
}

STATE = {
    "EMPTY": [
        {
            "value": ref(
                key="STATE:EMPTY-1",
                obj=ref("EMPTY")
            ),
            "expected": State().model_dump_json(exclude_none=True).encode(),
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="STATE:EMPTY-2",
                obj=ValueField({
                    "session": {},
                    "user": {},
                    "application": {},
                })
            ),
            "expected": ref("STATE:EMPTY-2").string,
            "raise_handler": does_not_raise()
        },
    ],
    "NOT_EMPTY": [
        {
            "value": ref(
                key="STATE:NOT_EMPTY-1",
                obj=ValueField({
                    "session": {
                        "value": 10
                    },
                    "user": {},
                    "application": {},
                })
            ),
            "expected": ref("STATE:NOT_EMPTY-1").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="STATE:NOT_EMPTY-2",
                obj=ValueField({
                    "session": {},
                    "user": {
                        "value": 42
                    },
                    "application": {},
                })
            ),
            "expected": ref("STATE:NOT_EMPTY-2").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="STATE:NOT_EMPTY-3",
                obj=ValueField({
                    "session": {},
                    "user": {},
                    "application": {
                        "value": 37
                    },
                })
            ),
            "expected": ref("STATE:NOT_EMPTY-3").string,
            "raise_handler": does_not_raise()
        },
        # TODO: add custom state check
    ],
    "ERROR": [
        {
            "value": ref(
                key="STATE:ERROR-1",
                obj=ValueField({
                    "application": [],
                })
            ),
            "expected": ref("STATE:ERROR-1").string,
            "raise_handler": pytest.raises(ValueError)
        },
    ]
}

SESSION_USER = {
    "NOT_EMPTY": [
        {
            "value": ref(
                key="SESSION_USER:NOT_EMPTY-1",
                obj=ValueField({
                    "user_id": "6C91DA5198D1758C6A9F63A7C5CDDF09359F683B13A18A151FBF4C8B092BB0C2"
                })
            ),
            "expected": ref("SESSION_USER:NOT_EMPTY-1").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="SESSION_USER:NOT_EMPTY-2",
                obj=ValueField({
                    "user_id": "6C91DA5198D1758C6A9F63A7C5CDDF09359F683B13A18A151FBF4C8B092BB0C2",
                    "access_token": "AgAAAAAB4vpbAAApoR1oaCd5yR6eiXSHqOGT8dT"
                })
            ),
            "expected": ref("SESSION_USER:NOT_EMPTY-2").string,
            "raise_handler": does_not_raise()
        },
    ],
    "ERROR": [
        {
            "value": ref(
                key="SESSION_USER:ERROR-1",
                obj=ref("EMPTY")
            ),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ref(
                key="SESSION_USER:ERROR-2",
                obj=ValueField({
                    "user_id": None,
                })
            ),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
    ]
}

SESSION_APPLICATION = {
    "NOT_EMPTY": [
        {
            "value": ref(
                key="SESSION_APPLICATION:NOT_EMPTY-1",
                obj=ValueField({
                    "application_id": "47C73714B580ED2469056E71081159529FFC676A4E5B059D629A819E857DC2F8"
                })
            ),
            "expected": ref("SESSION_APPLICATION:NOT_EMPTY-1").string,
            "raise_handler": does_not_raise()
        },
    ],
    "ERROR": [
        {
            "value": ref(
                key="SESSION_APPLICATION:ERROR-1",
                obj=ref("EMPTY")
            ),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ref(
                key="SESSION_APPLICATION:ERROR-2",
                obj=ValueField({
                    "application_id": None,
                })
            ),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ref(
                key="SESSION_APPLICATION:ERROR-3",
                obj=ValueField({
                    "application_id": "a" * 96,
                })
            ),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
    ]
}

SESSION = {
    "NOT_EMPTY": [
        {
            "value": ref(
                key="SESSION:NOT_EMPTY-1",
                obj=ValueField({
                    "message_id": 0,
                    "session_id": "2eac4854-fce721f3-b845abba-20d60",
                    "user_id": "47C73714B580ED2469056E71081159529FFC676A4E5B059D629A819E857DC2F8",
                    "new": True,
                    "skill_id": "3ad36498-f5rd-4079-a14b-788652932056",
                    "user": ref("SESSION_USER:NOT_EMPTY-1").obj,
                    "application": ref("SESSION_APPLICATION:NOT_EMPTY-1").obj,
                })
            ),
            "expected": ref("SESSION:NOT_EMPTY-1").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="SESSION:NOT_EMPTY-2",
                obj=ValueField({
                    "message_id": 42,
                    "session_id": "2eac4854-fce721f3-b845abba-20d60",
                    "user_id": "47C73714B580ED2469056E71081159529FFC676A4E5B059D629A819E857DC2F8",
                    "new": False,
                    "skill_id": "3ad36498-f5rd-4079-a14b-788652932056",
                    "user": ref("SESSION_USER:NOT_EMPTY-2").obj,
                    "application": ref("SESSION_APPLICATION:NOT_EMPTY-1").obj,
                })
            ),
            "expected": ref("SESSION:NOT_EMPTY-2").string,
            "raise_handler": does_not_raise()
        },
        {
            # User not authorized in yandex
            "value": ref(
                key="SESSION:NOT_EMPTY-3",
                obj=ValueField({
                    "message_id": 42,
                    "session_id": "2eac4854-fce721f3-b845abba-20d60",
                    "user_id": "47C73714B580ED2469056E71081159529FFC676A4E5B059D629A819E857DC2F8",
                    "new": False,
                    "skill_id": "3ad36498-f5rd-4079-a14b-788652932056",
                    "application": ref("SESSION_APPLICATION:NOT_EMPTY-1").obj,
                })
            ),
            "expected": ref("SESSION:NOT_EMPTY-3").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="SESSION:NOT_EMPTY-4",
                obj=ValueField({
                    "message_id": 12345678,
                    "session_id": "2eac4854-fce721f3-b845abba-20d60",
                    "user_id": "47C73714B580ED2469056E71081159529FFC676A4E5B059D629A819E857DC2F8",
                    "new": False,
                    "skill_id": "3ad36498-f5rd-4079-a14b-788652932056",
                    "application": ref("SESSION_APPLICATION:NOT_EMPTY-1").obj,
                })
            ),
            "expected": ref("SESSION:NOT_EMPTY-4").string,
            "raise_handler": does_not_raise()
        },
    ],
    "ERROR": [
        {
            "value": ref(
                key="SESSION:ERROR-1",
                obj=ref("EMPTY")
            ),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ref(
                key="SESSION:ERROR-2",
                obj=ref("EMPTY")
            ),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ref(
                key="SESSION:ERROR-3",
                obj=ValueField({
                    "message_id": 123456789,
                    "session_id": "2eac4854-fce721f3-b845abba-20d60" * 2,
                    "user_id": "47C73714B580ED2469056E71081159529FFC676A4E5B059D629A819E857DC2F8" * 2,
                    "new": False,
                    "skill_id": "3ad36498-f5rd-4079-a14b-788652932056" * 2,
                    "application": ref("SESSION_APPLICATION:ERROR-2").obj,
                })
            ),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ref(
                key="SESSION:ERROR-4",
                obj=ValueField({
                    "message_id": 123456789,
                    "session_id": "2eac4854-fce721f3-b845abba-20d60" * 2,
                    "user_id": "47C73714B580ED2469056E71081159529FFC676A4E5B059D629A819E857DC2F8" * 2,
                    "user": ref("SESSION_USER:ERROR-2").obj,
                    "skill_id": "3ad36498-f5rd-4079-a14b-788652932056" * 2,
                    "application": ref("SESSION_APPLICATION:ERROR-3").obj,
                })
            ),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
    ]
}

REQUEST_SHOW = {
    "ERROR": [
        {
            "value": ref(
                key="REQUEST_SHOW:ERROR-1",
                obj=ref("EMPTY")
            ),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ref(
                key="REQUEST_SHOW:ERROR-2",
                obj=ValueField({
                    "type": "Show.Pull"
                })
            ),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ref(
                key="REQUEST_SHOW:ERROR-3",
                obj=ValueField({
                    "show_type": "MORNING",
                })
            ),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
    ],
    "NOT_EMPTY": [
        {
            "value": ref(
                key="REQUEST_SHOW:NOT_EMPTY-1",
                obj=ValueField({
                    "type": "Show.Pull",
                    "show_type": "MORNING",
                })
            ),
            "expected": ref("REQUEST_SHOW:NOT_EMPTY-1").string,
            "raise_handler": does_not_raise()
        },
    ],
}

REQUEST_PURCHASE = {
    "ERROR": [
        {
            "value": ref(
                key="REQUEST_PURCHASE:ERROR-1",
                obj=ref("EMPTY")
            ),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ref(
                key="REQUEST_PURCHASE:ERROR-2",
                obj=ValueField({
                    "type": "Purchase.Other",
                    "purchase_request_id": "d432de19be8347d09f656d9fe966e2f9",
                    "purchase_token": "d432de19be8347d09f656d9fe966e2f9",
                    "order_id": "eeb59d64-9e6a-11ea-bb37-0242ac130002",
                    "purchase_timestamp": 1590399311.00,
                    "purchase_payload": None,
                })
            ),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
    ],
    "NOT_EMPTY": [
        {
            "value": ref(
                key="REQUEST_PURCHASE:NOT_EMPTY-1",
                obj=ValueField({
                    "type": "Purchase.Confirmation",
                    "purchase_request_id": "d432de19be8347d09f656d9fe966e2f9",
                    "purchase_token": "d432de19be8347d09f656d9fe966e2f9",
                    "order_id": "eeb59d64-9e6a-11ea-bb37-0242ac130002",
                    "purchase_timestamp": 1590399311,
                    "purchase_payload": {
                        "value": "payload"
                    },
                    "signed_data": "purchase_request_id=id_value&purchase_token=token_value&order_id=id_value&...",
                    "signature": "Pi6JNCFeeleRa...",
                })
            ),
            "expected": ref("REQUEST_PURCHASE:NOT_EMPTY-1").string,
            "raise_handler": does_not_raise()
        },
    ],
    "CUSTOM": [
        {
            "value": ref(
                key="REQUEST_PURCHASE:CUSTOM-1",
                obj=ValueField({
                    "type": "Purchase.Confirmation",
                    "purchase_request_id": "d432de19be8347d09f656d9fe966e2f9",
                    "purchase_token": "d432de19be8347d09f656d9fe966e2f9",
                    "order_id": "eeb59d64-9e6a-11ea-bb37-0242ac130002",
                    "purchase_timestamp": 1590399311,
                    "purchase_payload": {
                        "id": "22c5d173-000f-5000-9000-1bdf241d4651",
                        "status": "wait",
                        "paid": False,
                        "amount": "5",
                        "currency": "USD",
                    },
                    "signed_data": "purchase_request_id=id_value&purchase_token=token_value&order_id=id_value&...",
                    "signature": "Pi6JNCFeeleRa...",
                })
            ),
            "expected": ref("REQUEST_PURCHASE:CUSTOM-1").string,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="REQUEST_PURCHASE:CUSTOM-2",
                obj=ValueField(
                    obj={
                        "type": "Purchase.Confirmation",
                        "purchase_request_id": "d432de19be8347d09f656d9fe966e2f9",
                        "purchase_token": "d432de19be8347d09f656d9fe966e2f9",
                        "order_id": "eeb59d64-9e6a-11ea-bb37-0242ac130002",
                        "purchase_timestamp": 1590399311,
                        "purchase_payload": {
                            "id": "22c5d173-000f-5000-9000-1bdf241d4651",
                            "status": "wait",
                            "paid": True,
                            "amount": "300",
                        },
                        "signed_data": "purchase_request_id=id_value&purchase_token=token_value&order_id=id_value&...",
                        "signature": "Pi6JNCFeeleRa...",
                    })
            ),
            "expected": orjson.dumps(
                {
                    "type": "Purchase.Confirmation",
                    "purchase_request_id": "d432de19be8347d09f656d9fe966e2f9",
                    "purchase_token": "d432de19be8347d09f656d9fe966e2f9",
                    "order_id": "eeb59d64-9e6a-11ea-bb37-0242ac130002",
                    "purchase_timestamp": 1590399311,
                    "purchase_payload": {
                        "id": "22c5d173-000f-5000-9000-1bdf241d4651",
                        "status": "wait",
                        "paid": True,
                        "amount": "300",
                        "currency": "RUB",
                    },
                    "signed_data": "purchase_request_id=id_value&purchase_token=token_value&order_id=id_value&...",
                    "signature": "Pi6JNCFeeleRa...",
                }
            ),
            "raise_handler": does_not_raise()
        },
    ],
}

REQUEST_AUDIO_ERROR = [
    ref(
        key="REQUEST_AUDIO_ERROR-1",
        obj=ValueField({
            "type": request.audio.RequestAudioErrorType.MEDIA_ERROR_UNKNOWN,
            "message": "Что-то пошло не так 🙃"
        })
    ),
    ref(
        key="REQUEST_AUDIO_ERROR-2",
        obj=ValueField({
            "type": request.audio.RequestAudioErrorType.MEDIA_ERROR_SERVICE_UNAVAILABLE,
            "message": "указанный URL трека недоступен или некорректен."
        })
    ),
]

REQUEST_AUDIO = {
    "ERROR": [
        {
            "value": ref(
                key="REQUEST_AUDIO:ERROR-1",
                obj=ref("EMPTY")
            ),
            "expected": None,
            "has_error": None,
            "raise_handler": pytest.raises((ValueError, KeyError))
        },
        {
            "value": ref(
                key=f"REQUEST_AUDIO:ERROR-2",
                obj=ValueField({
                    "type": request.audio.RequestAudioType.AUDIO_PLAYER_PLAYBACK_FAILED
                })
            ),
            "expected": None,
            "has_error": None,
            "raise_handler": pytest.raises(ValueError)
        }
    ],
    "NOT_EMPTY": [
        *[
            {
                "value": ref(
                    key=f"REQUEST_AUDIO:NOT_EMPTY-{index}",
                    obj=ValueField({
                        "type": request_type
                    })
                ),
                "expected": ref(f"REQUEST_AUDIO:NOT_EMPTY-{index}").string,
                "has_error": False,
                "raise_handler": does_not_raise()
            } for index, request_type in enumerate(
                list(request.audio.RequestAudioType._value2member_map_.keys())[0: 4],
                start=1
            )
        ],
        {
            "value": ref(
                key="REQUEST_AUDIO:NOT_EMPTY-5",
                obj=ValueField({
                    "type": request.audio.RequestAudioType.AUDIO_PLAYER_PLAYBACK_FAILED,
                    "error": ref(key="REQUEST_AUDIO_ERROR-1").obj
                })
            ),
            "expected": ref("REQUEST_AUDIO:NOT_EMPTY-5").string,
            "has_error": True,
            "raise_handler": does_not_raise()
        },
        {
            "value": ref(
                key="REQUEST_AUDIO:NOT_EMPTY-6",
                obj=ValueField({
                    "type": request.audio.RequestAudioType.AUDIO_PLAYER_PLAYBACK_FAILED,
                    "error": ref(key="REQUEST_AUDIO_ERROR-2").obj
                })
            ),
            "expected": ref("REQUEST_AUDIO:NOT_EMPTY-6").string,
            "has_error": True,
            "raise_handler": does_not_raise()
        }
    ],
}
