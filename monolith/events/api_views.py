from django.http import JsonResponse
from .models import Conference, Location
from common.json import ModelEncoder, DateEncoder, QuerySetEncoder
from django.views.decorators.http import require_http_methods
import json
from events.models import State
from .acls import get_photo, get_weather_data


class ConferenceListEnconder(ModelEncoder, QuerySetEncoder):
    model = Conference
    properties = ["name"]

@require_http_methods(["GET", "POST"])
def api_list_conferences(request):
    if request.method == "GET":
        conferences = Conference.objects.all()
        return JsonResponse(
            {"conferences": conferences},
            encoder=ConferenceListEnconder
        )
    else:
        content = json.loads(request.body)
        try:
            location = Location.objects.get(id=content["location"])
            content["location"] = location
        except Location.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid location id"},
                status=400,
            )
        conferences = Conference.objects.create(**content)
        return JsonResponse(
            conferences,
            encoder=ConferenceDetailEncoder,
            safe=False
        )

class LocationListEncoder(ModelEncoder):
    model = Location
    properties = [
        "name",
        ]

class ConferenceDetailEncoder(DateEncoder, ModelEncoder):
    model = Conference
    properties = [
        "name",
        "description",
        "max_presentations",
        "max_attendees",
        "starts",
        "ends",
        "created",
        "updated",
        "location",
    ]
    encoders = {
        "location": LocationListEncoder(),
    }

@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_conference(request, id):
    if request.method == "GET":
        conference = Conference.objects.get(id=id)
        weather = get_weather_data(conference.location.city, conference.location.state.abbreviation)
        return JsonResponse(
            {"conference": conference, "weather": weather},
            encoder=ConferenceDetailEncoder,
            safe=False
        )
    elif request.method == "DELETE":
        count, _ = Conference.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0 })
    else:
        content = json.loads(request.body)

        try:
            location = Location.objects.get(id=content["location"])
            content["location"] = location
        except Location.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid location id"},
                status=400,
            )


        Conference.objects.filter(id=id).update(**content)
        conference = Conference.objects.get(id=id)
        return JsonResponse(
            conference,
            encoder=ConferenceDetailEncoder,
            safe=False
        )


class ListLocationEncoder(ModelEncoder, QuerySetEncoder):
    model = Location
    properties = [
        "name",
        ]

@require_http_methods(["GET", "POST"])
def api_list_locations(request):
    if request.method == "GET":
        all_locations = Location.objects.all()
        return JsonResponse(
            {"location": all_locations},
            encoder=ListLocationEncoder,
            safe=False
        )
    else:
        content = json.loads(request.body)

        try:
            state = State.objects.get(abbreviation=content["state"])
            content["state"] = state
        except State.DoesNotExist:
            return JsonResponse(
                {"message:" "Invalid state abbreviation"},
                status=400,
            )

        picture_url = get_photo(content["city"], content["state"].abbreviation)
        content.update(picture_url)

        all_locations = Location.objects.create(**content)
        return JsonResponse(
            {"location": all_locations},
            encoder=LocationDetailEncoder,
            safe=False
        )

class LocationDetailEncoder(ModelEncoder, DateEncoder):
    model = Location
    properties = [
        "name",
        "city",
        "room_count",
        "created",
        "updated",
        "picture_url",
    ]

    def get_extra_data(self, o):
        return { "state": o.state.abbreviation }

@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_location(request, id):
    if request.method == "GET":
        location = Location.objects.get(id=id)
        return JsonResponse(
            location,
            encoder=LocationDetailEncoder,
            safe=False
        )
    elif request.method == "DELETE":
        count, _ = Location.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0 })
    else:
        content = json.loads(request.body)
        try:
            state = State.objects.get(abbreviation=content["state"])
            content["state"] = state
        except State.DoesNotExist:
            return JsonResponse(
                {"message:" "Invalid state abbreviation"},
                status=400,
            )
        Location.objects.filter(id=id).update(**content)
        location = Location.objects.get(id=id)
        return JsonResponse(
            location,
            encoder = LocationDetailEncoder,
            safe=False
        )
