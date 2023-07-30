import re

import requests
from bs4 import BeautifulSoup

from core.applicants import Applicant, RankType


class AplicantsListFormatter:
    def __init__(self, url) -> None:
        self.url = url
        self.applicants = []
        self.hero = []

    def change_url(self, url) -> None:
        self.url = url

    def define_me(self, id):
        if not self.applicants:
            return "You need to update list first!"
        for applicant in self.applicants:
            if applicant.id == id:
                self.hero = applicant
                return "Your profile has been identified!"
        else:
            return "You are not in the list :("

    def update_list(self) -> list[Applicant]:
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            applicant_cards = soup.find_all(
                "div", class_="RatingPage_table__item__qMY0F"
            )
            self.applicants = AplicantsListFormatter._parse_applicants(applicant_cards)
            return self.applicants
        else:
            return []

    def get_off_the_path_applicants(self):
        counter = 0
        grey_status_applicants = []
        for applicant in self.applicants:
            if applicant.position >= self.hero.position:
                break
            if applicant.rank == RankType.GREY:
                counter += 1
                grey_status_applicants.append(applicant)

        print(
            f"Людей выше вас в списке, попдающих на другие направления, всего: {counter}"
        )
        # for applicant in grey_status_applicants:
        #     print(applicant)
        return

    def get_dark_horses_applicants(self):
        horses_counter = 0
        grey_horses_counter = 0
        foreigns_counter = 0
        foreigns_grey_counter = 0
        dark_horses_applicants = []
        for applicant in self.applicants:
            if applicant.position <= self.hero.position and applicant.exam_points > 0:
                continue

            if applicant.extra_points > 0 and (
                applicant.all_points == applicant.extra_points
            ):
                dark_horses_applicants.append(applicant)
                grey_horses_counter += 1 if applicant.rank == RankType.GREY else 0
                horses_counter += 1

            elif (
                applicant.average_mark >= self.hero.average_mark
                and applicant.exam_points == 0
            ):
                dark_horses_applicants.append(applicant)
                grey_horses_counter += 1 if applicant.rank == RankType.GREY else 0
                horses_counter += 1

            elif not applicant.id.isdigit():
                dark_horses_applicants.append(applicant)
                foreigns_grey_counter += 1 if applicant.rank == RankType.GREY else 0
                foreigns_counter +=1

        print(
            f"Людей ниже вас в списке, имеющих шансы вас обойти, всего: {horses_counter}\n"
            f"Из них {grey_horses_counter} попадают на другое направление\n"
            f"Иностранцев {foreigns_counter} из которых {foreigns_grey_counter} попадают на другое направление"
        )
        # for applicant in dark_horses_applicants:
        #     print(applicant)
        return

    @staticmethod
    def _parse_applicants(applicant_cards) -> list[Applicant]:
        applicants_list = []
        for card in applicant_cards:
            card_str = str(card)
            card_text = card.get_text()

            if re.search(r"green", card_str):
                rank = RankType.GREEN
            elif re.search(r"yellow", card_str):
                rank = RankType.YELLOW
            elif re.search(r"gray", card_str):
                rank = RankType.GREY
            else:
                rank = RankType.UNRANKED

            position = int(re.search(r"\d+", card_text).group(0))

            id = str(re.search(r"№(.*?)Приоритет:", card_text).group(1))

            priority = int(re.search(r"Приоритет:\s*(\d+)", card_text).group(1))

            test_type = re.search(r"Вид испытания:\s*(.*?)ИД", card_text).group(1)

            average_mark = re.search(
                r"Средний балл:\s*\*(.*?)Оригиналы документов", card_text
            ).group(1)
            average_mark = float(average_mark) if average_mark else 0

            extra_points = int(re.search(r"ИД:\s(\d*)Балл", card_text).group(1))

            exam_points = re.search(r"Балл ВИ:\s(\d*)", card_text).group(1)
            exam_points = int(exam_points) if exam_points else 0

            all_points = int(re.search(r"ВИ\+ИД:\s(\d*)", card_text).group(1))

            documents_status = re.search(
                r"Оригиналы документов:\s*(\w*)", card_text
            ).group(1)
            documents_status = True if documents_status == "да" else False

            applicant = Applicant(
                position=position,
                id=id,
                priority=priority,
                test_type=test_type,
                average_mark=average_mark,
                extra_points=extra_points,
                exam_points=exam_points,
                all_points=all_points,
                documents_status=documents_status,
                rank=rank,
            )

            applicants_list.append(applicant)

        return applicants_list
