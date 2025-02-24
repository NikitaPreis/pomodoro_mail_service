class MailClient:

    @staticmethod
    def send_welcom_email(to: str) -> None:
        return send_email_task.delay(
            subject='Welcome email',
            text=f'Welcome to pomodoro, {to}!',
            to=to
        )
