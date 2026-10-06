from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class ContentType(Base):
    __tablename__ = "content_types"
 
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    default_segmentation_strategy: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(Text, default="")


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    source_url: Mapped[str] = mapped_column(String(255), default="")
    content_type_id: Mapped[int] = mapped_column(ForeignKey("content_types.id"))
    file_path: Mapped[str] = mapped_column(String(500), default="")
    status: Mapped[str] = mapped_column(String(30), default="uploaded")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

    content_type: Mapped["ContentType"] = relationship()
    segments: Mapped[list["Segment"]] = relationship(back_populates="session")


class Segment(Base):
    __tablename__ = "segments"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
    segment_type: Mapped[str] = mapped_column(String(10))
    question: Mapped[str] = mapped_column(Text, default="")
    answer_or_summary: Mapped[str] = mapped_column(Text, default="")
    start_time: Mapped[int] = mapped_column(default=0)
    end_time: Mapped[int] = mapped_column(default=0)
    topic: Mapped[str] = mapped_column(String(255), default="")
    keywords: Mapped[str] = mapped_column(Text, default="")
    confidence: Mapped[float] = mapped_column(default=0.0)
    boundary_source: Mapped[str] = mapped_column(String(30), default="auto_detected")
    review_status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

    session: Mapped["Session"] = relationship(back_populates="segments")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String(256), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

    conversations: Mapped[list["Conversation"]] = relationship(back_populates="user")


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(255), default="New conversation")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

    user: Mapped["User"] = relationship(back_populates="conversations")
    messages: Mapped[list["ChatMessage"]] = relationship(back_populates="conversation")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"))
    role: Mapped[str] = mapped_column(String(10))  # user or assistant
    content: Mapped[str] = mapped_column(Text)
    citations: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

    conversation: Mapped["Conversation"] = relationship(back_populates="messages")


class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
    stage: Mapped[str] = mapped_column(String(50))
    error_message: Mapped[str] = mapped_column(String(50), default="pending")
    started_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    finished_at: Mapped[datetime | None] = mapped_column(default=datetime.now(timezone.utc))
