from abc import ABC, abstractmethod

class IEXchangeAPI(ABC):
    @abstractmethod
    def get_account_info(self):
        pass
    
    @abstractmethod
    def get_ticker(self, symbol: str):
        pass
    
    @abstractmethod
    def place_order(self, symbol: str, typr_: str, price: float, amount: float):
        pass
    
    @abstractmethod
    def cancel_order(self, order_id: str, symbol: str):
        pass