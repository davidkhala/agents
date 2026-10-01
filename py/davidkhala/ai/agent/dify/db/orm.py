import json

from sqlalchemy import Column, String, Text, JSON, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DifyBase(Base):
    __abstract__ = True  # keyword for SQLAlchemy
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())


class AppModelConfig(DifyBase):
    __tablename__ = "app_model_configs"
    __table_args__ = {"schema": "public"}

    app_id = Column(UUID(as_uuid=True), nullable=False)

    provider = Column(String(255))
    model_id = Column(String(255))
    configs = Column(JSON)

    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())

    opening_statement = Column(Text)
    suggested_questions = Column(Text)
    suggested_questions_after_answer = Column(Text)
    more_like_this = Column(Text)
    model = Column(Text)
    user_input_form = Column(Text)
    pre_prompt = Column(Text)
    agent_mode = Column(Text)
    speech_to_text = Column(Text)
    sensitive_word_avoidance = Column(Text)
    retriever_resource = Column(Text)

    dataset_query_variable = Column(String(255))
    prompt_type = Column(String(255), nullable=False, server_default="simple")

    chat_prompt_config = Column(Text)
    completion_prompt_config = Column(Text)
    dataset_configs = Column(Text)
    external_data_tools = Column(Text)
    file_upload = Column(Text)
    text_to_speech = Column(Text)

    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))

    def __repr__(self):
        return f"<AppModelConfig(id={self.id}, app_id={self.app_id}, provider={self.provider}, model_id={self.model_id})>"


class Graph:
    @staticmethod
    def convert(*records: list[dict]):
        return [{**record, "graph": Graph(**json.loads(record["graph"]))} for record in records]
