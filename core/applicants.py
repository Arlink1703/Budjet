from dataclasses import dataclass
from enum import Enum


class RankType(Enum):
    GREEN = "проходит"
    YELLOW = "не подал документы"
    GREY = "попал на другое направление"
    UNRANKED = "нет статуса "


@dataclass
class Applicant:
    id: str
    position: int
    priority: int
    test_type: str
    average_mark: float
    extra_points: int
    exam_points: int
    all_points: int
    documents_status: bool
    rank: RankType

    def __str__(self):
        return (
            "----------------------------------\n"
            f"ID: {self.id} "
            f"Место в списке: {self.position}\n"
            f"Приоритет: {self.priority} "
            f"Вид испытания: {self.test_type}\n"
            f"Общие баллы: {self.all_points} "
            f"Баллы: {self.exam_points} "
            f"Доп баллы: {self.extra_points}\n"
            f"Средний бал: {self.average_mark}\n"
            f"Документы: {'Поданы' if self.documents_status else 'Не поданы'} "
            f"Статус: {self.rank.value}\n"
            "----------------------------------"
        )

    def __getitem__(self, key):
        return getattr(self, key)
