from sqlalchemy.orm import Session
from app.models.quiz import Quiz, Question, Answer, QuizQuestion
from app.repositories.base_repo import BaseRepository

class QuizRepository(BaseRepository[Quiz]):
    def __init__(self, db: Session):
        super().__init__(Quiz, db)

class QuestionRepository(BaseRepository[Question]):
    def __init__(self, db: Session):
        super().__init__(Question, db)

class AnswerRepository(BaseRepository[Answer]):
    def __init__(self, db: Session):
        super().__init__(Answer, db)

class QuizQuestionRepository(BaseRepository[QuizQuestion]):
    def __init__(self, db: Session):
        super().__init__(QuizQuestion, db)
