import json


credentials_gcp = {
    "type": "service_account",
    "project_id": "wisdom-dev-340814",
    "private_key_id": "ab78b8143e098a83dd1f3c44e314349e74e3d3a9",
    "private_key": "-----BEGIN PRIVATE KEY-----\n"\
        "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDdcy6pPJHtrjOD\n"\
        "3fmKq1dPd/zvnmMhCq7Le2VRfjjhEw6ZL3yWER09+T4s1O0YdPfLh1jYlPR1hgHV\n"\
        "Imz5QWkO/w25UyA0C95ZhZJSEYPHSDvqovpB/GPyVAn6MPCcQ4w2OylD60alEv7B\n"\
        "9CAin6mol9EWmpic9yIJmH22Ra5ZCp+SGv71yps4Bml+KyRQaIZ3gtTmW7fCRSN8\n"\
        "3gMIofh65lqeu5cCFjMMJbKGW5oMqzPLKDofYOnc1iOhnGvxaOJMumm96PblBsnR\n"\
        "fe0mbUbUFMib2X6r1LzH7AfJOvsBzw4KI0VL5bJmcGoaeukD2+7o3gvpfg0vlLBI\n"\
        "q1xdSANTAgMBAAECggEAa7iVWJaRp8wG3Bz0v8skMBB+dfMWZmLDb1EJkpAzS+0Q\n"\
        "u1xZnsgZcOWWpIk5Ah4X0aX3hndCyQ5UQuC5oK/8UmKoQt+YOSkS0npCmHBTqXNO\n"\
        "Tg9UbBfBaIYPymfXCzRidpjltFe06CSqzx8ZKK6BAXVELNor5aLjqEZI1IrlygKU\n"\
        "vSJQC++9Iouv6piozRPCM8G9BBolxpiSx2Yaf328QnA79QETMVLmSQD9+K43BZkb\n"\
        "UtsvaJI9KgdWhcEBurGFo2oZUR0rmYL7H66Dz2c6eP49zJTqdggnu8cBd3YsP+HK\n"\
        "gehL9297lmDDjORGdZaO+BmuvHftruxDmrZ8NKn8GQKBgQDxelzRgPVcjA64w5p5\n"\
        "xM9KvpFKLqp+6xaRAtjCddaTg4bPC8NnDVRcz1ZOUxmODp9Oo1zxTtBA1QXYyUUS\n"\
        "Z+m7dnlGHCq7rIU4L5XVAWWVseTflVlwPBbGuVIBmbeqGgvor6I0w1IRR99nR/jd\n"\
        "gwtS8rhha2U89n3kiyAkqek8iQKBgQDqxHsenlbItpnbeLFECZOT6AiHvl48CN3A\n"\
        "uh5remzEoAhKGwy2BpdyyKeNuBzfjO51/0X/FDkBGqHq1bYI0MZr4qziEC3Wf/+q\n"\
        "qEofnxfn7hv9KJtf+t9+SVxrENQK1ke2yJimgR76WThzOnPqu528uT6c/Q7FNOry\n"\
        "T1DnE2wh+wKBgAM9H+eTcjcGjd/+h6DgeeNHwQ0cqR7AqnHRdvTMvc8GsZUvVDSa\n"\
        "oioIgeDVDn+wRIS6fjGiW/qyoLxynqGLkT/5a9D76brQqozBXqIXvbQPScGR8Dwo\n"\
        "IioSLD5nQGZgqQ465NMOV5hxvVZWSck2y70WElEELrxtleytzQWQ3db5AoGBANY0\n"\
        "ojXkuUB3w9iJvgxbRIk+vJHGs8rJODRCXcEpOhcKAaZEGgv35bW4uZDIfafHukh1\n"\
        "u9MrC3wjZbuUdXyDqZgEgkPeCUTfE1MOLFu/2JspGeaaZ3JiwAtFOosCFscwjsyL\n"\
        "KSU7SR2ZzLTuj5eMyjbJOwUYrKJpTzn5/tJoWVCDAoGAD6p/+ZU2xaFerlDTCRPV\n"\
        "Hna/hsjELR5iEL6XayerN/xClzV3HaqcqcrTcFdDnuf8hVDzWngPh09BbFhEQPUw\n"\
        "/LlaUiYro46SdhoyDMj/0db3w3t/2pJb+0Brmjj4Tio0ghmr7B5t5IXiTplGwPek\n"\
        "75NTPZaYe/3jOfvlJWEvsyc=\n-----END PRIVATE KEY-----\n",
    "client_email": "ruslan-mansurov-coding-exercis@wisdom-dev-340814.iam.gserviceaccount.com",
    "client_id": "115186629567316764719",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/"\
    "ruslan-mansurov-coding-exercis%40wisdom-dev-340814.iam.gserviceaccount.com",
}


with open("credentials_gcp.json", "w") as f:
    json.dump(credentials_gcp, f)