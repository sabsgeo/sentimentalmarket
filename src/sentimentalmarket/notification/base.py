from abc import ABC, abstractmethod

class INotify(ABC):
    
    @abstractmethod
    def send_notification(self, message) -> None :
        pass
    