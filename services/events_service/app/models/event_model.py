from ..enums.category_enum import CategoryEnum
from ..enums.event_status import EventStatusEnum
from app.utils.db import db
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID, ARRAY # type: ignore
from sqlalchemy import Enum # type: ignore

class Event(db.Model):
    __tablename__="events"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.String(1000)
    )

    short_description = db.Column(
        db.String(500)
    )

    organizer_id = db.Column(
        UUID(as_uuid=True),
        nullable=False
    )

    location = db.Column(
        db.String(500)
    )

    start_time = db.Column(
        db.DateTime
    )

    end_time = db.Column(
        db.DateTime
    )

    category = db.Column(
        Enum(CategoryEnum)
    )

    image_url = db.Column(
        db.String(5000)
    )

    capacity = db.Column(
        db.Integer
    )

    is_public = db.Column(
        db.Boolean
    )

    is_virtual = db.Column(
        db.Boolean
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.now(),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(),
        onupdate=datetime.now(),
        nullable=False
    )

    virtual_meeting_link = db.Column(
        db.String(500)
    )

    tags = db.Column(
        ARRAY(db.String)
    )

    status = db.Column(
        Enum(EventStatusEnum)
    )

    is_recurring = db.Column(
        db.Boolean
    )

    is_free = db.Column(
        db.Boolean
    )

    fee = db.Column(
        db.Integer
    )

    def __repr__(self):
        return '<Event %r' %(self.name)
    
    def to_json(self):
        return{
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'short_description': self.short_description,
            'organizer_id': str(self.organizer_id),
            'location': self.location,
            'start_time':str(self.start_time),
            'end_time': str(self.end_time),
            'capacity': self.capacity,
            'category': str(self.category.value),
            'tags': self.tags,
            'image_url': self.image_url,
            'is_public': self.is_public,
            'is_virtual': self.is_virtual,
            'is_recurring': self.is_recurring,
            'is_free': self.is_free,
            'fee': self.fee,
            'virtual_meeting_link': self.virtual_meeting_link,
            'status': str(self.status.value),
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }
    

    def to_json_with_organizer(self, organizer_name):
        return{
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'short_description': self.short_description,
            'organizer_id': str(self.organizer_id),
            'organizer_name': organizer_name,
            'location': self.location,
            'start_time':str(self.start_time),
            'end_time': str(self.end_time),
            'capacity': self.capacity,
            'category': self.category.value,
            'tags': self.tags,
            'image_url': self.image_url,
            'is_public': self.is_public,
            'is_virtual': self.is_virtual,
            'is_recurring': self.is_recurring,
            'is_free': self.is_free,
            'fee': self.fee,
            'virtual_meeting_link': self.virtual_meeting_link,
            'status': self.status.value,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }


