from app.utils.db import db
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID # type: ignore

class RSVP(db.Model):
    __tablename__="rsvp"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )

    user_id = db.Column(
        UUID(as_uuid=True),
        nullable=False
    )

    event_id = db.Column(
        UUID(as_uuid=True),
        nullable=False
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

    def __repr__(self):
        return '<RSVP %r' %(self.id)
    
    def to_json(self):
        return{
            'id': str(self.id),
            'event_id': str(self.event_id),
            'user_id': str(self.user_id),
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }
