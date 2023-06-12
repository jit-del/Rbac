class GenderType:
    OTHERS = 0
    MALE = 1
    FEMALE = 2

    CHOICES = (
        (OTHERS, "others"),
        (MALE, "male"),
        (FEMALE, "female"),
    )

class RoleType:
    ADMIN = 0  # Admin (all permissions)
    SOLUTION_PROVIDER = 1
    SOLUTION_SEEKER = 2

    CHOICES = (
        (ADMIN, "Admin"),
        (SOLUTION_PROVIDER, "solution_provider"),
        (SOLUTION_SEEKER, "solution_seeker")
    )