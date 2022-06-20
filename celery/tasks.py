from time import sleep
from logging import getLogger
import traceback

from celery import current_task, states
from celery.exceptions import Ignore

from worker import celery
from model import (
    UserRegister,
    UserLogin,
    UserLoginFederated,
    UserRegisterFederated
)

LOGGER = getLogger(__name__)


@celery.task(name='user.register', bind=True, acks_late=True)
def user_register(self, user_id):
    register = 0
    try:
        LOGGER.info('Starting register task')
        register += 1
        LOGGER.info('Finished register task')
        return {"result": f"New user register {user_id}",
                "total": f"{register}"}
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex


@celery.task(name='user.login', bind=True, acks_late=True)
def user_register(self, user_id):
    register = 0
    try:
        LOGGER.info('Starting register task')
        register += 1
        LOGGER.info('Finished register task')
        return {"result": f"New user register {user_id}",
                "total": f"{register}"}
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex
