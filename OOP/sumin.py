class InterestRate:
    def __init__(self, rate):
        self.rate = rate

    def effect(self):
        print(f"기준 금리는 {self.rate}%이며, 대출과 소비에 영향을 줍니다.")

class CentralBankRate(InterestRate):
    def effect(self):
        print(f"한국은행 기준금리 {self.rate}%는 물가 안정과 경기 조절에 중요한 역할을 합니다.")

class Inflation:
    def __init__(self, rate):
        self.rate = rate

    def effect(self):
        print(f"현재 인플레이션율은 {self.rate}%로, 실질 구매력에 영향을 줍니다.")

class CPIInflation(Inflation):
    def effect(self):
        print(f"CPI 기준 인플레이션율 {self.rate}%는 생활 물가에 심각한 영향을 미칩니다.")

class GDP:
    def __init__(self, value, unit="조 원"):
        self.value = value
        self.unit = unit

    def effect(self):
        print(f"GDP는 {self.value,}{self.unit}로 국가의 경제 규모를 나타냅니다.")

class NominalGDP(GDP):
    def effect(self):
        print(f"명목 GDP는 물가 변동을 고려하지 않고 {self.value}로 측정됩니다.")

class Unemployment:
    def __init__(self, rate):
        self.rate = rate

    def effect(self):
        print(f"실업률은 {self.rate}%이며, 노동시장의 상태를 나타냅니다.")

class YouthUnemployment(Unemployment):
    def effect(self):
        print(f"청년 실업률은 {self.rate}%로, 청년층 경제 활동에 큰 영향을 미칩니다.")

interest = CentralBankRate(2.75)
inflation = CPIInflation(20.3)
gdp = NominalGDP(2549)
unemployment = YouthUnemployment(5.9)            
