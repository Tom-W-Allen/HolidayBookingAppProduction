from flask import session, request
from common.enums.State import State
from domains.user.UserRepositoryInterface import IUserRepository
from mappers.BaseMapper import BaseMapper
import string
import random
import datetime


class ResetPasswordPageMapper(BaseMapper):
    def __init__(self, user_repository: IUserRepository,):
        self.user_repository = user_repository