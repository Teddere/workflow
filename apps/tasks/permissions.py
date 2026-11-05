from apps.account.models import User

def can_delete_task(user, task):

    if not user.is_authenticated:
        return False

    if user.role == User.Role.ADMIN:
        return True
    return (
        user.role == User.Role.MANAGER
        and task.project.manager_id == user.pk
    )

def can_edit_task(user, task):

    if not user.is_authenticated:
        return False

    if user.role == User.Role.ADMIN:
        return True

    if (
       user.role == User.Role.MANAGER
        and task.project.manager_id == user.pk
    ):
        return True

    if (
            user.role in (User.Role.MEMBER, User.Role.MANAGER)
            and task.project.members.filter(pk=user.pk).exists()
            and task.assigned_to == user.pk
    ):
        return True

    return False

def permission_task(user, tasks):

    for task in tasks:
        task.can_edit = can_edit_task(user, task)
        task.can_delete = can_delete_task(user, task)
    return tasks