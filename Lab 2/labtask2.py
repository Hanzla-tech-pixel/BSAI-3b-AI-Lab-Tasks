class ClassroomAgent:
    def __init__(self):
        self.previous = None

    def act(self, temp, occupied):
        if not occupied:
            mode = "ECO"
        elif temp < 20:
            mode = "HEAT"
        elif temp > 26:
            mode = "COOL"
        else:
            mode = "IDLE"

        send = mode != self.previous
        self.previous = mode

        return mode, send


agent = ClassroomAgent()

percepts = [
    (22, True), (22, True), (22, True),
    (20, True), (26, True), (19.9, True),
    (19.9, True), (26.1, True), (24, False),
    (15, False), (24, True)
]

for step, percept in enumerate(percepts, 1):
    mode, send = agent.act(*percept)
    result = "SEND" if send else "NO-SEND"

    print(step, percept, "Mode:", mode, result)