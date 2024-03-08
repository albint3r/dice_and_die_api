from app.domain.auth.entities.user_level import UserLevel


def next_level_basic_formula(user_level: UserLevel) -> int:
    """This is the default exp point system"""
    level = user_level.level
    exponent1 = 0.1
    exponent2 = 0.8
    base_exp = 50
    return int(exponent1 * (level ** 3) + exponent2 * (level ** 2) + base_exp * level)


def next_level_advance_formula(user_level: UserLevel) -> int:
    exponent = 1.5
    base_exp = 100
    return int(base_exp * (user_level.level ** exponent))
