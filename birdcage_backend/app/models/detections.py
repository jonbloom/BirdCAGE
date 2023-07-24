from app.utils.db import BaseModel
from peewee import IntegerField, TextField, DateTimeField, FloatField, ForeignKeyField
from app.models.streams import Stream
import datetime

class Detection(BaseModel):
    id = IntegerField(primary_key=True)
    timestamp = DateTimeField(default=datetime.datetime.now)
    stream = ForeignKeyField(Stream, backref='detections')
    scientific_name = TextField()
    common_name = TextField()
    confidence = FloatField()
    filename = TextField()

    class Meta:
        table_name = 'detections'

    @classmethod
    def create_table(cls, safe=True):
        super().create_table(cls)

        cls._meta.database.execute_sql('''
        CREATE VIEW IF NOT EXISTS daily_detections AS  
                      SELECT  
                          date(timestamp) AS date,  
                          common_name,  
                          COUNT(*) AS count  
                      FROM  
                          detections  
                      GROUP BY  
                          date(timestamp), common_name;''')