class VacuumEnvironment:
    def __init__(self, initial_state_number):
        # Mapping states 1-8 from your diagram: (Location, Status_A, Status_B)
        states_map = {
            1: ('A', 'Dirty', 'Dirty'),
            2: ('B', 'Dirty', 'Dirty'),
            3: ('A', 'Clean', 'Dirty'),
            4: ('B', 'Dirty', 'Clean'),
            5: ('A', 'Dirty', 'Clean'),
            6: ('B', 'Clean', 'Dirty'),
            7: ('A', 'Clean', 'Clean'),
            8: ('B', 'Clean', 'Clean')
        }
        
        self.location, self.status_A, self.status_B = states_map.get(initial_state_number, ('A', 'Dirty', 'Dirty'))
        print(f"Initialized State {initial_state_number} -> Location: {self.location}, Room A: {self.status_A}, Room B: {self.status_B}")

    def get_percept(self):
        current_status = self.status_A if self.location == 'A' else self.status_B
        return self.location, current_status

    def execute_action(self, action):
        print(f"Action taken: {action}")
        if action == 'Suck':
            if self.location == 'A':
                self.status_A = 'Clean'
            else:
                self.status_B = 'Clean'
        elif action == 'Move Right':
            self.location = 'B'
        elif action == 'Move Left':
            self.location = 'A'

    def is_goal_reached(self):
        return self.status_A == 'Clean' and self.status_B == 'Clean'

def reflex_vacuum_agent(percept):
    location, status = percept
    if status == 'Dirty':
        return 'Suck'
    elif location == 'A':
        return 'Move Right'
    elif location == 'B':
        return 'Move Left'

def run_simulation(state_num):
    env = VacuumEnvironment(state_num)
    steps = 0
    
    while not env.is_goal_reached() and steps < 5:
        percept = env.get_percept()
        action = reflex_vacuum_agent(percept)
        env.execute_action(action)
        steps += 1
        
    print(f"Goal Reached! Final Environment State -> Room A: {env.status_A}, Room B: {env.status_B}\n")

# Run the simulation for all 8 states sequentially
for state in range(1, 9):
    print(f"--- Running Simulation for State {state} ---")
    run_simulation(state)