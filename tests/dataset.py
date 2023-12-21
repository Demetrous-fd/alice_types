from contextlib import nullcontext as does_not_raise

import pytest
import orjson

from alice_types import InterfaceType


class ValueField:
    def __init__(self, obj: dict):
        self.obj = obj
        self.string = orjson.dumps(obj)
    

ANALYTICS_EVENT = {
    "ERROR": [
        {
            "value": ValueField({}),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ValueField({"name": "Test", "value": {"1": {"2": {"3": {"4": {"5": {"6": {}}}}}}}}),
            "expected": None,
            "raise_handler": pytest.raises(ValueError)
        },
    ],
    "NOT_EMPTY": [
        {
            "value": ValueField({"name": "Test"}),
            "expected": orjson.dumps({"name": "Test", "value": {}}),
            "raise_handler": does_not_raise()
        },
        {
            "value": ValueField({"name": "Test", "value": {}}),
            "expected": orjson.dumps({"name": "Test", "value": {}}),
            "raise_handler": does_not_raise()
        },
    ],
}

ANALYTICS = {
    "EMPTY": [
        {
            "value": ValueField({}),
            "length": 0,
            "raise_handler": does_not_raise()
        },
        {
            "value": ValueField({"events": []}),
            "length": 0,
            "raise_handler": does_not_raise()
        },

    ],
    "NOT_EMPTY": [
        {
            "value": ValueField({
                "events": [
                    ANALYTICS_EVENT["NOT_EMPTY"][0]["value"].obj
                ]
            }),
            "length": 1,
            "raise_handler": does_not_raise()
        },
        {
            "value": ValueField({
                "events": [
                    ANALYTICS_EVENT["NOT_EMPTY"][1]["value"].obj
                ]
            }),
            "length": 1,
            "raise_handler": does_not_raise()
        },
    ],
    "ERROR": [
        {
            "value": ValueField({
                "events": [
                    ANALYTICS_EVENT["ERROR"][0]["value"].obj
                ]
            }),
            "length": None,
            "raise_handler": pytest.raises(ValueError)
        },
        {
            "value": ValueField({
                "events": [
                    ANALYTICS_EVENT["ERROR"][1]["value"].obj
                ]
            }),
            "length": None,
            "raise_handler": pytest.raises(ValueError)
        }
    ]
}

INTERFACES = {
    "EMPTY": [
        {
            "value": ValueField({}),
            "expected": [],
            "has": [],
            "raise_handler": does_not_raise()
        },
    ],
    "NOT_EMPTY": [
        {
            "value": ValueField({"screen": {}, "account_linking": {}, "payments": {}}),
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
            "expected": '{"title":"Test","payload":{},"hide":false}',
            "raise_handler": does_not_raise()
        },
        {
            "value": ValueField({
                "title": "Test",
                "hide": True
            }),
            "expected": '{"title":"Test","payload":{},"hide":true}',
            "raise_handler": does_not_raise()
        },
        {
            "value": ValueField({
                "title": "Test",
                "url": "https://yandex.ru/dev/dialogs/alice/doc"
            }),
            "expected": '{"title":"Test","url":"https://yandex.ru/dev/dialogs/alice/doc","payload":{},"hide":false}',
            "raise_handler": does_not_raise()
        },
    ],
    "ERROR": [
        {
            "value": ValueField({}),
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
