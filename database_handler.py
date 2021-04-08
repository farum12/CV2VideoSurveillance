from database import init_db
from database import db_session
from models import settings
from sqlalchemy.sql.expression import func

# Analysis modes
# noAn, simple, 2areaVert, 3areaVert, 2areaHor, 3areaHor

def debugDb():
    #sets = settings('no','yes','simple','no', 'True', 'False', 'False', 300, 10)
    #db_session.add(sets)
    #db_session.commit()
    print(str(getLastSetting()))

def getLastSettingIndex():
    return db_session.query(func.max(settings.id)).scalar()

def getLastSetting():
    setting = settings.query.filter(settings.id == getLastSettingIndex()).first()
    return setting

def setNewSetting(displayTimestamp, displayBoundaries, analysisMode, useYOLO,
                  area1, area2, area3, sensitivity, maxTicks):
    sets = settings(displayTimestamp, displayBoundaries, analysisMode, useYOLO,
                    area1, area2, area3, int(sensitivity), int(maxTicks))
    db_session.add(sets)
    db_session.commit()