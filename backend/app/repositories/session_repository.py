from sqlalchemy.orm import Session as DBSession

from app.database.models import Session as VideoSession

class SessionRepository:
    def __init__(self, db: DBSession):
        self.db = db

    def create(self, title: str, source_url: str, content_type_id: int) -> VideoSession:
        session = VideoSession(
            title=title,
            source_url=source_url,
            content_type_id=content_type_id,
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_by_id(self, session_id: int) -> VideoSession | None:
        return self.db.get(VideoSession, session_id)

    def list_all(self) -> list[VideoSession]:
        return self.db.query(VideoSession).all()

    def update_status(self, session_id: int, status: str) -> VideoSession | None:
        session = self.get_by_id(session_id)
        if session is None:
            return None
        session.status = status
        self.db.commit()
        self.db.refresh(session)
        return session
