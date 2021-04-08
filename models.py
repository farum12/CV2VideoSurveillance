from sqlalchemy import Column, Integer, String
from database import Base

class settings(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    displayTimestamp = Column(String(10), unique=False)
    displayBoundaries = Column(String(10), unique=False)
    analysisMode = Column(String(10), unique=False)
    useYOLO = Column(String(10), unique=False)
    area1 = Column(String(6), unique=False)
    area2 = Column(String(6), unique=False)
    area3 = Column(String(6), unique=False)
    sensitivity = Column(Integer, unique=False)
    maxTicks = Column(Integer, unique=False)

    def __init__(self, displayTimestamp=None, displayBoundaries=None,
                 analysisMode=None, useYOLO=None, area1=None, area2=None,
                 area3=None, sensitivity=None, maxTicks=None):
        self.displayTimestamp = displayTimestamp
        self.displayBoundaries = displayBoundaries
        self.analysisMode = analysisMode
        self.useYOLO = useYOLO
        self.area1 = area1
        self.area2 = area2
        self.area3 = area3
        self.sensitivity = sensitivity
        self.maxTicks = maxTicks

    def __repr__(self):
        return '<Id %r>' % self.id