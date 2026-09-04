from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

from loans.models import Loan


class Command(BaseCommand):
    help = 'Sends an email reminder to members whose loans are due within 1 day.'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        reminder_window_start = now
        reminder_window_end = now + timedelta(days=1)

        due_soon_loans = Loan.objects.filter(
            status=Loan.Status.BORROWED,
            reminder_sent=False,
        ).select_related('member', 'book')

        sent_count = 0

        for loan in due_soon_loans:
            if reminder_window_start <= loan.due_date <= reminder_window_end:
                send_mail(
                    subject=f"Reminder: '{loan.book.title}' is due soon",
                    message=(
                        f"Hi {loan.member.first_name},\n\n"
                        f"This is a friendly reminder that your borrowed book "
                        f"'{loan.book.title}' by {loan.book.author} is due on "
                        f"{loan.due_date.strftime('%Y-%m-%d')}.\n\n"
                        f"Please return it to Readers' Haven on time to avoid "
                        f"it being marked as overdue.\n\n"
                        f"Thank you,\nReaders' Haven"
                    ),
                    from_email=None,
                    recipient_list=[loan.member.email],
                    fail_silently=False,
                )
                loan.reminder_sent = True
                loan.save(update_fields=['reminder_sent'])
                sent_count += 1

        self.stdout.write(self.style.SUCCESS(f'{sent_count} reminder email(s) sent.'))