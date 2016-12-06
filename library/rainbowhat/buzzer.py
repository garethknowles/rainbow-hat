from threading import Timer

import RPi.GPIO as GPIO

BUZZER = 13

_timeout = None

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)

# Set up the PWM and then set the pin to input
# to prevent the signal from being output.
# Since starting/stopping PWM causes a segfault,
# this is the only way to manage the buzzer.

pwm = GPIO.PWM(BUZZER, 1)
GPIO.setup(BUZZER, GPIO.IN)
pwm.start(50)

def note(frequency, duration=1.0):
    """Play a single note.

    :param frequency: Musical frequency in hertz
    :param duration: Optional duration in seconds, use None to sustain note

    """

    global _timeout

    if frequency <= 0:
        raise ValueError("Frequency must be > 0")

    if duration is not None and duration <= 0:
        raise ValueError("Duration must be > 0")

    clear_timeout()

    pwm.ChangeFrequency(frequency)
    GPIO.setup(BUZZER, GPIO.OUT)    

    if duration is not None and duration > 0:
        _timeout = Timer(duration, stop)
        _timeout.start()

def clear_timeout():
    """Clear any note timeout set.

    Will cause any pending playing note to be sustained.

    """

    global _timeout

    if _timeout is not None:
        _timeout.cancel()
        _timeout = None

def stop():
    """Stop buzzer.

    Immediately silences the buzzer.

    """

    clear_timeout()

    GPIO.setup(BUZZER, GPIO.IN)

