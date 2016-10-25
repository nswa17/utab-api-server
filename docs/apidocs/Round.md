# Round

[/v1.0/{tournament_name}/{round_num}]

### Get Round Information [GET]

+ Response 200 (application/json)
```
{
    "errors":null
    "data":
    {
        "current_round": 1,
        "status": 0,
        "constants":
        [
            {
                "random_pairing":4,
                "des_power_pairing":1,
                "des_w_o_same_a_insti":2,
                "des_w_o_same_b_insti":0,
                "des_w_o_same_c_insti":0,
                "des_with_fair_sides":1 /*property (int): preference(1 = most preferred)*/
            }
        ],
        "constants_of_adj":
        [
            {
                "random_allocation":4,
                "des_strong_strong":2,
                "des_with_fair_sides":3,
                "des_avoiding_conflicts":1,
                "des_avoiding_past":0,
                "des_priori_bubble":0,
                "des_chair_rotation":0
            }
        ]
    },
    "resource_url": ""
}
```
### Send Round Config [PUT]

+ Request (application/json)
```
{
    "constants": (defined above),
    "constants_of_adj": (defined above)
}
```
+ Response 200 (application/json)
```
{
    "errors": null,
    "data": same as above,
    "resource_url":""
}
```
### Finish Current Round [POST]

+ Request (application/json)
```
{
    "args": {"force": false},
    "data":
    {
        "current_round": 1
    }
}
```
+ Response 200 (application/json)
```
{
    "errors": [],
    "data":
    {
        "current_round": 1
    },
    "resource_url": ""
]
```