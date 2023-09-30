from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from models import Base, User, Question, Answer
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///quiz.db", echo=True)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


# with Session(engine) as session:
with Session() as session:
    spongebob = User(username="spongebob")
    session.add_all([spongebob])

    import json

    with open('q.json', 'r') as f:
        ppf = json.load(f)

        for i in ppf['lst']:
            question = Question(question=i['question'])
            session.add(question)
            session.commit()
            for a in i['answers']:
                answer = Answer(answer=a['answer'],
                                question=question,
                                is_correct=a['correct'])
                session.add(answer)
        
        session.commit()


    


# import json

# with open('flet-test/q.json', 'r') as f:
#     ppf = json.load(f)
#     print(ppf)
#     print(type(ppf))
