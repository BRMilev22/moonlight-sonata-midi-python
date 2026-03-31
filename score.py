from abc import ABC, abstractmethod


class Score(ABC):

    @property
    @abstractmethod
    def title(self):
        pass

    @property
    @abstractmethod
    def tempo(self):
        pass

    @abstractmethod
    def get_notes(self):
        pass
