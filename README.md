# mbta-tracker
This Python application uses the [MBTA v3 API](https://www.mbta.com/developers/v3-api) to provide a RESTful API for Boston's subway, lightrail, and Commuter Rail lines. Below is an example request is for the inbound Lowell Commuter Rail prediction from Lowell and response (note: API is not currently live):

  **Request:** 
  ```
  http://mbta-tracker-backend-api.com/prediction?stop=place-NHRML-0254&route=CR-Lowell&direction=1
  ```
  **Response:**
  ```
	{
		"status": None,
		"predictedTime": 2020-02-22T15:11:04-05:00,
		"alert": None
	}
```

It was deployed to Google Cloud Platform via Kubernetes (it has since been removed to save costs until further development). The end goal is to develop a mobile app that provides prediction times, status, and alerts for a user's favorite rail lines. You can see the progress for the mobile app development [here](https://github.com/ehean/MBTA-Tracker-Mobile-App). 

The repo is divided into the following directories:
* deploy - kubernetes deployment templates
* scripts - useful scripts for testing/deploying/etc.
* src - source code
* test - unit tests
