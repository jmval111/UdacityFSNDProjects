from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Category: Cricket
category1 = Category(name="Cricket", description="Cricket is a bat-and-ball game played between two teams of eleven players")

session.add(category1)
session.commit()


item1 = Item(name="ball", description="Cork covered by leather",
             category=category1)

session.add(item1)
session.commit()

item2 = Item(name="gloves", description="thickly padded above the fingers and on the thumb of the hand"
             , category=category1)

session.add(item2)
session.commit()

item3 = Item(name="bat", description="cane handle attached to a flat-fronted willow-wood blade", category=category1)

session.add(item3)
session.commit()


item4 = Item(name="Wicket-keeper's gloves", description=" includes webbing between the thumb and index fingers"
             , category=category1)

session.add(item4)
session.commit()


# Category: Football
category2 = Category(name="Soccer", description="kicking a ball with the foot to score a goal")

session.add(category2)
session.commit()


item1 = Item(name="Soccer ball", description=" ball inflated with air"
             , category=category2)

session.add(item1)
session.commit()

item2 = Item(
    name="Shin pads", description="protect shin",category=category2)

session.add(item2)
session.commit()


# Category: Hockey
category1 = Category(name="Hockey", description="maneuver a ball or a puck into the opponent's goal using a hockey stick")

session.add(category1)
session.commit()


item1 = Item(name="Hockey Stick", description="normally measures between 80 to 85cm"
             , category=category1)

session.add(item1)
session.commit()

print "added menu items!"
