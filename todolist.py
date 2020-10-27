from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


# noinspection SpellCheckingInspection
class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    date = Column(Date, default=datetime.today())
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def print_day_tasks(days_from_today):
    today = datetime.today() + timedelta(days=days_from_today)
    day_of_week = today.strftime('%A')
    day = today.day
    month = today.strftime('%b')
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    if len(rows) == 0:
        print(f"\n{day_of_week} {day} {month}:\nNothing to do!\n")
    else:
        print(f"\n{day_of_week} {day} {month}")
        for index, task in enumerate(rows, start=1):
            print(f"{index}. {task}")
        print()


usingTodoList = True
while usingTodoList:
    user_input = input("1) Today's tasks\n2) Week's tasks\n3) All tasks\n"
                       "4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit\n")
    if user_input == "1":
        print_day_tasks(0)
    elif user_input == "2":
        for i in range(7):
            print_day_tasks(i)
    elif user_input == "3":
        all_rows = session.query(Table).order_by(Table.deadline).all()
        print("\nAll tasks:")
        for idx, row in enumerate(all_rows, start=1):
            print(f"{idx}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        print()
    elif user_input == "4":
        today = datetime.today()
        missed_tasks = session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline).all()
        print("\nMissed tasks:")
        if len(missed_tasks) == 0:
            print("Nothing is missed!\n")
        else:
            for idx, row in enumerate(missed_tasks, start=1):
                print(f"{idx}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        print()
    elif user_input == "5":
        task_description = input("\nEnter task\n")
        task_deadline = input("Enter deadline\n")
        new_task = Table(task=f'{task_description}', deadline=datetime.strptime(f'{task_deadline}', '%Y-%m-%d').date())
        session.add(new_task)
        session.commit()
        print("The task has been added!\n")
    elif user_input == "6":
        print("\nChoose the number of the task you want to delete:")
        all_rows = session.query(Table).order_by(Table.deadline).all()
        for idx, row in enumerate(all_rows, start=1):
            print(f"{idx}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        delete_task_num = int(input())
        deleted_task = all_rows[delete_task_num - 1]
        session.delete(deleted_task)
        session.commit()
        print("The task has been deleted!\n")
    else:
        usingTodoList = False
        break
print("\nBye!")
