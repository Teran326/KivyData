from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.types import String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLITE = 'sqlite'
MYSQL = 'mysql'

Base = declarative_base()


class Popis(Base):
    __tablename__ = 'popis'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    popis = Column(String(1000), nullable=False)


class Rasa(Base):
    __tablename__ = 'rasa'

    id = Column(Integer, primary_key=True)
    nazev_rasy = Column(String(50), nullable=False)


class Povolani(Base):
    __tablename__ = 'povolani'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nazev_povolani = Column(String(50), nullable=False)
    popis_id = Column(Integer, ForeignKey('popis.id'), nullable=False)
    rasa_id = Column(Integer, ForeignKey('rasa.id'), nullable=False)


class Database:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
        MYSQL: 'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@localhost/{DB}'
    }

    def __init__(self, dbtype='sqlite', username='', password='', dbname='data'):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname, USERNAME=username, PASSWORD=password)
            self.engine = create_engine(engine_url, echo=False)
        else:
            print('DBType is not found in DB_ENGINE')

        Base.metadata.create_all(self.engine)
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def create_popis(self, popis):
        try:
            self.session.add(popis)
            self.session.commit()
            return True
        except:
            return False

    def create_rasa(self, rasa):
        try:
            self.session.add(rasa)
            self.session.commit()
            return True
        except:
            return False

    def create_povolani(self, povolani):
        try:
            self.session.add(povolani)
            self.session.commit()
            return True
        except:
            return False

    def create(self, povolani):
        try:
            self.session.add(povolani)
            self.session.commit()
            return True
        except:
            return False

    def read_all(self, order=Povolani.nazev_povolani):
        try:
            result = self.session.query(Povolani).order_by(order).all()
            return result
        except:
            return False

    def read_popis(self, order=Popis.popis):
        try:
            result = self.session.query(Popis).order_by(order).all()
            return result
        except:
            return False

    def read_popis_by_id(self, id):
        try:
            result = self.session.query(Popis).get(id)
            return result
        except:
            return False

    def read_rasa(self, order=Rasa.id):
        try:
            result = self.session.query(Rasa).order_by(order).all()
            return result
        except:
            return False

    def read_rasa_by_id(self, id):
        try:
            result = self.session.query(Rasa).get(id)
            return result
        except:
            return False

    def read_povolani(self, order=Povolani.id):
        try:
            result = self.session.query(Povolani).order_by(order).all()
            return result
        except:
            return False

    def read_povolani_by_id(self, id):
        try:
            result = self.session.query(Povolani).get(id)
            return result
        except:
            return False

    def read_by_id(self, id):
        try:
            result = self.session.query(Povolani).get(id)
            return result
        except:
            return False

    def update(self):
        try:
            self.session.commit()
            return True
        except:
            return False

    def delete_rasa(self, id):
        try:
            pokus = self.read_rasa_by_id(id)
            self.session.delete(pokus)
            self.session.commit()
            return True
        except:
            return False

    def delete_povolani(self, id):
        try:
            pokus = self.read_povolani_by_id(id)
            self.session.delete(pokus)
            self.session.commit()
            return True
        except:
            return False

    def delete_popis(self, id):
        try:
            pokus = self.read_popis_by_id(id)
            self.session.delete(pokus)
            self.session.commit()
            return True
        except:
            return False

    def delete(self, id):
        try:
            povolani = self.read_by_id(id)
            self.session.delete(povolani)
            self.session.commit()
            return True
        except:
            return False
