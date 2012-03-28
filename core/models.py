from django.contrib.auth.models import User
from django.db import models

from core.lists import (
    ALIGNMENT_CHOICES,
    DIRECTION_CHOICES,
    DOOR_RESET_CHOICES,
    DOOR_TRIGGER_TYPE_CHOICES,
    SEX_CHOICES,
    WEAPON_TYPE_CHOICES,
    )


### Area models ###
class AreaFlag(models.Model):
    """
    Flags that can be applied to an area.
    """
    TFC_id = models.PositiveIntegerField(blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()


class Area(models.Model):
    """
    A new TFC Area! Yay!
    """
    author = models.OneToOneField(User, blank=False)
    vnum = models.PositiveIntegerField(unique=True)

    name = models.TextField(blank=False, unique=True)
    forum = models.URLField(blank=True)

    level_low = models.PositiveSmallIntegerField(blank=False, default=1)
    level_high = models.PositiveSmallIntegerField(blank=False, default=50)
    flags = models.ManyToManyField(AreaFlag)

    notes = models.TextField()


class AreaHelp(models.Model):
    """
    A help file related to this area.

    BLOCK: #HELP
    """
    area = models.OneToOneField(Area, blank=False)
    keywords = models.CharField(max_length=50)
    level = models.SmallIntegerField(blank=False, default=0, help_text="Lowest level that can read this help.")
    blank_line = models.BooleanField(blank=False, default=False, help_text="Include blank line at the beginning of this help?")
    text = models.TextField(blank=False)


### Item models ###
# TODO: fill out the write_values() defs for each item type. use adv string formatting!
# TODO: write tests to ensure that the item type ids are correct and all t
class Spell(models.Model):
    """
    Approved spells.
    """
    TFC_id = models.PositiveIntegerField(blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)


class WeaponDamageType(models.Model):
    """
    Damage identifiers done by certain types of weapons.
    """
    TFC_id = models.PositiveIntegerField(blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)
    weapon_type = models.CharField(max_length=1, choices=WEAPON_TYPE_CHOICES)


class DrinkType(models.Model):
    """
    Types that a drinkable can be.
    """
    TFC_id = models.PositiveIntegerField(blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)
    adjective = models.CharField(max_length=50, blank=False, unique=True)


class ContainerFlag(models.Model):
    """
    Flags that can be applied to a container.
    """
    TFC_id = models.PositiveIntegerField(blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()


class ItemType(models.Model):
    """
    Types that an item can be.
    """
    TFC_id = models.PositiveIntegerField(blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()


class ExtraDescription(models.Model):
    """
    Extra description available to add to an object.
    """
    item = models.ForeignKey('Item', related_name='extra_descriptions')
    TFC_id = models.PositiveIntegerField(blank=False)

    keywords = models.TextField(blank=False)
    description = models.TextField(blank=False)


class WearFlag(models.Model):
    """
    Places an item can be worn.
    """
    TFC_id = models.PositiveIntegerField(blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()


class ResetWearFlag(models.Model):
    """
    Places an item can be reset to on a mobile.
    """
    TFC_id = models.PositiveIntegerField(blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()


class ItemExtraFlag(models.Model):
    """
    Extra flags available to apply to items.
    """
    TFC_id = models.PositiveIntegerField(blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()


class ItemModifier(models.Model):
    """
    Stats that an item can modify in some way - these are the Item Applies flags.
    If any of these are used on an item, it automatically gets the (Magical)
    ItemExtraFlag.
    """
    TFC_id = models.PositiveIntegerField(blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)
    requires_approval = models.BooleanField(blank=False, default=False)
    description = models.TextField()

### There is actually a reason for all this Item model madness. It has to do
### with properly displaying the fields for creation of item types to the
### area builder. This could all be cleaned up with some Class Factory
### magic (which would also make Item Types dynamically editable), but that
### is going to have to be on the wishlist for now.
class Item(models.Model):
    """
    An item that lives in a TFC Area.

    BLOCK: #OBJECTS
    """
    area = models.ForeignKey(Area, blank=False)
    vnum = models.PositiveIntegerField(blank=False)

    # names needs to be lower()d.
    names = models.TextField(help_text='A few keywords for this object.')
    
    # short_desc needs to be lower()d.
    short_desc = models.TextField(help_text='A short phrase identifying the object; e.g. "a stone hammer"')

    long_desc = models.TextField(help_text='Description of an object standing alone; e.g. "A heavy stone hammer lies here."')

    takeable = models.BooleanField(default=False)
    # A shopkeeper will sell most Item types, but not Trash.
    salable = True
    wear_flags = models.ForeignKey(WearFlag)
    weight = models.PositiveSmallIntegerField(default=4, help_text="Total weight including carrying weight if this is a container.")
    cost = models.PositiveIntegerField(default=1000)
    values = models.PositiveIntegerField(help_text="Number of coins")

    flammable = models.BooleanField(blank=False, default=False)
    metallic = models.BooleanField(blank=False, default=False)
    two_handed = models.BooleanField(blank=False, default=False)
    underwater_breath = models.BooleanField(blank=False, default=False)

    total_in_game = models.PositiveSmallIntegerField(blank=False, default=1, help_text="Total number of this item allowed in the game (won't reset when max is reached)")

    notes = models.TextField()

    class Meta:
        unique_together = ('area', 'vnum')


class Light(Item):
    """
    An item of the Light type.
    """
    item_type = 1
    hours = models.SmallIntegerField(blank=False, default=0, help_text="Number of hours of light. Use -1 for infinite and 0 for dead.")

    def write_values(self):
        """
        Prints out the values needed for a zone file.
        """
        print "0 0 %d 0" % (hours)


class Fountain(Item):
    """
    A fountain item.
    """
    item_type = 25
    spell = models.ForeignKey(Spell, blank=False)
    spell_level = models.PositiveSmallIntegerField(blank=False)
    drink_type = models.ForeignKey(DrinkType, blank=False)

    def write_values(self):
        pass

    
class BaseWeapon(Item):
    """
    Weapon base class. There are weapons and animal weapons.
    """
    minimum_damage = models.PositiveSmallIntegerField(blank=False)
    maximum_damage = models.PositiveSmallIntegerField(blank=False)
    weapon_damage_type = models.ForeignKey(WeaponDamageType, blank=False)

    class Meta:
        abstract = True


class BaseArmor(Item):
    """
    Base armor class. There is armor and animal armor.
    """
    ac_rating = models.SmallIntegerField(blank=False)

    class Meta:
        abstract = True


class BaseFood(Item):
    """
    Base food class. There is food and pet food.
    """
    hours = models.PositiveSmallIntegerField(blank=False)
    poison = models.SmallIntegerField(blank=False, default=0, help_text="0 is non-poisonous, non-zero is poisonous.")

    class Meta:
        abstract = True


class SimpleMagicalItem(Item):
    """
    A magical item that just has one charge of up to three spells.
    """
    spells = models.ManyToManyField(Spell, blank=False, help_text="Choose up to three spells. Only three will be exported, randomly if more exist.")
    spell_level = models.PositiveSmallIntegerField(blank=False)

    class Meta:
        abstract = True
        

class ChargedMagicalItem(Item):
    """
    A magical item with charges.
    """
    spell = models.ForeignKey(Spell, blank=False)
    spell_level = models.PositiveSmallIntegerField(blank=False)
    max_charges = models.PositiveSmallIntegerField(blank=False)
    remaining_charges = models.PositiveSmallIntegerField(blank=False)

    class Meta:
        abstract = True


class Weapon(BaseWeapon):
    item_type = 5

    def write_values(self):
        pass


class AnimalWeapon(BaseWeapon):
    """
    A weapon derived from an animal (e.g. a scorpion's stinger).)
    """
    item_type = 6

    def write_values(self):
        pass

    class Meta:
        verbose_name = 'animal-based weapon'


class Armor(BaseArmor):
    item_type = 9

    def write_values(self):
        pass

    class Meta:
        verbose_name = 'armor item'


class AnimalArmor(BaseArmor):
    """
    Armor derived from an animal. Mobs that have no_wear_armor
    can still wear animal armor.
    """
    item_type = 14

    def write_values(self):
        pass

    class Meta:
        verbose_name = 'animal-based armor item'


class Food(BaseFood):
    item_type = 19

    def write_values(self):
        pass

    class Meta:
        verbose_name = 'food item'


class PetFood(BaseFood):
    item_type = 11

    def write_values(self):
        pass

    class Meta:
        verbose_name = 'pet food item'


class Scroll(SimpleMagicalItem):
    item_type = 2

    def write_values(self):
        pass


class Potion(SimpleMagicalItem):
    item_type = 10

    def write_values(self):
        pass


class Pill(SimpleMagicalItem):
    item_type = 26

    def write_values(self):
        pass


class Wand(ChargedMagicalItem):
    item_type = 3

    def write_values(self):
        pass


class Staff(ChargedMagicalItem):
    item_type = 4

    def write_values(self):
        pass

    class Meta:
        verbose_name_plural = 'staves'


class Fetish(ChargedMagicalItem):
    item_type = 7

    def write_values(self):
        pass

    class Meta:
        verbose_name_plural = 'fetishes'


class Ring(ChargedMagicalItem):
    item_type = 29

    def write_values(self):
        pass


class Relic(ChargedMagicalItem):
    item_type = 33

    def write_values(self):
        pass


class NonMagicalItem(Item):
    class Meta:
        abstract = True


class Treasure(NonMagicalItem):
    item_type = 8

    def write_values(self):
        pass

    class Meta:
        verbose_name = 'treasure item'


class Furniture(NonMagicalItem):
    item_type = 12

    def write_values(self):
        pass

    class Meta:
        verbose_name = 'furniture item'


class Trash(NonMagicalItem):
    item_type = 13
    # Shopkeepers don't sell Trash. Sorry.
    salable = False

    def write_values(self):
        pass

    class Meta:
        verbose_name = 'trash item'


class Key(NonMagicalItem):
    item_type = 18

    def write_values(self):
        pass


class Boat(NonMagicalItem):
    item_type = 22

    def write_values(self):
        pass


class Decoration(NonMagicalItem):
    item_type = 27

    def write_values(self):
        pass


class Jewelry(NonMagicalItem):
    item_type = 30

    def write_values(self):
        pass

    class Meta:
        verbose_name = 'jewelry item'


class DrinkContainer(Item):
    """
    An item that can contain liquids.
    """
    item_type = 17
    capacity = models.SmallIntegerField(blank=False, help_text="Capacity of this drink container.")
    remaining = models.SmallIntegerField(blank=False, help_text="Amount remaining in the container.")
    drink_type = models.ForeignKey(DrinkType, blank=False)
    poison = models.SmallIntegerField(blank=False, default=0, help_text="0 is non-poisonous, non-zero is poisonous.")

    def write_values(self):
        pass


class Container(Item):
    """
    An item that can contain other non-liquid items.
    """
    item_type = 15
    key = models.ForeignKey(Key, blank=True)
    flags = models.ManyToManyField('ContainerFlag')

    def write_values(self):
        pass


class ItemContainerReset(models.Model):
    """
    AKA a Place Reset.

    Loads an object into another object. This will be placed onto a Container
    type object, since only containers can contain other objects.
    """
    container = models.ForeignKey(Container, blank=False, related_name='item_resets')
    item = models.ForeignKey(Item, blank=False, related_name='container_resets')
    reset_every_cycle = models.BooleanField(blank=False, default=False, help_text="Reset this item every cycle (instead of only when zone is deserted)?")
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name = 'item-container reset'
        unique_together = ('container', 'item')


class Money(Item):
    item_type = 20
    number_of_coins = models.SmallIntegerField(blank=False, default=1, help_text="How many coins is this money worth?")

    def write_values(self):
        pass

    class Meta:
        verbose_name = 'pile of money'
        verbose_name_plural = 'piles of money'


### Mobile models
class Race(models.Model):
    """
    Races available for shopkeepers.
    """
    TFC_id = models.SmallIntegerField(blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)


class KnownLanguage(models.Model):
    """
    Languages that mobiles can *know*. The Language called "God" has a
    different id if it is preferred vs. just known by a mob, so we have to
    have separate models, here.
    """
    TFC_id = models.PositiveIntegerField(blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)


class PreferredLanguage(models.Model):
    """
    Languages that mobiles can *prefer*. The Language called "God" has a
    different id if it is preferred vs. just known by a mob, so we have to
    have separate models, here.
    """
    TFC_id = models.PositiveIntegerField(blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)


class ActionFlag(models.Model):
    """
    Action flags available to apply to mobiles.
    """
    TFC_id = models.PositiveIntegerField(blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField(blank=False)


class AffectFlag(models.Model):
    """
    Affect flags available to apply to mobiles.
    """
    TFC_id = models.PositiveIntegerField(blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()
    implemented = models.BooleanField(blank=False, default=True)


class SpecialFunction(models.Model):
    """
    Additional functionality for mobiles.

    BLOCK: #SPECIALS
    """
    TFC_id = models.CharField(max_length=50, blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()
    generic = models.BooleanField(blank=False, default=True)


class Mobile(models.Model):
    """
    A creature that can move around and do stuff, but isn't human.

    BLOCK: #MOBILES
    """
    area = models.ForeignKey(Area, blank=False)
    vnum = models.PositiveIntegerField(blank=False)

    names = models.TextField()
    short_desc = models.TextField()
    long_desc = models.TextField()
    look_desc = models.TextField()

    level = models.PositiveSmallIntegerField(default=1, help_text="What level is this Mob?")
    alignment = models.PositiveSmallIntegerField(choices=ALIGNMENT_CHOICES)
    sex = models.SmallIntegerField(choices=SEX_CHOICES)
    is_animal = models.BooleanField(default=False, help_text="Is this Mob an animal?")
    spell = models.ForeignKey(Spell, blank=True, help_text="What spell (if any) does this Mob know?")

    affect_flags = models.ManyToManyField(AffectFlag)
    action_flags = models.ManyToManyField(ActionFlag)
    no_wear = models.BooleanField(default=False, help_text="Should this Mob be allowed to wear armor (animal armor excluded)?")
    special_functions = models.ManyToManyField(SpecialFunction, blank=True)

    known_languages = models.ManyToManyField(KnownLanguage, help_text="What languages does this Mob know?")
    preferred_language = models.ForeignKey(PreferredLanguage, help_text="What language does this Mob prefer?")

    total_in_game = models.PositiveSmallIntegerField(blank=False, default=1, help_text="Total number of this mob allowed in the game (won't reset when max is reached)")

    notes = models.TextField()

    class Meta:
        unique_together = ('area', 'vnum')


class Shopkeeper(models.Model):
    """
    A shopkeeper mob.

    BLOCK: #SHOPS
    """
    mobile = models.OneToOneField(Mobile, blank=False, unique=True, help_text="Which Mob is running this shop?")
    race = models.ForeignKey(Race, blank=False, help_text="What race is this shopkeeper?")
    will_buy = models.CommaSeparatedIntegerField(max_length=50, blank=True, help_text="Item types the mob will buy. Only the first 5 will be used.")
    opens = models.SmallIntegerField(blank=False, default=6, help_text="Hour of the day this shop opens. (0-23)")
    closes = models.SmallIntegerField(blank=False, default=23, help_text="Hour of the day this shop closes. (0-23)")

    reset_items = models.ManyToManyField(Item, blank=True)


class MobRoomReset(models.Model):
    """
    AKA a Mob Reset.

    Reset definition for a Mob into a Room.

    BLOCK: #RESETS
    """
    mobile = models.ForeignKey(Mobile, blank=False, related_name='room_resets')
    room = models.ForeignKey('Room', blank=False, related_name='mob_resets')
    reset_every_cycle = models.BooleanField(blank=False, default=False, help_text="Reset this item every cycle (instead of only when zone is deserted)?")
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name = 'mob-room reset'
        unique_together = ('mobile', 'room')


class MobItemReset(models.Model):
    """
    AKA a Give Reset, or an Equip Reset if a wear_location is set.

    Reset definition for an object into a Mob.

    BLOCK: #RESETS
    """
    item = models.ForeignKey(Item, blank=False, related_name='mob_resets')
    mobile = models.ForeignKey(Mobile, blank=False, related_name='item_resets')
    reset_every_cycle = models.BooleanField(blank=False, default=False, help_text="Reset this item every cycle (instead of only when zone is deserted)?")
    wear_location = models.ForeignKey(ResetWearFlag, blank=True, help_text="Optional: Where (if anywhere) do you want the Mob to equip this item?")
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name = 'mob-item reset'
        unique_together = ('item', 'mobile')


### Room and Door models ###
class RoomType(models.Model):
    """
    Types of terrain that a room can have/be.
    """
    TFC_id = models.PositiveIntegerField(blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()


class RoomFlag(models.Model):
    """
    Flags that can be applied to a room.
    """
    TFC_id = models.PositiveIntegerField(blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()
    implemented = models.BooleanField(blank=False, default=True)


class RoomSpecialFunction(models.Model):
    """
    Special functions that can be attached to a room.

    BLOCK: #RSPECS
    """
    TFC_id = models.CharField(max_length=50, blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()   


class Room(models.Model):
    """
    A room in TFC Area.

    BLOCK: #ROOMS
    """
    area = models.ForeignKey(Area, blank=False)
    vnum = models.PositiveIntegerField(blank=False)

    special_functions = models.ManyToManyField(RoomSpecialFunction, blank=True)

    notes = models.TextField()

    class Meta:
        unique_together = ('area', 'vnum')


class ItemRoomReset(models.Model):
    """
    AKA an Object Reset.

    Resets an Item into a Room.

    BLOCK: #RESETS
    """
    room = models.ForeignKey(Room, blank=False, related_name='object_resets')
    item = models.ForeignKey(Item, blank=False, related_name='room_resets')
    reset_every_cycle = models.BooleanField(blank=False, default=False, help_text="Reset this item every cycle (instead of only when zone is deserted)?")
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name = 'item-room reset'
        unique_together = ('room', 'item')


class DoorTrigger(models.Model):
    """
    Door special functions - holds both Prevent and Allow Door Specfuns (Triggers).

    BLOCK: #TRIGGERS
    """
    door = models.ForeignKey('Door', blank=False, related_name='triggers')
    TFC_id = models.CharField(max_length=50, blank=False)
    trigger_type = models.CharField(max_length=1, choices=DOOR_TRIGGER_TYPE_CHOICES)


class DoorType(models.Model):
    """
    Types that a door can be.
    """
    TFC_id = models.PositiveIntegerField(blank=False)
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()


class Door(models.Model):
    """
    A door leading out of a room. A room can have up to six doors, one in each direction.

    BLOCK: #ROOMS
    Listed along with the Room to which they are attached.
    """
    room = models.ForeignKey(Room, blank=False, related_name='exits')
    name = models.CharField(max_length=50, blank=False, help_text='A one-word description of the door (e.g. "door" or "gate")')
    direction = models.CharField(max_length=1, blank=False, choices=DIRECTION_CHOICES)
    door_type = models.ForeignKey(DoorType, blank=False)
    keywords = models.TextField(blank=False, help_text='Keywords for interacting with the door.')

    description = models.TextField(blank=True)
    room_to = models.ForeignKey(Room, blank=True, related_name='entrances')

    reset = models.BooleanField(blank=False, default=False, help_text="Should this door be reset?")
    reset_every_cycle = models.BooleanField(blank=False, default=False, help_text="Reset this door every cycle (instead of only when deserted)?")
    reset_value = models.SmallIntegerField(blank=True, choices=DOOR_RESET_CHOICES)
    reset_comment = models.TextField(blank=True)

    notes = models.TextField()

    class Meta:
        unique_together = ('room', 'direction')
