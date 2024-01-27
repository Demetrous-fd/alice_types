from pydantic import BaseModel


# TODO: Изучить работу директивы.
# TODO: account_linking_complete_event это директива ?
# https://yandex.ru/dev/dialogs/alice/doc/auth/make-skill.html#start-account-linking
class StartAccountLinking(BaseModel):
    pass
