Basics
Sendbox API are HTTP based RESTful APIs. API request and response format are in JSON.  

All request should be issued using HTTP protocol

All request requires authentication 

Content type for responses will always be application/json 

API Request 
To construct an API request the following components are required. 

Component 

Description 

The HTTP method

GET. Request  data from resource

POST . Submit data to a resource to process 

PUT . Update a resource 

DELETE . Deletes a resource  

The URL to the staging API service

https://sandbox.staging.sendbox.co/shipping

The URL to the live API service 

https://live.sendbox.co/shipping/

HTTP request header 

Includes the Content-type header with the value application/json 

A JSON request body

required for making a request

You are advised to make all test request on the staging API and ensure there are no errors before you deploy to users using the live API 

API response 
This describes the response format for Sendbox API 

Sendbox API calls return HTTP status codes in the response headers. API calls also return JSON response bodies that include information about the resource.

Each REST API request returns a success or error HTTP status code.we will talk about errors latter in the docs but for now, we will focus on success. 

status code

Description 

200

A successful GET request 

201

A successful POST, PUT request means your request is created or updated.

Fetching Data
Fetching data means you will like to retrieve data from a resource. Most times, you are required to set header parameters usually the content-type and the authorization key and make a get request to an endpoint. For example, let say we want to get all shipments, we can simply make a get request and a successful request will come back with a 200 status code and return all the shipments in JSON format.

Fetch Data
https://sandbox.staging.sendbox.co/shipping

https://live.sendbox.co/shipping/shipments

In this example, we are making a get request to shipment endpoint to fetch all shipments 

Request
Response
Headers 
Name

Type

Description

Authorization

String

Authorization-key

Content-type

String

application/json

Posting Data
Posting data is a little different from fetching data. here you are required to make a post request to the endpoint and pass in a body of JSON data you would like to post. For example, let's say you want to get delivery quotes for a shipment. You simply make a post request to the delivery quotes endpoint this returns a status code 201 and quotes of that shipments in JSON format. 

JSON body sample to make a post request


Copy
{
"origin_country":"Nigeria",
"origin_country_code":"NG", 
"origin_state" : "Lagos",
"destination_country":"Nigeria",
"destination_country_code":" ",
"destination_state": "Abuja",
"weight" : 3,
"destination_state_code":"ABV",
"origin_state_code": "LOS"
}
Post Data
https://sandbox.staging.sendbox.co/shipping/shipment_delivery_quote

https://live.sendbox.co/shipping/shipment_delivery_quote

In this example, we are making a post request to the shipment_delivery_quote endpoint.

Request
Response
Headers
Name

Type

Description

Authorization

String

Authorization-key

Content-type

String

application/json

Body Parameters 
Name

Type

Description

origin_country

String

senders country

origin_country_code

String

senders country code

origin_state

String

senders state

origin_state_code

String

senders state code 

destination_country

String

recipient country 

destination_country_code

String

recipient country code 

destination_state

String

recipient state

destination_state_code

String

recipient state code 

weight

float

weight of package 

Errors
Some errors might be encountered after an API request is made and a response is returned.

Validation Errors 
Validation errors occurs when one or more validation rules are not met. For example, not passing a required field in the body of a request this causes a 409 error 

Status code : 409 - Conflict error  


Copy
{
    "required field": [
        "error message"
    ]
}
Authentication Errors  
Authentication errors occur when you fail to authenticate a request or pass the correct authentication key or when you pass in an invalid key. For example making a request without an authorization key. 

Status code : 401 - unauthorized 


Copy
{
    "description": "Please provide an auth token as part of the request.",
    "title": "Auth token required"
}
Another instance of authentication error is making a request with a key that doesn't have permission to perform that request.

Status code : 403 forbidden  


Copy
{
"message" :"error message"
}
Other Errors
Status Code 

Description 

400 

The request could not be fulfilled because it already exists or is a bad request

404

The request could not be fulfilled as the request resources does not exist.   

500, 501

This request could not be completed quickly contact Sendbox if you encounter any of these response. it almost never happens

Authentication
Introduction
This document provides guidelines on how to authenticate your application with the Sendbox API. This updated version includes streamlined authentication processes and reflects recent changes to the API.

Getting Started
To integrate with the Sendbox API, you'll need to create an application and obtain an access token, which will be used for all subsequent API requests. Here's how to get started: 

It is important to note that all development and testing are done on staging. Once completed, remember to update the production URL and follow all the same steps. 

https://developers.sendbox.co/

Environment

Developer Dashboard URL

Base URL

Staging

https://developers.staging.sendbox.co/


https://sandbox.staging.sendbox.co/

Production

https://developers.sendbox.co/

https://live.sendbox.co/ 

 Create a New Application
Sign Up: Visit Sendbox for Developers and sign up for an account if you haven’t already.

Dashboard: After signing in, navigate to your dashboard and create a new application. You will need to provide the following details:

Name: The name of your application.

Description: A brief description of what your application does.

Webhook URL: The URL where Sendbox will send event notifications for your application.

After submitting this information, your application will be created successfully. Keep your application keys in a safe place as they will be required for making API requests.

 Authorization
Once your application is created, you'll be issued an access token. This token is crucial for authorizing API requests.

Access Token: The access token is used to authenticate your application. It should be included in the header of every API request.

 Making API Requests
To interact with the Sendbox API, include your access token in the header of your HTTP requests as shown below:


Copy
GET /your/api/endpoint
Host: live.sendbox.co
Authorization: {your-access-token}
Authorization Header:
The header must include the Authorization key, followed by  your access token.

Permanent Tokens
Please note that access tokens are now permanent and do not expire. There is no need to handle token refresh mechanisms.


Get Shipments
To get all shipments, you need to make a get request to the shipments' endpoint ensure to pass the required header parameters to get the appropriate response.

Get Shipments
https://live.sendbox.co/shipping/shipments    

This gets all the shipments

Request
Response
Headers
Name

Type

Description

Authorization

String

Authorization-key

Content-type

String

application/json


Copy
Staging URL: https://sandbox.staging.sendbox.co/shipping/shipments

Get Shipment
To get a particular shipment, you need to make a call to the shipments endpoint and pass id as a path parameter to get the appropriate response.

Get Shipment
https://live.sendbox.co/shipping/shipments/:id    

This gets a particular shipment by id 

Request
Response
Path Parameters
Name

Type

Description

id

number

the shipment id

Headers
Name

Type

Description

Authorization

String

Authorization-key

Content-type

String

application/json


Copy
Staging URL: Staging URL: https://sandbox.staging.sendbox.co/shipping/shipments/:id

Request Shipping Quotes
Getting shipment quotes requires you making a post request to the shipment delivery quote endpoint ensure to pass the required header parameters and body parameters to get the appropriate response.

A sample payload to request shipment quotes


Copy
{
        "origin" : {
            "first_name" : "Will",
            "last_name" : "Smith",
            "street" : "10 Olasheun Crescent",
            "street_line_2" : "HQ",
            "state" : "Lagos",
            "email" : null,
            "city" : "Obanikoro",
            "country" : "NG",
            "post_code" : "102216",
            "phone" : "+234 800 666 0419",
            "lng" : 3.37,
            "lat" : 6.56,
            "name" : null
        },
    "destination": {
        "first_name": "Joe",
        "last_name": "Goldberg",
        "post_code": "94612",
        "phone": "+1 267 000 0",
        "lng": -122.27,
        "lat": 37.81,
        "name": null,
        "street": "31 Hall Crescent",
        "street_line_2": "",
        "state": "paris",
        "email": "",
        "city": "paris",
        "country": "FR"
    },
    "weight" : 2,
        "dimension" : {
            "length" : 1,
            "width" : 1,
            "height" : 1
        },
        "incoming_option" : "pickup",
        "region" : "NG",
        "service_type" : "international",
        "package_type" : "general",
        "total_value" : 15000,
        "currency" : "NGN",
        "channel_code" : "api",
        "pickup_date" : "2023-07-20",
        "items" : [
            {
                "item_type" : "snail",
                "hts_code": "9001.21",
                "quantity" : 2,
                "name" : "African Wax Fabrics - Orange Lace Fabric that is Not Woven",
                "value" : 1500
            }
        ],
        "service_code": "standard",
        "customs_option": "recipient"
}
Adding currency to the shipping quotes payload will return quotes in whatever currency that was passed.

Service code value can be either one of the following: standard, premium or expedient. You can default it in your request. 


Copy
Staging URL: Staging URL: https://sandbox.staging.sendbox.co/shipping/shipment_delivery_quote
Get Shipping Quotes
https://live.sendbox.co/shipping/shipment_delivery_quote

This gets shipping quotes 

Request
Response
Headers
Name

Type

Description

Authorization

String

Authorization-key

Content-type

String

application/json

Body Parameters
Name

Type

Description

origin

object

senders details

destination

object

recipient details

currency

String

shop currency

weight

float

weight of package 

dimension

object

dimension details

incoming_option

string

incoming option can be pick up or drop off

region

string

what region is the package is shipped from

service_type

string

set to either international or local

package_type

string

package type

total_value

float

value of shipment

channel_code

string

channel the request is being made from in this case set it to api

pickup_date

string

date package is picked up

items

array

An array of objects that contain: 

 - name [String]

 - weight [Float]

 - item_type_code [String optional]

 - hts_code [String optional]

 - description [String]

 - quantity  [Integer]

 - value [Float]

service_code

string

can be set to international, local or nation-wide

customs_option

string

custom optionsCreate New Shipment
Creating a new shipment requires you making a post request to the shipment endpoint ensure to pass the required header parameters and body parameters to get the appropriate response

Sample Payload to request shipment 

Copy
{
        "origin" : {
            "first_name" : "Will",
            "last_name" : "Smith",
            "street" : "10 Olasheun Crescent",
            "street_line_2" : "HQ",
            "state" : "Lagos",
            "email" : null,
            "city" : "Obanikoro",
            "country" : "NG",
            "post_code" : "102216",
            "phone" : "+234 800 666 0419",
            "lng" : 3.37,
            "lat" : 6.56,
            "name" : null
        },
    "destination": {
        "first_name": "Joe",
        "last_name": "Goldberg",
        "post_code": "94612",
        "phone": "+1 267 000 0",
        "lng": -122.27,
        "lat": 37.81,
        "name": null,
        "street": "31 Hall Crescent",
        "street_line_2": "",
        "state": "paris",
        "email": "",
        "city": "paris",
        "country": "FR"
    },
    "weight" : 2,
        "dimension" : {
            "length" : 1,
            "width" : 1,
            "height" : 1
        },
        "incoming_option" : "pickup",
        "region" : "NG",
        "service_type" : "international",
        "package_type" : "general",
        "total_value" : 15000,
        "currency" : "NGN",
        "channel_code" : "api",
        "pickup_date" : "2023-07-20",
        "items" : [
            {
                "item_type" : "snail",
                "hts_code":"9000.10",
                "quantity" : 2,
                "name" : "African Wax Fabrics - Orange Lace Fabric that is Not Woven",
                "value" : 1500
            }
        ],
        "service_code": "standard",
        "customs_option": "recipient",
        "callback_url":"https://your_callback_url/"
        
}
 

Copy
Staging URL: https://sandbox.staging.sendbox.co/shipping/shipments
Create New Shipment
https://live.sendbox.co/shipping/shipments

This creates a new shipment

Request
Response
Headers
Name

Type

Description

Authorization

String

Authorization-key

Content-type

String

application/json

Body Parameters 
Name

Type

Description

origin

Object

senders details

destination

Object

recipient details

weight

Float

weight of package 

items

Array

An array of objects that contain: 

 - name [String]

 - weight [Float]

 - item_type_code [String optional]

 - hts_code [String optional]

 - description [String]

 - quantity  [Integer]

 - value [Float]

 

incoming_option

String

set to either pickup or dropoff

pickup_date

Date

date in ISO format 

total_value

Float

value of shipment

package_type

String

package type

channel_code 

String

channel the request is being made from; in this case set it to api

service_code

String

can be set to either international, nation-wide, and local.

region

String

region the shipment is being shipped from.

custom_options

String

custom options

callback_url

String

a webhook url to get the tracking update.

hts_code

String

pass in the item code to match it's description.

Payload Explained 
While some of the payloads are self explained, lets go over some of them that seem a bit confusing. 

channel_code 
This tells us where the request came from this case it's form the api. 

Items
This is an array of objects. It includes the name of what you are shipping, weight, item_type_code, package_size_code, a value which is the total price of the item(s) you are shipping, and quantity of your shipment. An example of an items payload will look like this 


Copy
"items": [
		{
			"name": "Laptop",
			"item_type_code": "other",
			"hts_code": "9001.10",
			"package_size_code": "medium",
			"quantity": 2,
			"weight": 3,
			"value":120000
		}
	]
Callback_url 
This should be a webhook url which you will pass with your other request shipment payloads. Sendbox will post tracking updates to this url from pending, processing and completed.

Fund your staging account
To stimulate a successful request on your staging account you have to fund your staging account by making a post to add_money endpoint

https://sandbox.staging.sendbox.co/payments/add_money
sandbox.staging.sendbox.co
Request
Response

Copy
{
  "amount": 10000
}
Check your staging account balance 
You can simply do this by doing a get to the staging payment profile

https://sandbox.staging.sendbox.co/payments/profile 

Stimulate webhooks events 
You can stimulate webhook events for tracking status on staging by sending tracking code to move_tracking endpoint

https://sandbox.staging.sendbox.co/shipping/move_tracking


Copy
{
  code: <tracking_code>
}

Calculate Landed Cost
This endpoint calculates the total landed cost of a shipment. To retrieve the landed cost, send a POST request to the landed cost endpoint using the same payload as required for the create shipment request. This will return the full breakdown of costs, including taxes, duties, and shipping fees, providing an accurate total cost for the shipment.

API Reference
POST   https://sandbox.staging.sendbox.co/shipping/landed_cost_estimate

Headers

Name
Value
Content-Type

application/json

Authorization

authorization-token

Body

Name
Type
Description
origin

object

Senders details

destination

object

Recipient details

weight

float

Weight of package

items

array

An array of objects that contain: 

 - name [String]

 - weight [Float]

 - item_type_code [String optional]

 - hts_code [String optional]

 - description [String]

 - quantity  [Integer]

 - value [Float]

incoming_option

string

set to either pickup or dropoff

pickup_date

date

date in ISO format 

total_value

float

value of shipment

service_code

string

can be set to either international, nation-wide, or local.

package_type

string

package type

channel_code

string

channel the request is being made from; in this case set it to api

region

string

region the shipment is being shipped from.

callback_url

string

a webhook url to get the tracking update.

hts_code

string

pass in the item code to match it's description.

Response

200

Copy
{
    "customs_option": "sender",
    "dimension": {
        "length": 1.0,
        "width": 1.0,
        "height": 1.0
    },
    "incoming_option": "pickup",
    "estimate": {
        "code": "duties_and_taxes",
        "name": "Duties and taxes",
        "description": "import duties and taxes",
        "value": 18.93,
        "breakdown": [
            {
                "code": "duties",
                "name": "Duties",
                "description": "",
                "value": 0.0
            },
            {
                "code": "taxes",
                "name": "Taxes",
                "description": "",
                "value": 12.22
            },
            {
                "code": "fees",
                "name": "Fees",
                "description": "",
                "value": 6.71
            }
        ],
        "exchange_rate": 1669.025
    },
    "weight": 0.2,
    "currency": "NGN",
    "service_code": "standard",
    "origin": {
        "country": "NG",
        "lat": 6.56,
        "post_code": "102216",
        "first_name": "Emotu",
        "state": "abuja",
        "city": "maitama",
        "lng": 3.37
    },
    "destination": {
        "country": "GB",
        "lat": 37.81,
        "post_code": "94612",
        "first_name": "Ubani",
        "state": "london",
        "city": "london",
        "last_name": "Balogun",
        "lng": -122.27
    },
    "items": [
        {
            "name": "African Wax Fabrics - Orange Lace Fabric that is Not Woven",
            "item_type": "herbal_tea",
            "value": 100000.0,
            "quantity": 4,
            "weight": 0.5,
            "hts_code": "1211.90.8980",
            "disclaim": true
        }
    ],
    "service_type": "international",
    "total_value": 100000.0,
    "pickup_date": "2023-07-20T07:17:10.582Z",
    "package_type": "general",
    "region": "NG",
    "instance_id": "6136dfa6a1ab9d318bcfcb94",
    "user_id": "61f3f297f0bb8f001a8a34e0",
    "entity_id": null
}

Tracking Shipment
Tracking a shipment requires you make a post request to the tracking endpoint, passing the shipment tracking number in the body of your request.

Track Shipment 
https://live.sendbox.co/shipping/tracking

This tracks a shipment 

Request
Response
Headers
Name

Type

Description

Authorization

String

Authorization-key

Content-type

String

application/json

Body Parameters 
Name 

Type

Description

code

String

shipment tracking code


Copy
Staging URL: https://sandbox.staging.sendbox.co/shipping/tracking
Tracking Response 
At different times, there are different tracking status in the payload. Sendbox allows you track your shipment in real-time. 

Book on hold
This means the shipment hasn't been paid for. User might need to fund their account to complete their shipment request. it comes back with code:"drafted" as the status code in the response.

Pending
This means the shipment request was successful and is waiting to be picked up.  comes back with code:"pending" as the status code in the response.

Pick up started
This means shipment has been picked up. comes back with code:"pickup_started" as the status code in the response.

Pick up completed 
This means the pick up process has been completed. comes back with code:"pickup_completed" in the status code response.

Delivery Started 
This means the delivery process has started. comes back with code:in_delivery in the status code response.

In Transit 
This means delivery is in transit and it's updated in real-time. Comes back with code:"in_transit" as the status code in the response.

Delivered 
This means the entire process has been completed and the shipment has been delivered. Comes back with code:"deliverd" as the status code in the response. 

Saved Addresses
Sendbox gives you access to user's saved addresses so you can easily get addresses used before that are saved. Make a request to saved address endpoint and pass in right header parameters.

https://live.sendbox.co/auth/addresses​

Request
Response
Headers
Name

Type

Description

Authorization

String

Authorization-Key

Content-Type

String 

application/json

