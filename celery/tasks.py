from time import sleep
from logging import getLogger
import traceback

from celery import current_task, states
from celery.exceptions import Ignore

from worker import celery, red
from model import (
    UserRegister,
    UserLogin,
    UserLoginFederated,
    UserRegisterFederated
)

LOGGER = getLogger(__name__)



@celery.task(name='user.register', bind=True, acks_late=True)
def user_register(self, user_id):
    try:
        LOGGER.info('Starting register task')
        total = red.hincrby("metric:user.register", "quantity", 1)

        LOGGER.info('Finished register task')
        return {"result": f"New user register {user_id}",
                "total": f"{total}"}
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
    try:
        LOGGER.info('Starting login task')
        total = red.hincrby("metric:user.login", "quantity", 1)
        LOGGER.info('Finished login task')

        return {"result": f"New user login {user_id}",
                "total": f"{total}"}
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex


#@celery.task(name='user.login.federated', bind=True, acks_late=True)
#def user_register(self, user_id):
#    try:
#        LOGGER.info('Starting login federated task')
#        total = red.hincrby("metric:user.login.federated", "quantity", 1)
#        LOGGER.info('Finished login federated task')
#        return {"result": f"New user login federated {user_id}",
#                "total": f"{total}"}
#    except Exception as ex:
#        self.update_state(
#            state=states.FAILURE,
#            meta={
#                'exc_type': type(ex).__name__,
#                'exc_message': traceback.format_exc().split('\n')
#            })
#        raise ex


#@celery.task(name='user.register.federated', bind=True, acks_late=True)
#def user_register(self, user_id):
#    try:
#        LOGGER.info('Starting register federated task')
#        total = red.hincrby("metric:user.register.federated", "quantity", 1)
#        LOGGER.info('Finished register federated task')
#        return {"result": f"New user register {user_id}",
#                "total": f"{total}"}
#    except Exception as ex:
#        self.update_state(
#            state=states.FAILURE,
#            meta={
#                'exc_type': type(ex).__name__,
#                'exc_message': traceback.format_exc().split('\n')
#            })
#        raise ex


@celery.task(name='user.register.result', bind=True, acks_late=True)
def user_register(self):
    try:
        metric_name = "metric:user.register"
        total = red.hget(metric_name, "quantity")
        if not total:
            total = 0
        else:
            total = total.decode("utf-8")
        return {"metric_name": metric_name,
                "total": total}
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex


@celery.task(name='user.login.result', bind=True, acks_late=True)
def user_register(self):
    try:
        metric_name = "metric:user.login"
        total = red.hget(metric_name, "quantity")
        if not total:
            total = 0
        else:
            total = total.decode("utf-8")
        return {"metric_name": metric_name,
                "total": total}
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex