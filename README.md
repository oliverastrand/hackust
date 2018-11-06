# Hong Kong Hackathon hackUST
A mobile application created in Django called UberTourism that creates itineraries for tourists for specific cities. This is done by scraping TripAdvisor and using Google Maps API to calculate distances between attractions. Through this we are able to offer recommended full-day itineraries, information about each attraction, and the ability to order Ubers to easily travel between the attractions. 

Note that in the final version that we presented (folder "hackustFinalVersion") the full functionality with TripAdvisor and Google Maps API is not completely implemented due to time constrictions during the Hackathon.

| Choosing city  | Itinerary overview | Attraction details |
| ------------- | ------------- | -------------- |
| <img src="https://github.com/oliverastrand/hackust/blob/phase_one_final/ProjectScreenshots/Choose%20city.png" width="300"> | <img src="https://github.com/oliverastrand/hackust/blob/phase_one_final/ProjectScreenshots/Itinerary%20overview.png" width="300">  | <img src="https://github.com/oliverastrand/hackust/blob/phase_one_final/ProjectScreenshots/Attraction%20details.png" width="300">|

# Install
sudo pip3 install geopy<br />
sudo pip3 install googlemaps<br />
sudo pip3 install Wikipedia

Run with the following command while in the folder hackust/hackust/:

```bash
$ python manage.py runserver
```
