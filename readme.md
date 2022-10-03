POST requests are sent to this endpoint
==

***Endpoint - ...***


_With the help of this script, requests are received and processed, 
converted into the required format and transmitted to crm in the form of a task / transaction / company/contact_

---


* A request with an empty value of the field *"INN"* will not be accepted
* If the server accepted the request, the response will be - *202*
* If an internal error has occurred, the response will be - *500*
* If the request is different from what was in the example (not all fields are passed), the response will be- *422* + information about which fields are missing in *JSON format*

---


* The value of the field *"Bank"* by default: *"Not filled in"*
