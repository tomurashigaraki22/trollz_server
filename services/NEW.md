Create Address
Create an address for getting rates or arranging pickup and delivery.

/addresses
POST https://api.terminal.africa/v1/addresses

This endpoint allows you to add a new address to your account.

Headers
Name
Type
Description
Authorization*

String

Set value to Bearer SECRET_KEY

Content-Type

String

Set value to application/json

Request Body
Name
Type
Description
city*

String

Address city.

country*

String

ISO 2 country code for address.

email

String

Email of person at address.

first_name

String

First name of person at address. Required for arranging pickup / delivery.

is_residential

Boolean

Indicates if address is a residential address or not. Defaults to true.

last_name

String

Last name of person at address. Required for arranging pickup / delivery.

line1

String

Street address. Required for arranging pickup / delivery.

line2

String

Second line of street address.

metadata

Object

Additional information for an address. 

name

String

Full name of person at address.

phone

String

Phone number of person at address. Required for arranging pickup / delivery.

state*

String

Address state

zip

String

Zip / Postal code. Required for arranging pickup / delivery.

200 Address created successfully.

Copy
{
	status: true,
	message: 'Address created successfully',
	data: {
		address_id: 'AD-00632494667',	
		city: 'Lagos',
		coordinates: {
				lat: 6.5969424,
				lng: 3.3542992
		},	
		country: 'NG',
		email: 'augustus_obi@shipmonk.ng',
		first_name: 'Augustus',
		is_residential: true,
		last_name: 'Obi',
		line1: '1121 Allen Avenue, Ikeja',
		line2: '',
		metadata: {
			my_app_customer_id: 11234
		},
		name: 'Augustus Obi',
		phone: '+2348122340000',
		state: 'Lagos',
		zip: '121006',
		created_at: '2021-07-13T20:25:53.011Z',
		updated_at: '2021-07-13T20:25:53.011Z'
	}
}


Get Addresses
Fetch list of addresses available for a user.

/addresses
GET https://api.terminal.africa/v1/addresses

This endpoint allows you to get a list of all addresses available.

Query Parameters
Name
Type
Description
perPage

Number

Specify how many records will be sent in a single response. Defaults to 100.

page

Number

Specify what page of records will be sent in response. Defaults to 1.

Headers
Name
Type
Description
Authorization*

String

Set value to Bearer SECRET_KEY

200 Addresses retrieved successfully.

Copy
{
    "status": true,
    "message": "Addresses retrieved successfully",
    "data": {
        "addresses": [
            {
                "address_id": "AD-00632494667",
                "city": "Lagos",
                "coordinates": {
                    "lat": 6.5969424,
                    "lng": 3.3542992
                },
                "country": "NGA",
                "email": "augustus_obi@shipmonk.ng",
                "first_name": "Augustus",
                "id": "d799c2679e644279b59fe661ac8fa488",
                "is_residential": true,
                "last_name": "Obi",
                "line1": "1121 Allen Avenue, Ikeja",
                "line2": "",
                "metadata": {
                    "my_app_customer_id": 11234
                },
                "name": "Augustus Obi",
                "phone": "+2348122340000",
                "state": "Lagos",
                "zip": "121006",
                "created_at": "2021-07-13T20:25:53.011Z",
                "updated_at": "2021-07-13T20:25:53.011Z"
            }],
        "pagination": {
            "perPage": 100,
            "prevPage": null,
            "nextPage": 2,
            "currentPage": 1,
            "total": 3,
            "pageCount": 3,
            "pagingCounter": 1,
            "hasPrevPage": false,
            "hasNextPage": true	
        }
    }
}
Previous
Create Address
Next
Get Address
Last updated 3 years ago

Get Address
Fetch details of a specific address.

/addresses/:address_id
GET https://api.terminal.africa/v1/addresses/:address_id

This endpoint allows you to retrieve the details of a specific address.

Path Parameters
Name
Type
Description
address_id*

string

Unique address_id of the address.

Headers
Name
Type
Description
Authorization*

string

Set value to Bearer SECRET_KEY

200 Address retrieved successfully.

Copy
{
	status: true,
	message: 'Address retrieved successfully',
	data: {
		address_id: 'AD-00632494667',	
		city: 'Lagos',
		coordinates: {
				lat: 6.5969424,
				lng: 3.3542992
		},	
		country: 'NGA',
		email: 'augustus_obi@shipmonk.ng',
		first_name: 'Augustus',
		id: 'd799c2679e644279b59fe661ac8fa488',
		is_residential: true,
		last_name: 'Obi',
		line1: '1121 Allen Avenue, Ikeja',
		line2: '',
		metadata: {
			my_app_customer_id: 11234
		},
		name: 'Augustus Obi',
		phone: '+2348122340000',
		state: 'Lagos',
		zip: '121006',
		created_at: '2021-07-13T20:25:53.011Z',
		updated_at: '2021-07-13T20:25:53.011Z'
	}
}
Previous
Get Addresses
Next
Get Default Address
Last updated 3 years ago

Update Address
Update information for an existing address.

/addresses/:address_id
PUT https://api.terminal.africa/v1/addresses/:address_id

This endpoint allows you to update an existing address.

Path Parameters
Name
Type
Description
address_id*

String

Unique identifier for address

Headers
Name
Type
Description
Authorization*

String

Set value to Bearer SECRET_KEY

Content-Type

String

Set value to application/json

Request Body
Name
Type
Description
city*

String

Address city.

country*

String

ISO 2 country code for address.

email

String

Email of person at address.

first_name

String

First name of person at address. Required for arranging pickup / delivery.

is_residential

Boolean

Indicates if address is a residential address or not. Defaults to true.

last_name

String

Last name of person at address. Required for arranging pickup / delivery.

line1

String

Street address. Required for arranging pickup / delivery.

line2

String

Second line of street address

metadata

Object

Additional information for an address. 

name

String

Full name of person at address

phone

String

Phone number of person at address. Must match country provided in address. Required for arranging pickup / delivery.

state

String

Address state

zip

String

Zip / Postal code. Required for arranging pickup / delivery.

200: OK Address updated successfully.

Copy
{
	status: true,
	message: 'Address updated successfully',
	data: {
		city: 'Lagos',
		coordinates: { lat: 6.5969424, lng: 3.3542992 },
		country: 'NG',
		email: 'augustus_obi@shipmonk.ng',
		first_name: 'Augustus',
		is_residential: true,
		last_name: 'Obi',
		line1: '1121 Allen Avenue, Ikeja',
		line2: '',
		metadata: {
			my_app_customer_id: 11234
		},		
		phone: '+2348122340000',
		state: 'Lagos',
		zip: '121006',
		address_id: 'AD-00632494667',
		created_at: 2022-05-23T00:00:01.223Z,
		updated_at: 2022-05-23T00:00:01.223Z,
	}
}
Previous
Set Default Address
Next
Validate Address
Last updated 1 year ago


Validate Address
Validate details for an address

/addresses/validate
POST https://api.terminal.africa/v1/addresses/validate

This endpoint allows you to validate the details of any global address. For list of accepted countries check (Validation Countries). Also see API Pricing for usage fees.

Headers
Name
Type
Description
Authorization*

String

Set value to Bearer SECRET_KEY

Content-Type

String

Set value to application/json

Request Body
Name
Type
Description
city*

String

Address city.

country*

String

ISO 2 country code for address. Must be one of the addresses available here.

line1*

String

Street address. Required for arranging pickup / delivery.

line2

String

Second line of street address.

state*

String

State of street address.

zip*

String

Zip / Postal code. Required for arranging pickup / delivery.

200: OK Address validated successfully

Copy
{
    "status": true,
    "message": "Address validated successfully",
    "data": {
        "is_valid": true,
        "original_address": {
            "city": "London",
            "state": "London",
            "country": "GB",
            "email": "claudettearnold@hotmail.co.uk",
            "first_name": "Claudette",
            "is_residential": true,
            "last_name": "Arnold",
            "line1": "43 northumberland park",
            "line2": "",
            "phone": "+44 7908908329",
            "zip": "N17 OTB",
            "user": "USER-27450202164"
        },
        "validation_results": {
            "country_valid": true,
            "city_valid": true,
            "state_valid": true,
            "address_valid": true,
            "zip_valid": true
        },
        "validation_messages": [
            {
                "code": "POSTAL_MISMATCH",
                "field": "postalCode",
                "severity": "warning",
                "message": "The postal code was corrected.",
                "meta": {
                    "inputPostal": "N17 OTB",
                    "updatedPostal": "N17 0TB"
                }
            }
        ],
        "suggestion_provided": true,
        "suggested_address": {
            "line1": "43 northumberland park",
            "city": "London",
            "zip": "N17 OTB",
            "country": "GB"
        }
    }
}
Previous
Update Address
Next
Carriers
Last updated 5 months ago




Carriers
The Carriers API allows you to manage information on available carriers for your account.

The Carrier Object
This section describes the different attributes available for a carrier.

Attribute

Type

Description

active

boolean

Indicates if carrier is active for an account.

available_countries

array

List of user countries carrier is available in.

carrier_id

string

Unique reference for carrier.

contact

object

Contact information for carrier.

domestic

boolean

Indicates if the carrier is available for intracity / intrastate delivery.

logo

string

URL image of carrier logo.

international

boolean

Indicates if the carrier is available for international delivery.

metadata

object

Provide additional information for a carrier.

name

string

Name of carrier.

regional

boolean

Indicates if the carrier is available for inter-city / inter-state delivery.

requires_invoice

boolean

Indicates if printout of commercial invoice is required for pickup.

requires_waybill

boolean

Indicates if printout of waybill is required for pickup.

slug

string

Unique slug to identify carrier.

supports_multi_parcels

boolean

Indicates if carrier supports multiple parcel shipments.

created_at

datetime

Time carrier created

updated_at

datetime

Time carrier last updated

Previous
Validate Address
Next
Get CarriersGet Carriers
Fetch list of all carriers available on TShip API.

/carriers
GET https://api.terminal.africa/v1/carriers

This endpoint allows you to get a list of carriers available on TShip.

Query Parameters
Name
Type
Description
active

Boolean

If true, only active carriers on the shipmonk platform will be returned. If set to false, only inactive carriers will be returned. If blank, all available carriers will be returned.

type

String

Specify the type of carrier. Available options are domestic, regional or international.

perPage

Number

Specify how many records will be included in a single response. Defaults to 100.

page

Number

Specify what page of records will be sent in response. Defaults to 1.

Headers
Name
Type
Description
Authorization*

String

Set value to Bearer SECRET_KEY

Content-Type

String

Set value to application/json

200 Carriers retrieved successfully.

Copy
{
    "status": true,
    "message": "Carriers retrieved successfully",
    "data": {
        "carriers": [
            {
                "active": true,
                "available_countries": [
                    "GH",
                    "KE",
                    "NG",
                    "SA",
                    "UG",
                    "GB",
                    "US"
                ],
                "contact": {
                    "email": "nginquiry@dhl.com",
                    "phone": "012700908"
                },
                "domestic": true,
                "international": true,
                "logo": "https://ucarecdn.com/dcdd8109-af8c-4057-8104-192be821dd6e/download4.png",
                "name": "DHL Express",
                "regional": true,
                "requires_invoice": true,
                "requires_waybill": true,
                "slug": "dhl-ng",
                "carrier_id": "CA-81957188177",
                "__v": 0,
                "created_at": "2022-06-04T01:37:40.930Z",
                "updated_at": "2022-06-04T01:37:40.930Z"
            },
            {
                "active": false,
                "available_countries": [
                    "NG"
                ],
                "contact": {
                    "email": "info@darum.com.ng",
                    "phone": "+2349131288529"
                },
                "domestic": true,
                "international": false,
                "logo": "https://ucarecdn.com/c9e79717-96c4-44e3-92b1-aff58f23475f/download.png",
                "name": "Darum",
                "regional": false,
                "requires_invoice": false,
                "requires_waybill": false,
                "slug": "darum",
                "carrier_id": "CA-58583827047",
                "__v": 0,
                "created_at": "2022-06-04T01:37:40.930Z",
                "updated_at": "2022-06-04T01:37:40.930Z"
            },
            {
                "active": false,
                "available_countries": [
                    "NG"
                ],
                "contact": {
                    "email": "hello@errand360.ng",
                    "phone": "+234012299989"
                },
                "domestic": true,
                "international": false,
                "logo": "https://ucarecdn.com/cea51824-153b-4738-a6d4-9e7b5a8375d5/Errand360logocoloured.png",
                "name": "Errand360",
                "regional": false,
                "requires_invoice": false,
                "requires_waybill": false,
                "slug": "errand360",
                "carrier_id": "CA-20216731467",
                "__v": 0,
                "created_at": "2022-06-04T01:37:40.930Z",
                "updated_at": "2022-06-04T01:37:40.930Z"
            },
            {
                "active": true,
                "available_countries": [
                    "NG"
                ],
                "contact": {
                    "email": "e-tailing@redstarplc.com",
                    "phone": "017215670"
                },
                "domestic": true,
                "international": false,
                "logo": "https://ucarecdn.com/375a5012-2691-40c2-b147-149f0e134d8d/purepngcomfedexlogologobrandlogoiconslogos251519939539h7rji.png",
                "name": "Fedex (Red Star Express)",
                "regional": true,
                "requires_invoice": true,
                "requires_waybill": true,
                "slug": "fedex",
                "carrier_id": "CA-31377601348",
                "__v": 0,
                "created_at": "2022-06-04T01:37:40.930Z",
                "updated_at": "2022-06-04T01:37:40.930Z"
            },
            {
                "active": true,
                "available_countries": [
                    "NG"
                ],
                "contact": {
                    "email": "info@giglogistics.com",
                    "phone": "+2348139851120"
                },
                "domestic": true,
                "international": false,
                "logo": "https://ucarecdn.com/3045d9f6-5417-465b-a8cf-3ebbaf540bcf/download.png",
                "name": "GIG Logistics",
                "regional": true,
                "requires_invoice": false,
                "requires_waybill": false,
                "slug": "gigl",
                "carrier_id": "CA-71017347351",
                "__v": 0,
                "created_at": "2022-06-04T01:37:40.930Z",
                "updated_at": "2022-06-04T01:37:40.930Z"
            },
            {
                "active": false,
                "available_countries": [
                    "NG"
                ],
                "contact": {
                    "email": "support@gokada.ng",
                    "phone": "+2347067343882"
                },
                "domestic": true,
                "international": false,
                "logo": "https://ucarecdn.com/e7b4b7da-2ba2-4cb0-82bd-cc1c3c61b48a/60352f431157c33dde33a6e3_Gokada_logo.png",
                "name": "Gokada",
                "regional": false,
                "requires_invoice": false,
                "requires_waybill": false,
                "slug": "gokada",
                "carrier_id": "CA-07032569055",
                "__v": 0,
                "created_at": "2022-06-04T01:37:40.930Z",
                "updated_at": "2022-06-04T01:37:40.930Z"
            },
            {
                "active": true,
                "available_countries": [
                    "NG"
                ],
                "contact": {
                    "email": "support@kwik.delivery",
                    "phone": "013438198"
                },
                "domestic": true,
                "international": false,
                "logo": "https://ucarecdn.com/d399a2ad-c831-46de-a8fe-94f8056a3c29/60dc787ac0166774ecb59f04_gy2h4u35onr2nrmuapjt.png",
                "name": "Kwik Delivery",
                "regional": false,
                "requires_invoice": false,
                "requires_waybill": false,
                "slug": "kwik",
                "carrier_id": "CA-18228854618",
                "__v": 0,
                "created_at": "2022-06-04T01:37:40.931Z",
                "updated_at": "2022-06-04T01:37:40.931Z"
            },
            {
                "active": true,
                "available_countries": [
                    "GH",
                    "NG"
                ],
                "contact": {
                    "email": "support@sendbox.ng",
                    "phone": "017006150"
                },
                "domestic": true,
                "international": true,
                "logo": "https://ucarecdn.com/3273a236-bd33-4c37-9f87-2bcf4e59275f/6035307b31150075cabc780d_EeNJnpVz_400x400.jpg",
                "name": "Sendbox",
                "regional": true,
                "requires_invoice": false,
                "requires_waybill": false,
                "slug": "sendbox",
                "carrier_id": "CA-85479996273",
                "__v": 0,
                "created_at": "2022-06-04T01:37:40.931Z",
                "updated_at": "2022-06-04T01:37:40.931Z"
            },
            {
                "active": true,
                "available_countries": [
                    "NG"
                ],
                "contact": {
                    "email": "",
                    "phone": ""
                },
                "domestic": true,
                "international": false,
                "logo": "https://ucarecdn.com/f2904861-edb2-4ec7-b3c0-a01a9a3029f4/1649168596524.jpeg",
                "name": "Sendstack",
                "regional": false,
                "requires_invoice": false,
                "requires_waybill": false,
                "slug": "sendstack",
                "carrier_id": "CA-86012707216",
                "__v": 0,
                "created_at": "2022-06-04T01:37:40.931Z",
                "updated_at": "2022-06-04T01:37:40.931Z"
            },
            {
                "active": true,
                "available_countries": [
                    "NG"
                ],
                "contact": {
                    "email": "hello@topship.africa",
                    "phone": "+2349080777728"
                },
                "domestic": true,
                "international": true,
                "logo": "https://ucarecdn.com/7fa80800-1325-4f3f-8782-ed2fe45f4ab3/1643276093908.jpeg",
                "name": "Topship",
                "regional": true,
                "requires_invoice": false,
                "requires_waybill": false,
                "slug": "topship",
                "carrier_id": "CA-49411197653",
                "__v": 0,
                "created_at": "2022-06-04T01:37:40.931Z",
                "updated_at": "2022-06-04T01:37:40.931Z"
            },
            {
                "active": true,
                "available_countries": [
                    "NG"
                ],
                "contact": {
                    "email": "support@terminal.africa",
                    "phone": "+2349161154291"
                },
                "domestic": true,
                "international": false,
                "logo": "https://ucarecdn.com/b948ff34-7caa-4c2c-b10a-fb966ed83263/tQxVwcJSowYD7xwWDYidd9.jpeg",
                "name": "Uber",
                "regional": false,
                "requires_invoice": false,
                "requires_waybill": false,
                "slug": "uber",
                "carrier_id": "CA-01091597938",
                "__v": 0,
                "created_at": "2022-06-04T01:37:40.932Z",
                "updated_at": "2022-06-04T01:37:40.932Z"
            },
            {
                "active": false,
                "available_countries": [
                    "NG"
                ],
                "contact": {
                    "email": "",
                    "phone": ""
                },
                "domestic": true,
                "international": true,
                "logo": "https://ucarecdn.com/c2d4dcb2-1483-47a5-ab14-447a990f5827/60dc7947195c0078fabff349_1200pxUnited_Parcel_Service_logo_2014svg.png",
                "name": "United Parcel Services",
                "regional": true,
                "requires_invoice": true,
                "requires_waybill": true,
                "slug": "ups",
                "carrier_id": "CA-19429970231",
                "__v": 0,
                "created_at": "2022-06-04T01:37:40.932Z",
                "updated_at": "2022-06-04T01:37:40.932Z"
            }
        ],
        "pagination": {
            "page": 1,
            "perPage": 100,
            "prevPage": null,
            "nextPage": null,
            "currentPage": 1,
            "total": 12,
            "pageCount": 1,
            "pagingCounter": 1,
            "hasPrevPage": false,
            "hasNextPage": false
        }
    }
}
Previous
Carriers
Next
Get Carrier
Last updated 5 months ag


Get Carrier
Fetch details of a specific carrier.

/carriers/:carrier_id
GET https://api.terminal.africa/v1/carriers/:carrier_id

This endpoint allows you to retrieve details of a specific carrier.

Path Parameters
Name
Type
Description
carrier_id*

string

Unique carrier_id for carrier.

Headers
Name
Type
Description
Authorization*

string

Set value to Bearer SECRET_KEY

Content-Type

string

Set value to application/json

200 Carrier retrieved successfully.

Copy
{
	status: true,
	message: 'Carrier retrieved successfully',
	data: {
		active: true,
		carrier_id: 'CA-01521075089',
		domestic: true,
		id: 'loYZh5J47D6gJUKOExXeO1RLcMARScLi',
		international: true,		
		logo: 'https://ucarecdn.com/dcdd8109-af8c-4057-8104-192be821dd6e/download4.png',
		metadata: {},
		name: 'DHL Express',
		created_at: '2021-07-13T20:25:53.011Z',
		updated_at: '2021-07-13T20:25:53.011Z'
	}
}
Previous
Get Carriers
Next
Enable Carrier
Last updated 5 months ago

Enable Carrier
Enable a specific carrier for a user.

/carriers/enable/:carrier_id
POST https://api.terminal.africa/v1/carriers/enable/:carrier_id

This endpoint allows you to enable a carrier. One of domestic, international or regional query parameters is required in request.

Path Parameters
Name
Type
Description
carrier_id*

string

Unique carrier_id for carrier.

Query Parameters
Name
Type
Description
domestic

boolean

Set to true to enable carrier for domestic rates and deliveries.

international

boolean

Set to true to enable carrier for international  rates and deliveries.

regional

boolean

Set to true to enable carrier for regional  rates and deliveries.

Headers
Name
Type
Description
Authorization*

string

Set value to Bearer SECRET_KEY

Content-Type

string

Set value to application/json

200 Carrier enabled successfully.

Copy
{
	status: true,
	message: 'Carrier enabled successfully',
	data: {
		active: true,
		carrier_id: 'CA-01521075089',
		domestic: true,
		id: 'loYZh5J47D6gJUKOExXeO1RLcMARScLi',
		international: true,		
		logo: 'https://ucarecdn.com/dcdd8109-af8c-4057-8104-192be821dd6e/download4.png',
		metadata: {},
		name: 'DHL Express',
		created_at: '2021-07-13T20:25:53.011Z',
		updated_at: '2021-07-13T20:25:53.011Z'
	}
}
Previous
Get Carrier
Next
Enable Multiple Carriers
Last updated 7 months ago


Enable Multiple Carriers
Enable multiple carriers for a user.

/v1/carriers/multiple/enable
POST https://api.terminal.africa/v1/carriers/multiple/enable

This endpoint allows you to enable multiple carriers in a single call.

Headers
Name
Type
Description
Authorization*

String

Set value to Bearer SECRET_KEY

Content-Type

String

Set value to application/json

Request Body
Name
Type
Description
carriers*

Object

List of Carrier Objects to be enabled.

200: OK Carriers Enabled Successfully.

Copy
{
    "status": true,
    "message": "Carriers Enabled Successfully",
    "data": {
        "domestic": [
            "CA-58583827047",
            "CA-86012707216",
            "CA-81957188177",
            "CA-31377601348",
            "CA-71017347351",
            "CA-18228854618",
            "CA-85479996273",
            "CA-49411197653",
            "CA-19429970231",
            "CA-39897596546"
        ],
        "international": [
            "CA-31377601348",
            "CA-81957188177",
            "CA-89391853795",
            "CA-85479996273",
            "CA-19429970231",
            "CA-49411197653",
            "CA-39897596546"
        ],
        "regional": [
            "CA-18228854618",
            "CA-86012707216",
            "CA-31377601348",
            "CA-81957188177",
            "CA-85479996273",
            "CA-71017347351",
            "CA-49411197653",
            "CA-19429970231",
            "CA-39897596546"
        ]
    }
}
Previous
Enable Carrier
Next
Disable Carrier
Last updated 3 years ago


Drop-off Locations
Fetch list of all carriers available on TShip API.

/carriers/locations/drop-off
GET https://api.terminal.africa/v1/carriers/locations/drop-off

This endpoint allows you to get a list of Drop-off locations.

Query Parameters
Name
Type
Description
country*

String

ISO-2 country code

state

String

Specify the state to which drop-off locations should be returned

city

String

Specify city to which drop-off locations should be returned

carrier*

String

Specify carrier for drop-off locations

Headers
Name
Type
Description
Authorization*

String

Set value to Bearer SECRET_KEY

Content-Type

String

Set value to application/json

200 List of drop-off locations

Copy
{
    "status": true,
    "message": "List of drop-off locations",
    "data": [
        {
            "_id": "6481ba1d1188097217dde7e5",
            "address": "Royal Bed Estate, 1 Afolabi Aina Street By New Alade Market",
            "carrier": "sendbox",
            "city": "Ikeja",
            "country": "NG",
            "email": "",
            "phone": "2349087792932",
            "state": "Lagos",
            "drop_off_location_id": "DO-3TWJFCNM2HM8TPJR",
            "__v": 0,
            "created_at": "2023-06-08T11:23:09.866Z",
            "updated_at": "2023-06-08T11:23:09.866Z",
            "id": "6481ba1d1188097217dde7e5"
        },
        {
            "_id": "6481ba1d1188097217dde7e6",
            "address": "41 Oritshe Street off Balogun Bus Stop, Awolowo, Ikeja",
            "carrier": "sendbox",
            "city": "Ikeja",
            "country": "NG",
            "email": "",
            "phone": "2349087792932",
            "state": "Lagos",
            "drop_off_location_id": "DO-47EQ7S8GVHTYUT5B",
            "__v": 0,
            "created_at": "2023-06-08T11:23:09.866Z",
            "updated_at": "2023-06-08T11:23:09.866Z",
            "id": "6481ba1d1188097217dde7e6"
        },
        {
            "_id": "6481ba1d1188097217dde7f4",
            "address": "Aramex logistics Center, Pilgrims and Cargo Terminal,MM1 Airport road, Ikeja-Lagos.",
            "carrier": "aramex",
            "city": "Ikeja",
            "country": "NG",
            "email": "",
            "phone": "",
            "state": "Lagos",
            "drop_off_location_id": "DO-COY31LL38XZEFFIM",
            "__v": 0,
            "created_at": "2023-06-08T11:23:09.866Z",
            "updated_at": "2023-06-08T11:23:09.866Z",
            "id": "6481ba1d1188097217dde7f4"
        },
        {
            "_id": "6481ba1d1188097217dde7fd",
            "address": "14, TOYIN STREET, IKEJA, LAGOS-STATE, IKEJA\n, LAGOS\nSTATE",
            "carrier": "ups",
            "city": "Ikeja",
            "country": "NG",
            "email": "",
            "phone": "",
            "state": "Lagos",
            "drop_off_location_id": "DO-BTVXER8CM6FSWSBB",
            "__v": 0,
            "created_at": "2023-06-08T11:23:09.867Z",
            "updated_at": "2023-06-08T11:23:09.867Z",
            "id": "6481ba1d1188097217dde7fd"
        },
        {
            "_id": "6481ba1d1188097217dde822",
            "address": "50/52 TOYIN SREET, IKEJA",
            "carrier": "fedex",
            "city": "Ikeja",
            "country": "NG",
            "email": "",
            "phone": "",
            "state": "Lagos",
            "drop_off_location_id": "DO-WA6HVCXFSWNI9X7I",
            "__v": 0,
            "created_at": "2023-06-08T11:23:09.868Z",
            "updated_at": "2023-06-08T11:23:09.868Z",
            "id": "6481ba1d1188097217dde822"
        },
        {
            "_id": "6481ba1d1188097217dde82c",
            "address": "74,OPEBI ROAD IKEJA",
            "carrier": "fedex",
            "city": "Ikeja",
            "country": "NG",
            "email": "",
            "phone": "",
            "state": "Lagos",
            "drop_off_location_id": "DO-1D1R7RB1X01ZZ278",
            "__v": 0,
            "created_at": "2023-06-08T11:23:09.868Z",
            "updated_at": "2023-06-08T11:23:09.868Z",
            "id": "6481ba1d1188097217dde82c"
        },
        {
            "_id": "6481ba1d1188097217dde85b",
            "address": "45 allen avenue, opposite studio 24",
            "carrier": "dhl-ng",
            "city": "Ikeja",
            "country": "NG",
            "email": "esther.nwajei@dhl.com",
            "phone": "2348039077000",
            "state": "Lagos",
            "drop_off_location_id": "DO-NZJL3G5DKO654ESG",
            "__v": 0,
            "created_at": "2023-06-08T11:23:09.869Z",
            "updated_at": "2023-06-08T11:23:09.869Z",
            "id": "6481ba1d1188097217dde85b"
        },
        {
            "_id": "6481ba1d1188097217dde85c",
            "address": "41 Joel Ogunnaike Steet Ikeja GRA",
            "carrier": "dhl-ng",
            "city": "Ikeja",
            "country": "NG",
            "email": "esther.nwajei@dhl.com",
            "phone": "2348039077000",
            "state": "Lagos",
            "drop_off_location_id": "DO-NQHISW914YKTSECA",
            "__v": 0,
            "created_at": "2023-06-08T11:23:09.869Z",
            "updated_at": "2023-06-08T11:23:09.869Z",
            "id": "6481ba1d1188097217dde85c"
        },
        {
            "_id": "6481ba1d1188097217dde85d",
            "address": "NAHCO",
            "carrier": "dhl-ng",
            "city": "Ikeja",
            "country": "NG",
            "email": "esther.nwajei@dhl.com",
            "phone": "2348039077000",
            "state": "Lagos",
            "drop_off_location_id": "DO-QN6D6LA74FC103TL",
            "__v": 0,
            "created_at": "2023-06-08T11:23:09.869Z",
            "updated_at": "2023-06-08T11:23:09.869Z",
            "id": "6481ba1d1188097217dde85d"
        },
        {
            "_id": "6481ba1d1188097217dde860",
            "address": "79 Awolowo way,Ikeja.",
            "carrier": "dhl-ng",
            "city": "Ikeja",
            "country": "NG",
            "email": "",
            "phone": "2349133768866",
            "state": "Lagos",
            "drop_off_location_id": "DO-6RAUI3503924OWSP",
            "__v": 0,
            "created_at": "2023-06-08T11:23:09.869Z",
            "updated_at": "2023-06-08T11:23:09.869Z",
            "id": "6481ba1d1188097217dde860"
        }
    ]
}
Previous
Disable Multiple Carriers
Next
Claims
Last updated 7 months ago


Create Packaging
Create new packaging for wrapping parcels

/packaging
POST https://api.terminal.africa/v1/packaging

This endpoint allows you to add new packaging.

Headers
Name
Type
Description
Authorization*

string

Set value to Bearer SECRET_KEY

Content-Type

string

Set value to application/json

Request Body
Name
Type
Description
height*

number

Height of packaging.

length*

number

Length of packaging.

name*

string

Name of packaging.

size_unit*

string

Unique size unit for packaging, only cm available at this time.

type*

string

Type of packaging. Accepted values are box, envelope and soft-packaging.

width*

number

Width of packaging.

weight*

number

Weight of packaging.

weight_unit*

string

Weight unit of packaging. Only kg available at this time.

200

Copy
{
	status: true,
	message: 'Packaging created successfully',
	data: {
		height: 5,
		id: 'LsuiGzcYlz4dKRYnEXeobJu9gnVbQVXN',
		length: 40,
		name: 'Soft Packaging',
		packaging_id: 'PA-97263925515',
		size_unit: 'cm',
		type: 'soft-package',
		weight: 0.01,
		weight_unit: 'kg',		
		width: 30,
		created_at: '2021-07-13T20:25:53.011Z',
		updated_at: '2021-07-13T20:25:53.011Z'
	}
}
Previous
Packaging
Next
Update Packaging
Last updated 3 years ago

Update Packaging
Update information for an existing packaging.

/packaging/:packaging_id
PUT https://api.terminal.africa/v1/packaging/:packaging_id

This endpoint allows you to update an existing packaging.

Path Parameters
Name
Type
Description
packaging_id*

String

Unique packaging_id for packaging.

Headers
Name
Type
Description
Authorization*

String

Set value to Bearer SECRET_KEY

Content-Type

String

Set value to application/json

200: OK Packaging updated successfully.

Copy
{
    // Response
}
Previous
Create Packaging
Next
Get Packaging
Last updated 5 months ago

et Packaging
Fetch list of packaging available for a user.

/packaging
GET https://api.terminal.africa/v1/packaging

This endpoint allows you to retrieve a list of packaging available for a user.

Query Parameters
Name
Type
Description
type

String

When provided, returns types of packaging that match the value provided. e.g. soft-package

perPage

Number

Specify how many records will be included in a single response. Defaults to 100.

page

Number

Specify what page will be included in a single response. Defaults to 1.

Headers
Name
Type
Description
Authorization*

string

Set value to Bearer SECRET_KEY

200 Packaging retrieved successfully.

Copy
{
    "status": true,
    "message": "Packaging retrieved successfully",
    "data": {
        "packaging": [
            {
                "height": 5,
                "id": "LsuiGzcYlz4dKRYnEXeobJu9gnVbQVXN",
                "length": 40,
                "name": "Soft Packaging",
                "packaging_id": "PA-97263925515",
                "size_unit": "cm",
                "type": "soft-package",
                "weight": 0.01,
                "weight_unit": "kg",
                "width": 30,
                "created_at": "2021-07-13T20:25:53.011Z",
                "updated_at": "2021-07-13T20:25:53.011Z"
            },
            {
                "height": 20,
                "id": "33QSBg4cpi9mPcV2IwJg0ZZzRNUcC9l",
                "length": 20,
                "name": "Box Packaging",
                "packaging_id": "PA-45873778254",
                "size_unit": "cm",
                "type": "box-package",
                "weight": 0.01,
                "weight_unit": "kg",
                "width": 20,
                "created_at": "2021-07-13T20:25:53.011Z",
                "updated_at": "2021-07-13T20:25:53.011Z"
            }],
        "pagination": {
            "perPage": 100,
            "prevPage": null,
            "nextPage": 2,
            "currentPage": 1,
            "total": 3,
            "pageCount": 3,
            "pagingCounter": 1,
            "hasPrevPage": false,
            "hasNextPage": true	
        }
    }
}
Previous
Update Packaging
Next
Terminal Default Packaging
Last updated 5 months ago

Create Parcel
Create a parcel for a shipment.

/parcels
POST https://api.terminal.africa/v1/parcels

This endpoint allows you to create a new parcel for a shipment.

Headers
Name
Type
Description
Authorization*

string

Set value to Bearer SECRET_KEY

Content-Type

string

Set value to application/json

Request Body
Name
Type
Description
description

string

Description of parcel.

items*

array

Object array of items in parcel. See Parcel Item object under MISCALLANEOUS for attributes required for each item.  

metadata

object

Additional information for a parcel.

packaging*

string

Unique id of packaging used to wrap items in parcel.

proof_of_payments

array

An array of string containing urls to documents/files

rec_docs

array

An array of string containing urls of images of parcel on a scale or with measuring tape

weight_unit*

string

Weight unit of parcel. Only kg is allowed at this time.

200 Parcel created successfully.

Copy
{
	status: true,
	message: 'Parcel created successfully',
	data: {
		description: true,
		id: 'Zt4Xh2pbbCmeVcr5YH9lsFHGqoW3i5w3',
		items: [{
			description: 'Shoes purchased from Shipmonk Store',
			name: 'Rubber Boots',
			currency: 'NGN',
			value: 25000',
			weight: 2.5
			quantity: 1
		}],
		metadata: {},		
		proof_of_payments: [],
		rec_docs: [],
		packaging: 'PA-97263925515',
		parcel_id: 'PC-25164820699',
		totalWeight: 2.51,
		weight: 2.5,
		weight_unit: 'kg',
		created_at: '2021-07-13T20:25:53.011Z',
		updated_at: '2021-07-13T20:25:53.011Z'
	}
}
Previous
Parcels
Next
Update Parcel
Last updated 1 year ago


Update Parcel
Update a parcel for a shipment.

/parcels/:parcel_id
PUT https://api.terminal.africa/v1/parcels/:parcel_id

This endpoint allows you to update information in an existing parcel. Only unused parcels can be updated.

Path Parameters
Name
Type
Description
parcel_id*

String

Unique parcel_id for parcel.

Headers
Name
Type
Description
Authorization*

String

Set value to Bearer SECRET_KEY

Content-Type

String

Set value to application/json

Request Body
Name
Type
Description
description

String

Description of items in parcel.

items

Array

List of items in parcel. Array of parcel item objects representing the items in the parcel.

packaging

String

Unique packaging_id to be used in parcel.

metadata

Object

Additional information for a parcel.

200: OK Parcel updated successfully.

Copy
{
	status: true,
	message: 'Parcel updated successfully',
	data: {
		description: "Cardboard box containing shoes from Shipmonk store",
		id: 'Zt4Xh2pbbCmeVcr5YH9lsFHGqoW3i5w3',
		items: [{
			description: 'Shoes purchased from Shipmonk Store',
			name: 'Rubber Boots',
			currency: 'NGN',
			value: 25000',
			weight: 2.5
			quantity: 1
		}],
		metadata: {},		
		packaging: 'PA-97263925515',
		parcel_id: 'PC-25164820699',
		totalWeight: 2.51,
		weight: 2.5,
		weight_unit: 'kg',
		created_at: '2021-07-13T20:25:53.011Z',
		updated_at: '2021-07-13T20:25:53.011Z'
	}
}
Previous
Create Parcel
Next
Get Parcels
Last updated 5 months ago

Get Parcels
Fetch a list of parcels available for a user.

/parcels
GET https://api.terminal.africa/v1/parcels

This endpoint allows you to get a list of all parcels available for a user.

Query Parameters
Name
Type
Description
perPage

Number

Specify how many records will be returned in a single request. Defaults to 100.

page

Number

Specify what page of records will be sent in response. Defaults to 1.

Headers
Name
Type
Description
Authorization*

string

Set value to Bearer SECRET_KEY

200 Parcels retrieved successfully.

Copy
{
    "status": true,
    "message": "Parcels retrieved successfully",
    "data": {
        "parcels": [
            {
                "_id": "6353c7f49f186020811fa296",
                "description": "Apple MacBook Pro with Charger, Wireless mouse and Keyboard",
                "items": [
                    {
                        "description": "Apple MacBook Pro with Charger, Wireless mouse and Keyboard",
                        "name": "0% off on Offer on deals",
                        "currency": "NGN",
                        "value": 1399,
                        "quantity": 1,
                        "weight": 2
                    }
                ],
                "packaging": "PA-12668277208",
                "total_weight": 2,
                "user": "USER-22498158801",
                "weight_unit": "kg",
                "parcel_id": "PC-13423942661",
                "created_at": "2022-10-22T10:37:40.804Z",
                "updated_at": "2022-10-22T10:37:40.804Z",
                "__v": 0,
                "id": "6353c7f49f186020811fa296"
            }
        ],
        "pagination": {
            "page": 1,
            "perPage": 1,
            "prevPage": null,
            "nextPage": 2,
            "currentPage": 1,
            "total": 2,
            "pageCount": 2,
            "pagingCounter": 1,
            "hasPrevPage": false,
            "hasNextPage": true
        }
    }
}
Previous
Update Parcel
Next
Get Parcel
Last updated 5 months ago


Get Parcel
Fetch details of a specific parcel.

/parcels/:id
GET https://api.terminal.africa/v1/parcels/:parcel_id

This endpoint allows you to retrieve details of a specific parcel.

Path Parameters
Name
Type
Description
parcel_id*

string

id of parcel.

Headers
Name
Type
Description
Authorization*

string

Set value to Bearer SECRET_KEY

200 Parcel retrieved successfully.

Copy
{
	status: true,
	message: 'Parcel retrieved successfully',
	data: {
		description: true,
		id: 'Zt4Xh2pbbCmeVcr5YH9lsFHGqoW3i5w3',
		items: [{
			description: 'Shoes purchased from Shipmonk Store',
			name: 'Rubber Boots',
			currency: 'NGN',
			value: 25000',
			weight: 2.5
			quantity: 1
		}],
		metadata: {},		
		packaging: 'LsuiGzcYlz4dKRYnEXeobJu9gnVbQVXN',
		parcel_id: 'PC-25164820699',
		total_weight: 2.51,
		weight: 2.5,
		weight_unit: 'kg',
		created_at: '2021-07-13T20:25:53.011Z',
		updated_at: '2021-07-13T20:25:53.011Z'
	}
}
Previous
Get Parcels
Next
Rates
Last updated 3 years ago


Get Rates for Shipment
Fetch available shipping rates for a shipment.

/rates
GET https://api.terminal.africa/v1/rates/shipment

This endpoint allows you to retrieve rates for a shipment. Must include parcel_id and one of pickup_address & delivery_address or shipment_id. To return cash on delivery rates for carriers who supports cash-on-delivery,  set cash_on_delivery to true if shipment_id does not include a shipment_type of cash-on-delivery. 

Query Parameters
Name
Type
Description
currency

string

Currency for rates. Defaults to NGN. Available options are AED, AUD, CAD, CNY, EUR, GBP, GHS, HKD, KES, NGN, TZS, UGX, USD, ZAR.

pickup_address

string

Unique id for pickup address. Required if shipment_id not provided.

delivery_address

string

Unique id for delivery address. Required if shipment_id not provided.

shipment_id

string

Unique id of shipment. Required if delivery_address and pickup_address not provided.

parcel_id

string

Unique id of parcel. Not required if shipment id is provided.

cash_on_delivery

boolean

Set to true to return rates for carriers who supports cash-on-delivery

Headers
Name
Type
Description
Authorization*

string

Set value to Bearer SECRET_KEY

200 Rates retrieved successfully.

Copy
{
	status: true,
	message: 'Rates retrieved successfully',
	data: [{
		amount: 14000,
		carrier_id: 'loYZh5J47D6gJUKOExXeO1RLcMARScLi',
		carrier_logo: 'https://ucarecdn.com/dcdd8109-af8c-4057-8104-192be821dd6e/download4.png',
		carrier_name: 'DHL Express',
		carrier_rate_description: 'EXPRESS 12:00 DOC',
		currency: 'NGN',
		delivery_time: 'Within 5 days.',
		id: 'bQVMwQZndHbIq6PQD5oiaGWxetLCXGkp',
		includes_insurance: false,
		insurance_coverage: 0,
		insurance_fee: 0,
		metadata: {},
		pickup_time: 'Tue Jul 13 2021 before 17:00 GMT',
		rate_id: 'RT-30798955894',
		shipment: 'RAl6LhWojcnJtlojLcw4XWgSpjBsjF38',
		created_at: '2021-07-13T20:25:53.011Z',
		updated_at: '2021-07-13T20:25:53.011Z'
	},{
		amount: 12500,
		carrier_id: 'hWiA1ZLw3SIr3VeCEbUKpjqVsijHrNjZ',
		carrier_logo: 'https://ucarecdn.com/c2d4dcb2-1483-47a5-ab14-447a990f5827/60dc7947195c0078fabff349_1200pxUnited_Parcel_Service_logo_2014svg.png',		
		carrier_name: 'United Parcel Services',
		carrier_rate_description: '',
		currency: 'NGN',
		delivery_time: 'Delivery within 1, 2, or 3 days based on where your package started and where it’s being sent.',		
		id: 'eDcN2a86N5OdWp3rzJLF2qoovG2BqLkC',
		includes_insurance: false,
		insurance_coverage: 0,
		insurance_fee: 0,
		metadata: {},
		pickup_time: 'Tue Jul 13 2021 before 17:00 GMT',
		rate_id: 'RT-97421991024',
		shipment: 'RAl6LhWojcnJtlojLcw4XWgSpjBsjF38',
		created_at: '2021-07-13T20:25:53.011Z',
		updated_at: '2021-07-13T20:25:53.011Z'
	},{
		amount: 11000,
		carrier_id: 'xOkhPcycBm75msJ8l6BU81vWRaA3p0tp',
		carrier_logo: 'https://ucarecdn.com/3273a236-bd33-4c37-9f87-2bcf4e59275f/6035307b31150075cabc780d_EeNJnpVz_400x400.jpg',
		carrier_name: 'Sendbox',
		carrier_rate_description: 'Standard Delivery',
		currency: 'NGN',
		delivery_time: 'Between 5 - 7 business days.',		
		id: 'A7c64epPiVyz2NZ5Cs3uNWuPznXUKFwj',
		includes_insurance: false,
		insurance_coverage: 0,
		insurance_fee: 0,
		metadata: {},	
		pickup_time: 'Between 12 - 24 hours',
		rate_id: 'RT-49826156746',
		shipment: 'RAl6LhWojcnJtlojLcw4XWgSpjBsjF38',	
		created_at: '2021-07-13T20:25:53.011Z',
		updated_at: '2021-07-13T20:25:53.011Z'
	}],
	pageData: {
    "total": 3,
    "perPage": 100,
    "page": 1,
    "pageCount": 1		
	}
}
Previous
Rates
Next
Get Quotes for Shipment
Last updated 5 months ago

Get Quotes for Shipment
Fetch available shipping quotes for a shipment

/rates/shipment/quotes
POST https://api.terminal.africa/v1/rates/shipment/quotes

This endpoint allows you to retrieve rates for a shipment. To return cash on delivery rates for carriers who supports cash-on-delivery,  set cash_on_delivery to true

Headers
Name
Type
Description
Authorization*

string

Set value to Bearer SECRET_KEY

Content-Type*

string

Set value to application/json

Request Body
Name
Type
Description
pickup_address*

object

Pickup Address Object. Refer to Create Address under Addresses to see attributes required to create a pickup address

delivery_address*

object

Delivery Address Object. Refer to Create Address under Addresses to see attributes required to create a delivery address

carrier_id

string

Unique id for carrier. Include carrier_id to return rates for specific carrier

currency

string

Currency for rates. Defaults to NGN. Available options are AED, AUD, CAD, CNY, EUR, GBP, GHS, HKD, KES, NGN, TZS, UGX, USD, ZAR.

parcel*

object

Parcel Object. Refer to Create Parcel under Parcels API Endpoints to see attributes required.
packaging_id not necessary in parcel object if persist_data is set to false.

cash_on_delivery

Boolean

Set to true to return cash on rates that supports cash on delivery.

persist_data

Boolean

Set to true if you want to use the response rate_id to arrange shipment/delivery. If this is true, every field in pickup and delivery address is required

200 Rates retrieved successfully.

Copy
{
    "status": true,
    "message": "Rates retrieved successfully",
    "data": [
        {
            "amount": 47500,
            "carrier_logo": "https://terminal-static-file.s3.amazonaws.com//uploads/2025-04-22-09-59-51-Terminal-Cargo-Logo.png",
            "carrier_name": "Terminal Air Cargo",
            "carrier_rate_description": "Air Cargo",
            "carrier_reference": "CA-4BWTMDHQKXZNP7J",
            "carrier_slug": "air-cargo",
            "currency": "NGN",
            "delivery_date": "2025-07-15T09:42:03.300Z",
            "delivery_eta": 10080,
            "delivery_time": "Within 7 days",
            "id": "rate_KqfMWgZixcxs1u6Y",
            "insurance_coverage": 0,
            "includes_duties": false,
            "insurance_fee": 0,
            "includes_insurance": false,
            "metadata": {
                "default_parcel": {
                    "packaging_dimension": {},
                    "parcel_total_weight": 2,
                    "parcel_value": 100,
                    "packages": [
                        {
                            "weight": 2.5,
                            "dimensions": {}
                        }
                    ]
                },
                "address_payload": {
                    "pickup_address": {
                        "city": "Kosofe",
                        "state": "Lagos",
                        "country": "NG",
                        "zip": "101123"
                    },
                    "delivery_address": {
                        "city": "Brookside",
                        "state": "Delaware",
                        "country": "US",
                        "zip": "101123"
                    }
                },
                "is_manual": true,
                "shipment_cost": 2000,
                "score": 10,
                "_id": null,
                "avgActualTurnaroundTime": 0,
                "avgActualPickupTime": 2,
                "avgRating": 0,
                "insurance_fee": 0,
                "insurance_currency": "NGN",
                "insurance_default_fee": 0,
                "insurance_default_currency": "NGN",
                "cod_processing_fee": 0
            },
            "pickup_date": "2025-07-08T09:42:03.300Z",
            "pickup_eta": 120,
            "pickup_time": "Within 2 hours",
            "rate_id": "RT-22JT23TDIBVHZOEC",
            "used": false,
            "dropoff_available": true,
            "dropoff_required": true,
            "default_amount": 0,
            "default_currency": "NGN",
            "cargo_type": "air",
            "type": "cargo",
            "user": "USER-1234567890",
            "delivery_address": "AD-PZZZXKSX3SX57COL",
            "pickup_address": "AD-C1XHAICYZ9F6EPF6",
            "parcel": "PC-QCSM5VYTI8ZARJPG"
        },
        {
            "amount": 77726.89,
            "default_amount": 77726.89,
            "default_currency": "NGN",
            "carrier_logo": "https://terminal-static-file.s3.us-east-1.amazonaws.com/images/Terminal+Express.svg",
            "carrier_name": "Terminal Express",
            "carrier_rate_description": "Express Shipping",
            "carrier_reference": "CA-ZLN8GIFB8EX1Z653",
            "carrier_slug": "terminal-express",
            "currency": "NGN",
            "delivery_date": "2025-07-13T09:42:04.504Z",
            "delivery_eta": 7200,
            "delivery_time": "Within 5 days",
            "id": "rate_jhDp5MZGHn3miz8W",
            "insurance_coverage": 0,
            "includes_duties": false,
            "insurance_fee": 0,
            "includes_insurance": false,
            "metadata": {
                "carrierFee": 72889.39,
                "default_parcel": {
                    "packaging_dimension": {},
                    "parcel_total_weight": 2,
                    "parcel_value": 100,
                    "packages": [
                        {
                            "weight": 2.5,
                            "dimensions": {}
                        }
                    ]
                },
                "address_payload": {
                    "pickup_address": {
                        "city": "Kosofe",
                        "state": "Lagos",
                        "country": "NG",
                        "zip": "101123"
                    },
                    "delivery_address": {
                        "city": "Brookside",
                        "state": "Delaware",
                        "country": "US",
                        "zip": "101123"
                    }
                },
                "shipment_cost": 72889.39,
                "score": 0,
                "avgRating": 0,
                "insurance_fee": 0,
                "insurance_currency": "NGN",
                "insurance_default_fee": 0,
                "insurance_default_currency": "NGN",
                "cod_processing_fee": 0
            },
            "pickup_date": "2025-07-10T09:42:04.504Z",
            "pickup_eta": 2880,
            "pickup_time": "Within 2 days",
            "rate_id": "RT-6ILI6FAC8622NYB0",
            "used": false,
            "user": "USER-1234567890",
            "delivery_address": "AD-PZZZXKSX3SX57COL",
            "pickup_address": "AD-C1XHAICYZ9F6EPF6",
            "parcel": "PC-QCSM5VYTI8ZARJPG"
        },
        {
            "amount": 93851.13,
            "default_amount": 93851.13,
            "default_currency": "NGN",
            "carrier_logo": "https://terminal-static-file.s3.amazonaws.com/images/Terminal-Premium-Logo-3.png",
            "carrier_name": "Terminal Premium",
            "carrier_rate_description": "International Economy",
            "carrier_reference": "CA-VO8R8JDFOBTGOP91",
            "carrier_slug": "terminal-premium",
            "currency": "NGN",
            "delivery_date": "2025-07-13T09:42:04.338Z",
            "delivery_eta": 7200,
            "delivery_time": "Within 5 days",
            "id": "rate_uYzbK9EKlZw6MqdP",
            "insurance_coverage": 0,
            "includes_duties": false,
            "insurance_fee": 0,
            "includes_insurance": false,
            "metadata": {
                "carrierFee": 81927.66,
                "default_parcel": {
                    "packaging_dimension": {},
                    "parcel_total_weight": 2,
                    "parcel_value": 100,
                    "packages": [
                        {
                            "weight": 2.5,
                            "dimensions": {}
                        }
                    ]
                },
                "address_payload": {
                    "pickup_address": {
                        "city": "Kosofe",
                        "state": "Lagos",
                        "country": "NG",
                        "zip": "101123"
                    },
                    "delivery_address": {
                        "city": "Brookside",
                        "state": "Delaware",
                        "country": "US",
                        "zip": "101123"
                    }
                },
                "shipment_cost": 81927.66,
                "score": 0,
                "avgRating": 0,
                "insurance_fee": 0,
                "insurance_currency": "NGN",
                "insurance_default_fee": 0,
                "insurance_default_currency": "NGN",
                "cod_processing_fee": 0
            },
            "pickup_date": "2025-07-10T09:42:04.338Z",
            "pickup_eta": 2880,
            "pickup_time": "Within 2 days",
            "rate_id": "RT-WM6M9CAFX3JK01X0",
            "used": false,
            "user": "USER-1234567890",
            "delivery_address": "AD-PZZZXKSX3SX57COL",
            "pickup_address": "AD-C1XHAICYZ9F6EPF6",
            "parcel": "PC-QCSM5VYTI8ZARJPG"
        },
    ]
}
Previous
Get Rates for Shipment
Next
Get Rates for Multi-Parcel Shipment
Last updated 10 months ago

Get Rates for Multi-Parcel Shipment
Fetch available shipping rates for a multi-parcel shipment.

/rates
POST https://api.terminal.africa/v1/rates/multi/shipment

This endpoint allows you to retrieve rates for a shipment. Must include parcel_id and one of pickup_address & delivery_address or shipment_id and .

Headers
Name
Type
Description
Authorization*

string

Set value to Bearer SECRET_KEY

Request Body
Name
Type
Description
currency

String

Currency for rates. Defaults to NGN. Available options are AED, AUD, CAD, CNY, EUR, GBP, GHS, HKD, KES, NGN, TZS, UGX, USD, ZAR.

delivery_address

String

Unique id for delivery address. Required if shipment_id not provided.

parcels

Array

List of parcel_ids to be included in shipment. Not required if shipment_id is provided.

pickup_address

String

Unique id for pickup address. Required if shipment_id not provided.

shipment_id

String

Unique id of shipment. Required if delivery_address and pickup_address not provided.

200 Rates retrieved successfully.

Copy
{
	status: true,
	message: 'Rates retrieved successfully',
	data: [{
		amount: 14000,
		carrier_id: 'loYZh5J47D6gJUKOExXeO1RLcMARScLi',
		carrier_logo: 'https://ucarecdn.com/dcdd8109-af8c-4057-8104-192be821dd6e/download4.png',
		carrier_name: 'DHL Express',
		carrier_rate_description: 'EXPRESS 12:00 DOC',
		currency: 'NGN',
		delivery_time: 'Within 5 days.',
		id: 'bQVMwQZndHbIq6PQD5oiaGWxetLCXGkp',
		includes_insurance: false,
		insurance_coverage: 0,
		insurance_fee: 0,
		metadata: {},
		pickup_time: 'Tue Jul 13 2021 before 17:00 GMT',
		rate_id: 'RT-30798955894',
		shipment: 'RAl6LhWojcnJtlojLcw4XWgSpjBsjF38',
		created_at: '2021-07-13T20:25:53.011Z',
		updated_at: '2021-07-13T20:25:53.011Z'
	},{
		amount: 12500,
		carrier_id: 'hWiA1ZLw3SIr3VeCEbUKpjqVsijHrNjZ',
		carrier_logo: 'https://ucarecdn.com/c2d4dcb2-1483-47a5-ab14-447a990f5827/60dc7947195c0078fabff349_1200pxUnited_Parcel_Service_logo_2014svg.png',		
		carrier_name: 'United Parcel Services',
		carrier_rate_description: '',
		currency: 'NGN',
		delivery_time: 'Delivery within 1, 2, or 3 days based on where your package started and where it’s being sent.',		
		id: 'eDcN2a86N5OdWp3rzJLF2qoovG2BqLkC',
		includes_insurance: false,
		insurance_coverage: 0,
		insurance_fee: 0,
		metadata: {},
		pickup_time: 'Tue Jul 13 2021 before 17:00 GMT',
		rate_id: 'RT-97421991024',
		shipment: 'RAl6LhWojcnJtlojLcw4XWgSpjBsjF38',
		created_at: '2021-07-13T20:25:53.011Z',
		updated_at: '2021-07-13T20:25:53.011Z'
	},{
		amount: 11000,
		carrier_id: 'xOkhPcycBm75msJ8l6BU81vWRaA3p0tp',
		carrier_logo: 'https://ucarecdn.com/3273a236-bd33-4c37-9f87-2bcf4e59275f/6035307b31150075cabc780d_EeNJnpVz_400x400.jpg',
		carrier_name: 'Sendbox',
		carrier_rate_description: 'Standard Delivery',
		currency: 'NGN',
		delivery_time: 'Between 5 - 7 business days.',		
		id: 'A7c64epPiVyz2NZ5Cs3uNWuPznXUKFwj',
		includes_insurance: false,
		insurance_coverage: 0,
		insurance_fee: 0,
		metadata: {},	
		pickup_time: 'Between 12 - 24 hours',
		rate_id: 'RT-49826156746',
		shipment: 'RAl6LhWojcnJtlojLcw4XWgSpjBsjF38',	
		created_at: '2021-07-13T20:25:53.011Z',
		updated_at: '2021-07-13T20:25:53.011Z'
	}],
	pageData: {
    "total": 3,
    "perPage": 100,
    "page": 1,
    "pageCount": 1		
	}
}
Previous
Get Quotes for Shipment
Next
Get Rates
Last updated 2 years ago

Get Rates
Fetch a list of rates generated by a user.

/rates
GET https://api.terminal.africa/v1/rates

This endpoint allows you to get a list of all rates generated by a user.

Query Parameters
Name
Type
Description
perPage

Number

Specify how many records will be returned in a single request. Defaults to 100.

page

Number

Specify what page of records will be sent in response. Defaults to 1.

Headers
Name
Type
Description
Authorization*

String

Set value to Bearer SECRET_KEY

200: OK Rates retrieved successfully.

Copy
{
	status: true,
	message: 'Rates retrieved successfully',
	data: {
		rates: [{
                    "amount": 5048.08,
                    "breakdown": [],
                    "carrier_logo": "https://ucarecdn.com/dcdd8109-af8c-4057-8104-192be821dd6e/download4.png",
                    "carrier_name": "DHL Express + (Parcel Insurance)",
                    "carrier_rate_description": "EXPRESS DOMESTIC",
                    "carrier_reference": "CA-81957188177",
                    "carrier_slug": "dhl-ng",
                    "currency": "NGN",
                    "delivery_address": "AD-80439326931",
                    "delivery_date": "2022-06-15T22:59:00.000Z",
                    "delivery_eta": 4237,
                    "delivery_time": "Within 3 days",
                    "insurance_coverage": 0,
                    "insurance_fee": 3500,
                    "includes_insurance": true,
                    "metadata": {
                        "localProductCode": "N",
                        "productCode": "N"
                    },
                    "parcel": "PC-09284697565",
                    "pickup_address": "AD-77298486083",
                    "pickup_eta": 1440,
                    "pickup_time": "Within 24 hours",
                    "rate_id": "RT-98930123958",
                    "used": true,
                    "user": "USER-12568655307",
                    "created_at": "2022-06-13T00:22:37.782Z",
                    "updated_at": "2022-06-13T00:25:03.834Z"
                }],
		pagination: {
    			"total": 1,
    			"perPage": 100,
    			"page": 1,
    			"pageCount": 1		
		}
	}
}
Previous
Get Rates for Multi-Parcel Shipment
Next
Get Rate
Last updated 3 years ago

Shipments
Create Shipment
Create a shipment

/shipments
POST https://api.terminal.africa/v1/shipments

This endpoint allows you to create a shipment.

Headers
Name
Type
Description
Authorization*

string

Set value to Bearer SECRET_KEY

Content-Type*

string

Set value to application/json

Request Body
Name
Type
Description
address_from*

string

Unique id of pickup address.

address_to*

string

Unique id of delivery address.

metadata

object

Additional information for shipment.

parcel

string

Id of parcel. One of parcel or parcels must be provided.

address_return

string

Unique id of return address. If not provided, pickup_address is used by default.

shipment_purpose

string

Purpose of shipment. Options are commercial, personal, sample, return-after-repair, return-for-repair.

parcels

Array

List of parcel ids for creating a multi-parcel shipments. One of parcel or parcels must be provided.

shipment_type

string

Type of shipment to be created. Options are cash-on-delivery. Required if shipment is to be specified as cash-on-delivery

200 Shipment created successfully.

Copy
{
	status: true,
	message: 'Shipment created successfully',
	data: {
		address_from: {
			address_id: 'AD-00632494667',	
			city: 'Lagos',
			coordinates: {
					lat: 6.5969424,
					lng: 3.3542992
			},	
			country: 'NGA',
			email: 'augustus_obi@shipmonk.ng',
			first_name: 'Augustus',
			id: 'd799c2679e644279b59fe661ac8fa488',
			is_residential: true,
			last_name: 'Obi',
			line1: '1121 Allen Avenue, Ikeja',
			line2: '',
			metadata: {
				my_app_customer_id: 11234
			},
			name: 'Augustus Obi',
			phone: '+2348122340000',
			state: 'Lagos',
			zip: '121006'			
		},
		address_return: {
			address_id: 'AD-00632494667',	
			city: 'Lagos',
			coordinates: {
					lat: 6.5969424,
					lng: 3.3542992
			},	
			country: 'NGA',
			email: 'augustus_obi@shipmonk.ng',
			first_name: 'Augustus',
			id: 'd799c2679e644279b59fe661ac8fa488',
			is_residential: true,
			last_name: 'Obi',
			line1: '1121 Allen Avenue, Ikeja',
			line2: '',
			metadata: {
				my_app_customer_id: 11234
			},
			name: 'Augustus Obi',
			phone: '+2348122340000',
			state: 'Lagos',
			zip: '121006'		
		},
		address_to: {
			address_id: 'AD-95918335217',	
			city: 'London',
			coordinates: {
					lat: 43.653226,
					lng: -79.3831843
			},	
			country: 'GBR',
			email: 'timothy@shipmonk.ng',
			first_name: 'Timothy',
			id: 'S3YLVnGo9eKpMMbEQcWjgCraLqnNY2Oy',
			is_residential: true,
			last_name: 'Odunubi',
			line1: '45 Greenwich Lane, London',
			line2: '',
			metadata: {
				my_app_customer_id: 10567
			},
			name: 'Timothy Odunubi',
			phone: '+447514022567',
			state: '',
			zip: 'SE5 4HB'		
		},
		events: [],
		id: 'BUbL05Ecprhc2q17Xh9woRSwNpXJehay',
		metadata: {},
		parcel: {
			description: true,
			id: 'Zt4Xh2pbbCmeVcr5YH9lsFHGqoW3i5w3',
			items: [{
				description: 'Shoes purchased from Shipmonk Store',
				name: 'Rubber Boots',
				currency: 'NGN',
				value: 25000',
				weight: 2.5
				quantity: 1
			}],
			metadata: {},		
			packaging: 'LsuiGzcYlz4dKRYnEXeobJu9gnVbQVXN',
			parcel_id: 'PC-25164820699',
			total_weight: 2.51,
			weight: 2.5,
			weight_unit: 'kg'		
		},
		rate: '',
		shipment_id: 'SH-40208776515',
		status: 'draft',
		created_at: '2021-07-13T20:25:53.011Z',
		updated_at: '2021-07-13T20:25:53.011Z'
	}
}
Previous
Shipments
Next
Create Quick Shipment
Last updated 2 years ago

Shipments
Create Quick Shipment
Create a quick shipment. Pass all required details, including address and parcel in a single API call.

/shipments/quick
POST https://api.terminal.africa/v1/shipments/quick

This endpoint allows you to create a shipment.

Headers
Name
Type
Description
Authorization*

string

Set value to Bearer SECRET_KEY

Content-Type*

string

Set value to application/json

Request Body
Name
Type
Description
pickup_address**

object

Pickup address details for shipment. Refer to Address Object to see attributes required for pickup_address.

delivery_address*

object

Delivery address details for shipment. Refer to Address Object to see attributes required for delivery_address.

metadata

object

Provide additional context for a shipment.

shipment_purpose

string

Purpose of shipment. Options are commercial, personal, sample, return-after-repair, return-for-repair.

parcel

object

Parcel details for shipment. Refer to Parcel Object to see attributes required for delivery_address. Required if parcels is not included

shipment_type

string

Type of shipment to be created. Options are cash-on-delivery. Required if shipment is to be specified as cash-on-delivery

parcels

array

Array of Parcel Object. Required if parcel is not included

200 Shipment created successfully.

Copy
{
	status: true,
	message: 'Shipment created successfully',
	data: {
		address_from: {
			address_id: 'AD-00632494667',	
			city: 'Lagos',
			coordinates: {
					lat: 6.5969424,
					lng: 3.3542992
			},	
			country: 'NGA',
			email: 'augustus_obi@shipmonk.ng',
			first_name: 'Augustus',
			id: 'd799c2679e644279b59fe661ac8fa488',
			is_residential: true,
			last_name: 'Obi',
			line1: '1121 Allen Avenue, Ikeja',
			line2: '',
			metadata: {
				my_app_customer_id: 11234
			},
			name: 'Augustus Obi',
			phone: '+2348122340000',
			state: 'Lagos',
			zip: '121006'			
		},
		address_return: {
			address_id: 'AD-00632494667',	
			city: 'Lagos',
			coordinates: {
					lat: 6.5969424,
					lng: 3.3542992
			},	
			country: 'NGA',
			email: 'augustus_obi@shipmonk.ng',
			first_name: 'Augustus',
			id: 'd799c2679e644279b59fe661ac8fa488',
			is_residential: true,
			last_name: 'Obi',
			line1: '1121 Allen Avenue, Ikeja',
			line2: '',
			metadata: {
				my_app_customer_id: 11234
			},
			name: 'Augustus Obi',
			phone: '+2348122340000',
			state: 'Lagos',
			zip: '121006'		
		},
		address_to: {
			address_id: 'AD-95918335217',	
			city: 'London',
			coordinates: {
					lat: 43.653226,
					lng: -79.3831843
			},	
			country: 'GBR',
			email: 'timothy@shipmonk.ng',
			first_name: 'Timothy',
			id: 'S3YLVnGo9eKpMMbEQcWjgCraLqnNY2Oy',
			is_residential: true,
			last_name: 'Odunubi',
			line1: '45 Greenwich Lane, London',
			line2: '',
			metadata: {
				my_app_customer_id: 10567
			},
			name: 'Timothy Odunubi',
			phone: '+447514022567',
			state: '',
			zip: 'SE5 4HB'		
		},
		events: [],
		id: 'BUbL05Ecprhc2q17Xh9woRSwNpXJehay',
		metadata: {},
		parcel: {
			description: true,
			id: 'Zt4Xh2pbbCmeVcr5YH9lsFHGqoW3i5w3',
			items: [{
				description: 'Shoes purchased from Shipmonk Store',
				name: 'Rubber Boots',
				currency: 'NGN',
				value: 25000',
				weight: 2.5
				quantity: 1
			}],
			metadata: {},		
			packaging: 'LsuiGzcYlz4dKRYnEXeobJu9gnVbQVXN',
			parcel_id: 'PC-25164820699',
			total_weight: 2.51,
			weight: 2.5,
			weight_unit: 'kg'		
		},
		rate: '',
		shipment_id: 'SH-40208776515',
		status: 'draft',
		created_at: '2021-07-13T20:25:53.011Z',
		updated_at: '2021-07-13T20:25:53.011Z'
	}
}
Previous
Create Shipment
Next
Update Shipment
Last updated 5 months ago

Update Shipment
Update information for an existing draft shipment.

/shipments/:shipment_id
PUT https://api.terminal.africa/v1/shipments/:shipment_id

This endpoint allows you to update a draft shipment.

Path Parameters
Name
Type
Description
shipment_id*

String

Unique reference for the shipment.

Request Body
Name
Type
Description
address_to

String

Unique id of delivery address.

address_from

String

Pickup address for shipment.

address_return

String

Return address for shipment.

metadata

Object

Provides additional information for a shipment.

parcel

String

Unique identifier of parcel to be shipped.

shipment_purpose

String

Purpose of shipment. Options are commercial, personal, sample, return-after-repair, return-for-repair.

parcels

Array

List of parcel ids for creating a multi-parcel shipments. One of parcel or parcels must be provided.

200: OK Shipment updated successfully.

Copy
{
    "status": true,
    "message": "Shipment updated successfully",
    "data": {
        "_id": "6375050a6d4274c046f439df",
        "address_to": {
            "user": "USER-27450202164",
            "city": "Leeds",
            "coordinates": {
                "lat": 53.809487,
                "lng": -1.5072216,
                "place_id": "ChIJD53YWnlceUgRsmVRYbUVibA"
            },
            "country": "GB",
            "email": "nnamdiokoh43@gmail.com",
            "first_name": "Nnamdi",
            "is_residential": true,
            "last_name": "Okoh",
            "line1": "2 Seaforth Avenue",
            "line2": "",
            "phone": "+447522689641",
            "place_id": "ChIJD53YWnlceUgRsmVRYbUVibA",
            "state": "Leeds",
            "zip": "LS96BE",
            "address_id": "AD-03203451781",
            "created_at": "2022-10-09T10:13:46.176Z",
            "updated_at": "2022-10-09T10:13:46.176Z",
            "__v": 0
        },
        "address_from": {
            "user": "USER-27450202164",
            "city": "Bethesda",
            "coordinates": {
                "lat": 38.9908175,
                "lng": -77.0987004,
                "place_id": "Eiw0ODUwIFJ1Z2J5IEF2ZSAjNDAxLCBCZXRoZXNkYSwgTUQgMjA4MTQsIFVTQSIfGh0KFgoUChIJ21n-ZGHJt4kRUJYKH_5GV40SAzQwMQ"
            },
            "country": "US",
            "email": "pickup@example.com",
            "first_name": "Diva",
            "is_residential": true,
            "last_name": "Lenore",
            "line1": "4850 Rugby Avenue",
            "line2": "Apt. 401",
            "metadata": {
                "platform": "logistics"
            },
            "phone": "+12027902590",
            "place_id": "Eiw0ODUwIFJ1Z2J5IEF2ZSAjNDAxLCBCZXRoZXNkYSwgTUQgMjA4MTQsIFVTQSIfGh0KFgoUChIJ21n-ZGHJt4kRUJYKH_5GV40SAzQwMQ",
            "state": "Maryland",
            "zip": "20814",
            "address_id": "AD-07132639725",
            "created_at": "2022-09-05T23:52:28.436Z",
            "updated_at": "2022-09-05T23:52:28.436Z",
            "__v": 0
        },
        "address_return": {
            "user": "USER-27450202164",
            "city": "Victoria Island",
            "coordinates": {
                "lat": 6.4263118,
                "lng": 3.4184293,
                "place_id": "ChIJ1SArPc2KOxARwfjurnR1bXY"
            },
            "country": "NG",
            "email": "nnamdiokoh43@gmail.com",
            "first_name": "Nnamdi",
            "is_residential": true,
            "last_name": "Okoh",
            "line1": "4 Gabaro Street, Victoria Island, Lagos",
            "line2": "",
            "phone": "+2348122689641",
            "place_id": "ChIJ1SArPc2KOxARwfjurnR1bXY",
            "state": "Lagos",
            "zip": "--",
            "address_id": "AD-97595221861",
            "created_at": "2022-10-09T10:12:36.450Z",
            "updated_at": "2022-10-09T10:12:36.450Z",
            "__v": 0
        },
        "parcel": {
            "_id": "63429e4a12432be769d4b027",
            "description": "sets of electronics package items description",
            "items": [
                {
                    "description": "iphone x sets of description testing",
                    "name": "Iphone x",
                    "weight": 0.5,
                    "quantity": 2,
                    "value": 100000,
                    "currency": "NGN"
                }
            ],
            "metadata": {
                "platform": "logistics",
                "type": "third_party"
            },
            "packaging": {
                "_id": "63429e2512432be769d4b01d",
                "height": 1,
                "length": 47,
                "name": "DHL Express Large Flyer",
                "size_unit": "cm",
                "type": "soft-packaging",
                "user": "USER-27450202164",
                "weight": 0.1,
                "weight_unit": "kg",
                "width": 38,
                "packaging_id": "PA-05804394376",
                "created_at": "2022-10-09T10:10:45.673Z",
                "updated_at": "2022-10-09T10:10:45.673Z",
                "__v": 0
            },
            "total_weight": 0.5,
            "user": "USER-27450202164",
            "weight_unit": "kg",
            "parcel_id": "PC-09857312356",
            "created_at": "2022-10-09T10:11:22.631Z",
            "updated_at": "2022-10-09T10:11:22.631Z",
            "__v": 0,
            "contains_perishables": false,
            "total_value": 100000,
            "id": "63429e4a12432be769d4b027"
        },
        "pickup_date": null,
        "shipment_purpose": "personal",
        "status": "draft",
        "user": {
            "business_category": "",
            "_id": "62b62e12cd7114864f36572c",
            "admin": false,
            "carriers": {
                "domestic": [
                    "CA-07032569055",
                    "CA-18228854618",
                    "CA-31377601348",
                    "CA-71017347351",
                    "CA-85479996273",
                    "CA-49411197653",
                    "CA-19429970231",
                    "CA-81957188177"
                ],
                "international": [
                    "CA-85479996273",
                    "CA-49411197653",
                    "CA-19429970231",
                    "CA-81957188177",
                    "CA-42199963340"
                ],
                "regional": [
                    "CA-07032569055",
                    "CA-18228854618",
                    "CA-31377601348",
                    "CA-71017347351",
                    "CA-85479996273",
                    "CA-49411197653",
                    "CA-19429970231",
                    "CA-81957188177"
                ]
            },
            "company_name": "Eclectic Source",
            "country": "NG",
            "email": "team@theeclecticsource.com",
            "first_name": "Nnamdi",
            "last_name": "Okoh",
            "metadata": {
                "storeId": "CF1X33wJMCaG2s7d5OckHBoWQlj2",
                "totalShipment": 113,
                "totalShipmentAmount": 228267.76,
                "totalWalletInflow": 0,
                "octa_profile_id": "61669082052317172646fzxiobn3lisj"
            },
            "phone": "+2348122689641",
            "public_key": "pk_test_mmXALQGeB2rS6ZG54UMu1nQUThCUp7fK",
            "secret_key": "sk_test_HbftxQxW3VsovsWhtU6yDM53zn12gRfX",
            "wallet": "6342ed1cd5acb7ed14f6c4cd",
            "user_id": "USER-27450202164",
            "created_at": "2022-06-24T21:35:14.842Z",
            "updated_at": "2022-11-22T18:18:40.896Z",
            "__v": 1,
            "plan": "webflow",
            "barred_countries": [],
            "country_state": "Lagos",
            "referralCode": "REF-41078297020",
            "account_active": false,
            "wallet_enabled": true,
            "name": "Nnamdi Okoh",
            "id": "62b62e12cd7114864f36572c"
        },
        "events": [],
        "shipment_id": "SH-59981754867",
        "created_at": "2022-11-16T15:43:06.657Z",
        "updated_at": "2022-11-24T21:43:10.807Z",
        "__v": 0,
        "metadata": {
            "shipment_payload": {}
        }
    }
}
Previous
Create Quick Shipment
Next
Get Shipments
Last updated 2 years ago

Get Shipments
Fetch a list of all shipments available for a user.

/shipments
GET https://api.terminal.africa/v1/shipments

This endpoint allows you to get a list of shipments available for a user. 

Query Parameters
Name
Type
Description
perPage

string

Specify how many results will be returned in a single request. Defaults to 100.

page

string

Specify what page of records will be sent in response. Defaults to 1.

popluate

boolean

Indicate if full details should be provided for select fields including address_from, address_return, address_to, carrier, parcel.

status

string

Status of shipment. Must be one of cancelled, confirmed, delivered, draft, in-transit, pending

Headers
Name
Type
Description
Authorization*

string

Set value to Bearer ACCESS_TOKEN

200 Shipments retrieved successfully.

Copy
{
	status: true,
	message: 'Shipments retrieved successfully',
	data: [{
		address_from: {
			address_id: 'AD-00632494667',	
			city: 'Lagos',
			coordinates: {
					lat: 6.5969424,
					lng: 3.3542992
			},	
			country: 'NGA',
			email: 'augustus_obi@shipmonk.ng',
			first_name: 'Augustus',
			id: 'd799c2679e644279b59fe661ac8fa488',
			is_residential: true,
			last_name: 'Obi',
			line1: '1121 Allen Avenue, Ikeja',
			line2: '',
			metadata: {
				my_app_customer_id: 11234
			},
			name: 'Augustus Obi',
			phone: '+2348122340000',
			state: 'Lagos',
			zip: '121006'			
		},
		address_return: {
			address_id: 'AD-00632494667',	
			city: 'Lagos',
			coordinates: {
					lat: 6.5969424,
					lng: 3.3542992
			},	
			country: 'NGA',
			email: 'augustus_obi@shipmonk.ng',
			first_name: 'Augustus',
			id: 'd799c2679e644279b59fe661ac8fa488',
			is_residential: true,
			last_name: 'Obi',
			line1: '1121 Allen Avenue, Ikeja',
			line2: '',
			metadata: {
				my_app_customer_id: 11234
			},
			name: 'Augustus Obi',
			phone: '+2348122340000',
			state: 'Lagos',
			zip: '121006'		
		},
		address_to: {
			address_id: 'AD-95918335217',	
			city: 'London',
			coordinates: {
					lat: 43.653226,
					lng: -79.3831843
			},	
			country: 'GBR',
			email: 'timothy@shipmonk.ng',
			first_name: 'Timothy',
			id: 'S3YLVnGo9eKpMMbEQcWjgCraLqnNY2Oy',
			is_residential: true,
			last_name: 'Odunubi',
			line1: '45 Greenwich Lane, London',
			line2: '',
			metadata: {
				my_app_customer_id: 10567
			},
			name: 'Timothy Odunubi',
			phone: '+447514022567',
			state: '',
			zip: 'SE5 4HB'		
		},
		events: [],
		id: 'BUbL05Ecprhc2q17Xh9woRSwNpXJehay',
		metadata: {},
		parcel: {
			description: true,
			id: 'Zt4Xh2pbbCmeVcr5YH9lsFHGqoW3i5w3',
			items: [{
				description: 'Shoes purchased from Shipmonk Store',
				name: 'Rubber Boots',
				currency: 'NGN',
				value: 25000',
				weight: 2.5
				quantity: 1
			}],
			metadata: {},		
			packaging: 'LsuiGzcYlz4dKRYnEXeobJu9gnVbQVXN',
			parcel_id: 'PC-25164820699',
			total_weight: 2.51,
			weight: 2.5,
			weight_unit: 'kg'		
		},
		rate: '',
		shipment_id: 'SH-40208776515',
		status: 'draft',
		created_at: '2021-07-13T20:25:53.011Z',
		updated_at: '2021-07-13T20:25:53.011Z'		
	}],
	pageData: {
    		"total": 1,
    		"perPage": 100,
    		"page": 1,
    		"pageCount": 1		
	}
	
}
Previous
Update Shipment
Next
Get Shipments v2
Last updated 2 years ago

Get Shipments v2
Fetch a list of all shipments available for a user.

/shipments
GET https://api.terminal.africa/v2/shipments

This endpoint allows you to get a list of shipments available for a user. 

Query Parameters
Name
Type
Description
perPage

string

Specify how many results will be returned in a single request. Defaults to 50.

page

string

Specify what page of records will be sent in response. Defaults to 1.

status

string

Status of shipment. Must be one of cancelled, confirmed, delivered, draft, in-transit, pending

search

String

Search for shipments using text string. The searchable fields includes  tracking_number, shipment_id, shipment reference. 

Eg: ?search=search_text

orderBy

String

Order a shipments. Default to DESC created_at (-created_at).  Ordering fields includes: created_at, updated_at, pickup_date, delivery_date, amount.

EXAMPLES OF DESC ORDERING

1. ?orderBy=-created_at

2. ?orderBy=-amount

3. ?orderBy=-updated_at

EXAMPLES OF ASC ORDERING

1. ?orderBy=created_at

2. ?orderBy=amount

3. ?orderBy=updated_at

pickup_country

String

Filter shipment by pickup country

Eg ?pickup_country=NG

delivery_country

String

Filter shipment by delivery country

Eg ?delivery_country=NG

pickup_state

String

Filter shipment by pickup state

Eg ?pickup_state=Lagos

delivery_state

String

Filter shipment by delivery state

Eg ?delivery_state=Lagos

pickup_city

String

Filter shipment by pickup city

Eg ?pickup_city=Apapa

delivery_city

String

Filter shipment by delivery city

Eg ?delivery_city=Apapa

carrier_slug

String

Filter shipments by carrier_slug

eg?carrier_slug=dhl

carrier_id

String

Filter shipments by carrier_id

eg?carrier_id=CA-81957188177

start_date

String

Filter from shipment creation start date. Format: YYYY-MM-DD

eg ?start_date=2023-05-01

end_date

String

Filter from shipment creation end date. Format: YYYY-MM-DD

eg ?end_date=2023-05-01

Headers
Name
Type
Description
Authorization*

string

Set value to Bearer ACCESS_TOKEN

200 Shipments retrieved successfully.

Copy
```json
{
    "status": true,
    "message": "Shipments retrieved successfully",
    "data": {
        "shipments": [
            {
                "_index": "shipments",
                "_id": "SH-WZZM27DZ8DEIP6QB",
                "_score": null,
                "_source": {
                    "address_to": "AD-K6MR9ACBQ0S38T9T",
                    "address_from": "AD-O3E5K3XN1YMSOAHO",
                    "address_return": "AD-O3E5K3XN1YMSOAHO",
                    "parcel": "PC-5X8DU2SSCZ44AZZ8",
                    "parcels": [],
                    "pickup_date": "2023-09-16T12:20:17.053Z",
                    "cancellation_request": false,
                    "cancellation_reason": "",
                    "shipment_cost_currency": "NGN",
                    "shipment_purpose": "personal",
                    "status": "confirmed",
                    "type": "terminal",
                    "source": "web",
                    "created_source": "web",
                    "user": "USER-22070036153",
                    "events": [
                        {
                            "created_at": "2023-09-14T12:20:17.053Z",
                            "description": "Shipment arranged by Tolulope Oguntade",
                            "location": "Ikeja, NG",
                            "status": "confirmed"
                        }
                    ],
                    "shipment_id": "SH-WZZM27DZ8DEIP6QB",
                    "created_at": "2023-09-14T12:14:34.721Z",
                    "updated_at": "2023-09-14T12:20:17.055Z",
                    "carrier": "CA-81957188177",
                    "delivery_arranged": "2023-09-14T12:20:17.053Z",
                    "delivery_date": "2023-09-19T23:59:00.000Z",
                    "rate": "RT-QEWREK6BYRC4F4DO",
                    "shipment_cost": 23577.96,
                    "tracking_number": "3847758972",
                    "international_tracking_number": "",
                    "reference": "CBJ230915031861",
                    "carrier_tracking_url": "https://www.dhl.com/global-en/home/tracking.html?tracking-id=3847758972",
                    "shipping_label_url": "https://api.terminal.africa/v1/shipments/label/SH-WZZM27DZ8DEIP6QB.pdf",
                    "commercial_invoice_url": "https://api.terminal.africa/v1/shipments/commercial-invoice/SH-WZZM27DZ8DEIP6QB.pdf",
                    "tracking_url": "https://app.terminal.africa/shipments/track/SH-WZZM27DZ8DEIP6QB",
                    "user_email": "parcelsnigeria@gmail.com",
                    "user_phone": "",
                    "user_company_name": "Parcels Nigeria",
                    "user_business_category": "consultant",
                    "user_account_type": "3pl",
                    "user_country": "NG",
                    "user_country_state": "",
                    "user_name": "Tolulope Oguntade",
                    "user_storeId": "dmNhphFCXKTYCCTcQJOPbryn6bB2",
                    "user_wallet": "6278e2739619f23000874d56",
                    "user_referredBy": "",
                    "user_referralCode": "REF-84841000717",
                    "pickup_email": "parcelsnigeria@gmail.com",
                    "delivery_email": "parcelsnigeria@gmail.com",
                    "return_email": "parcelsnigeria@gmail.com",
                    "pickup_name": "Lara Evelyn",
                    "delivery_name": "Priscille Manlan",
                    "return_name": "Lara Manlan",
                    "pickup_city": "Ikeja",
                    "delivery_city": "Newark",
                    "return_city": "Ikeja",
                    "pickup_state": "Lagos",
                    "delivery_state": "Delaware",
                    "return_state": "Lagos",
                    "pickup_country": "NG",
                    "delivery_country": "US",
                    "return_country": "NG",
                    "pickup_zip": "105102",
                    "delivery_zip": "19702",
                    "return_zip": "105102",
                    "pickup_line1": "782b Rev. Emmanuel Adubifa Street, Ikeja, Nig",
                    "delivery_line1": "1405 Gregory Drive, Newark, DE, USA",
                    "return_line1": "782b Rev. Emmanuel Adubifa Street, Ikeja, Nig",
                    "carrier_name": "DHL Express",
                    "carrier_logo": "https://ucarecdn.com/dcdd8109-af8c-4057-8104-192be821dd6e/download4.png",
                    "carrier_slug": "dhl-ng",
                    "amount": 23577.96
                },
                "sort": [
                    1694693674721
                ]
            },
            {
                "_index": "shipments",
                "_id": "SH-28GIZ6WNYRMGLII2",
                "_score": null,
                "_source": {
                    "address_to": "AD-3TVI0BWYTVFMNPMW",
                    "address_from": "AD-6QAY79GCAVEVSZI4",
                    "address_return": "AD-6QAY79GCAVEVSZI4",
                    "parcel": "PC-WOTT6EV8Y3UCPB9W",
                    "parcels": [],
                    "pickup_date": "2023-09-16T10:30:36.373Z",
                    "cancellation_request": false,
                    "cancellation_reason": "",
                    "shipment_cost_currency": "NGN",
                    "shipment_purpose": "personal",
                    "status": "confirmed",
                    "type": "terminal",
                    "source": "web",
                    "created_source": "web",
                    "user": "USER-22070036153",
                    "events": [
                        {
                            "created_at": "2023-09-14T10:30:36.373Z",
                            "description": "Shipment arranged by Tolulope Oguntade",
                            "location": "Ikeja, NG",
                            "status": "confirmed"
                        }
                    ],
                    "shipment_id": "SH-28GIZ6WNYRMGLII2",
                    "created_at": "2023-09-14T10:27:25.458Z",
                    "updated_at": "2023-09-14T10:30:36.374Z",
                    "carrier": "CA-81957188177",
                    "delivery_arranged": "2023-09-14T10:30:36.373Z",
                    "delivery_date": "2023-09-15T23:59:00.000Z",
                    "rate": "RT-R9STD54YM120O6EX",
                    "shipment_cost": 4434.6,
                    "tracking_number": "1707192756",
                    "international_tracking_number": "",
                    "reference": "CBJ230915026870",
                    "carrier_tracking_url": "https://www.dhl.com/global-en/home/tracking.html?tracking-id=1707192756",
                    "shipping_label_url": "https://api.terminal.africa/v1/shipments/label/SH-28GIZ6WNYRMGLII2.pdf",
                    "commercial_invoice_url": "https://api.terminal.africa/v1/shipments/commercial-invoice/SH-28GIZ6WNYRMGLII2.pdf",
                    "tracking_url": "https://app.terminal.africa/shipments/track/SH-28GIZ6WNYRMGLII2",
                    "user_email": "parcelsnigeria@gmail.com",
                    "user_phone": "",
                    "user_company_name": "Parcels Nigeria",
                    "user_business_category": "consultant",
                    "user_account_type": "3pl",
                    "user_country": "NG",
                    "user_country_state": "",
                    "user_name": "Tolulope Oguntade",
                    "user_storeId": "dmNhphFCXKTYCCTcQJOPbryn6bB2",
                    "user_wallet": "6278e2739619f23000874d56",
                    "user_referredBy": "",
                    "user_referralCode": "REF-84841000717",
                    "pickup_email": "parcelsnigeria@gmail.com",
                    "delivery_email": "parcelsnigeria@gmail.com",
                    "return_email": "parcelsnigeria@gmail.com",
                    "pickup_name": "Barcutt Logistics",
                    "delivery_name": "Maikyau Princess",
                    "return_name": "Barcutt Princess",
                    "pickup_city": "Ikeja",
                    "delivery_city": "Abuja",
                    "return_city": "Ikeja",
                    "pickup_state": "Lagos",
                    "delivery_state": "Abuja",
                    "return_state": "Lagos",
                    "pickup_country": "NG",
                    "delivery_country": "NG",
                    "return_country": "NG",
                    "pickup_zip": "105102",
                    "delivery_zip": "900108",
                    "return_zip": "105102",
                    "pickup_line1": "782b Rev. Emmanuel Adubifa Street, Ikeja, Nig",
                    "delivery_line1": "House 14, Aclose Eagleville Estate, Mabushi",
                    "return_line1": "782b Rev. Emmanuel Adubifa Street, Ikeja, Nig",
                    "carrier_name": "DHL Express",
                    "carrier_logo": "https://ucarecdn.com/dcdd8109-af8c-4057-8104-192be821dd6e/download4.png",
                    "carrier_slug": "dhl-ng",
                    "amount": 4434.6
                },
                "sort": [
                    1694687245458
                ]
            },
            {
                "_index": "shipments",
                "_id": "SH-MAOPQZBNWOFQQFQC",
                "_score": null,
                "_source": {
                    "address_to": "AD-2912LZK1ZZZ5O0KQ",
                    "address_from": "AD-DE0NV0H03VTTBZZR",
                    "address_return": "AD-DE0NV0H03VTTBZZR",
                    "parcel": "PC-0SSTLONL9NWAW11V",
                    "parcels": [],
                    "pickup_date": "2023-09-13T15:43:27.658Z",
                    "cancellation_request": false,
                    "cancellation_reason": "",
                    "shipment_cost_currency": "NGN",
                    "shipment_purpose": "personal",
                    "status": "delivered",
                    "type": "terminal",
                    "source": "web",
                    "created_source": "web",
                    "user": "USER-22070036153",
                    "events": [
                        {
                            "created_at": "2023-09-13T13:43:27.658Z",
                            "description": "Shipment arranged by Tolulope Oguntade",
                            "location": "Yaba, NG",
                            "status": "confirmed"
                        },
                        {
                            "created_at": "2023-09-13T15:00:00.000Z",
                            "description": "Pickup completed by JOLAOSHO",
                            "location": "Yaba, NG",
                            "status": "in-transit"
                        },
                        {
                            "created_at": "2023-09-13T18:00:00.000Z",
                            "description": "Delivery completed by JOLAOSHO",
                            "location": "Ikeja, NG",
                            "status": "delivered"
                        }
                    ],
                    "shipment_id": "SH-MAOPQZBNWOFQQFQC",
                    "created_at": "2023-09-13T13:40:39.789Z",
                    "updated_at": "2023-09-13T18:15:02.562Z",
                    "carrier": "CA-18228854618",
                    "delivery_arranged": "2023-09-13T13:43:27.658Z",
                    "delivery_date": "2023-09-13T15:43:15.874Z",
                    "rate": "RT-8PR6UNOVOIFDTG1W",
                    "shipment_cost": 2251.88,
                    "transaction_reference": "TR-I43SYVC71VM574FB9A4H5HKRTZ643KJ",
                    "tracking_number": "974858RH319",
                    "international_tracking_number": "",
                    "reference": "974858RH319",
                    "carrier_tracking_url": "https://dashboard.kwik.delivery/tracking/index.html?jobID=2e68771349c057641186cc029f133e91",
                    "shipping_label_url": "",
                    "commercial_invoice_url": "",
                    "tracking_url": "https://app.terminal.africa/shipments/track/SH-MAOPQZBNWOFQQFQC",
                    "user_email": "parcelsnigeria@gmail.com",
                    "user_phone": "",
                    "user_company_name": "Parcels Nigeria",
                    "user_business_category": "consultant",
                    "user_account_type": "3pl",
                    "user_country": "NG",
                    "user_country_state": "",
                    "user_name": "Tolulope Oguntade",
                    "user_storeId": "dmNhphFCXKTYCCTcQJOPbryn6bB2",
                    "user_wallet": "6278e2739619f23000874d56",
                    "user_referredBy": "",
                    "user_referralCode": "REF-84841000717",
                    "pickup_email": "parcelsnigeria@gmail.com",
                    "delivery_email": "parcelsnigeria@gmail.com",
                    "return_email": "parcelsnigeria@gmail.com",
                    "pickup_name": "Lara Evelyn",
                    "delivery_name": "Parcels Nigeria",
                    "return_name": "Lara Nigeria",
                    "pickup_city": "Yaba",
                    "delivery_city": "Ikeja",
                    "return_city": "Yaba",
                    "pickup_state": "Lagos",
                    "delivery_state": "Lagos",
                    "return_state": "Lagos",
                    "pickup_country": "NG",
                    "delivery_country": "NG",
                    "return_country": "NG",
                    "pickup_zip": "101245",
                    "delivery_zip": "105102",
                    "return_zip": "101245",
                    "pickup_line1": "31b Simpson Street, Lagos, Nigeria",
                    "delivery_line1": "782b Rev. Emmanuel Adubifa Street, Ikeja, Nig",
                    "return_line1": "31b Simpson Street, Lagos, Nigeria",
                    "carrier_name": "Kwik Delivery",
                    "carrier_logo": "https://ucarecdn.com/d399a2ad-c831-46de-a8fe-94f8056a3c29/60dc787ac0166774ecb59f04_gy2h4u35onr2nrmuapjt.png",
                    "carrier_slug": "kwik",
                    "amount": 2702.26
                },
                "sort": [
                    1694612439789
                ]
            },
            {
                "_index": "shipments",
                "_id": "SH-B7LD62MNVMI1PHY0",
                "_score": null,
                "_source": {
                    "address_to": "AD-GI5O5EXIX857X7V8",
                    "address_from": "AD-KYQVV7EZF0M7AULH",
                    "address_return": "AD-KYQVV7EZF0M7AULH",
                    "parcel": "PC-VTJR1VHPNGP6USTX",
                    "parcels": [],
                    "pickup_date": "2023-09-15T13:30:59.539Z",
                    "cancellation_request": false,
                    "cancellation_reason": "",
                    "shipment_cost_currency": "NGN",
                    "shipment_purpose": "personal",
                    "status": "in-transit",
                    "type": "terminal",
                    "source": "web",
                    "created_source": "web",
                    "user": "USER-22070036153",
                    "events": [
                        {
                            "created_at": "2023-09-13T13:30:59.539Z",
                            "description": "Shipment arranged by Tolulope Oguntade",
                            "location": "Ikeja, NG",
                            "status": "confirmed"
                        },
                        {
                            "created_at": "2023-09-13T00:00:00.000Z",
                            "description": "Shipment picked up",
                            "location": "Lagos-NG",
                            "status": "PU"
                        },
                        {
                            "created_at": "2023-09-13T20:00:20.280Z",
                            "description": "Processed at LAGOS-NIGERIA",
                            "location": "Lagos-NG",
                            "status": "PL"
                        },
                        {
                            "created_at": "2023-09-13T22:30:15.648Z",
                            "description": "Shipment has departed from a DHL facility LAGOS-NIGERIA",
                            "location": "Lagos-NG",
                            "status": "DF"
                        },
                        {
                            "created_at": "2023-09-13T23:30:17.381Z",
                            "description": "Shipment is in transit to destination",
                            "location": "Lagos-NG",
                            "status": "TR"
                        },
                        {
                            "created_at": "2023-09-14T01:00:17.852Z",
                            "description": "Shipment has departed from a DHL facility LAGOS-NIGERIA",
                            "location": "Lagos-NG",
                            "status": "DF"
                        },
                        {
                            "created_at": "2023-09-14T06:30:15.016Z",
                            "description": "Arrived at DHL Sort Facility  PORT HARCOURT-NIGERIA",
                            "location": "Port Harcourt-NG",
                            "status": "AF"
                        },
                        {
                            "created_at": "2023-09-14T07:30:21.627Z",
                            "description": "Shipment has departed from a DHL facility PORT HARCOURT-NIGERIA",
                            "location": "Port Harcourt-NG",
                            "status": "DF"
                        }
                    ],
                    "shipment_id": "SH-B7LD62MNVMI1PHY0",
                    "created_at": "2023-09-13T13:27:23.871Z",
                    "updated_at": "2023-09-14T07:30:21.627Z",
                    "carrier": "CA-81957188177",
                    "delivery_arranged": "2023-09-13T13:30:59.539Z",
                    "delivery_date": "2023-09-18T13:30:50.075Z",
                    "rate": "RT-3ILA3GUL1YFQNQLO",
                    "shipment_cost": 1935.1,
                    "transaction_reference": "TR-HY45ACJCENP34S9UAC3YQ5C48P7RK7M",
                    "tracking_number": "3361371484",
                    "international_tracking_number": "",
                    "reference": "CBJ230914030325",
                    "carrier_tracking_url": "https://www.dhl.com/global-en/home/tracking.html?tracking-id=3361371484",
                    "shipping_label_url": "https://api.terminal.africa/v1/shipments/label/SH-B7LD62MNVMI1PHY0.pdf",
                    "commercial_invoice_url": "https://api.terminal.africa/v1/shipments/commercial-invoice/SH-B7LD62MNVMI1PHY0.pdf",
                    "tracking_url": "https://app.terminal.africa/shipments/track/SH-B7LD62MNVMI1PHY0",
                    "user_email": "parcelsnigeria@gmail.com",
                    "user_phone": "",
                    "user_company_name": "Parcels Nigeria",
                    "user_business_category": "consultant",
                    "user_account_type": "3pl",
                    "user_country": "NG",
                    "user_country_state": "",
                    "user_name": "Tolulope Oguntade",
                    "user_storeId": "dmNhphFCXKTYCCTcQJOPbryn6bB2",
                    "user_wallet": "6278e2739619f23000874d56",
                    "user_referredBy": "",
                    "user_referralCode": "REF-84841000717",
                    "pickup_email": "parcelsnigeria@gmail.com",
                    "delivery_email": "parcelsnigeria@gmail.com",
                    "return_email": "parcelsnigeria@gmail.com",
                    "pickup_name": "Mummy Swift",
                    "delivery_name": "Azubuike Grace Amarachi",
                    "return_name": "Mummy Grace Amarachi",
                    "pickup_city": "Ikeja",
                    "delivery_city": "Warri",
                    "return_city": "Ikeja",
                    "pickup_state": "Lagos",
                    "delivery_state": "Delta",
                    "return_state": "Lagos",
                    "pickup_country": "NG",
                    "delivery_country": "NG",
                    "return_country": "NG",
                    "pickup_zip": "105102",
                    "delivery_zip": "0000",
                    "return_zip": "105102",
                    "pickup_line1": "782b Rev. Emmanuel Adubifa Street, Ikeja, Nig",
                    "delivery_line1": "Old Julius Berger Yard, Km 4 Warri,",
                    "return_line1": "782b Rev. Emmanuel Adubifa Street, Ikeja, Nig",
                    "carrier_name": "DHL Express",
                    "carrier_logo": "https://ucarecdn.com/dcdd8109-af8c-4057-8104-192be821dd6e/download4.png",
                    "carrier_slug": "dhl-ng",
                    "amount": 2322.12
                },
                "sort": [
                    1694611643871
                ]
            }
        ],
        "pagination": {
            "prevPage": null,
            "nextPage": 2,
            "hasNextPage": true,
            "hasPrevPage": false,
            "total": 11234,
            "perPage": 4,
            "currentPage": 1,
            "pageCounter": 1,
            "pageCount": 2809
        }
    }
}
```
Previous
Get Shipments
Next
Get Shipment
Last updated 2 years ago

Get Shipment
Fetch details of a specific shipment.

/shipments/:shipment_id
GET https://api.terminal.africa/v1/shipments/:shipment_id

This endpoint allows you to retrieve details for a shipment.

Path Parameters
Name
Type
Description
id

string

id of shipment.

Headers
Name
Type
Description
Authorization*

string

Set value to Bearer SECRET_KEY

200 Shipment retrieved successfully.

Copy
{
    status: true,
    message: 'Shipment retrieved successfully.',
    data: {
			address_from: {
				address_id: 'AD-00632494667',	
				city: 'Lagos',
				coordinates: {
						lat: 6.5969424,
						lng: 3.3542992
				},	
				country: 'NGA',
				email: 'augustus_obi@shipmonk.ng',
				first_name: 'Augustus',
				id: 'd799c2679e644279b59fe661ac8fa488',
				is_residential: true,
				last_name: 'Obi',
				line1: '1121 Allen Avenue, Ikeja',
				line2: '',
				metadata: {
					my_app_customer_id: 11234
				},
				name: 'Augustus Obi',
				phone: '+2348122340000',
				state: 'Lagos',
				zip: '121006'			
			},
			address_return: {
				address_id: 'AD-00632494667',	
				city: 'Lagos',
				coordinates: {
						lat: 6.5969424,
						lng: 3.3542992
				},	
				country: 'NGA',
				email: 'augustus_obi@shipmonk.ng',
				first_name: 'Augustus',
				id: 'd799c2679e644279b59fe661ac8fa488',
				is_residential: true,
				last_name: 'Obi',
				line1: '1121 Allen Avenue, Ikeja',
				line2: '',
				metadata: {
					my_app_customer_id: 11234
				},
				name: 'Augustus Obi',
				phone: '+2348122340000',
				state: 'Lagos',
				zip: '121006'		
			},
			address_to: {
				address_id: 'AD-95918335217',	
				city: 'London',
				coordinates: {
						lat: 43.653226,
						lng: -79.3831843
				},	
				country: 'GBR',
				email: 'timothy@shipmonk.ng',
				first_name: 'Timothy',
				id: 'S3YLVnGo9eKpMMbEQcWjgCraLqnNY2Oy',
				is_residential: true,
				last_name: 'Odunubi',
				line1: '45 Greenwich Lane, London',
				line2: '',
				metadata: {
					my_app_customer_id: 10567
				},
				name: 'Timothy Odunubi',
				phone: '+447514022567',
				state: '',
				zip: 'SE5 4HB'		
			},
			events: [],
			id: 'BUbL05Ecprhc2q17Xh9woRSwNpXJehay',
			metadata: {},
			parcel: {
				description: true,
				id: 'Zt4Xh2pbbCmeVcr5YH9lsFHGqoW3i5w3',
				items: [{
					description: 'Shoes purchased from Shipmonk Store',
					name: 'Rubber Boots',
					currency: 'NGN',
					value: 25000',
					weight: 2.5
					quantity: 1
				}],
				metadata: {},		
				packaging: 'LsuiGzcYlz4dKRYnEXeobJu9gnVbQVXN',
				parcel_id: 'PC-25164820699',
				total_weight: 2.51,
				weight: 2.5,
				weight_unit: 'kg',
				created_at: '2021-07-13T20:25:53.011Z',
				updated_at: '2021-07-13T20:25:53.011Z'
			},
			rate: '',
			shipment_id: 'SH-40208776515',
			status: 'draft'    
    }
}
Previous
Get Shipments v2
Next
Track a Shipment
Last updated 3 years ago

Track a Shipment
Get tracking details for a shipment.

/shipments/track/:shipment_id
GET https://api.terminal.africa/v1/shipments/track/:shipment_id

This endpoint allows you to track the most recent status of a shipment.

Path Parameters
Name
Type
Description
shipment_id*

String

Unique reference for shipment.

Headers
Name
Type
Description
Authorization*

String

Set value to Bearer SECRET_KEY

200 Shipment tracking status retrieved successfully.

Copy
{
    "status": true,
    "message": "Shipment tracking status retrieved successfully",
    "data": {
        "address_to": {
            "user": "USER-12568655307",
            "city": "Apapa",
            "coordinates": {
                "lat": 6.48,
                "lng": 3.3758384
            },
            "country": "NG",
            "email": "danielozeh@gmail.com",
            "first_name": "Daniel",
            "is_residential": true,
            "last_name": "Ozeh",
            "line1": "045 Oladimeji street",
            "line2": "",
            "phone": "+2348134277988",
            "state": "Lagos",
            "zip": "100123",
            "address_id": "AD-80439326931",
            "created_at": "2022-06-09T11:27:47.885Z",
            "updated_at": "2022-06-09T11:27:47.885Z"
        },
        "address_from": {
            "user": "USER-12568655307",
            "city": "Lagos",
            "coordinates": {
                "lat": 6.6112856,
                "lng": 3.3582179
            },
            "country": "NG",
            "email": "nnamdi@terminal.africa",
            "first_name": "Nnamdi",
            "is_residential": true,
            "last_name": "Okoh",
            "line1": "12 Olaiya street, alausa",
            "line2": "",
            "phone": "+2348122689641",
            "state": "Lagos",
            "zip": "100126",
            "address_id": "AD-77298486083",
            "created_at": "2022-06-10T20:27:14.051Z",
            "updated_at": "2022-06-10T20:27:14.051Z"
        },
        "carrier": {},
        "carrier_tracking_number": "",
        "delivery_arranged": "",
        "delivery_date": "",
        "pickup_date": null,
        "status": "draft",
        "tracking_status": {},
        "events": [],
        "shipment_id": "SH-16380611554"
    }
}
Previous
Get Shipment
Next
Cancel Shipment
Last updated 3 years ago

Cancel Shipment
Cancel pickup for a shipment.

/shipments/cancel
POST https://api.terminal.africa/v1/shipments/cancel

This endpoint allows you to cancel a shipment before carrier pickup.

Headers
Name
Type
Description
Authorization*

string

Set value to Bearer SECRET_KEY

Content-Type

string

Set value to application/json

Request Body
Name
Type
Description
shipment_id*

string

Unique reference for shipment.

200 Shipment canceled successfully.

Copy
{
    status: true,
    message: 'Shipment canceled successfully.',
    data: {
			address_from: {
				address_id: 'AD-00632494667',	
				city: 'Lagos',
				coordinates: {
						lat: 6.5969424,
						lng: 3.3542992
				},	
				country: 'NGA',
				email: 'augustus_obi@shipmonk.ng',
				first_name: 'Augustus',
				id: 'd799c2679e644279b59fe661ac8fa488',
				is_residential: true,
				last_name: 'Obi',
				line1: '1121 Allen Avenue, Ikeja',
				line2: '',
				metadata: {
					my_app_customer_id: 11234
				},
				name: 'Augustus Obi',
				phone: '+2348122340000',
				state: 'Lagos',
				zip: '121006'			
			},
			address_return: {
				address_id: 'AD-00632494667',	
				city: 'Lagos',
				coordinates: {
						lat: 6.5969424,
						lng: 3.3542992
				},	
				country: 'NGA',
				email: 'augustus_obi@shipmonk.ng',
				first_name: 'Augustus',
				id: 'd799c2679e644279b59fe661ac8fa488',
				is_residential: true,
				last_name: 'Obi',
				line1: '1121 Allen Avenue, Ikeja',
				line2: '',
				metadata: {
					my_app_customer_id: 11234
				},
				name: 'Augustus Obi',
				phone: '+2348122340000',
				state: 'Lagos',
				zip: '121006'		
			},
			address_to: {
				address_id: 'AD-95918335217',	
				city: 'London',
				coordinates: {
						lat: 43.653226,
						lng: -79.3831843
				},	
				country: 'GBR',
				email: 'timothy@shipmonk.ng',
				first_name: 'Timothy',
				id: 'S3YLVnGo9eKpMMbEQcWjgCraLqnNY2Oy',
				is_residential: true,
				last_name: 'Odunubi',
				line1: '45 Greenwich Lane, London',
				line2: '',
				metadata: {
					my_app_customer_id: 10567
				},
				name: 'Timothy Odunubi',
				phone: '+447514022567',
				state: '',
				zip: 'SE5 4HB'		
			},
			events: [{
				created_at: '2021-07-10T02:25:30.421Z',
				description: 'Shipment arranged by Augsustus Obi',
				location: 'Lagos-NG',
				status: 'confirmed'
			},{
				created_at: '2021-07-13T12:45:29.728Z',
				description: 'Pickup canceled by Augustus Obi',
				location: 'Lagos',
				status: 'canceled'
			}],
			id: 'BUbL05Ecprhc2q17Xh9woRSwNpXJehay',
			metadata: {},
			parcel: {
				description: true,
				id: 'Zt4Xh2pbbCmeVcr5YH9lsFHGqoW3i5w3',
				items: [{
					description: 'Shoes purchased from Shipmonk Store',
					name: 'Rubber Boots',
					currency: 'NGN',
					value: 25000',
					weight: 2.5
					quantity: 1
				}],
				metadata: {},		
				packaging: 'LsuiGzcYlz4dKRYnEXeobJu9gnVbQVXN',
				parcel_id: 'PC-25164820699',
				total_weight: 2.51,
				weight: 2.5,
				weight_unit: 'kg'		
			},
			rate: 'bQVMwQZndHbIq6PQD5oiaGWxetLCXGkp',
			shipment_id: 'SH-40208776515',
			status: 'canceled',
			created_at: '2021-07-13T20:25:53.011Z',
			updated_at: '2021-07-13T20:25:53.011Z'			    
    }
}
Previous
Track a Shipment
Next
Delete Shipment
Last updated 3 years ago

Delete Shipment
Delete a shipment

/shipments
DELETE https://api.terminal.africa/v1/shipments

This endpoint allows you to delete a draft shipment.

Headers
Name
Type
Description
Authorization*

string

Set value to Bearer SECRET_KEY

Content-Type*

string

Set value to application/json

Request Body
Name
Type
Description
shipment_id*

string

Unique id of shipment.

200 Shipment deleted successfully.

Copy
{
	status: true,
	message: 'Shipment deleted successfully',
	data: null
}
Previous
Cancel Shipment
Next
Duplicate Shipment
Last updated 3 years ago

Arrange Pickup & Delivery for Shipment
/shipments/pickup
POST https://api.terminal.africa/v1/shipments/pickup

This api endpoint allows you to arrange pickup for a shipment.

Headers
Name
Type
Description
Authorization*

String

Set value to Bearer SECRET_KEY

Content-Type

String

Set value to application/json

Request Body
Name
Type
Description
dropoff_id

String

Unique reference for Drop off locations.

duty_payer

Enum

Indicate if payer for import duties is account_holder, sender or receiver. 

rate_id*

String

Unique reference of selected rate.

shipment_id

String

Unique id of existing draft shipment. If shipment_id is not provided, a new shipment is generated automatically.

purchase_insurance

Boolean

Use this to indicate if insurance coverage should be provided for the shipment.

cash_to_collect

Number

Cash to be collected by riders. Required if rate_id passed is a cash_on_delivery rate

200 Pickup for shipment arranged successfully.

Copy
{
    status: true,
    message: 'Pickup for shipment arranged successfully.',
    data: {
			address_from: {
				address_id: 'AD-00632494667',	
				city: 'Lagos',
				coordinates: {
						lat: 6.5969424,
						lng: 3.3542992
				},	
				country: 'NGA',
				email: 'augustus_obi@shipmonk.ng',
				first_name: 'Augustus',
				id: 'd799c2679e644279b59fe661ac8fa488',
				is_residential: true,
				last_name: 'Obi',
				line1: '1121 Allen Avenue, Ikeja',
				line2: '',
				metadata: {
					my_app_customer_id: 11234
				},
				name: 'Augustus Obi',
				phone: '+2348122340000',
				state: 'Lagos',
				zip: '121006'			
			},
			address_return: {
				address_id: 'AD-00632494667',	
				city: 'Lagos',
				coordinates: {
						lat: 6.5969424,
						lng: 3.3542992
				},	
				country: 'NGA',
				email: 'augustus_obi@shipmonk.ng',
				first_name: 'Augustus',
				id: 'd799c2679e644279b59fe661ac8fa488',
				is_residential: true,
				last_name: 'Obi',
				line1: '1121 Allen Avenue, Ikeja',
				line2: '',
				metadata: {
					my_app_customer_id: 11234
				},
				name: 'Augustus Obi',
				phone: '+2348122340000',
				state: 'Lagos',
				zip: '121006'		
			},
			address_to: {
				address_id: 'AD-95918335217',	
				city: 'London',
				coordinates: {
						lat: 43.653226,
						lng: -79.3831843
				},	
				country: 'GBR',
				email: 'timothy@shipmonk.ng',
				first_name: 'Timothy',
				id: 'S3YLVnGo9eKpMMbEQcWjgCraLqnNY2Oy',
				is_residential: true,
				last_name: 'Odunubi',
				line1: '45 Greenwich Lane, London',
				line2: '',
				metadata: {
					my_app_customer_id: 10567
				},
				name: 'Timothy Odunubi',
				phone: '+447514022567',
				state: '',
				zip: 'SE5 4HB'		
			},
			events: [{
				created_at: '2021-07-10T02:25:30.421Z',
				description: 'Shipment arranged by Augsustus Obi',
				location: 'Lagos-NG',
				status: 'confirmed'
			}],
			extras: {
				tracking_number: '12945827642',
				tracking_url: 'https://www.dhl.com/global-en/home/tracking/tracking-express.html?submit=1&tracking-id=12945827642'
			},
			id: 'BUbL05Ecprhc2q17Xh9woRSwNpXJehay',
			metadata: {},
			parcel: {
				description: true,
				id: 'Zt4Xh2pbbCmeVcr5YH9lsFHGqoW3i5w3',
				items: [{
					description: 'Shoes purchased from Shipmonk Store',
					name: 'Rubber Boots',
					currency: 'NGN',
					value: 25000',
					weight: 2.5
					quantity: 1
				}],
				metadata: {},		
				packaging: 'LsuiGzcYlz4dKRYnEXeobJu9gnVbQVXN',
				parcel_id: 'PC-25164820699',
				total_weight: 2.51,
				weight: 2.5,
				weight_unit: 'kg'		
			},
			rate: 'bQVMwQZndHbIq6PQD5oiaGWxetLCXGkp',
			shipment_id: 'SH-40208776515',
			status: 'confirmed',
			created_at: '2021-07-13T20:25:53.011Z',
			updated_at: '2021-07-13T20:25:53.011Z'
    }
}
Previous
Duplicate Shipment
Next
Transactions
Last updated 5 months ago

