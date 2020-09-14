
Functionality
-------------


1. How are you?
2. What time is it?
3. Where is? - Google Maps (B).
4. What is the weather in? - OpenWeatherMap (C).
5. Search? - Google (B).
6. Calendar? - GCal (show next 5/10 events) (C).
7. Sites? -> list  possibilities.
8. "Reddit"/"Golem" etc. to choose which site to open BY NAME (B).
9. Open - Spotify/Messenger.
11. Chuck Norris? - get a random joke (C).
12. Numbers? - random number facts (C).
13. Advice? - random advice (C).
15. Who is + 2 names? - wikipedia (C)
10. Stop Listening/Thank you.



CHANGES
--------

- used to open browser like that
	location_url = "https://www.google.com/search?q=" + sentence
	site_arg = '/usr/bin/open -a  "/Applications/Brave Browser.app"  ' + location_url
	os.system(site_arg)

-> changed to: webbrowser.open(URL)


- Pick a random name from a list to call me.
- changed "news" to be "sites" command.
- changed the site references from triggers "1/2/3" to their respective names "reddit/golem" etc.
- changed some variables to constants
- added a configurations file, moved the constants there

