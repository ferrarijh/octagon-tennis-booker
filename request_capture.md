Last update: Apr 7, 2026

### ConflictCheck

Check conflict request:
```
POST https://rioc.civicpermits.com/Permits/ConflictCheck
```
```json
{
  "FacilityNames": [
    "Tennis Courts"
  ],
  "FacilityIds": [
    "036dfea4-c487-47b0-b7fe-c9cbe52b7c98"
  ],
  "Dates": [
    {
      "Start": "2026-04-09T12:00:00",
      "Stop": "2026-04-09T13:00:00"
    }
  ]
}
```

Check conflict response - no conflict:
```
200 OK

[]
```

Check conflict response - conflict exists:
```
200 OK

[0]
```

### Permits

Request permit
```
POST https://rioc.civicpermits.com/Permits
```
```json
{
  "Activity": "tennis",
  "Events": [
    {
      "FacilityNames": [
        "Tennis Courts"
      ],
      "FacilityIds": [
        "036dfea4-c487-47b0-b7fe-c9cbe52b7c98"
      ],
      "Dates": [
        {
          "Start": "2026-04-09T12:00:00",
          "Stop": "2026-04-09T13:00:00"
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
      "StringValue": "2",
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
      "StringValue": "Yes",
      "CheckboxValue": [
        "Yes"
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
      "StringValue": "No",
      "CheckboxValue": [
        "No"
      ]
    },
    {
      "Id": "a31f4297075e4dab8c0ef154f2b9b1c1",
      "StringValue": "",
      "CheckboxValue": []
    }
  ]
}
```