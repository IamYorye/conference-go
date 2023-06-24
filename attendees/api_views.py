from django.http import JsonResponse
from .models import Attendee
from common.json import ModelEncoder, DateEncoder, QuerySetEncoder
from events.api_views import ConferenceListEnconder
from django.views.decorators.http import require_http_methods
import json
from events.models import Conference
from attendees.models import Attendee

class AttendeesListEncoder(ModelEncoder, QuerySetEncoder):
    model = Attendee
    properties = ["name"]

@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_id):
    if request.method == "GET":
        attendee = Attendee.objects.filter(conference = conference_id)
        return JsonResponse(
            {"attendees": attendee},
            encoder=AttendeesListEncoder,
            safe=False
            )
    else:
        content = json.loads(request.body)
        try:
            conference = Conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )
        attendee = Attendee.objects.create(**content)
        return JsonResponse(
            {"attendees": attendee},
            encoder=AttendeesListEncoder,
            safe=False
            )

class AttendeeShowEncoder(ModelEncoder, DateEncoder, QuerySetEncoder):
    model = Attendee
    properties = [
        "email",
        "name",
        "company_name",
        "created",
        "conference",
    ]
    encoders = {
    "conference": ConferenceListEnconder(),
    }

@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_attendee(request, id):
    if request.method == "GET":
        attendee = Attendee.objects.get(id=id)
        return JsonResponse(
            attendee,
            encoder=AttendeeShowEncoder,
            safe=False
    )
    elif request.method == "DELETE":
        count, _ = Attendee.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0 })
    else:
        content = json.loads(request.body)
        try:
            if "conference" in content:
                conference = Conference.objects.get(id=content["conference"])
                content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )
        Attendee.objects.filter(id=id).update(**content)
        attendee = Attendee.objects.get(id=id)
        return JsonResponse(
        attendee,
        encoder=AttendeeShowEncoder,
        safe=False
        )
