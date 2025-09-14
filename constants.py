SESSION_COOKIE_NAME = ".ASPXAUTH"
COURTS = {
    "court1": "036dfea4-c487-47b0-b7fe-c9cbe52b7c98",
    "court2": "175bdff8-016e-46ab-a9df-829fe40c0754",
    "court3": "9bdef00b-afa0-4b6b-bf9a-75899f7f97c7",
    "court4": "d311851d-ce53-49fc-9662-42adcda26109",
    "court5": "8a5ca8e8-3be0-4145-a4ef-91a69671295b",
    "court6": "77c7f42c-8891-4818-a610-d5c1027c62fe"
}
LOGIN_URL = "https://rioc.civicpermits.com/Account/Login"
CHECK_AVAIL_URL = "https://rioc.civicpermits.com/Permits/ConflictCheck"
EMAIL_DEFAULT = "ferrarijm9@gmail.com"
PERMIT_REQUEST_URL = "https://rioc.civicpermits.com/Permits"

"""
sample permit request body (json):

{
  "Activity": "tennis",
  "Events": [
    {
      "FacilityNames": [
        "Tennis Courts"
      ],
      "FacilityIds": [
        "77c7f42c-8891-4818-a610-d5c1027c62fe"
      ],
      "Dates": [
        {
          "Start": "2025-09-15T12:00:00",
          "Stop": "2025-09-15T13:00:00"
        }
      ]
    }
  ],
  "Responses": [
    {
      "Id": "11e79e5d3daf4712b9e6418d2691b976",
      "StringValue": "tennis doubles match",
      "CheckboxValue": []
    },
    {
      "Id": "af8966101be44676b4ee564b052e1e87",
      "StringValue": "4",
      "CheckboxValue": []
    },
    {
      "Id": "f28f0dbea8b5438495778b0bb0ddcd93",
      "StringValue": "no",
      "CheckboxValue": []
    },
    {
      "Id": "d46cb434558845fb9e0318ab6832e427",
      "StringValue": "no",
      "CheckboxValue": []
    },
    {
      "Id": "1221940f5cca4abdb5288cfcbe284820",
      "StringValue": "",
      "CheckboxValue": []
    },
    {
      "Id": "3754dcef7216446b9cc4bf1cd0f12a2e",
      "StringValue": "",
      "CheckboxValue": [
        ""
      ]
    },
    {
      "Id": "0ce54956c4b14746ae5d364507da1e85",
      "StringValue": "",
      "CheckboxValue": []
    },
    {
      "Id": "6b1dda4172f840c7879662bcab1819db",
      "StringValue": "",
      "CheckboxValue": []
    },
    {
      "Id": "06b3f73192a84fd6b88758e56a64c3ad",
      "StringValue": "",
      "CheckboxValue": [
        ""
      ]
    },
    {
      "Id": "a31f4297075e4dab8c0ef154f2b9b1c1",
      "StringValue": "",
      "CheckboxValue": []
    }
  ]
}
"""

from enum import Enum

class ReservationResponse(Enum):
    ACTIVITY_DESCRIPTION = (
        "What activity will be taking place? Please be specific.",
        "11e79e5d3daf4712b9e6418d2691b976",
    )
    PARTICIPANT_COUNT = (
        "How many people are expected to take part in the requested activity?",
        "af8966101be44676b4ee564b052e1e87",
    )
    PARTICIPANT_CHARGE = (
        "Are participants charged? If YES, how much is each participant charged?",
        "f28f0dbea8b5438495778b0bb0ddcd93",
    )
    SPECTATOR_CHARGE = (
        "Are spectators charged? If YES, how much is each spectator charged?",
        "d46cb434558845fb9e0318ab6832e427",
    )
    TABLE_PACKAGE = (
        "Table/Chair for Indoor Events Package A: 12 tables / 25 Chairs or Package B: 24 tables / 50 Chairs",
        "1221940f5cca4abdb5288cfcbe284820",
    )
    PREVIOUS_PERMIT = (
        "Have you had a permit on Roosevelt Island for this request before?",
        "3754dcef7216446b9cc4bf1cd0f12a2e",
    )
    LIVE_ENTERTAINMENT = (
        "Will there be live entertainment/amplified sound? If YES, please explain.",
        "0ce54956c4b14746ae5d364507da1e85",
    )
    ADVERTISEMENT = (
        "Will the event be advertised? If YES, please explain.",
        "6b1dda4172f840c7879662bcab1819db",
    )
    ONSITE_SECURITY = (
        "Will there be on site security?",
        "06b3f73192a84fd6b88758e56a64c3ad",
    )
    PARKING_NEEDS = (
        "Please describe parking needs. Be sure to include number and type(s) of vehicles.",
        "a31f4297075e4dab8c0ef154f2b9b1c1",
    )

    def __init__(self, description: str, field_id: str):
        self.description = description
        self.field_id = field_id

RESPONSES_DEFAULT = [
    {
        "Id": ReservationResponse.ACTIVITY_DESCRIPTION.field_id,
        "StringValue": "tennis doubles match",
        "CheckboxValue": []
    },
    {
        "Id": ReservationResponse.PARTICIPANT_COUNT.field_id,
        "StringValue": "4",
        "CheckboxValue": []
    },
    {
        "Id": ReservationResponse.PARTICIPANT_CHARGE.field_id,
        "StringValue": "no",
        "CheckboxValue": []
    },
    {
        "Id": ReservationResponse.SPECTATOR_CHARGE.field_id,
        "StringValue": "no",
        "CheckboxValue": []
    },
    {
        "Id": ReservationResponse.TABLE_PACKAGE.field_id,
        "StringValue": "",
        "CheckboxValue": []
    },
    {
        "Id": ReservationResponse.PREVIOUS_PERMIT.field_id,
        "StringValue": "",
        "CheckboxValue": [
            ""
        ]
    },
    {
        "Id": ReservationResponse.LIVE_ENTERTAINMENT.field_id,
        "StringValue": "",
        "CheckboxValue": []
    },
    {
        "Id": ReservationResponse.ADVERTISEMENT.field_id,
        "StringValue": "",
        "CheckboxValue": []
    },
    {
        "Id": ReservationResponse.ONSITE_SECURITY.field_id,
        "StringValue": "",
        "CheckboxValue": [
            ""
        ]
    },
    {
        "Id": ReservationResponse.PARKING_NEEDS.field_id,
        "StringValue": "",
        "CheckboxValue": []
    }
]

PERMIT_REQUEST_BODY_TEMPLATE = {
    "Activity": "tennis",
    "Events": [
        {
            "FacilityNames": [
                "Tennis Courts"
            ],
            "FacilityIds": [
                # court_id to be filled in here #
            ],
            "Dates": [
                {
                    "Start": "", # "yyyy-MM-ddTHH:00:00"
                    "Stop": "" # 1h after start, same format
                }
            ]
        }
    ],
    "Responses": RESPONSES_DEFAULT
}