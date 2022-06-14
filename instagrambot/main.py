# imports
from instapy import InstaPy
from instapy import smart_run

# login credentials
insta_username = input("Enter Instagram Username")
insta_password = input("Enter Instagram Password")
# get an InstaPy session!
# set headless_browser=True to run InstaPy in the background
session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=False)

with smart_run(session):
  """ Activity flow """		
  # general settings			
  
  # activity		
  nonfollowers = session.pick_nonfollowers(username=insta_username, live_match=True, store_locally=True)
  print(nonfollowers)
