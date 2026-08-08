class LogicVariables:
    """
    Mainly sets up variables to determine, when to render or not and when to update movements or not.
    It is also important for hitstops in interactions between the player and enemies.
    """

    def __init__(self) -> None:
        self.MOVEMENTS: bool = True
        self.RENDER: bool = True
        self.hitstop_timer = 0
