from pubapp.models import Character, CharacterUser


def update_or_create_user_character_relations(user):
    characters = Character.objects.all()
    for character in characters:
        relation = CharacterUser.objects.filter(user=user, character=character).first()
        if relation is None:
            relation = CharacterUser()
            relation.user = user
            relation.character = character
            relation.drinks = 0
            relation.save()