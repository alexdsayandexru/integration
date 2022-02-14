from datetime import datetime


class LoggerService:
    @staticmethod
    def log(message: str, date_time=None) -> datetime:
        now_time = datetime.now()

        text = '[{}] - {}'.format(now_time, message)
        if date_time:
            text = '[{}] - {}. Duration:[{}]'.format(now_time, message, (now_time - date_time))

        print(text)
        return now_time

    @staticmethod
    def log_exception(exception: BaseException):
        return LoggerService.log(f"Unexpected {exception=}, {type(exception)=}")
