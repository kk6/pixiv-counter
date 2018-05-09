# -*- coding: utf-8 -*-
import peewee as pw

db = pw.SqliteDatabase('pixiv.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class Word(BaseModel):
    text = pw.CharField(unique=True)


class SearchResult(BaseModel):
    word = pw.ForeignKeyField(Word, backref='results')
    stored_at = pw.DateField()
    num_of_safe = pw.IntegerField()
    num_of_r18 = pw.IntegerField()

    @property
    def num_of_all(self):
        return self.num_of_safe + self.num_of_r18
