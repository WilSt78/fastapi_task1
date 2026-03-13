from fastapi import HTTPException, status


def is_there_user(id: int, users: dict):
    if id not in users:
        return False
    return True
