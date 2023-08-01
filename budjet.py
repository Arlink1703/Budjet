from core.aplicants_list_formater import AplicantsListFormatter


if __name__ == "__main__":
    url = "https://abit.itmo.ru/ranking/master/budget/7431"
    id = "15706229463"
    formatter = AplicantsListFormatter(url)
    formatter.update_list()
    formatter.define_me(id)
    print(f"Общее количество подавших: {len(formatter.applicants)}\n"
          f"Последнее место по списку: {formatter.last_one}")
    print(f"Ваш профиль:\n" f"{formatter.hero}")
    formatter.get_off_the_path_applicants()
    formatter.get_dark_horses_applicants()
