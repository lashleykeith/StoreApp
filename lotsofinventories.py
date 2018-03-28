# Populating the Database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, InventoryItem, User

engine = create_engine('sqlite:///storeinventorywithusers.db')
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

# Create a user
User1 = User(name="Avishek", email="contactavishek239@gmail.com")

#Menu for Burger Joint
store1 = Store(name = "Burger Joint")

session.add(store1)
session.commit()


inventoryItem1 = InventoryItem(name = "Creamy Chicken Mushroom Club", description = "Roasted boneless chicken and mushroom duxelles mixed with creamy cheese dressing", price = "Rs 150", course = "Weight", store = store1)

session.add(inventoryItem1)
session.commit()

inventoryItem2 = InventoryItem(name = "Chicken Burger", description = "Juicy grilled chicken patty with tomato mayo and lettuce", price = "Rs 165", course = "Weapon", store = store1)

session.add(inventoryItem2)
session.commit()

inventoryItem3 = MenuItem(name = "Chocolate Butterscotch Cake", description = "Made with buttery caramel nuts crushed and folded with chocolate cream for a velvet touch", price = "Rs 250", course = "Pad", store = store1)

session.add(inventoryItem3)
session.commit()

inventoryItem4 = InventoryItem(name = "Big Joe Lamb Burger", description = "American inspired burger with minced lamb patty, topped with lamb mince, a savoury ranch spread and cheese sauce layered in a homemade multigrain loaf", price = "Rs 180", course = "Weapon", store = store1)

session.add(inventoryItem4)
session.commit()

inventoryItem5 = InventoryItem(name = "Chicken Club Sandwich", description = "Oozing with cheese and layered with chicken ham and whole chicken", price = "Rs 150", course = "Weapon", store = store1)

session.add(inventoryItem5)
session.commit()

inventoryItem6 = InventoryItem(name = "Mocha Latte", description = "Dark chocolate paired with caffeine", price = "Rs 120", course = "Other_Material", store = store1)

session.add(inventoryItem6)
session.commit()

inventoryItem7 = InventoryItem(name = "Smokin' Grill Burger", description = "Chicken mince is seasoned with smoky wood fire seasoning and grilled to a juicy perfection", price = "Rs 165", course = "Weapon", store = store1)

session.add(inventoryItem7)
session.commit()

inventoryItem8 = InventoryItem(name = "Big Cheese Burger", description = "Made with patty made of chicken mince stuffed with gooey cheddar cheese", price = "Rs 165", course = "Weapon", store = store1)

session.add(inventoryItem8)
session.commit()




#Menu for Super Stir Fry
store2 = Store(name = "Super Stir Fry")

session.add(store2)
session.commit()


inventoryItem1 = InventoryItem(name = "Chilli Orange Chicken Popcorn", description = "Fried chicken popcorn tossed in mandarin chilli soy sauce", price = "Rs 150", course = "Weapon", store = store2)

session.add(inventoryItem1)
session.commit()

inventoryItem2 = InventoryItem(name = "Spinach and Mozzarella Chicken", description = "Tender chicken breast is stuffed with fresh spinach and mozzarella cheese", price = "Rs 220", course = "Weapon", store = store2)

session.add(inventoryItem2)
session.commit()

inventoryItem3 = InventoryItem(name = "Chilly Paneer Roll", description = "Chilli paneer with a mix of fresh peppers and soya in a lovely chilli paste", price = "Rs 190", course = "Weight", store = store2)

session.add(inventoryItem3)
session.commit()

inventoryItem4 = InventoryItem(name = "Chicken Teriyaki Stir Fry", description = "Chunks of batter-fried chicken that's been marinated in rich spices and stir-fried along with peppers, crunchy onion, and teriyaki sauce", price = "Rs 180", course = "Weapon", store = store2)

session.add(inventoryItem4)
session.commit()

inventoryItem5 = InventoryItem(name = "Cream of Mushroom Chicken Soup", description = "Made with shredded chicken, fresh shiitake and button mushrooms", price = "Rs 149", course = "Weight", store = store2)

session.add(inventoryItem5)
session.commit()

inventoryItem6 = MenuItem(name = "Vanilla Whey & Peanut Butter Smoothie", description = "Whey smoothie prepared with banana, in-house peanut butter, and oats", price ="Rs 200", course ="Other_Material", store = store2)

session.add(inventoryItem6)
session.commit()

inventoryItem7 = InventoryItem(name = "Cheesecake", description="Consists of a mixture of soft, fresh cheese, eggs, and sugar", price ="Rs 90", course ="Pad", store = store2)

session.add(inventoryItem7)
session.commit()


#Menu for Panda Garden
store3 = Store(name = "Panda Garden")

session.add(store3)
session.commit()


inventoryItem1 = InventoryItem(name = "Vietnamese Pho", description = "A Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and shredded chicken", price = "Rs 150", course = "Weight", store = store3)

session.add(inventoryItem1)
session.commit()

inventoryItem2 = InventoryItem(name = "Chinese Dumpling Soup", description = "A common Chinese dumpling which generally consists of minced chicken meat and finely chopped vegetables wrapped into a piece of dough skin", price = "Rs 150", course = "Weapon", store = store3)

session.add(inventoryItem2)
session.commit()

inventoryItem3 = InventoryItem(name = "Korean Sesame Chicken Bowl", description = "Succulent chicken chunks are fried to perfection with the authentic sriracha sauce", price = "Rs 200", course = "Weapon", store = store3)

session.add(inventoryItem3)
session.commit()

inventoryItem4 = InventoryItem(name = "Japanese Crunchy Veggie Salad", description = "This Japanese salad is packed with fresh greens topped with pearls of crunchy tempura and dressed with a luscious and spicy wasabi mayonnaise dip", price = "Rs 160", course = "Weapon", store = store3)

session.add(inventoryItem4)
session.commit()

inventoryItem5 = InventoryItem(name ="Chantilly cake", description = "Chocolate cakes with a Chantilly frosting", price ="Rs 60", course ="Pad", store = store3)

session.add(inventoryItem5)
session.commit()

inventoryItem6 = InventoryItem(name="Chocolate, Rock Salt & Chilli Smoothie", description ="Contains dark chocolate, spicy chillis, and rock salt", price="Rs 170", course ="Other_Material", store = store3)

session.add(inventoryItem6)
session.commit()


#Menu for Eatfit
store4 = Store(name = "Eatfit")

session.add(inventory4)
session.commit()


inventoryItem1 = InventoryItem(name = "Red Velvet Cheesecake", description = "Made with sweet, smooth cream cheese and layers of dark red velvet", price = "Rs 100", course = "Pad", store = store4)

session.add(inventoryItem1)
session.commit()

inventoryItem2 = InventoryItem(name = "Spinach Mushroom Potpie", description = "Nutritious wilted spinach tossed with button mushrooms, peppers and zucchini", price = "Rs 220", course = "Weapon", store = store4)

session.add(inventoryItem2)
session.commit()

inventoryItem3 = InventoryItem(name = "Honey Boba Shaved Snow", description = "Milk snow layered with honey boba, jasmine tea jelly, grass jelly, caramel, cream, and freshly made mochi", price = "Rs 90", course = "Other_Material", store = store4)

session.add(inventoryItem3)
session.commit()

inventoryItem4 = InventoryItem(name = "Mediterranean Balsamic Veg Salad", description = "Veggie fiesta made with roasted bell peppers, carrots, haricot beans, zucchini and baby corn flavoured with paprika, rosemary and balsamic vinegar", price = "Rs 140", course="Weight", store = store4)

session.add(inventoryItem4)
session.commit()

inventoryItem5 = InventoryItem(name = "XO Baked Basa Noodle Bowl", description = "Delectable Basa fillet, marinated in XO sauce, pepper, oil, wrapped in banana leaf and baked to perfection", price = "Rs 230", course = "Weapon", store = store4)

session.add(inventoryItem5)
session.commit()




#Menu for Bistro
store5 = Store(name = "Bistro")

session.add(store5)
session.commit()


inventoryItem1 = InventoryItem(name = "Shellfish Tower", description = "A Grilled Shellfish with spiced Onions", price = "Rs 240", course = "Weapon", store = store5)

session.add(inventoryItem1)
session.commit()

inventoryItem2 = InventoryItem(name = "Jamaican Jerk Chicken with Grilled Vegetables", description = "Juicy chicken breasts marinated in a traditional Jamaican spice mix", price = "Rs 240", course = "Weapon", store = store5)

session.add(inventoryItem2)
session.commit()

inventoryItem3 = InventoryItem(name = "Spanish Chicken Stew & Rice", description = "Healthy chicken stew made with zero-cream tomato base sauce", price = "Rs 170", course = "Weapon", store = store5)

session.add(inventoryItem3)
session.commit()

inventoryItem4 = InventoryItem(name = "Chocolate Icecream", description = "Icecream with dark chocolate", price = "Rs 69", course = "Pad", store = store5)

session.add(inventoryItem4)
session.commit()

inventoryItem5 = InventoryItem(name = "Malaysian Chicken Curry", description = "Malaysian curry made with diced chicken and veggies and enriched with the aromatic flavour of coconut milk and basil leaves", price = "Rs 240", course = "Weapon", store = store5)

session.add(inventoryItem5)
session.commit()

inventoryItem6 = InventoryItem(name ="Vanilla & Peanut Butter Smoothie", description = "Smoothie prepared with banana, in-house peanut butter, and oats", price="Rs 100", course="Other_Material", store =  store5)

session.add(inventoryItem6)
session.commit()

inventoryItem7 = InventoryItem(name="Antipasto", description ="Traditional antipasto includes cured meats, olives, peperoncini, mushrooms, anchovies, artichoke hearts, various cheese, pickled meats and vegetables", price="Rs 150", course="Weight", store = store5)

session.add(inventoryItem7)
session.commit()


#Menu for Andala's Kitchen
store6 = Store(name = "Andala\'s Kitchen")

session.add(store6)
session.commit()


inventoryItem1 = InventoryItem(name = "Black Pepper Honey Chicken", description = "Chicken is marinated in an oriental spice mix and grilled with black pepper sauce and honey", price = "Rs 140", course = "Weapon", store = store6)

session.add(inventoryItem1)
session.commit()

inventoryItem2 = InventoryItem(name = "Chicken Tennessee Steak", description = "Butterfly chicken steak, grilled to perfection and served on a bed of aromatic herb butter rice", price = "Rs 150", course = "Weapon", store = store6)

session.add(inventoryItem2)
session.commit()

inventoryItem3 = InventoryItem(name = "Lemongrass Thai Chicken Steak", description = "Vietnamese style grilled chicken spiced with zesty lemon grass", price = "Rs 200", course = "Weight", store = store6)

session.add(inventoryItem3)
session.commit()

inventoryItem4 = InventoryItem(name = "Fruit Cake", description = "Fruity pound cake flavoured with currants and cherries", price = "Rs 60", course = "Pad", store = store6)

session.add(inventoryItem4)
session.commit()

inventoryItem5 = InventoryItem(name ="Chocolate & Chilli Smoothie", description="Contains dark chocolate and spicy chillis with rich antioxidants", price ="Rs 70", course="Other_Material", store = store6)

session.add(inventoryItem5)
session.commit() 


#Menu for India Palace
store7 = Store(name = "India Palace")

session.add(store7)
session.commit()

inventoryItem1 = InventoryItem(name = "Nilgiri Chicken Korma & Rice", description = "Nilgiri chicken flavoured with coconut milk and a medley of spices", price = "Rs 170", course = "Weight", store = store7)

session.add(inventoryItem1)
session.commit()



inventoryItem2 = InventoryItem(name = "Hyderabadi Chicken Biryani", description = "Fragrant rice cooked with succulent chicken drumsticks slow roasted in spicy authentic flavours", price = "Rs 220", course = "Weapon", store = store7)

session.add(inventoryItem2)
session.commit()

inventoryItem3 = InventoryItem(name = "Doodhiya Malai Chicken Tikka", description = "Succulent chicken marinated with malai cream and oven roasted to excellence", price = "Rs 200", course = "Weapon", store = store7)

session.add(inventoryItem3)
session.commit()

inventoryItem4 = InventoryItem(name = "Oriental Dragon Veggies 'N' Hakka Noodles", description = "Fresh broccoli, baby corn, bok choy, mushrooms and Chinese cabbage tossed in a spicy chili oyster sauce served with the classic Hakka noodles", price = "Rs 200", course = "Weapon", store = store7)

session.add(inventoryItem4)
session.commit()

inventoryItem5 = InventoryItem(name = "Slim Dry Fruit Lassi", description = "Packed with the health benefits of probiotics in curd, and cashew and almonds", price = "Rs 80", course = "Other_Material", store = store7)

session.add(inventoryItem5)
session.commit()

inventoryItem6 = InventoryItem(name = "Rasgulla Lychee Mousse", description = "traditional Rasagulla in the form of a fruity cheesecake mousse", price = "Rs 50", course = "Pad", store = store7)

session.add(inventoryItem6)
session.commit()




#Menu for Tim Tai
store8 = Store(name = "Tim Tai")

session.add(store8)
session.commit()


inventoryItem1 = InventoryItem(name = "Fruit 'N' Nut Cheesecake", description = "Fruit and nut loaded vanilla cheese cake bar dipped in pure dark chocolate and coated with cherries", price = "Rs 75", course = "Pad", store = store8)

session.add(inventoryItem1)
session.commit()

inventoryItem2 = InventoryItem(name = "Nasi Goreng", description = "Fried rice tossed with Bok Choy, broccoli, Chinese cabbage with peanuts added for a crunch", price = "Rs 200", course = "Weapon", store = store8)

session.add(inventoryItem2)
session.commit()

inventoryItem3 = InventoryItem(name = "Slim Cold Coffee", description = "With caffeine punch and a dash of sweetness, our slim cold coffee will help you reset at any point of the day", price = "Rs 170", course = "Other_Material", store = store8)

session.add(inventoryItem3)
session.commit()

inventoryItem4 = InventoryItem(name = "Spicy Habanero Burrito Bowl", description = "This bowl of awesome comes with habanero rice, red lentil chickpea cutlet, Sour Cream, creamy Chipotle sauce and fresh veggies", price = "Rs 180", course="Weight", store = store8)

session.add(inventoryItem4)
session.commit()

inventoryItem5 = InventoryItem(name = "Stir Fried Chilli Paneer with Brown Rice", description = "Fresh paneer, tossed in sweet chili sauce with crunchy peppers and fresh veggies", price = "Rs 220", course = "Weapon", store = store8)

session.add(inventoryItem5)
session.commit()



print "Added inventory items!"

