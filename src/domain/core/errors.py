from fastapi import HTTPException


class WebSocketColumnError(HTTPException):
    """This is the baseclass of Columns errors"""
