# Still waiting on what Neutral should be!
ALIGNMENT_CHOICES = (
    (0, 'Neutral'),
    (-1000, 'Evil'),
    (1000, 'Good'),
    )

SEX_CHOICES = (
    (0, 'None'),
    (1, 'Male'),
    (2, 'Female'),
    )

WEAPON_TYPE_CHOICES = (
    ('B', 'Blunt'),
    ('S', 'Sharp'),
    )

DIRECTION_CHOICES = (
    (0, 'North'),
    (1, 'East'),
    (2, 'South'),
    (3, 'West'),
    (4, 'Up'),
    (5, 'Down'),
    )

DOOR_RESET_CHOICES = (
    (0, 'Open'),
    (1, 'Closed'),
    (2, 'Locked'),
    )

DOOR_TRIGGER_TYPE_CHOICES = (
    ('P', 'Prevent'),
    ('A', 'Allow'),
    )

ITEM_TYPE_CLASSES = [
    'Light',
    'Fountain',
    'Weapon',
    'AnimalWeapon',
    'Armor',
    'AnimalArmor',
    'Food',
    'PetFood',
    'Scroll',
    'Potion',
    'Pill',
    'Wand',
    'Staff',
    'Fetish',
    'Ring',
    'Relic',
    'Treasure',
    'Furniture',
    'Trash',
    'Key',
    'Boat',
    'Decoration',
    'Jewelry',
    'DrinkContainer',
    'Container',
    'Money',
    ]
