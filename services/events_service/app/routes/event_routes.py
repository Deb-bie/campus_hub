from flask import Blueprint, request, jsonify # type: ignore
from ..utils.db import db
from ..models.event_model import Event
from ..services.user_profile_service import get_user_by_email

# blueprint
event_blueprint = Blueprint("event", __name__, url_prefix="/api/events")

# create event
@event_blueprint.route("/create", methods=["POST"])
def create_event():

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        user_email = request.headers.get('x-user-email')
        auth_header = request.headers.get("Authorization")

        if not user_email or not auth_header:
            return jsonify(
                {
                    "error": "Unauthorized - Missing headers"        
                }
            ), 401
        
        token = auth_header.replace("Bearer ", "")
        user_info = get_user_by_email(user_email, token)

        organizer_id = user_info.get("user_id")
        organizer_first_name = user_info.get("first_name")
        organizer_last_name = user_info.get("last_name")

        organizer_name = organizer_first_name + " " + organizer_last_name
        name = data['name']
        description = data['description']
        short_description = data['short_description']
        location = data['location']
        start_time = data['start_time']
        end_time = data['end_time']
        category = data['category']
        image_url = data['image_url']
        capacity = data['capacity']
        tags = data['tags']
        is_public = data['is_public']
        is_virtual = data['is_virtual']
        is_recurring = data['is_recurring']
        is_free = data['is_free']
        fee = data['fee']
        virtual_meeting_link = data['virtual_meeting_link']
        status = data['status']

        event = Event()
        event.name = name
        event.description = description
        event.short_description = short_description
        event.organizer_id = organizer_id
        event.location = location
        event.start_time = start_time
        event.end_time = end_time
        event.category = category
        event.image_url = image_url
        event.capacity = capacity
        event.tags = tags
        event.is_public =is_public
        event.is_virtual = is_virtual
        event.is_recurring = is_recurring
        event.is_free = is_free
        event.fee = fee
        event.virtual_meeting_link = virtual_meeting_link
        event.status = status

        db.session.add(event)
        db.session.commit()

        return jsonify(
            {
                'message': "successful",
                'result': event.to_json_with_organizer(organizer_name),
                'status_code': 201
            }
        )
    
    except Exception as e:
        db.session.rollback()
        return jsonify (
            {
                'error': str(e),
                'status_code': 400
            }
        )


@event_blueprint.route("/edit/<uuid:event_id>", methods=["PUT"])
def edit_event(event_id):
    try:
        user_email = request.headers.get('x-user-email')
        auth_header = request.headers.get("Authorization")
        token = auth_header.replace("Bearer ", "")

        data = request.get_json()
        event:Event = Event.query.get(event_id)

        if not event:
            return jsonify(
                {
                    "error": "Event does not exist"
                }
            ), 404
        
        if not data:
            return jsonify(
                {
                    "error": "Invalid or missing data"
                }
            ), 400
        
        if not user_email or not auth_header:
            return jsonify(
                {
                    "error": "Unauthorized - Missing headers"        
                }
            ), 401
        
        
        user_info = get_user_by_email(user_email, token)
        organizer_id = user_info.get("user_id")

        if organizer_id != event.organizer_id:
            return jsonify(
                {
                    'error': "This user does not have permission to update this event"
                }
            )

        organizer_first_name = user_info.get("first_name")
        organizer_last_name = user_info.get("last_name")
        organizer_name = organizer_first_name + " " + organizer_last_name

        event.name = data.get("name", event.name)
        event.description = data.get("description", event.description)
        event.short_description = data.get("short_description", event.short_description)
        event.location = data.get("location", event.location)
        event.start_time = data.get("start_time", event.start_time)
        event.end_time = data.get("end_time", event.end_time)
        event.category = data.get("category", event.category)
        event.image_url = data.get("image_url", event.image_url)
        event.capacity = data.get("capacity", event.capacity)
        event.tags = data.get("tags", event.tags)
        event.is_public = data.get("is_public", event.is_public)
        event.is_virtual = data.get("is_virtual", event.is_virtual)
        event.is_recurring = data.get("is_recurring", event.is_recurring)
        event.is_free = data.get("is_free", event.is_free)
        event.fee = data.get("fee", event.fee)
        event.virtual_meeting_link = data.get("virtual_meeting_link", event.virtual_meeting_link)
        event.status = data.get("status", event.status)


        db.session.commit()

        return jsonify(
            {
                'message': "successful",
                'result': event.to_json_with_organizer(organizer_name),
                'status_code': 210
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify (
            {
                'error': str(e),
                'status_code': 400
            }
        )


