class Case:

    def __init__ (self, id: int, x: float, y: float, dt: datetime.datetime, 
                  weekday: str, priority: float = None, 
                  delayed: datetime = datetime.timedelta(minutes = 0)):

        self.id         = id
        self.location   = Point (x,y)
        self.weekday    = weekday
        self.datetime   = dt
        self.priority   = priority
        self.delayed    = delayed

