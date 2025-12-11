from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('postgresql://babdus:asdfqwer@localhost:5432/verbs')

# Create a declarative base class
Base = declarative_base()

# Define the Book model
class VerbForm(Base):
    __tablename__ = 'verb_form'

    id = Column(Integer, primary_key=True)

    word_form = Column(String(128))
    verb = Column(String(128))
    screeve = Column(String(128))
    subject_number = Column(String(8))
    subject_person = Column(Integer)
    object_number = Column(String(8))
    object_person = Column(Integer)
    preverb = Column(String(16))
    blueprint = Column(String)

    __table_args__ = (
        UniqueConstraint(
            'verb',
            'screeve',
            'subject_number',
            'subject_person',
            'object_number',
            'object_person',
            'preverb',
            'blueprint',
            name='_unique_word_form'
        ),
    )

    def __repr__(self):
        return f"<VerbForm(word_form='{self.word_form}', verb='{self.verb}', screeve='{self.screeve}', subject='{self.subject_person} {self.subject_number}', object='{self.object_person} {self.object_number}', preverb='{self.preverb}', blueprint='{self.blueprint}')>"

# Create all tables in the engine
Base.metadata.create_all(engine)