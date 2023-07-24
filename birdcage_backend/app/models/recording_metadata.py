from app.utils.db import BaseModel
from peewee import IntegerField, TextField, DateTimeField, ForeignKeyField
from app.models.streams import Stream
import datetime

class RecordingMetadata(BaseModel):
    id = IntegerField(primary_key=True)
    filename = TextField(unique=True)
    stream = ForeignKeyField(Stream, backref='recordings')
    timestamp = DateTimeField(default=datetime.datetime.now)