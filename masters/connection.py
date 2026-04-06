from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, mapped_column

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
    trad_screeve = Column(String(128))
    subject_number = Column(String(8))
    subject_person = Column(Integer)
    object_number = Column(String(8))
    object_person = Column(Integer)
    preverb = Column(String(16))
    blueprint = Column(String)
    word_form_id = Column(Integer)

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


class WordForm(Base):
    __tablename__ = 'word_forms'

    id = Column(Integer, primary_key=True)
    word_form = Column(String(128))


class Concordance(Base):
    __tablename__ = 'concordances'

    id = Column(Integer, primary_key=True)

    query_word = Column(String(128))
    optional_word_form_id = mapped_column(ForeignKey('optional_word_forms.id'))
    optional_word_form = relationship('OptionalWordForm', back_populates='concordances')

    query_part_of_speech_id = mapped_column(ForeignKey('parts_of_speech.id'))
    query_part_of_speech = relationship('PartOfSpeech', back_populates='query_words')

    contexts = relationship('Context', back_populates='concordance')


class OptionalWordForm(Base):
    __tablename__ = 'optional_word_forms'

    id = Column(Integer, primary_key=True)
    word_form = Column(String(128))
    word_form_id = Column(Integer)
    concordances = relationship('Concordance', back_populates='optional_word_form')


class Context(Base):
    __tablename__ = 'contexts'

    id = Column(Integer, primary_key=True)

    direction = Column(String(16))
    concordance_id = mapped_column(ForeignKey('concordances.id'))
    concordance = relationship('Concordance', back_populates='contexts')
    context_words = relationship('ContextWord', back_populates='context')


class ContextWord(Base):
    __tablename__ = 'context_words'

    id = Column(Integer, primary_key=True)

    word = Column(String(128))
    position = Column(Integer)

    part_of_speech_id = mapped_column(ForeignKey('parts_of_speech.id'))
    part_of_speech = relationship('PartOfSpeech', back_populates='context_words')

    context_id = mapped_column(ForeignKey('contexts.id'))
    context = relationship('Context', back_populates='context_words')


class PartOfSpeech(Base):
    __tablename__ = 'parts_of_speech'

    id = Column(Integer, primary_key=True)
    part_of_speech = Column(String(128))

    context_words = relationship('ContextWord', back_populates='part_of_speech')
    query_words = relationship('Concordance', back_populates='query_part_of_speech')


# Create all tables in the engine
Base.metadata.create_all(engine)