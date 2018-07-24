from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import PlaceCategory, Base, Place, User

# -*- coding: utf-8 -*-
 
engine = create_engine('postgresql://catalog:catalog@localhost:5432/catalogdb')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



# Create dummy user
User1 = User(name="Dan", email="danvieira2@gmail.com")
session.add(User1)
session.commit()

#Menu for UrbanBurger
category1 = PlaceCategory(user_id=1, name = "Parks")

session.add(category1)
session.commit()

place2 = Place(user_id=1, name = "Seven Presidents Oceanfront Park", description = "Public ocean park featuring a mile of sandy beach & 38 acres of land, plus restrooms & showers.", price = "free", category = category1)

session.add(place2)
session.commit()


place1 = Place(user_id=1, name = "Hartshorne Woods Park", description = "Forested park home to WWII-era bunkers, popular for 14 miles of hiking, biking & equestrian trails.", price = "free", category = category1)

session.add(place1)
session.commit()

place2 = Place(user_id=1, name = "Fort Hancock", description = "National historic landmark & park featuring a museum exhibiting coastal defense gun batteries.", price = "per car: $15.00", category = category1)

session.add(place2)
session.commit()

place3 = Place(user_id=1, name = "Sunset Park", description = "A lake park close to concert venues and restaurants.", price = "free", category = category1)

session.add(place3)
session.commit()

place4 = Place(user_id=1, name = "Joe Palaia Park Addition", description = "The former Deal Test Site boasts trails, fields & a role in the history of wireless communication.", price = "free", category = category1)

session.add(place4)
session.commit()

place5 = Place(user_id=1, name = "Huber Woods Park", description = "Park with 360+ acres of green space, multi-use trails & an environmental center with exhibits.", price = "free", category = category1)

session.add(place5)
session.commit()

place6 = Place(user_id=1, name = "Henry Hudson Trail / Popamora Point", description = "Hidden bay beach with views of Sandy Hook and NYC", price = "free", category = category1)

session.add(place6)
session.commit()

place7 = Place(user_id=1, name = "Mount Mitchill Scenic Overlook", description = "At 266 feet, this overlook in Atlantic Highlands sits on the highest natural elevation on the  Atlantic seaboard (excluding islands) from Maine to the Yucatan providing beautiful views of Sandy Hook, Sandy Hook Bay, Raritan Bay and the New York skyline.", price = "free", category = category1)

session.add(place7)
session.commit()




#Menu for Super Stir Fry
category2 = PlaceCategory(user_id=1, name = "Outdoor Activities")

session.add(category2)
session.commit()


place1 = Place(user_id=1, name = "Monmouth Park", description = "An American race track for thoroughbred horse racing ", price = "$5.00", category = category2)

session.add(place1)
session.commit()

place2 = Place(user_id=1, name = "Hollywood Golf Club", description = "Hollywood Golf Club is home to a well renowned championship golf course designed by Walter J. Travis in 1917 and masterfully restored to its original intent by Tom Doak and Renaissance Golf Design in 2014.", price = "inquire", category = category2)

session.add(place2)
session.commit()

place3 = Place(user_id=1, name = "Asbury Splash Park", description = "Beachside kids playground in a small, gated area with various whimsical fountains & padded grounds.", price = "$14.50", category = category2)

session.add(place3)
session.commit()

place4 = Place(user_id=1, name = "Long Branch Beach", description = "Beach in Long Branch, NJ", price = "$7.00", category = category2)

session.add(place4)
session.commit()

place5 = Place(user_id=1, name = "Sandy Hook Beach", description = "Large Beach with restaurant and views of NYC.", price = "per car: $15.00", category = category2)

session.add(place5)
session.commit()

place6 = Place(user_id=1, name = "Ocean Grove Beach", description = "Beach in Victorian town of Ocean Grove. Closed on Sundays", price = "$6.00", category = category2)

session.add(place6)
session.commit()




#Menu for Panda Garden
category3 = PlaceCategory(user_id=1, name = "Indoor Activities")

session.add(category3)
session.commit()


place1 = Place(user_id=1, name = "Escape the Puzzle", description = "Escape Rooms in Long Branch NJ", price = "$60.00", category = category3)

session.add(place1)
session.commit()

place2 = Place(user_id=1, name = "Silverball Museum", description = "Boardwalk game arcade starring pinball machines from the 1930s to the present, plus a snack bar.", price = "$14.99", category = category3)

session.add(place2)
session.commit()

place3 = Place(user_id=1, name = "Asbury Lanes", description = "Bustling bowling center for league & individual play, plus onsite cafe & live entertainment.", price = "$12.99", category = category3)

session.add(place3)
session.commit()

place4 = Place(user_id=1, name = "Asbury Park Convention Hall", description = "Restored waterfront boardwalk offers iconic music venues, bars, restaurants, shopping & an arcade.", price = "free", category = category3)

session.add(place4)
session.commit()

place2 = Place(user_id=1, name = "Sky Zone Trampoline Park", description = "Chain of indoor trampoline parks featuring freestyle bouncing, dodgeball, fitness programs & more.", price = "$19.99", category = category3)

session.add(place2)
session.commit()


#Menu for Thyme for that
category4 = PlaceCategory(user_id=1, name = "Bars")

session.add(category4)
session.commit()


place1 = Place(user_id=1, name = "Jack's Goal Line Stand", description = "Casual haunt featuring basic bar food, craft brews & TVs tuned to sports in a laid-back atmosphere.", price = "happy hour: $5.00 beers", category = category4)

session.add(place1)
session.commit()

place2 = Place(user_id=1, name = "The Wine Loft", description = "Upscale spot for wine by the glass or bottle served alongside eclectic tapas in a refined setting.", price = "$20 - $500 per bottle", category = category4)

session.add(place2)
session.commit()

place3 = Place(user_id=1, name = "Asbury Festhalle & Biergarten", description = "Upbeat restaurant & bar with German food, frequent music & a rooftop patio, plus an array of beer.", price = "happy hour: $6.00 beers", category = category4)

session.add(place3)
session.commit()

place4 = Place(user_id=1, name = "Johnny Mac House of Spirits", description = "Eccentric watering hole with cozy smoking chairs & draft beer galore plus free pizza with a drink.", price = "happy hour: $5.00 beers", category = category4)

session.add(place4)
session.commit()

place5 = Place(user_id=1, name = "The Anchor's Bend", description = "Vibrant, beachfront hangout serving up draft brews, cocktails & American plates amid nautical decor.", price = "happy hour: $7.00 cocktails", category = category4)

session.add(place5)
session.commit()

place2 = Place(user_id=1, name = "Donovan's Reef", description = "Chill hangout by the beach with a pub menu, outdoor tiki bar & patio, plus a lineup of live bands.", price = "happy hour: $6.00 beers", category = category4)

session.add(place2)
session.commit()



#Menu for Tony's Bistro
category5 = PlaceCategory(user_id=1, name = "Museums")

session.add(category5)
session.commit()


place1 = Place(user_id=1, name = "Historical Society of Ocean Grove", description = "Historical artifacts related to the history of Ocean Grove.", price = "free", category = category5)

session.add(place1)
session.commit()

place2 = Place(user_id=1, name = "InfoAge - Science History Learning Center and Museum", description = "Exhibits on radio, computers, electronics & warfare technology housed at a former military base.", price = "$9.00", category = category5)

session.add(place2)
session.commit()

place3 = Place(user_id=1, name = "Allen House", description = "Built around 1710, this building houses a museum that recreates its time as an 18th-century tavern.", price = "$8", category = category5)

session.add(place3)
session.commit()

place4 = Place(user_id=1, name = "Eatontown Historical Museum", description = "Charming 18th-century residence & museum offering weekly tours of its period-furnished surrounds", price = "free", category = category5)

session.add(place4)
session.commit()



# ne category
category6 = PlaceCategory(user_id=1, name = "Shopping")

session.add(category6)
session.commit()


place1 = Place(user_id=1, name = "Monmouth Mall", description = "Hundreds of stores", price = "various", category = category6)

session.add(place1)
session.commit()

place2 = Place(user_id=1, name = "Neptune Shopping Center", description = "Dozens of outlets for various brands", price = "various", category = category6)

session.add(place2)
session.commit()

place3 = Place(user_id=1, name = "Pier Village", description = "Shops and restaurants on the shore", price = "various", category = category6)

session.add(place3)
session.commit()

place4 = Place(user_id=1, name = "Brave New World", description = "Surf and Snow clothing gear", price = "various", category = category6)

session.add(place4)
session.commit()




#Menu for Auntie Ann's
category7 = PlaceCategory(user_id=1, name = "Concert Venues")

session.add(category7)
session.commit()

place9 = Place(user_id=1, name = "Stone Pony", description = "National acts headline this rocking, historic music club known for launching Springsteen & Bon Jovi.", price = "various", category = category7)

session.add(place9)
session.commit()



place1 = Place(user_id=1, name = "Porta", description = "Trendy Italian spot with picnic-table seating, boasting gourmet wood fired pies, bocce & live music.", price = "free", category = category7)

session.add(place1)
session.commit()

place2 = Place(user_id=1, name = "Langosta Lounge", description = "Vibrant beachfront restaurant featuring an eclectic menu, full bar & occasional live music.", price = "free", category = category7)

session.add(place2)
session.commit()

place3 = Place(user_id=1, name = "Wonder Bar", description = "Quirky bar with frequent live music, TV sports & a dog friendly patio with designated play times.", price = "various", category = category7)

session.add(place3)
session.commit()


print "added items!"
