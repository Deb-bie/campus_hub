from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify # type: ignore
from app.utils.validators import validate_rsvp_data # type: ignore
from app.services.elasticsearch_service import ElasticsearchService
from app.utils.exceptions import SearchServiceError, ValidationError
from app import redis_client
from app.kafka import publisher
from app.models.rsvp import RSVP
from ..utils.db import db
from ..models.event_model import Event
from ..services.user_profile_service import get_user_by_email
import logging
import json

# blueprint
rsvp_blueprint = Blueprint("rsvp", __name__, url_prefix="/api/events")
rsvp_blueprint.strict_slashes = False

logger = logging.getLogger(__name__)

# create event
@rsvp_blueprint.route("/<uuid:event_id>/rsvp", methods=["POST"])
def create_rsvp(event_id):
    """Create a new RSVP"""

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid or missing JSON body"}), 400
        
        validate_rsvp_data(data)

        user_id = data['user_id']

        user_email = request.headers.get('x-user-email')
        auth_header = request.headers.get("Authorization")

        if not user_email or not auth_header:
            return jsonify(
                {
                    "error": "Unauthorized - Missing headers"        
                }
            ), 401
        
        event = Event.query.get(event_id)

        if not event:
            return jsonify(
                {
                    "error": "Event not found"        
                }
            ), 404
        
        existing_rsvp = RSVP.query.filter_by(event_id=event_id, user_id=user_id).first()
        
        if existing_rsvp:
            return jsonify(
                {
                    "error": "Already RSVP'd"
                }
            ), 200

        
        token = auth_header.replace("Bearer ", "")
        user_info = get_user_by_email(user_email, token)
        print(user_info)

        
        if (user_info.get('user_id') == user_id):

            rsvp = RSVP()
            rsvp.user_id = user_id
            rsvp.event_id = event_id

            print(user_id)
            print(event_id)

            db.session.add(rsvp)
            db.session.commit()

            # print(rsvp)

            publisher.publish_event("rsvp_created", "New rsvp created", rsvp.to_json())

            return jsonify(
                {
                    'message': "successful",
                    'result': rsvp.to_json(),
                    'status_code': 201
                }
            )
        
        else:
            return jsonify(
                {
                    "error": "Unauthorized"        
                }
            ), 401

    
    except ValidationError as e:
        db.session.rollback()
        return jsonify(
            {
                'error': str(e)
            }
        ), 400
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error: {e}")
        return jsonify(
            {
                'error': f'Internal server error: {e}'
            }
        ), 500


@rsvp_blueprint.route("/<uuid:user_id>/rsvps", methods=["GET"])
def get_all_rsvps_events_for_a_user(user_id):
    try:
        rsvps = RSVP.query.filter(RSVP.user_id == user_id).all()
        rsvps_data = []

        for rsvp in rsvps:
            rsvps_data.append(
                rsvp.to_json()
            )

        return jsonify(rsvps_data)

 
    except Exception as e:
        return jsonify (
            {
                'error': str(e),
                'status_code': 400
            }
        )


@rsvp_blueprint.route("/<uuid:event_id>/<uuid:user_id>/rsvp", methods=["DELETE"])
def remove_rsvp(event_id, user_id):
    """Remove RSVP"""

    try:
        user_email = request.headers.get('x-user-email')
        auth_header = request.headers.get("Authorization")

        if not user_email or not auth_header:
            return jsonify(
                {
                    "error": "Unauthorized - Missing headers"        
                }
            ), 401
        
        event = Event.query.get(event_id)

        if not event:
            return jsonify(
                {
                    "error": "Event not found"        
                }
            ), 404
        
        existing_rsvp = RSVP.query.filter_by(event_id=event_id, user_id=user_id).first()
        
        if not existing_rsvp:
            return jsonify(
                {
                    "error": "This event has not been RSVPd"
                }
            ), 200

        token = auth_header.replace("Bearer ", "")
        user_info = get_user_by_email(user_email, token)

        print("user_info: ", user_info)
        print("user_id: ", user_id)

        print(type(user_info.get('user_id')))
        print(type(user_id))
        
        if (user_info.get('user_id') == str(user_id)):

            db.session.delete(existing_rsvp)
            db.session.commit()


            return jsonify(
                {
                    'message': "successful",
                    'result': "RSVP removed",
                    'status_code': 200
                }
            )
        
        else:
            return jsonify(
                {
                    "error": "Unauthorized"        
                }
            ), 401

    except ValidationError as e:
        db.session.rollback()
        return jsonify(
            {
                'error': str(e)
            }
        ), 400
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error: {e}")
        return jsonify(
            {
                'error': f'Internal server error: {e}'
            }
        ), 500


@rsvp_blueprint.route("/rsvps/<uuid:event_id>", methods=["GET"])
def get_all_rsvps_for_an_event(event_id):
    try:
        rsvps = RSVP.query.filter(RSVP.event_id == event_id).all()
        rsvps_data = []

        for rsvp in rsvps:
            rsvps_data.append(
                rsvp.to_json()
            )

        return jsonify(rsvps_data)

 
    except Exception as e:
        return jsonify (
            {
                'error': str(e),
                'status_code': 400
            }
        )

