def better_time(cd: int) -> str:

    time: str = f"{cd} s"
    if cd > 60:
        minutes: int = cd - (cd % 60)
        seconds: int = cd - minutes
        minutes: int = int(minutes / 60)
        time: str = f"{minutes}min {seconds}s"
        if minutes > 60:
            hoursglad: int = minutes - (minutes % 60)
            hours = int(hoursglad / 60)
            minutes: int = minutes - (hours*60)
            time: str = f"{hours}h {minutes}min {seconds}s"

    return time